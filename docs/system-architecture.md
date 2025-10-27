# OCI Delivery Agent Architecture

This document outlines the LangChain-driven workflow that orchestrates proof-of-delivery intelligence across Oracle Cloud Infrastructure (OCI) services.

## Project Structure

The project is organized into development and production environments for optimal workflow management:

```
├── dashboards/                      # Frontend dashboard application
│   ├── frontend/                   # React-based dashboard interface
│   │   ├── src/pages/              # Role-specific dashboards
│   │   │   ├── CustomerService/    # Customer service dashboard
│   │   │   ├── Driver/             # Driver performance dashboard
│   │   │   └── OperationsManager/  # Operations management dashboard
│   │   └── dist/                   # Built dashboard assets
│   └── wireframes/                 # Dashboard design specifications
├── development/                     # Development Environment
│   ├── .env                        # Development configuration
│   ├── src/oci_delivery_agent/     # Source code for development
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
├── delivery-function/               # Main Production Function
│   ├── func.yaml                    # Function configuration
│   ├── func.py                      # Function entry point
│   ├── requirements.txt             # Python dependencies
│   └── src/oci_delivery_agent/     # Deployable source code
├── face-blur-function/              # Face Blurring Service
│   ├── func.yaml                    # Function configuration
│   ├── func.py                      # Face blurring function
│   ├── requirements.txt           # Python dependencies
│   └── src/oci_delivery_agent/     # Source code
└── venv/                           # Shared virtual environment
```

## Development Workflow

1. **Local Development**: Edit code in `development/src/oci_delivery_agent/`
2. **Testing**: Run tests with sample assets in `development/tests/`
3. **Sync to Production**: Copy changes to `delivery-function/src/oci_delivery_agent/`
4. **Deploy**: Use Fn Project CLI from `delivery-function/` directory

## 1. Event Trigger & Ingestion
1. **OCI Events** listens to `com.oraclecloud.objectstorage.createobject` events filtered to the delivery bucket prefix.
2. Events route to an **OCI Function** (`src/oci_delivery_agent/handlers.py::handler`).
3. The function parses the event payload to determine the object path and delivery metadata payload.

## 2. Retrieval & Metadata Enrichment
- `ObjectRetrievalTool` calls Object Storage via the Python SDK to download the image and capture metadata.
- The image payload is Base64 encoded so that downstream LangChain chains can share the asset without direct binary handling.

## 3. EXIF & Geolocation Extraction
- `ExifExtractionTool` leverages Pillow to unpack EXIF blocks, flatten GPS metadata, and normalize it for distance calculations.
- `compute_location_accuracy` in `chains.py` converts GPS coordinates to decimal degrees and evaluates the Haversine distance against expected delivery coordinates stored in the event payload or retrieved via a geocoding API.

## 4. Visual Intelligence (Context-Aware Sequential Chaining)
- `ImageCaptionTool` uses OCI Generative AI Vision models to analyze delivery scenes and generate structured JSON captions with scene type, package visibility, location details, environmental conditions, and safety assessment.
- `DamageDetectionTool` leverages OCI Generative AI Vision models to detect and classify package damage with structured JSON output including overall severity, specific damage indicators (box deformation, corner damage, leakage, packaging integrity), and confidence scores.
- **Context Passing**: Caption results are passed to damage assessment to ensure consistency. The damage model receives information about identified packages (e.g., "white plastic bag and blue cooler") so both tools analyze the same items.
- **Package Definition**: Supports all delivery item types including cardboard boxes, plastic bags, envelopes, coolers, containers, and parcels.

## 5. LangChain Orchestration
- `build_caption_chain` processes structured JSON captions from the vision model to produce reviewer-friendly summaries using OCI Generative AI chat API.
- `run_quality_pipeline` orchestrates retrieval, EXIF parsing, captioning, and damage detection tools. It computes delivery quality metrics using structured JSON outputs and feeds them into reviewer prompts.
- **Structured JSON Processing**: All vision tools return structured JSON for consistent pipeline processing and quality scoring.
- **OCI Generative AI Integration**: Uses the `chat` API with `DedicatedServingMode` and endpoint OCID for production-grade text generation.

## 6. Delivery Quality Index
- `compute_quality_index` merges timeliness, location accuracy, and damage scores using configurable weights to produce a normalized Delivery Quality Index.
- Scores and supporting metadata are packaged into a JSON payload ready for storage.

## 7. Persistence & Alerts
- `store_quality_event` is the hook for persisting results into Autonomous Data Warehouse or an OCI Database table.
- `trigger_alert` publishes to Notifications or Streaming when the LLM assessment flags the delivery for manual review.

## 8. OCI Generative AI Implementation
- **API Endpoint**: Uses `https://inference.generativeai.{region}.oci.oraclecloud.com` for chat API calls
- **Authentication**: Leverages OCI SDK configuration from `~/.oci/config` or environment variables
- **Model Access**: Requires `OCI_TEXT_MODEL_OCID` (endpoint OCID) and `OCI_COMPARTMENT_ID`
- **Request Format**: Uses `GenericChatRequest` with `DedicatedServingMode` for production endpoints
- **Multimodal Support**: Supports both text and image content for vision analysis
- **Structured Output**: Vision models return structured JSON with specific schemas for captions and damage detection
- **Response Handling**: Extracts text from nested `chat_response.choices[0].message.content[0].text` structure
- **Error Handling**: Graceful fallback with detailed error messages for debugging

## 9. Extensibility
- The `toolset` factory enables registering additional LangChain tools (e.g., OCR, additional computer vision models).
- Configuration is centralized via `config.py`, ensuring deployment environments can adjust weights, endpoints, or alerting thresholds without code changes.
- `python -m oci_delivery_agent.start` provides a CLI harness mirroring the production workflow for rapid iteration and manual testing.
