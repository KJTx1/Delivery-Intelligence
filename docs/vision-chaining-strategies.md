# Vision Tool Chaining Strategies

## Problem Statement

The system was making two independent calls to OCI GenAI Vision API:
1. **Image Captioning** - identifies packages and scene details
2. **Damage Assessment** - evaluates package damage

Because these calls were independent, they sometimes gave conflicting results. For example:
- Caption: "A white plastic bag and a blue cooler are visible"
- Damage: "Package is not visible"

This happened because each call independently determined what constitutes a "package," leading to inconsistent results.

---

## Solution Options

### Option 1: Context-Aware Sequential Chaining ✅ (IMPLEMENTED)

**Strategy:** Pass caption results to damage assessment as context, ensuring consistency.

**How it works:**
1. Run image captioning first to identify all delivery items
2. Pass caption results (especially `packageVisible` and `packageDescription`) to damage assessment
3. Damage assessment uses this context to evaluate the same items the caption identified

**Benefits:**
- ✅ Ensures consistency between caption and damage assessment
- ✅ Provides explicit context to the damage model about what to evaluate
- ✅ Still makes two calls but they're now coordinated
- ✅ Each model still specializes in its task (separation of concerns)
- ✅ Easy to debug - can see what context was passed

**Implementation:**

```python
# In chains.py:
# Step 1: Get caption first
caption_json = tools["caption"].run(encoded_payload)
caption_dict = json.loads(caption_json)

# Step 2: Pass caption context to damage assessment
damage_report = json.loads(tools["damage"].run(
    encoded_payload=encoded_payload,
    caption_context=caption_json  # Context passed here
))
```

```python
# In tools.py - VisionClient._damage_json_prompt():
context_section = ""
if caption_context:
    pkg_visible = caption_context.get("packageVisible", False)
    pkg_desc = caption_context.get("packageDescription", "")
    if pkg_visible and pkg_desc:
        context_section = (
            f"CONTEXT: Prior analysis identified packages in this image: {pkg_desc}\n"
            f"Your damage assessment should evaluate these identified items.\n\n"
        )
```

**Example prompt enhancement:**
```
CONTEXT: Prior analysis identified packages in this image: A white plastic bag and a blue cooler with a white lid are visible.
Your damage assessment should evaluate these identified items.

[Rest of damage assessment instructions...]
```

---

### Option 2: Post-Processing Reconciliation (Simple Fallback)

**Strategy:** Add logic after both API calls to detect and resolve conflicts.

**How it works:**
1. Run both caption and damage assessment independently
2. Check for conflicts (e.g., caption says package visible, damage says not visible)
3. Apply reconciliation rules (e.g., trust caption's `packageVisible` determination)

**Benefits:**
- ✅ Simple to implement
- ✅ No changes to API calls
- ✅ Can add sophisticated conflict resolution logic

**Drawbacks:**
- ❌ Doesn't prevent the root cause (conflicting assessments)
- ❌ Just picks one result over another
- ❌ The damage model still doesn't know what packages to evaluate

**Implementation Example:**

```python
def reconcile_vision_results(caption_dict, damage_report):
    """Reconcile conflicts between caption and damage assessment."""
    
    # If caption says package is visible but damage says no
    if caption_dict.get("packageVisible") and not damage_report.get("packageVisible"):
        print("⚠️  Conflict detected: Caption found packages, damage did not")
        print(f"   Packages identified: {caption_dict.get('packageDescription')}")
        
        # Trust caption's determination and update damage report
        damage_report["packageVisible"] = True
        damage_report["uncertainties"] = (
            f"Damage assessment initially missed packages. "
            f"Caption identified: {caption_dict.get('packageDescription')}"
        )
    
    return damage_report
```

---

### Option 3: Unified Single Vision Call (Most Efficient)

**Strategy:** Combine both caption and damage assessment into a single API call with unified prompt.

**How it works:**
1. Create a comprehensive prompt that asks for both scene analysis AND damage assessment
2. Parse a single combined JSON response with both sets of information
3. Extract caption and damage data from the unified response

**Benefits:**
- ✅ Most cost-efficient (one API call instead of two)
- ✅ Inherently consistent (single model response)
- ✅ Faster overall execution

**Drawbacks:**
- ❌ More complex prompt engineering
- ❌ Harder to parse (one large JSON structure)
- ❌ Loss of modularity and separation of concerns
- ❌ Harder to debug when issues occur
- ❌ May reduce quality if model tries to do too much at once

**Implementation Sketch:**

```python
def analyze_delivery_image(self, image_bytes: bytes) -> Dict[str, Any]:
    """Single unified vision call for both caption and damage assessment."""
    
    unified_prompt = """
    Analyze this delivery image and provide ONLY a JSON object with:
    {
      "scene": {
        "sceneType": "...",
        "packageVisible": true|false,
        "packageDescription": "...",
        "location": {...},
        "environment": {...},
        "safetyAssessment": {...}
      },
      "damage": {
        "overall": {...},
        "indicators": {...},
        "packageVisible": true|false
      }
    }
    
    IMPORTANT: The packageVisible field must be consistent in both sections.
    """
    
    # Make single API call
    response = client.chat(...)
    
    # Parse unified response
    result = parse_json(response)
    return {
        "caption": result["scene"],
        "damage": result["damage"]
    }
```

---

### Option 4: Two-Stage with Reconciliation (Hybrid)

**Strategy:** Combine Option 1 and Option 2 - pass context AND add reconciliation.

**How it works:**
1. Run caption first
2. Pass caption context to damage assessment (Option 1)
3. Add reconciliation logic as a safety net (Option 2)

**Benefits:**
- ✅ Most robust - prevents AND fixes conflicts
- ✅ Context passing reduces conflicts in the first place
- ✅ Reconciliation catches any remaining issues

**Drawbacks:**
- ❌ Most complex implementation
- ❌ May be overkill if Option 1 works well

---

## Recommendation & Implementation Status

**Chosen Solution: Option 1 (Context-Aware Sequential Chaining)**

This option provides the best balance of:
- **Consistency** - Damage assessment knows what packages to evaluate
- **Modularity** - Each tool still has a clear, focused responsibility
- **Debuggability** - Easy to see what context was passed and why
- **Quality** - Each model focuses on its specialized task

### Files Modified

**1. delivery-function/src/oci_delivery_agent/tools.py**
- Modified `VisionClient._damage_json_prompt()` to accept `caption_context` parameter
- Modified `VisionClient.detect_damage()` to accept `caption_context` parameter
- Modified `DamageDetectionTool._run()` to accept and parse `caption_context` parameter

**2. delivery-function/src/oci_delivery_agent/chains.py**
- Modified `run_quality_pipeline()` to pass caption results to damage detection
- Added import for `Optional` type hint
- Optimized to avoid parsing caption_json twice

**3. development/src/oci_delivery_agent/tools.py** (same changes as #1)

**4. development/src/oci_delivery_agent/chains.py** (same changes as #2)

### Testing the Changes

Run your test again and you should see consistent `packageVisible` values:

```bash
printf '{"test_type":"full","data":{"resourceName":"delivery1.png"},"additionalDetails":{"expectedLatitude":40.7128,"expectedLongitude":-74.0060,"promisedTime":"2025-10-15T21:00:00Z"}}' | fn invoke delivery-agent-app-chi delivery-quality-function
```

Expected result:
```json
{
  "caption_json": {
    "packageVisible": true,
    "packageDescription": "A white plastic bag and a blue cooler with a white lid are visible."
  },
  "damage_report": {
    "packageVisible": true,  // ✅ Now consistent with caption
    "overall": {
      "severity": "none",
      "score": 0.0,
      "rationale": "Both packages appear intact with no visible damage"
    }
  }
}
```

---

## Future Enhancements

If you still see occasional conflicts, consider adding Option 2 (reconciliation) as a safety net:

```python
# In chains.py, after getting both results:
damage_report = reconcile_vision_results(caption_dict, damage_report)
```

This would catch any remaining edge cases where the context passing didn't fully resolve the conflict.

