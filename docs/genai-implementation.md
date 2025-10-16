# OCI Generative AI Implementation

This document details the OCI Generative AI integration for vision-based delivery quality assessment.

## Overview

The OCI Delivery Agent uses OCI Generative AI Vision models to analyze delivery photos and extract structured information for quality assessment. The implementation supports both image captioning and damage detection with structured JSON outputs.

## Architecture

### GenAI Vision Pipeline
```
Object Storage Image → Base64 Encoding → GenAI Vision API → Structured JSON → Quality Assessment
```

### Key Components
- **VisionClient**: Handles OCI Generative AI API communication
- **ImageCaptionTool**: Generates structured scene descriptions
- **DamageDetectionTool**: Detects and classifies package damage
- **LangChain Integration**: Orchestrates the complete pipeline

## API Configuration

### Required Environment Variables
```bash
OCI_COMPARTMENT_ID=<YOUR_COMPARTMENT_ID>
OCI_TEXT_MODEL_OCID=<YOUR_ENDPOINT_OCID>  # Endpoint OCID
OCI_GENAI_HOSTNAME=https://inference.generativeai.us-chicago-1.oci.oraclecloud.com
```

### Authentication
- Uses OCI SDK configuration from `~/.oci/config`
- Supports both user-based and instance principal authentication
- Requires IAM policies for Generative AI access

## Vision Models

### Image Captioning Model
- **Purpose**: Analyze delivery scenes and extract structured information
- **Input**: Base64-encoded image + descriptive prompt
- **Output**: Structured JSON with scene analysis

#### Caption JSON Schema
```json
{
  "sceneType": "delivery|package|entrance|other",
  "packageVisible": true|false,
  "packageDescription": "string",
  "location": {
    "type": "doorstep|porch|mailbox|driveway|entrance|inside|other",
    "description": "string"
  },
  "environment": {
    "weather": "clear|rainy|cloudy|snowy|unknown",
    "timeOfDay": "morning|afternoon|evening|night|unknown",
    "conditions": "string"
  },
  "safetyAssessment": {
    "protected": true|false,
    "visible": true|false,
    "secure": true|false,
    "notes": "string"
  },
  "overallDescription": "string"
}
```

### Damage Detection Model
- **Purpose**: Detect and classify package damage
- **Input**: Base64-encoded image + damage analysis prompt
- **Output**: Structured JSON with damage assessment

#### Damage JSON Schema
```json
{
  "overall": {
    "severity": "none|minor|moderate|severe",
    "score": 0.0-1.0,
    "rationale": "string"
  },
  "indicators": {
    "boxDeformation": {
      "present": true|false,
      "severity": "none|minor|moderate|severe",
      "evidence": "string"
    },
    "cornerDamage": {
      "present": true|false,
      "severity": "none|minor|moderate|severe",
      "evidence": "string"
    },
    "leakage": {
      "present": true|false,
      "severity": "none|minor|moderate|severe",
      "evidence": "string"
    },
    "packagingIntegrity": {
      "present": true|false,
      "severity": "none|minor|moderate|severe",
      "evidence": "string"
    }
  },
  "packageVisible": true|false,
  "uncertainties": "string"
}
```

## Implementation Details

### API Request Structure
```python
# Chat API with multimodal content
chat_detail = oci.generative_ai_inference.models.ChatDetails()

# Text content
text_content = oci.generative_ai_inference.models.TextContent()
text_content.text = prompt

# Image content
image_content = oci.generative_ai_inference.models.ImageContent()
image_content.source = oci.generative_ai_inference.models.ImageSource()
image_content.source.data = base64_image

# Message with both text and image
message = oci.generative_ai_inference.models.Message()
message.role = "USER"
message.content = [text_content, image_content]

# Chat request
chat_request = oci.generative_ai_inference.models.GenericChatRequest()
chat_request.messages = [message]
chat_request.max_tokens = 600
chat_request.temperature = 0.1  # Low temperature for consistent JSON

# Serving mode
chat_detail.serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
    endpoint_id=model_ocid
)
```

### JSON Parsing and Validation
- Robust JSON extraction from model responses
- Substring recovery for malformed JSON
- Schema validation for structured outputs
- Error handling with fallback responses

### Prompt Engineering
- **Caption Prompts**: Focus on delivery scene analysis with specific JSON schema
- **Damage Prompts**: Target specific damage indicators with severity scoring
- **Consistency**: Low temperature (0.1) for structured output generation
- **Validation**: Keywords-based validation for damage severity assessment

## Quality Assessment Integration

### Damage Scoring
```python
def compute_damage_score(damage_report: dict) -> float:
    """Convert damage report to quality score (0.0 = damaged, 1.0 = perfect)"""
    if isinstance(damage_report.get("overall"), dict):
        score = damage_report["overall"].get("score", 0.0)
        return max(0.0, 1 - float(score))
    return 0.5  # Default neutral score
```

### Location Analysis
- GPS coordinates from EXIF data
- Distance calculation using Haversine formula
- Location accuracy scoring based on expected delivery coordinates

### Timeliness Assessment
- EXIF timestamp comparison with expected delivery time
- Time-based quality scoring with configurable weights

## Error Handling

### Common Issues and Solutions
1. **Model Not Found (404)**: Verify endpoint OCID and compartment access
2. **Authentication Errors**: Check OCI configuration and IAM policies
3. **JSON Parsing Errors**: Implement substring recovery and validation
4. **Vision Processing Failures**: Optimize prompts and image preprocessing

### Fallback Strategies
- Local file fallback for testing environments
- Default responses for failed vision processing
- Error logging and monitoring integration

## Performance Considerations

### Optimization
- **Image Preprocessing**: Resize large images to reduce API payload
- **Caching**: Cache model responses for repeated analysis
- **Batch Processing**: Process multiple images in parallel
- **Timeout Handling**: Configure appropriate timeouts for API calls

### Cost Management
- **Token Usage**: Monitor API token consumption
- **Image Size**: Optimize image dimensions for cost efficiency
- **Caching**: Reduce redundant API calls with response caching

## Testing and Validation

### Test Coverage
- **Unit Tests**: Individual tool functionality
- **Integration Tests**: End-to-end pipeline testing
- **Vision Tests**: Image analysis accuracy validation
- **JSON Schema Tests**: Output format validation

### Validation Methods
- **Manual Review**: Visual inspection of test images
- **Automated Scoring**: Programmatic quality assessment
- **A/B Testing**: Compare different model configurations
- **Error Analysis**: Monitor and analyze failure cases

## Deployment Considerations

### Production Requirements
- **High Availability**: Multiple endpoint configurations
- **Scalability**: Auto-scaling for high-volume processing
- **Monitoring**: Comprehensive logging and alerting
- **Security**: Secure credential management and access control

### Configuration Management
- **Environment Variables**: Centralized configuration
- **Model Selection**: Dynamic endpoint configuration
- **Quality Thresholds**: Configurable scoring parameters
- **Alerting Rules**: Customizable notification triggers
