# API Response Format Guide

## 📊 **Quality Metrics Explained**

### **Clear Naming Convention**
Our API uses **business-friendly naming** to avoid confusion between damage probability and quality scores.

| Field | Type | Range | Meaning | Example |
|-------|------|-------|---------|---------|
| `package_quality` | float | 0.0-1.0 | Package condition (higher = better) | `0.9` = 90% quality |
| `location_accuracy` | float | 0.0-1.0 | GPS accuracy (higher = better) | `0.8` = 80% accurate |
| `timeliness` | float | 0.0-1.0 | Delivery timing (higher = better) | `0.75` = 75% on-time |
| `quality_index` | float | 0.0-1.0 | Overall quality score | `0.85` = 85% overall |

## 🎯 **Damage Assessment Structure**

### **AI Model Output (Raw)**
```json
{
  "damage_report": {
    "overall": {
      "severity": "minor",           // AI-detected level
      "score": 0.1,                 // AI damage probability (0-1)
      "rationale": "Minor corner damage detected"
    },
    "indicators": {
      "leakage": {
        "present": false,
        "severity": "none",
        "evidence": "No visible moisture"
      },
      "cornerDamage": {
        "present": true,
        "severity": "minor", 
        "evidence": "Slight dent in corner"
      }
    }
  }
}
```

### **Our System Processing**
- **AI `score`**: Damage probability (0.0 = no damage, 1.0 = certain damage)
- **Our `package_quality`**: Quality score (0.0 = poor, 1.0 = perfect)
- **Conversion**: `package_quality = 1 - damage_probability`

## 📈 **Quality Score Interpretation**

| Package Quality | Condition | Business Impact | Action |
|-----------------|-----------|-----------------|--------|
| `0.9 - 1.0` | Excellent | No issues | ✅ Accept |
| `0.7 - 0.9` | Good | Minor cosmetic | ✅ Accept |
| `0.5 - 0.7` | Fair | Some damage | ⚠️ Review |
| `0.3 - 0.5` | Poor | Significant damage | ❌ Reject |
| `0.0 - 0.3` | Severe | Major damage | ❌ Reject |

## 🔧 **Severity Level Mapping**

| AI Severity | Severity Score | Package Quality | Meaning |
|-------------|----------------|-----------------|---------|
| `"none"` | 0.05 | 0.95 | 95% quality (excellent) |
| `"minor"` | 0.35 | 0.65 | 65% quality (good) |
| `"moderate"` | 0.65 | 0.35 | 35% quality (poor) |
| `"severe"` | 0.90 | 0.10 | 10% quality (severe) |

## 🎯 **Example API Response**

```json
{
  "metadata": {
    "content_type": "image/jpeg",
    "object_name": "delivery_photo.jpg"
  },
  "quality_metrics": {
    "location_accuracy": 0.0,        // GPS mismatch
    "timeliness": 0.875,            // 87.5% on-time
    "package_quality": 0.9,          // 90% quality (excellent)
    "quality_index": 0.662           // 66.2% overall quality
  },
  "damage_report": {
    "overall": {
      "severity": "none",
      "score": 0.0,                  // AI: 0% damage probability
      "rationale": "No damage visible"
    },
    "indicators": {
      "leakage": {"present": false, "severity": "none"},
      "boxDeformation": {"present": false, "severity": "none"},
      "cornerDamage": {"present": false, "severity": "none"},
      "packagingIntegrity": {"present": false, "severity": "none"}
    }
  },
  "assessment": {
    "status": "Accept",
    "issues": [],
    "insights": "Package delivered in excellent condition"
  }
}
```

## 🚀 **Key Benefits**

- **No Confusion**: Clear distinction between damage probability and quality
- **Business Friendly**: Intuitive interpretation (higher = better)
- **Consistent**: All quality metrics follow same pattern
- **Actionable**: Clear thresholds for business decisions
