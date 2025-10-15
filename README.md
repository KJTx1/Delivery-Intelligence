# OCI Delivery Agent

Serverless delivery quality assessment system using OCI Functions, Generative AI Vision, and Object Storage with structured JSON processing.

## Features

- **🖼️ AI-Powered Image Analysis**: Uses OCI Generative AI Vision models for structured image captioning and damage detection
- **📦 Object Storage Integration**: Automatically processes images uploaded to OCI Object Storage
- **🔍 EXIF Metadata Extraction**: Extracts GPS coordinates and camera metadata from delivery photos
- **📊 Quality Scoring**: Computes delivery quality index based on timeliness, location accuracy, and damage assessment
- **⚡ Serverless Architecture**: Built on OCI Functions for automatic scaling and cost efficiency
- **🎯 Structured JSON Output**: All AI tools return structured JSON for consistent pipeline processing

## Quick Deploy

```bash
python3 deploy_function.py
```

## Configuration

Set these variables in OCI Console → Functions → Your Function → Configuration:

- **OCI Authentication**: OCI_USER_OCID, OCI_FINGERPRINT, OCI_KEY_FILE, OCI_TENANCY_OCID, OCI_REGION
- **OCI Resources**: OCI_COMPARTMENT_ID, OCI_OS_NAMESPACE, OCI_OS_BUCKET
- **AI Services**: OCI_TEXT_MODEL_OCID (endpoint OCID), OCI_GENAI_HOSTNAME
- **Quality Settings**: WEIGHT_TIMELINESS, WEIGHT_LOCATION, WEIGHT_DAMAGE, MAX_DISTANCE_METERS

### Environment Setup

Copy `env.example` to `.env` and configure your OCI credentials:

```bash
cp env.example .env
# Edit .env with your OCI configuration
```

## Usage

Upload delivery images to your Object Storage bucket to trigger automatic quality assessment.

## Project Structure

```
├── src/oci_delivery_agent/          # Core application code
│   ├── handlers.py                  # OCI Function entry point
│   ├── tools.py                     # LangChain tools (Object Storage, EXIF, Vision)
│   ├── chains.py                    # LangChain orchestration
│   └── config.py                    # Configuration management
├── tests/                           # Test files
│   └── test_caption_tool.py         # Vision tool testing
├── docs/                            # Documentation
│   ├── architecture.md              # System architecture
│   └── genai-implementation.md       # GenAI implementation details
├── deploy_function.py               # OCI Function deployment script
└── env.example                     # Environment configuration template
```

## Testing

```bash
# Test image captioning and damage detection with Object Storage
python tests/test_caption_tool.py
```

## AI Vision Capabilities

### Image Captioning
Returns structured JSON with:
- Scene type (delivery/package/entrance/other)
- Package visibility and description
- Location details (doorstep/porch/mailbox/etc.)
- Environmental conditions (weather, time of day)
- Safety assessment (protected, visible, secure)

### Damage Detection
Returns structured JSON with:
- Overall severity and confidence score
- Specific damage indicators:
  - Box deformation (crushed corners, bent edges)
  - Corner damage (abraded, torn, dented)
  - Leakage (liquid stains, moisture)
  - Packaging integrity (tears, holes, dents)
- Package visibility and uncertainties

## Recent Improvements

### Structured JSON Processing
- **Enhanced Vision Models**: Improved prompts for consistent JSON output
- **Damage Detection**: Specific indicators for box deformation, corner damage, leakage, and packaging integrity
- **Scene Analysis**: Comprehensive delivery scene assessment with safety and environmental factors
- **Quality Scoring**: Refined algorithms for damage probability and location accuracy

### Production Readiness
- **Object Storage Integration**: Full production pipeline with OCI Object Storage
- **Error Handling**: Robust JSON parsing with fallback strategies
- **Performance Optimization**: Efficient image processing and API usage
- **Testing Framework**: Comprehensive test coverage for all components

### Documentation
- **Architecture Guide**: Complete system design documentation
- **GenAI Implementation**: Detailed technical documentation for AI integration
- **API Reference**: Comprehensive configuration and usage examples