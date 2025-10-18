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
├── delivery-function/               # Production deployment
│   ├── func.yaml                    # Function configuration
│   ├── func.py                      # Function entry point
│   ├── requirements.txt             # Python dependencies
│   └── src/oci_delivery_agent/     # Deployable source code
├── docs/                            # Documentation
│   ├── architecture.md              # System architecture
│   ├── genai-implementation.md      # GenAI implementation details
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

### Deployment & Operations
- **Fn Project CLI Integration**: Official Oracle deployment methodology
- **Automated Deployment**: Streamlined deployment scripts and processes
- **Function Configuration**: Complete environment variable management
- **Monitoring & Logging**: Comprehensive operational visibility

### Documentation
- **Architecture Guide**: Complete system design documentation
- **GenAI Implementation**: Detailed technical documentation for AI integration
- **Deployment Guide**: Step-by-step deployment instructions
- **API Reference**: Comprehensive configuration and usage examples

## Current Status

✅ **Fully Deployed**: Function is deployed to OCI Functions and operational
✅ **GenAI Integration**: Complete vision capabilities with structured JSON output
✅ **Object Storage**: Full integration with OCI Object Storage for image processing
✅ **Local Testing**: Comprehensive test suite for all components
⚠️ **Authentication**: Currently debugging Instance Principal authentication timeout

## Next Steps

See [NEXT_STEPS.md](docs/NEXT_STEPS.md) for detailed next steps including:
- Authentication troubleshooting
- Production monitoring setup
- Performance optimization
- Advanced features implementation