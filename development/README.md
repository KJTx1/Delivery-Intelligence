# Development Environment

This directory contains all development and testing resources for the OCI Delivery Agent project.

## Structure

```
development/
├── src/oci_delivery_agent/     # Source code for local development
│   ├── __init__.py
│   ├── chains.py              # LangChain orchestration
│   ├── config.py              # Configuration management
│   ├── handlers.py            # OCI Function entry point
│   ├── start.py               # Local development server
│   └── tools.py               # LangChain tools (Object Storage, EXIF, Vision)
├── tests/                      # Test files
│   ├── test_caption_tool.py   # Vision tool testing
│   └── test_damage_samples.py # Damage detection testing
├── assets/                     # Test assets and sample data
│   └── deliveries/             # Sample delivery images
│       ├── sample.jpg
│       ├── damage1.jpg
│       ├── damage2.jpg
│       ├── damage3.jpg
│       ├── damage4.jpg
│       └── damage5.jpg
└── README.md                   # This file
```

## Development Workflow

### 1. Local Development
- **Edit code** in `src/oci_delivery_agent/`
- **Test locally** using the test files in `tests/`
- **Use sample assets** from `assets/` for testing

### 2. Testing
```bash
# From project root, activate virtual environment
cd /Users/zhizhyan/Desktop/Codex
source venv/bin/activate

# Navigate to development directory
cd development

# Run caption tool tests
python tests/test_caption_tool.py

# Run damage detection tests
python tests/test_damage_samples.py
```

### Test Results
- ✅ **Environment Loading**: `.env` file loads correctly
- ✅ **Object Storage**: Automatic fallback to local assets
- ✅ **GenAI Vision**: Full image captioning and damage detection
- ✅ **Asset Management**: Sample images accessible from `assets/`

### 3. Deployment
- **Sync changes** from `development/src/` to `../delivery-function/src/`
- **Deploy** using Fn Project CLI from `../delivery-function/`

## Key Features

- **Local Development**: All source code in one place for easy editing
- **Comprehensive Testing**: Full test suite with sample assets
- **Asset Management**: Organized test images and data
- **Clean Separation**: Development vs. production deployment

## Environment Configuration

The development environment uses a `.env` file for configuration:
- **Location**: `development/.env`
- **Purpose**: Local development and testing
- **Variables**: OCI credentials, endpoints, and local settings
- **Loading**: Automatically loaded by test files with `load_dotenv('.env')`

## Import Paths

The test files automatically add the `src/` directory to the Python path:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

This allows importing `oci_delivery_agent` modules directly in tests.

## Sample Assets

- **sample.jpg**: Clean delivery image for basic testing
- **damage1-5.jpg**: Various damage scenarios for damage detection testing

All assets are located in `assets/deliveries/` and are used by the test files for comprehensive testing.
