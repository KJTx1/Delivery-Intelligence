# OCI Delivery Agent with LangChain

This repository demonstrates how to orchestrate a proof-of-delivery quality agent on Oracle Cloud Infrastructure (OCI) using LangChain tools and chains. The workflow follows the stages described in the internal specification and connects Object Storage, Vision, Generative AI, Maps, and Notifications services.

## Components
- `src/oci_delivery_agent/config.py`: Dataclasses for managing deployment configuration.
- `src/oci_delivery_agent/tools.py`: LangChain `BaseTool` implementations that wrap Object Storage, EXIF extraction, captioning, and damage detection.
- `src/oci_delivery_agent/chains.py`: Delivery quality scoring logic, including the Delivery Quality Index computation and SequentialChain orchestration.
- `src/oci_delivery_agent/handlers.py`: OCI Function handler that ties Events, LangChain, persistence, and notifications together.
- `docs/architecture.md`: High-level architecture and data flow documentation.

## Running the Workflow
1. Deploy the `handler` function to OCI Functions with appropriate IAM policies.
2. Configure environment variables for Object Storage, Vision endpoints, and notification targets.
3. Connect the function to an OCI Events rule watching the delivery image bucket.
4. Ensure Pillow, LangChain, and OCI SDK dependencies are included in the function image or layer.

For local testing, a LangChain start script is available:

```bash
python -m oci_delivery_agent.start \
  sample_delivery.jpg \
  37.7749 \
  -122.4194 \
  2024-01-10T17:00:00 \
  2024-01-10T16:45:00 \
  --dry-run \
  --local-asset-root ./local_assets
```

The script mirrors the OCI workflow while allowing dry-run execution using a fake LLM. Omit `--dry-run` and provide real OCI configuration values to send requests to deployed Generative AI and Vision services.

## Extending
- Add new LangChain tools for OCR, barcode scanning, or customer signature verification.
- Replace the placeholder Vision client logic with calls to live OCI Vision/Data Science endpoints.
- Implement `store_quality_event` and `trigger_alert` to integrate with ADW, Notifications, or Stream Processing.
