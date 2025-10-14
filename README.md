# OCI Delivery Agent

Serverless delivery quality assessment system using OCI Functions, Generative AI, and Vision services.

## Quick Deploy

```bash
python3 deploy_function.py
```

## Configuration

Set these variables in OCI Console → Functions → Your Function → Configuration:

- **OCI Authentication**: OCI_USER_OCID, OCI_FINGERPRINT, OCI_KEY_FILE, OCI_TENANCY_OCID, OCI_REGION
- **OCI Resources**: OCI_COMPARTMENT_ID, OCI_OS_BUCKET, OCI_OS_BUCKET_OCID
- **AI Services**: OCI_TEXT_MODEL_OCID, OCI_GENAI_HOSTNAME, OCI_CAPTION_ENDPOINT, OCI_DAMAGE_ENDPOINT
- **Quality Settings**: WEIGHT_TIMELINESS, WEIGHT_LOCATION, WEIGHT_DAMAGE, MAX_DISTANCE_METERS

## Usage

Upload delivery images to your Object Storage bucket to trigger quality assessment.