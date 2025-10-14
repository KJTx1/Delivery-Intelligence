# Step 4: OCI Function Deployment

## Prerequisites
- ✅ Object Storage policy configured
- ✅ Environment variables set up
- ✅ Dynamic group created (if using dynamic group approach)

## Deployment Options

### Option 1: OCI Console (Recommended for Testing)

#### 1. Create Application
1. Go to **Developer Services** → **Functions** → **Applications**
2. Click **Create Application**
3. Fill in details:
   - **Name:** `delivery-agent-app`
   - **Compartment:** Your compartment
   - **VCN:** Select or create a VCN
   - **Subnet:** Select a subnet
4. Click **Create**

#### 2. Create Function
1. In your application, click **Create Function**
2. Fill in details:
   - **Name:** `delivery-quality-function`
   - **Runtime:** Python 3.9
   - **Memory:** 512 MB
   - **Timeout:** 300 seconds
3. Click **Create**

#### 3. Deploy Code
1. **Prepare deployment package:**
   ```bash
   # Create deployment directory
   mkdir function-deployment
   cd function-deployment
   
   # Copy source code
   cp -r ../src .
   cp ../requirements.txt .
   
   # Create requirements.txt if it doesn't exist
   cat > requirements.txt << EOF
   langchain==0.1.0
   pillow
   python-dotenv
   oci
   EOF
   ```

2. **Create zip file:**
   ```bash
   zip -r function.zip .
   ```

3. **Upload to function:**
   - Go to your function in OCI Console
   - Click **Deploy**
   - Upload the `function.zip` file
   - Click **Deploy**

### Option 2: OCI CLI Deployment

#### 1. Install OCI CLI
```bash
# Install OCI CLI
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

#### 2. Configure OCI CLI
```bash
oci setup config
# Follow prompts to configure your credentials
```

#### 3. Deploy Function
```bash
# Create application
oci fn application create \
  --compartment-id <your-compartment-id> \
  --display-name delivery-agent-app \
  --subnet-ids '["<your-subnet-id>"]'

# Create function
oci fn function create \
  --application-id <application-id> \
  --display-name delivery-quality-function \
  --image fnproject/python:3.9

# Deploy code
oci fn function deploy \
  --function-id <function-id> \
  --from-file function.zip
```

## Environment Configuration

### 1. Set Environment Variables
In your function configuration, set these environment variables:

```bash
# Local Development
LOCAL_ASSET_ROOT=./local_assets
DELIVERY_PREFIX=deliveries/

# Quality Weights
WEIGHT_TIMELINESS=0.3
WEIGHT_LOCATION=0.3
WEIGHT_DAMAGE=0.4
MAX_DISTANCE_METERS=50
QUALITY_TABLE=delivery_quality_events

# OCI Configuration
OCI_OS_NAMESPACE=your_oci_namespace
OCI_OS_BUCKET=your_delivery_bucket
OCI_COMPARTMENT_ID=your_compartment_id
OCI_TEXT_MODEL_OCID=your_model_id
OCI_CAPTION_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
OCI_DAMAGE_ENDPOINT=https://vision.oci.oraclecloud.com/20220125/analyzeImage
NOTIFICATION_TOPIC_ID=your_topic_id
```

### 2. Configure Function Handler
Make sure your function has the correct entry point:

```python
# In your function code
def handler(ctx, data):
    from oci_delivery_agent.handlers import handler as delivery_handler
    return delivery_handler(ctx, data)
```

## Testing the Function

### 1. Test with Sample Event
Create a test event payload:

```json
{
  "data": {
    "resourceName": "deliveries/sample_delivery.jpg"
  },
  "eventTime": "2024-01-10T16:45:00Z",
  "additionalDetails": {
    "expectedLatitude": 37.7749,
    "expectedLongitude": -122.4194,
    "promisedTime": "2024-01-10T17:00:00Z"
  }
}
```

### 2. Invoke Function
```bash
# Test function locally
oci fn function invoke \
  --function-id <function-id> \
  --file test-event.json

# Or test via OCI Console
# Go to Functions → Your Function → Test
```

### 3. Check Logs
```bash
# View function logs
oci fn function logs \
  --function-id <function-id> \
  --limit 50
```

## Troubleshooting

### Common Issues:
1. **Import errors** - Check requirements.txt
2. **Permission errors** - Verify IAM policies
3. **Timeout errors** - Increase function timeout
4. **Memory errors** - Increase function memory

### Debug Steps:
1. **Check function logs** for error messages
2. **Verify environment variables** are set correctly
3. **Test individual components** using step3-component-tests.py
4. **Check IAM policies** for proper permissions

## Next Steps

After successful deployment:
1. **Test with real Object Storage events**
2. **Verify quality calculations** work correctly
3. **Test different delivery scenarios**
4. **Monitor function performance**

Ready to deploy your function? 🚀
