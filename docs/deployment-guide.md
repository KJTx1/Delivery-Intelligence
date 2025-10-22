# OCI Function Deployment Guide

This guide explains how to deploy the OCI Delivery Agent to OCI Functions using the official [Oracle documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsuploading.htm).

## Prerequisites

1. **OCI CLI configured** with proper authentication
2. **Fn Project CLI installed** (recommended approach)
3. **Docker installed** and running (for Fn Project CLI)
4. **OCI Container Registry access** (OCIR)
5. **VCN with subnets** for function deployment
6. **IAM policies** for Generative AI access

## Project Structure

The project is organized into development and production environments:

```
├── dashboards/                      # Frontend dashboard application
│   ├── frontend/                   # React-based dashboard interface
│   └── wireframes/                 # Dashboard design specifications
├── development/                     # Development environment
│   ├── .env                        # Development configuration
│   ├── src/oci_delivery_agent/     # Source code for development
│   ├── tests/                      # Test files
│   └── assets/                     # Test assets
├── delivery-function/               # Main production function
│   ├── func.yaml                   # Function configuration
│   ├── func.py                     # Function entry point
│   └── src/oci_delivery_agent/     # Deployable source code
├── face-blur-function/              # Face blurring service
│   ├── func.yaml                   # Function configuration
│   ├── func.py                     # Face blurring function
│   └── src/oci_delivery_agent/     # Source code
└── venv/                           # Shared virtual environment
```

## Development Workflow

### 1. Local Development
```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to development directory
cd development

# Edit source code in src/oci_delivery_agent/
# Test with sample assets in assets/
# Run tests: python tests/test_caption_tool.py
```

### 2. Sync to Production
```bash
# Copy development code to production deployment
cp -r development/src/oci_delivery_agent/* delivery-function/src/oci_delivery_agent/
cp -r development/src/oci_delivery_agent/* face-blur-function/src/oci_delivery_agent/
```

### 3. Deploy to OCI Functions

#### Deploy Main Delivery Function
```bash
# Deploy main delivery function
cd delivery-function
fn -v deploy --app delivery-agent-app
```

#### Deploy Face Blur Function
```bash
# Deploy face blur function
cd face-blur-function
fn -v deploy --app face-blur-app
```

## Method 1: Fn Project CLI (Recommended)

Based on the [official Oracle documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsuploading.htm), this is the preferred method for deploying functions.

### 1. Install Fn Project CLI

```bash
# Install Fn Project CLI
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh

# Verify installation
fn --version
```

### 2. Set Up Fn Project Context

```bash
# Create Fn Project context for OCI
fn create context oci --api-url https://functions.us-ashburn-1.oci.oraclecloud.com
fn use context oci
fn update context registry <YOUR_REGION>.ocir.io/<YOUR_NAMESPACE>
fn update context compartment-id <YOUR_COMPARTMENT_ID>
```

### 3. Deploy Function

```bash
# Navigate to function directory
cd delivery-function

# Deploy function (builds, pushes, and deploys in one command)
fn -v deploy --app delivery-agent-app
```

### 4. Set Environment Variables

```bash
# Get function ID
FUNCTION_ID=$(oci fn function list --application-id <YOUR_APPLICATION_ID> --query 'data[0].id' --raw-output)

# Set environment variables
oci fn function update --function-id $FUNCTION_ID --config OCI_COMPARTMENT_ID=<YOUR_COMPARTMENT_ID>
oci fn function update --function-id $FUNCTION_ID --config OCI_OS_NAMESPACE=<YOUR_NAMESPACE>
oci fn function update --function-id $FUNCTION_ID --config OCI_OS_BUCKET=<YOUR_BUCKET_NAME>
oci fn function update --function-id $FUNCTION_ID --config OCI_TEXT_MODEL_OCID=<YOUR_ENDPOINT_OCID>
oci fn function update --function-id $FUNCTION_ID --config OCI_GENAI_HOSTNAME=https://inference.generativeai.us-chicago-1.oci.oraclecloud.com
```

## Method 2: Manual Docker Build

## Deployment Steps

### 1. Build Docker Image

```bash
# Build the Docker image
docker build -t iad.ocir.io/<YOUR_NAMESPACE>/delivery-agent:latest .

# Login to OCIR
docker login iad.ocir.io

# Push the image
docker push iad.ocir.io/<YOUR_NAMESPACE>/delivery-agent:latest
```

### 2. Create Function Application

```bash
# Create application (already done)
oci fn application create \
  --compartment-id <YOUR_COMPARTMENT_ID> \
  --display-name delivery-agent-app \
  --subnet-ids '["<YOUR_SUBNET_ID>"]'
```

### 3. Create Function

```bash
# Create function with custom image
oci fn function create \
  --application-id <YOUR_APPLICATION_ID> \
  --display-name delivery-quality-function \
  --image <YOUR_REGION>.ocir.io/<YOUR_NAMESPACE>/delivery-agent:latest \
  --memory-in-mbs 1024 \
  --timeout-in-seconds 300
```

### 4. Set Environment Variables

```bash
# Set required environment variables
oci fn function update \
  --function-id <FUNCTION_ID> \
  --config OCI_COMPARTMENT_ID=<YOUR_COMPARTMENT_ID>

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config OCI_OS_NAMESPACE=<YOUR_NAMESPACE>

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config OCI_OS_BUCKET=<YOUR_BUCKET_NAME>

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config OCI_TEXT_MODEL_OCID=<YOUR_ENDPOINT_OCID>

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config OCI_GENAI_HOSTNAME=https://inference.generativeai.us-chicago-1.oci.oraclecloud.com

# Set quality weights
oci fn function update \
  --function-id <FUNCTION_ID> \
  --config WEIGHT_TIMELINESS=0.3

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config WEIGHT_LOCATION=0.3

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config WEIGHT_DAMAGE=0.4

oci fn function update \
  --function-id <FUNCTION_ID> \
  --config MAX_DISTANCE_METERS=100
```

### 5. Test Function

```bash
# Create test event
cat > test-event.json << EOF
{
  "data": {
    "resourceName": "sample.jpg"
  },
  "eventTime": "2024-01-10T16:45:00Z",
  "additionalDetails": {
    "expectedLatitude": 37.7749,
    "expectedLongitude": -122.4194,
    "promisedTime": "2024-01-10T17:00:00Z"
  }
}
EOF

# Test function
oci fn function invoke \
  --function-id <FUNCTION_ID> \
  --file test-event.json
```

## Alternative: Manual Deployment via OCI Console

### 1. Create Function Application
1. Go to **OCI Console → Developer Services → Functions**
2. Click **Create Application**
3. Name: `delivery-agent-app`
4. VCN: Select your VCN
5. Subnet: Select your subnet
6. Click **Create**

### 2. Create Function
1. In your application, click **Create Function**
2. Name: `delivery-quality-function`
3. Image: `iad.ocir.io/<YOUR_NAMESPACE>/delivery-agent:latest`
4. Memory: 1024 MB
5. Timeout: 300 seconds
6. Click **Create**

### 3. Configure Environment Variables
1. Go to **Functions → Your Function → Configuration**
2. Add these environment variables:
   - `OCI_COMPARTMENT_ID`: Your compartment OCID
   - `OCI_OS_NAMESPACE`: Your Object Storage namespace
   - `OCI_OS_BUCKET`: Your Object Storage bucket name
   - `OCI_TEXT_MODEL_OCID`: Your GenAI endpoint OCID
   - `OCI_GENAI_HOSTNAME`: Your GenAI hostname
   - `WEIGHT_TIMELINESS`: 0.3
   - `WEIGHT_LOCATION`: 0.3
   - `WEIGHT_DAMAGE`: 0.4
   - `MAX_DISTANCE_METERS`: 100

### 4. Set Up Authentication
Add these authentication variables in OCI Console:
- `OCI_USER_OCID`: Your user OCID
- `OCI_FINGERPRINT`: Your API key fingerprint
- `OCI_KEY_FILE`: Your private key content
- `OCI_TENANCY_OCID`: Your tenancy OCID
- `OCI_REGION`: Your region (e.g., us-ashburn-1)

## Monitoring and Logs

### View Function Logs
```bash
oci fn function logs --function-id <FUNCTION_ID>
```

### Monitor Function Metrics
1. Go to **OCI Console → Monitoring → Metrics**
2. Select **Functions** namespace
3. View function execution metrics

## Current Status

✅ **Function Deployed**: Successfully deployed to OCI Functions
✅ **GenAI Integration**: Complete vision capabilities implemented
✅ **Object Storage**: Full integration working
⚠️ **Authentication**: Currently debugging Instance Principal timeout

## Troubleshooting

### Current Issue: Instance Principal Authentication Timeout

**Problem**: Function hangs when testing Instance Principal authentication
**Symptoms**: 
- Basic connectivity works (`test_type: "basic"`)
- Imports work (`test_type: "imports"`)
- Authentication test hangs (`test_type: "auth"`)

**Debugging Steps**:
1. Check OCI Console logs for detailed error messages
2. Verify Dynamic Group and IAM policies
3. Test with timeout handling (implemented in func.py)
4. Consider fallback to environment variable authentication

### Common Issues

1. **Authentication Errors**
   - Verify OCI credentials are correctly set
   - Check IAM policies for Generative AI access
   - **Current**: Instance Principal authentication timeout

2. **Function Timeout**
   - Increase timeout in function configuration
   - Optimize image processing for faster execution
   - **Current**: Authentication timeout (10 seconds)

3. **Memory Issues**
   - Increase memory allocation for GenAI processing
   - Optimize image size before processing
   - **Current**: 2048MB allocated

4. **GenAI API Errors**
   - Verify endpoint OCID is correct
   - Check compartment access for Generative AI
   - Ensure IAM policies allow Generative AI usage

### Debug Steps

1. **Check Function Logs**
   ```bash
   oci fn function logs --function-id <FUNCTION_ID> --limit 50
   ```

2. **Test Locally**
   ```bash
   python tests/test_caption_tool.py
   ```

3. **Verify Environment Variables**
   ```bash
   oci fn function get --function-id <FUNCTION_ID>
   ```

## Production Considerations

### Security
- Use instance principal authentication when possible
- Store sensitive credentials in OCI Vault
- Implement proper IAM policies

### Performance
- Monitor function execution time
- Optimize image processing
- Consider caching for repeated requests

### Cost Optimization
- Monitor function invocations
- Optimize memory allocation
- Use appropriate timeout values

### Scaling
- Functions auto-scale based on demand
- Monitor concurrent executions
- Set appropriate concurrency limits
