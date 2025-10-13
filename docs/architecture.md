# OCI Delivery Agent Workflow

This document outlines the LangChain-driven workflow that orchestrates proof-of-delivery intelligence across Oracle Cloud Infrastructure (OCI) services.

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

## 4. Visual Intelligence
- `ImageCaptionTool` integrates with an OCI Vision or OCI Data Science deployment endpoint to summarize scene context.
- `DamageDetectionTool` invokes a custom Vision model or YOLO deployment to classify visible package damage likelihood.

## 5. LangChain Orchestration
- `build_caption_chain` blends raw metadata with model-generated captions to produce a reviewer-friendly summary using a text LLM hosted on OCI Generative AI.
- `run_quality_pipeline` composes retrieval, EXIF parsing, captioning, and damage detection tools. It computes delivery quality metrics and feeds them into a reviewer prompt handled by `build_workflow_chain`.

## 6. Delivery Quality Index
- `compute_quality_index` merges timeliness, location accuracy, and damage scores using configurable weights to produce a normalized Delivery Quality Index.
- Scores and supporting metadata are packaged into a JSON payload ready for storage.

## 7. Persistence & Alerts
- `store_quality_event` is the hook for persisting results into Autonomous Data Warehouse or an OCI Database table.
- `trigger_alert` publishes to Notifications or Streaming when the LLM assessment flags the delivery for manual review.

## 8. Extensibility
- The `toolset` factory enables registering additional LangChain tools (e.g., OCR, additional computer vision models).
- Configuration is centralized via `config.py`, ensuring deployment environments can adjust weights, endpoints, or alerting thresholds without code changes.
- `python -m oci_delivery_agent.start` provides a CLI harness mirroring the production workflow for rapid iteration and manual testing.
