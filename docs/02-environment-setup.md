# Step 2: Environment Configuration Setup

## Environment Variables Required

### Core Configuration
```bash
# Local Development
LOCAL_ASSET_ROOT=./local_assets
DELIVERY_PREFIX=deliveries/

# Quality Weights (must sum to 1.0)
WEIGHT_TIMELINESS=0.3
WEIGHT_LOCATION=0.3
WEIGHT_DAMAGE=0.4

# Geolocation Settings
MAX_DISTANCE_METERS=50

# Database Configuration
QUALITY_TABLE=delivery_quality_events
```

### OCI Service Configuration
```bash
# Object Storage
OCI_OS_NAMESPACE=your_oci_namespace
OCI_OS_BUCKET=your_delivery_bucket

# Compartment and AI Services
OCI_COMPARTMENT_ID=<YOUR_COMPARTMENT_ID>
OCI_TEXT_MODEL_OCID=<YOUR_ENDPOINT_OCID>

# Vision Services (optional for local testing)
OCI_CAPTION_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
OCI_DAMAGE_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage

# Notification Service
NOTIFICATION_TOPIC_ID=<YOUR_TOPIC_ID>
```

## Setup Instructions

### 1. Create Environment File
```bash
# Copy the template
cp env.example .env

# Edit with your actual values
nano .env
```

### 2. Configure for Local Testing
For local testing, you only need:
```bash
# Essential for local testing
LOCAL_ASSET_ROOT=./local_assets
DELIVERY_PREFIX=deliveries/
WEIGHT_TIMELINESS=0.3
WEIGHT_LOCATION=0.3
WEIGHT_DAMAGE=0.4
MAX_DISTANCE_METERS=50
QUALITY_TABLE=delivery_quality_events

# Dummy values for OCI services (not used in dry-run mode)
OCI_OS_NAMESPACE=dummy
OCI_OS_BUCKET=dummy
OCI_COMPARTMENT_ID=ocid1.compartment.oc1..dummy
OCI_TEXT_MODEL_OCID=ocid1.generativeai.oc1..dummy
OCI_CAPTION_ENDPOINT=https://dummy.com
OCI_DAMAGE_ENDPOINT=https://dummy.com
NOTIFICATION_TOPIC_ID=ocid1.onstopic.oc1..dummy
```

### 3. Configure for Production
For production deployment, replace dummy values with real OCI resource IDs:
```bash
# Real OCI values
OCI_OS_NAMESPACE=your_actual_namespace
OCI_OS_BUCKET=your_actual_bucket
OCI_COMPARTMENT_ID=<YOUR_ACTUAL_COMPARTMENT_ID>
OCI_TEXT_MODEL_OCID=<YOUR_ACTUAL_ENDPOINT_OCID>
# ... etc
```

## Validation

### 1. Check Environment Loading
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Check essential variables
required_vars = [
    'LOCAL_ASSET_ROOT',
    'WEIGHT_TIMELINESS',
    'WEIGHT_LOCATION', 
    'WEIGHT_DAMAGE',
    'MAX_DISTANCE_METERS'
]

for var in required_vars:
    value = os.environ.get(var)
    print(f"{var}: {value}")
```

### 2. Validate Quality Weights
```python
# Ensure weights sum to 1.0
timeliness = float(os.environ.get('WEIGHT_TIMELINESS', '0.3'))
location = float(os.environ.get('WEIGHT_LOCATION', '0.3'))
damage = float(os.environ.get('WEIGHT_DAMAGE', '0.4'))

total = timeliness + location + damage
print(f"Total weights: {total}")
assert abs(total - 1.0) < 0.01, "Weights must sum to 1.0"
```

### 3. Test Local Asset Directory
```python
import os
from pathlib import Path

local_root = os.environ.get('LOCAL_ASSET_ROOT', './local_assets')
if not os.path.exists(local_root):
    os.makedirs(local_root, exist_ok=True)
    print(f"Created directory: {local_root}")
else:
    print(f"Directory exists: {local_root}")
```

## Next Steps
After environment is configured, we'll move to Step 3: Component Testing.
