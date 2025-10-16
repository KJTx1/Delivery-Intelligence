# OCI Generative AI Integration Guide

Based on the [official OCI Generative AI Inference API documentation](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-inference/20231130/), this guide covers how to integrate OCI GenAI with the delivery quality assessment system.

## 🎯 OCI GenAI API Overview

The OCI Generative AI service provides access to large language models through the Inference API, supporting models like:
- **Cohere Command** - For text generation and analysis
- **Meta Llama 2** - For conversational AI and reasoning
- **Custom models** - Your own fine-tuned models

## 🔧 Configuration

### **Required Environment Variables:**
```bash
# OCI Generative AI Configuration
OCI_TEXT_MODEL_OCID=<YOUR_ENDPOINT_OCID>
OCI_GENAI_ENDPOINT=https://generativeai.oci.oraclecloud.com/20231130/endpoints

# Optional: Dedicated serving endpoint
OCI_GENAI_SERVING_ENDPOINT=https://generativeai.oci.oraclecloud.com/20231130/endpoints/{endpoint-id}/generateText
```

### **API Endpoints:**
- **Base Endpoint**: `https://generativeai.oci.oraclecloud.com/20231130/endpoints`
- **GenerateText**: `POST /endpoints/{endpoint-id}/generateText` ✅ **Recommended for quality assessment**
- **Chat**: `POST /endpoints/{endpoint-id}/chat` ❌ **Not needed for structured analysis**
- **Model Management**: `GET /endpoints` (list available models)

## 🚀 Integration in Delivery Quality System

### **1. Text Analysis for Quality Assessment**

The OCI GenAI service will be used for:
- **Delivery description analysis** - Understanding delivery context
- **Quality reasoning** - Explaining quality scores and recommendations
- **Natural language processing** - Converting structured data to human-readable reports

### **2. API Usage Examples**

#### **Generate Quality Assessment Report:**
```python
import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient

def generate_quality_report(quality_data):
    """Generate human-readable quality assessment report using OCI GenAI"""
    
    client = GenerativeAiInferenceClient(
        config=oci.config.from_file(),
        service_endpoint=os.getenv('OCI_GENAI_ENDPOINT')
    )
    
    prompt = f"""
    Analyze this delivery quality data and provide a comprehensive assessment:
    
    Quality Scores:
    - Timeliness: {quality_data['timeliness_score']}
    - Location Accuracy: {quality_data['location_score']}
    - Damage Assessment: {quality_data['damage_score']}
    - Overall Quality Index: {quality_data['quality_index']}
    
    Context:
    - Expected Location: {quality_data['expected_location']}
    - Actual Location: {quality_data['actual_location']}
    - Delivery Time: {quality_data['delivery_time']}
    - Promised Time: {quality_data['promised_time']}
    
    Provide:
    1. Overall assessment
    2. Key issues identified
    3. Recommendations for improvement
    4. Risk level assessment
    """
    
    response = client.generate_text(
        endpoint_id=os.getenv('OCI_TEXT_MODEL_OCID'),
        generate_text_details={
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop_sequences": ["END_REPORT"]
        }
    )
    
    # Based on official GenerateText API documentation
    return response.data.choices[0].text
```

#### **Analyze Delivery Context:**
```python
def analyze_delivery_context(delivery_data):
    """Use OCI GenAI to analyze delivery context and extract insights"""
    
    prompt = f"""
    Analyze this delivery information and extract key insights:
    
    Delivery Data:
    - Object Name: {delivery_data['object_name']}
    - Event Time: {delivery_data['event_time']}
    - Expected Location: {delivery_data['expected_location']}
    - Promised Time: {delivery_data['promised_time']}
    
    Provide analysis on:
    1. Delivery urgency level
    2. Potential risk factors
    3. Context-specific quality requirements
    4. Recommended quality thresholds
    """
    
    # Implementation similar to above
    return analysis_result
```

## 📊 Quality Assessment Integration

### **Enhanced Quality Pipeline with OCI GenAI:**

1. **Data Collection** - GPS, timeliness, image analysis
2. **Structured Scoring** - Mathematical quality calculations
3. **OCI GenAI Analysis** - Natural language reasoning and explanation
4. **Report Generation** - Human-readable quality reports
5. **Recommendation Engine** - AI-powered improvement suggestions

### **Example Quality Report Output:**
```
DELIVERY QUALITY ASSESSMENT REPORT
=====================================

Overall Quality Index: 0.73 (Good)

ANALYSIS:
The delivery shows good performance with minor areas for improvement. 
The timeliness score of 0.8 indicates the package arrived close to 
the promised time, while the location accuracy of 0.9 shows excellent 
GPS precision. The damage assessment of 0.5 suggests some quality 
concerns that require attention.

KEY ISSUES:
- Image quality indicates possible handling damage
- Delivery was 15 minutes late
- GPS coordinates show slight deviation from expected location

RECOMMENDATIONS:
1. Review handling procedures to prevent damage
2. Optimize delivery routes for better timeliness
3. Verify GPS accuracy in delivery area

RISK LEVEL: LOW - Acceptable delivery with minor improvements needed
```

## 🔐 Authentication & Permissions

### **Required IAM Policies:**
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

### **Dynamic Group Matching Rule:**
```
resource.type = 'fnfunc' 
resource.compartment.id = '<YOUR_COMPARTMENT_ID>'
```

## 🧪 Testing OCI GenAI Integration

### **Test Script:**
```python
def test_genai_integration():
    """Test OCI GenAI integration with delivery quality system"""
    
    # Test data
    quality_data = {
        'timeliness_score': 0.8,
        'location_score': 0.9,
        'damage_score': 0.5,
        'quality_index': 0.73,
        'expected_location': (37.7749, -122.4194),
        'actual_location': (37.7849, -122.4094),
        'delivery_time': '2024-01-10T17:15:00Z',
        'promised_time': '2024-01-10T17:00:00Z'
    }
    
    # Generate report
    report = generate_quality_report(quality_data)
    print("Generated Report:")
    print(report)
    
    # Test context analysis
    context = analyze_delivery_context({
        'object_name': 'deliveries/sample.jpg',
        'event_time': '2024-01-10T17:15:00Z',
        'expected_location': (37.7749, -122.4194),
        'promised_time': '2024-01-10T17:00:00Z'
    })
    print("\nContext Analysis:")
    print(context)
```

## 🎯 Benefits of OCI GenAI Integration

1. **Natural Language Reports** - Human-readable quality assessments
2. **Intelligent Analysis** - AI-powered insights and recommendations
3. **Contextual Understanding** - Better interpretation of delivery data
4. **Automated Documentation** - Generate comprehensive quality reports
5. **Risk Assessment** - AI-driven risk analysis and mitigation suggestions

## 📚 References

- [OCI Generative AI Inference API Documentation](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-inference/20231130/)
- [OCI GenAI Service Overview](https://docs.oracle.com/en-us/iaas/generative-ai/)
- [OCI IAM Policies for GenAI](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policies.htm)

---

**Ready to integrate OCI GenAI with your delivery quality system!** 🚀
