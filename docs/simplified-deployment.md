# Simplified OCI Function Deployment

## 🎯 Core Environment Variables

For basic OCI Function deployment, you only need these essential variables:

### **Required Variables:**
```bash
# OCI Authentication (Required for function runtime)
OCI_USER_OCID=ocid1.user.oc1..your_user_id
OCI_FINGERPRINT=your_api_key_fingerprint
OCI_KEY_FILE=/Users/oci_api_key.pem
OCI_TENANCY_OCID=ocid1.tenancy.oc1..your_tenancy_id
OCI_REGION=us-ashburn-1

# OCI Compartment
OCI_COMPARTMENT_ID=ocid1.compartment.oc1..your_compartment_id

# OCI Object Storage Bucket
OCI_OS_BUCKET=your_delivery_bucket
OCI_OS_BUCKET_OCID=ocid1.bucket.oc1..your_bucket_id

# OCI Generative AI Configuration
OCI_TEXT_MODEL_OCID=ocid1.generativeai.oc1..your_model_id
OCI_GENAI_HOSTNAME=https://inference.generativeai.us-ashburn-1.oci.oraclecloud.com

# OCI Vision Service Endpoints
OCI_CAPTION_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
OCI_DAMAGE_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
```

### **Quality Configuration (Auto-set by deployment script):**
```bash
WEIGHT_TIMELINESS=0.3
WEIGHT_LOCATION=0.3
WEIGHT_DAMAGE=0.4
MAX_DISTANCE_METERS=50
DELIVERY_PREFIX=deliveries/
LOCAL_ASSET_ROOT=./local_assets
```

## 🚀 Deployment Steps

### 1. **Set up your environment:**
```bash
# Copy the simplified environment template
cp env.simplified .env

# Edit with your actual values
nano .env
```

### 2. **Deploy the function:**
```bash
# Run the deployment script
python3 deploy_function.py
```

### 3. **Manual OCI Console Configuration:**
After deployment, set these in OCI Console → Functions → Your Function → Configuration:

```bash
# OCI Authentication
OCI_USER_OCID=ocid1.user.oc1..your_actual_user_id
OCI_FINGERPRINT=your_actual_api_key_fingerprint
OCI_KEY_FILE=/Users/oci_api_key.pem
OCI_TENANCY_OCID=ocid1.tenancy.oc1..your_actual_tenancy_id
OCI_REGION=us-ashburn-1

# OCI Resources
OCI_COMPARTMENT_ID=ocid1.compartment.oc1..your_actual_compartment_id
OCI_OS_BUCKET=your_actual_delivery_bucket
OCI_OS_BUCKET_OCID=ocid1.bucket.oc1..your_actual_bucket_id
OCI_TEXT_MODEL_OCID=ocid1.generativeai.oc1..your_actual_model_id
OCI_GENAI_HOSTNAME=https://inference.generativeai.us-ashburn-1.oci.oraclecloud.com
OCI_CAPTION_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
OCI_DAMAGE_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
```

## 🧪 Testing

### **Test Event (JSON):**
```json
{
  "data": {
    "resourceName": "deliveries/sample.jpg"
  },
  "eventTime": "2024-01-10T16:45:00Z",
  "additionalDetails": {
    "expectedLatitude": 37.7749,
    "expectedLongitude": -122.4194,
    "promisedTime": "2024-01-10T17:00:00Z"
  }
}
```

### **Test Command:**
```bash
# Test via OCI CLI
oci fn function invoke \
  --function-id <your-function-id> \
  --file test-event.json

# Or test via OCI Console
# Go to Functions → Your Function → Test
```

## 📋 What's Excluded

This simplified deployment **excludes**:
- ❌ Object Storage namespace configuration
- ❌ Database table configuration  
- ❌ Notification service setup
- ❌ Complex IAM policies

## ✅ What's Included

This simplified deployment **includes**:
- ✅ Core quality assessment logic
- ✅ GPS location validation
- ✅ Timeliness scoring
- ✅ Image quality assessment
- ✅ OCI Vision AI integration
- ✅ OCI Generative AI integration

## 🎯 Next Steps

After successful deployment:
1. **Test with sample events**
2. **Verify quality calculations**
3. **Add Object Storage integration later**
4. **Add database persistence later**

Ready for simplified deployment! 🚀
