# OCI GenAI GenerateText Implementation Guide

Based on the [official OCI GenerateText API documentation](https://docs.oracle.com/en-us/iaas/api/#/EN/generative-ai-inference/20231130/GenerateTextResult/GenerateText), this guide provides the correct implementation for delivery quality assessment.

## 🎯 GenerateText API Overview

The `generateText` endpoint is perfect for your delivery quality system because it:
- **Generates structured text** from prompts
- **Processes single requests** efficiently  
- **Returns consistent responses** for quality reports
- **Supports batch processing** for multiple deliveries

## 🔧 Correct API Implementation

### **1. Import and Setup**
```python
import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference.models import GenerateTextDetails
import os

def setup_genai_client():
    """Setup OCI GenAI client with proper configuration"""
    
    # Load OCI configuration
    config = oci.config.from_file()
    
    # Get hostname from environment
    hostname = os.getenv('OCI_GENAI_HOSTNAME')
    
    # Initialize client with correct hostname
    client = GenerativeAiInferenceClient(
        config=config,
        service_endpoint=hostname
    )
    
    return client

def get_generate_text_endpoint():
    """Construct the generateText endpoint dynamically"""
    hostname = os.getenv('OCI_GENAI_HOSTNAME')
    return f"{hostname}/20231130/actions/generateText"
```

### **2. Generate Quality Assessment Report**
```python
def generate_quality_report(quality_data, client):
    """
    Generate comprehensive quality assessment using OCI GenAI GenerateText
    Based on official API documentation
    """
    
    prompt = f"""
    DELIVERY QUALITY ASSESSMENT ANALYSIS
    
    Quality Metrics:
    - Timeliness Score: {quality_data['timeliness_score']:.2f}
    - Location Accuracy: {quality_data['location_score']:.2f}  
    - Damage Assessment: {quality_data['damage_score']:.2f}
    - Overall Quality Index: {quality_data['quality_index']:.3f}
    
    Delivery Context:
    - Expected Location: {quality_data['expected_location']}
    - Actual Location: {quality_data['actual_location']}
    - Delivery Time: {quality_data['delivery_time']}
    - Promised Time: {quality_data['promised_time']}
    - Distance from Expected: {quality_data.get('distance_meters', 'N/A')}m
    
    Please provide:
    1. Overall quality assessment (Excellent/Good/Fair/Poor)
    2. Key strengths and weaknesses
    3. Specific recommendations for improvement
    4. Risk level assessment (Low/Medium/High)
    5. Action items for delivery team
    
    Format as a professional quality report.
    END_REPORT
    """
    
    # Create GenerateTextDetails object as per official API
    generate_text_details = GenerateTextDetails(
        prompt=prompt,
        max_tokens=800,
        temperature=0.7,
        top_p=0.9,
        stop_sequences=["END_REPORT"]
    )
    
    try:
        # Call the official GenerateText API
        response = client.generate_text(
            endpoint_id=os.getenv('OCI_TEXT_MODEL_OCID'),
            generate_text_details=generate_text_details
        )
        
        # Extract text from response based on official API structure
        if response.data and response.data.choices:
            return response.data.choices[0].text
        else:
            return "Error: No response generated"
            
    except Exception as e:
        return f"Error generating quality report: {str(e)}"
```

### **3. Analyze Delivery Context**
```python
def analyze_delivery_context(delivery_data, client):
    """
    Analyze delivery context using OCI GenAI GenerateText
    """
    
    prompt = f"""
    DELIVERY CONTEXT ANALYSIS
    
    Delivery Information:
    - Object: {delivery_data['object_name']}
    - Event Time: {delivery_data['event_time']}
    - Expected Location: {delivery_data['expected_location']}
    - Promised Time: {delivery_data['promised_time']}
    
    Analyze and provide:
    1. Delivery urgency assessment
    2. Potential risk factors
    3. Context-specific quality requirements
    4. Recommended quality thresholds
    5. Special handling considerations
    
    END_ANALYSIS
    """
    
    generate_text_details = GenerateTextDetails(
        prompt=prompt,
        max_tokens=600,
        temperature=0.6,
        top_p=0.8,
        stop_sequences=["END_ANALYSIS"]
    )
    
    try:
        response = client.generate_text(
            endpoint_id=os.getenv('OCI_TEXT_MODEL_OCID'),
            generate_text_details=generate_text_details
        )
        
        return response.data.choices[0].text if response.data.choices else "Analysis failed"
        
    except Exception as e:
        return f"Error analyzing delivery context: {str(e)}"
```

## 🚀 Integration with Delivery Quality System

### **Enhanced Quality Pipeline:**
```python
def run_enhanced_quality_pipeline(delivery_data):
    """Run quality pipeline with OCI GenAI integration"""
    
    # 1. Calculate structured quality scores
    timeliness_score = calculate_timeliness_score(delivery_data)
    location_score = calculate_location_score(delivery_data)
    damage_score = calculate_damage_score(delivery_data)
    quality_index = calculate_quality_index(timeliness_score, location_score, damage_score)
    
    # 2. Setup OCI GenAI client
    client = setup_genai_client()
    
    # 3. Generate AI-powered quality report
    quality_data = {
        'timeliness_score': timeliness_score,
        'location_score': location_score,
        'damage_score': damage_score,
        'quality_index': quality_index,
        'expected_location': delivery_data['expected_location'],
        'actual_location': delivery_data['actual_location'],
        'delivery_time': delivery_data['delivery_time'],
        'promised_time': delivery_data['promised_time'],
        'distance_meters': delivery_data.get('distance_meters')
    }
    
    # 4. Generate comprehensive quality report
    ai_report = generate_quality_report(quality_data, client)
    
    # 5. Analyze delivery context
    context_analysis = analyze_delivery_context(delivery_data, client)
    
    return {
        'quality_scores': quality_data,
        'ai_quality_report': ai_report,
        'context_analysis': context_analysis,
        'recommendation': get_recommendation(quality_index),
        'risk_level': assess_risk_level(quality_index, context_analysis)
    }
```

## 📊 Example Output

### **AI-Generated Quality Report:**
```
DELIVERY QUALITY ASSESSMENT REPORT
=====================================

OVERALL ASSESSMENT: GOOD (Quality Index: 0.73)

QUALITY BREAKDOWN:
- Timeliness: 0.80 (Slightly late but acceptable)
- Location Accuracy: 0.90 (Excellent GPS precision)
- Damage Assessment: 0.50 (Some quality concerns)

KEY FINDINGS:
✅ Strengths:
- Excellent location accuracy
- Good overall performance
- Professional delivery execution

⚠️ Areas for Improvement:
- Image quality suggests possible handling issues
- 15-minute delay beyond promised time
- Minor GPS deviation from expected location

RECOMMENDATIONS:
1. Review handling procedures to prevent damage
2. Optimize delivery routes for better timeliness
3. Verify GPS accuracy in delivery area
4. Implement quality checks for image capture

RISK LEVEL: LOW
- Acceptable delivery with minor improvements needed
- No immediate action required
- Monitor for pattern improvements

ACTION ITEMS:
- Schedule follow-up with delivery team
- Review handling procedures
- Update delivery time estimates
```

## 🔐 Required IAM Permissions

Based on the official API documentation, ensure your function has these permissions:

```json
{
  "statements": [
    {
      "effect": "Allow",
      "action": "generativeai:generateText",
      "resource": "endpoints/*"
    },
    {
      "effect": "Allow",
      "action": "generativeai:listEndpoints", 
      "resource": "*"
    }
  ]
}
```

## 🧪 Testing Implementation

```python
def test_genai_integration():
    """Test OCI GenAI GenerateText integration"""
    
    # Test data
    delivery_data = {
        'object_name': 'deliveries/sample.jpg',
        'event_time': '2024-01-10T17:15:00Z',
        'expected_location': (37.7749, -122.4194),
        'actual_location': (37.7849, -122.4094),
        'promised_time': '2024-01-10T17:00:00Z',
        'distance_meters': 1417.3
    }
    
    # Setup client
    client = setup_genai_client()
    
    # Test quality report generation
    quality_data = {
        'timeliness_score': 0.8,
        'location_score': 0.9,
        'damage_score': 0.5,
        'quality_index': 0.73,
        'expected_location': delivery_data['expected_location'],
        'actual_location': delivery_data['actual_location'],
        'delivery_time': delivery_data['event_time'],
        'promised_time': delivery_data['promised_time'],
        'distance_meters': delivery_data['distance_meters']
    }
    
    # Generate AI report
    report = generate_quality_report(quality_data, client)
    print("AI Quality Report:")
    print(report)
    
    # Test context analysis
    context = analyze_delivery_context(delivery_data, client)
    print("\nContext Analysis:")
    print(context)
```

## 📚 References

- [Official OCI GenerateText API Documentation](https://docs.oracle.com/en-us/iaas/api/#/EN/generative-ai-inference/20231130/GenerateTextResult/GenerateText)
- [OCI GenAI Service Overview](https://docs.oracle.com/en-us/iaas/generative-ai/)
- [OCI IAM Policies for GenAI](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policies.htm)

---

**Ready to implement OCI GenAI GenerateText for intelligent delivery quality assessment!** 🚀
