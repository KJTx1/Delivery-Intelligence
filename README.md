# OCI Delivery Agent

Serverless delivery quality assessment system using OCI Functions, Generative AI Vision, and Object Storage with structured JSON processing.

## Features

- **🖼️ AI-Powered Image Analysis**: Uses OCI Generative AI Vision models for structured image captioning and damage detection
- **🔒 Privacy Protection**: Automatic face detection and blurring to protect privacy (GDPR/CCPA compliant)
- **📦 Object Storage Integration**: Automatically processes images uploaded to OCI Object Storage
- **🔍 EXIF Metadata Extraction**: Extracts GPS coordinates and camera metadata from delivery photos
- **📊 Quality Scoring**: Computes delivery quality index based on timeliness, location accuracy, and damage assessment
- **⚡ Serverless Architecture**: Built on OCI Functions for automatic scaling and cost efficiency
- **🎯 Structured JSON Output**: All AI tools return structured JSON for consistent pipeline processing
- **🎨 Dashboard Interface**: Complete React-based dashboard for Customer Service, Drivers, and Operations Managers

## Quick Deploy

### Method 1: Fn Project CLI (Recommended)
```bash
# Install Fn Project CLI
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh

# Set up context
fn create context oci --api-url https://functions.us-ashburn-1.oci.oraclecloud.com
fn use context oci
fn update context registry iad.ocir.io/<YOUR_NAMESPACE>
fn update context compartment-id <YOUR_COMPARTMENT_ID>

# Deploy function
cd delivery-function
fn -v deploy --app delivery-agent-app
```

### Method 2: Manual OCI CLI (Alternative)
```bash
# Use OCI CLI directly for deployment
oci fn function deploy --function-id <FUNCTION_ID> --image <IMAGE_URI>
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
├── dashboards/                      # Frontend dashboard application
│   ├── frontend/                   # React-based dashboard interface
│   │   ├── src/                    # Dashboard source code
│   │   │   ├── pages/              # Role-specific dashboards
│   │   │   │   ├── CustomerService/ # Customer service dashboard
│   │   │   │   ├── Driver/         # Driver performance dashboard
│   │   │   │   └── OperationsManager/ # Operations management dashboard
│   │   │   ├── shared/             # Shared components and utilities
│   │   │   └── services/           # API integration services
│   │   └── dist/                   # Built dashboard assets
│   └── wireframes/                 # Dashboard design specifications
├── development/                     # Development environment
│   ├── src/oci_delivery_agent/     # Source code for local development
│   │   ├── handlers.py              # OCI Function entry point
│   │   ├── tools.py                 # LangChain tools (Object Storage, EXIF, Vision)
│   │   ├── chains.py                # LangChain orchestration
│   │   └── config.py                # Configuration management
│   ├── tests/                       # Test files
│   │   ├── test_caption_tool.py     # Vision tool testing
│   │   └── test_damage_samples.py   # Damage detection testing
│   ├── assets/                      # Test assets and sample data
│   │   └── deliveries/              # Sample delivery images
│   └── README.md                    # Development documentation
├── delivery-function/               # Production deployment (main function)
│   ├── func.yaml                    # Function configuration
│   ├── func.py                      # Function entry point
│   ├── requirements.txt             # Python dependencies
│   └── src/oci_delivery_agent/     # Deployable source code
├── face-blur-function/              # Face blurring service
│   ├── func.yaml                    # Function configuration
│   ├── func.py                      # Face blurring function
│   ├── requirements.txt             # Python dependencies
│   └── src/oci_delivery_agent/     # Source code
├── docs/                            # Documentation
│   ├── system-architecture.md       # System architecture
│   ├── genai-vision-implementation.md # GenAI implementation details
│   └── deployment-guide.md          # Complete deployment guide
└── env.example                     # Environment configuration template
```

## Testing

### Local Development Testing
```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to development directory
cd development

# Test image captioning and damage detection
python tests/test_caption_tool.py

# Test damage detection on all samples
python tests/test_damage_samples.py
```

### Production Deployment
```bash
# Deploy to OCI Functions (no venv needed)
cd delivery-function
fn -v deploy --app delivery-agent-app

# Set environment variables in OCI Console
# OCI Console → Functions → Your Function → Configuration
```

### Environment Differences

| Aspect | Development (Local) | Production (OCI Functions) |
|--------|-------------------|---------------------------|
| **Python Environment** | `venv/` virtual environment | Docker container |
| **Configuration** | `.env` file | OCI Console environment variables |
| **Data Source** | Local assets (`development/assets/`) | OCI Object Storage |
| **Authentication** | Local OCI config file | Instance Principal |
| **Execution** | Interactive testing | Serverless, event-driven |
| **Dependencies** | Installed in `venv/` | Built into Docker image |

### Virtual Environment Usage

#### **Development (Uses `venv/`)**
```bash
# Activate virtual environment for local development
source venv/bin/activate
cd development
python tests/test_caption_tool.py
```

#### **Production (No `venv/` needed)**
```bash
# Deploy to OCI Functions (uses Docker container)
cd delivery-function
fn -v deploy --app delivery-agent-app
```

**Why this difference?**
- **Development**: Uses local Python with `venv/` for isolated package management
- **Production**: Uses Docker container with built-in dependencies, no local Python needed

### Test Results
- ✅ **Object Storage**: Automatic fallback to local assets
- ✅ **GenAI Vision**: Full image captioning and damage detection
- ✅ **Environment**: Proper `.env` file loading
- ✅ **Assets**: Sample images for comprehensive testing

## Privacy Protection (Face Blurring)

The system automatically detects and blurs human faces in delivery photos **before** processing with the vision model.

### Features
- ✅ **Automatic Detection**: Uses OpenCV Haar Cascades for fast, accurate face detection
- ✅ **Adaptive Blur**: Automatically scales blur intensity based on face size (40% coverage)
- ✅ **Strong Anonymization**: All faces equally unrecognizable, from small (60px) to large (700px)
- ✅ **Configurable**: Adjust blur intensity and detection sensitivity
- ✅ **No Impact on Analysis**: Package damage and scene context remain fully analyzable
- ✅ **Compliance Ready**: Helps meet GDPR, CCPA, and BIPA requirements

### Quick Start

Face blurring is **enabled by default**. No configuration needed!

```python
# Default usage (face blurring enabled)
config = WorkflowConfig(
    object_storage=ObjectStorageConfig(...),
    vision=VisionConfig(...)
    # Face blurring automatically enabled
)

result = run_quality_pipeline(config, llm, context, "photo.jpg")
print(result["privacy"]["faces_blurred"])  # True
```

### Custom Configuration

```python
from oci_delivery_agent.config import PrivacyConfig

# Maximum blur for sensitive environments
config = WorkflowConfig(
    ...,
    privacy=PrivacyConfig(
        enable_face_blurring=True,
        blur_intensity=71  # Maximum anonymization
    )
)
```

### Standalone Usage

```python
from oci_delivery_agent.tools import blur_faces_in_image

with open("photo.jpg", "rb") as f:
    image_bytes = f.read()

anonymized = blur_faces_in_image(image_bytes)

with open("anonymized.jpg", "wb") as f:
    f.write(anonymized)
```

### Testing

```bash
cd development/tests
python test_face_blur.py
```

### Documentation
- 📘 **Quick Start**: [face-blurring-quickstart.md](docs/face-blurring-quickstart.md)
- 📚 **Full Guide**: [face-blurring-privacy.md](docs/face-blurring-privacy.md)
- 💡 **Examples**: `development/examples/face_blur_example.py`

## AI Vision Capabilities

### Context-Aware Sequential Chaining
The vision pipeline uses **context passing** to ensure consistency between tools:
1. **Caption Tool** identifies all packages and delivery items first
2. **Damage Tool** receives caption results as context
3. Both tools analyze the same items for consistent results

### Image Captioning
Returns structured JSON with:
- Scene type (delivery/package/entrance/other)
- Package visibility and description (all item types: boxes, bags, coolers, envelopes)
- Location details (doorstep/porch/mailbox/etc.)
- Environmental conditions (weather, time of day)
- Safety assessment (protected, visible, secure)

### Damage Detection (Context-Aware)
Returns structured JSON with:
- **Context Integration**: Receives caption results to know what packages to evaluate
- Overall severity and confidence score
- Specific damage indicators:
  - Box deformation (crushed corners, bent edges)
  - Corner damage (abraded, torn, dented)
  - Leakage (liquid stains, moisture)
  - Packaging integrity (tears, holes, dents)
- Package visibility and uncertainties
- **Package Type Support**: Evaluates all delivery items (boxes, bags, coolers, containers, parcels)

## Recent Improvements

### Context-Aware Vision Pipeline (Latest!)
- **Sequential Chaining**: Caption results inform damage assessment for consistency
- **Package Type Support**: Recognizes all delivery items (boxes, bags, coolers, envelopes, containers)
- **Conflict Prevention**: Ensures both vision tools agree on package visibility
- **Context Passing**: Damage assessment receives caption results as prompt context
- **Improved Accuracy**: Damage tool knows exactly what items to evaluate
- **Documentation**: Complete chaining strategy documentation in `docs/vision-chaining-strategies.md`

### Privacy & Security
- **Face Blurring**: Automatic face detection and anonymization using OpenCV
- **Privacy Configuration**: Fully configurable privacy settings with validation
- **Compliance Support**: GDPR, CCPA, and BIPA compliance features
- **Performance**: <300ms overhead for face detection and blurring
- **Testing Suite**: Comprehensive tests for face detection accuracy

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

### Deployment & Operations
- **Fn Project CLI Integration**: Official Oracle deployment methodology
- **Automated Deployment**: Streamlined deployment scripts and processes
- **Function Configuration**: Complete environment variable management
- **Monitoring & Logging**: Comprehensive operational visibility

### Documentation
- **Architecture Guide**: Complete system design documentation
- **GenAI Implementation**: Detailed technical documentation for AI integration
- **Deployment Guide**: Step-by-step deployment instructions
- **Privacy Guide**: Comprehensive face blurring documentation
- **API Reference**: Comprehensive configuration and usage examples

## Current Status

✅ **Fully Deployed**: Main delivery function is deployed to OCI Functions and operational
✅ **Face Blur Function**: Standalone face blurring service is deployed and working
✅ **GenAI Integration**: Complete vision capabilities with structured JSON output
✅ **Object Storage**: Full integration with OCI Object Storage for image processing
✅ **Dashboard Interface**: Complete React-based dashboard for all user roles
✅ **Local Testing**: Comprehensive test suite for all components
✅ **Privacy Protection**: Face blurring functionality is working as expected
✅ **Code Cleanup**: All unnecessary documentation and code files have been removed

## Architecture Overview

The system now consists of three main components:

1. **Main Delivery Function** (`delivery-function/`): Handles delivery quality assessment with AI vision
2. **Face Blur Function** (`face-blur-function/`): Dedicated service for privacy protection
3. **Dashboard Interface** (`dashboards/frontend/`): React-based user interface for all stakeholders

## Next Steps

- Production monitoring setup
- Performance optimization
- Advanced features implementation
- Dashboard deployment and integration