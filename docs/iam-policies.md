# IAM Policies Required for OCI Delivery Agent Function

This document outlines the minimum IAM policies required for the OCI Function to operate the delivery quality workflow.

## Function Identity Requirements

The OCI Function needs a **Dynamic Group** with the following matching rules:
```
resource.type = 'fnfunc'
resource.compartment.id = '<your-compartment-id>'
```

## Required IAM Policies

### 1. Object Storage Access
**Policy Name:** `DeliveryAgent-ObjectStorage-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to manage objects in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'
Allow dynamic-group DeliveryAgent-DynamicGroup to read buckets in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'
```

**Specific Permissions Needed:**
- `objectstorage:object:read` - To download delivery photos
- `objectstorage:bucket:read` - To access bucket metadata

### 2. OCI Vision Service Access
**Policy Name:** `DeliveryAgent-Vision-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-vision-family in compartment <compartment-name>
```

**Specific Permissions Needed:**
- `ai-service-vision:analyze-image` - For image captioning and damage detection
- `ai-service-vision:analyze-document` - If using document analysis features

### 3. OCI Generative AI Service Access
**Policy Name:** `DeliveryAgent-GenerativeAI-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-generative-family in compartment <compartment-name>
```

**Specific Permissions Needed:**
- `ai-service-generative:generate-text` - For LLM text generation
- `ai-service-generative:generate-image` - If using image generation features

### 4. OCI Notification Service Access
**Policy Name:** `DeliveryAgent-Notification-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to use ons in compartment <compartment-name>
```

**Specific Permissions Needed:**
- `ons:topic:publish` - To send quality alerts and notifications

### 5. Database Access (Autonomous Data Warehouse)
**Policy Name:** `DeliveryAgent-Database-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to manage autonomous-database-family in compartment <compartment-name>
Allow dynamic-group DeliveryAgent-DynamicGroup to use database-family in compartment <compartment-name>
```

**Specific Permissions Needed:**
- `database:autonomous-database:read` - To read database metadata
- `database:autonomous-database:connect` - To establish database connections
- `database:table:write` - To insert quality event records

### 6. Compartment Access
**Policy Name:** `DeliveryAgent-Compartment-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to read compartments in compartment <compartment-name>
```

**Specific Permissions Needed:**
- `compartment:read` - To access compartment information for service calls

## Complete Policy Example

Here's a consolidated policy that includes all required permissions:

```sql
-- Object Storage Access
Allow dynamic-group DeliveryAgent-DynamicGroup to manage objects in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'
Allow dynamic-group DeliveryAgent-DynamicGroup to read buckets in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'

-- AI Services Access
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-vision-family in compartment <compartment-name>
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-generative-family in compartment <compartment-name>

-- Notification Service Access
Allow dynamic-group DeliveryAgent-DynamicGroup to use ons in compartment <compartment-name>

-- Database Access
Allow dynamic-group DeliveryAgent-DynamicGroup to manage autonomous-database-family in compartment <compartment-name>
Allow dynamic-group DeliveryAgent-DynamicGroup to use database-family in compartment <compartment-name>

-- Compartment Access
Allow dynamic-group DeliveryAgent-DynamicGroup to read compartments in compartment <compartment-name>
```

## Service-Specific Resource Requirements

### Object Storage
- **Namespace:** Your OCI Object Storage namespace
- **Bucket:** Specific bucket containing delivery photos
- **Objects:** Read access to objects with the configured delivery prefix

### Vision Service
- **Compartment:** Access to the compartment containing Vision service resources
- **Endpoints:** Access to image analysis endpoints for captioning and damage detection

### Generative AI
- **Compartment:** Access to the compartment containing Generative AI resources
- **Model:** Access to the specific text generation model (OCI_TEXT_MODEL_OCID)

### Notification Service
- **Topic:** Access to the notification topic (NOTIFICATION_TOPIC_ID)
- **Compartment:** Access to the compartment containing the notification topic

### Database
- **Autonomous Database:** Access to the ADW instance for storing quality events
- **Table:** Write access to the quality events table (QUALITY_TABLE)

## Security Considerations

1. **Principle of Least Privilege:** Only grant the minimum permissions required
2. **Resource-Specific Access:** Use resource-specific conditions where possible
3. **Compartment Isolation:** Ensure the function only accesses resources in the designated compartment
4. **Audit Logging:** Enable audit logging for all service interactions

## Testing the Policies

After applying these policies, test the function with:

```bash
# Test with a sample delivery photo
python -m oci_delivery_agent.start \
  sample_delivery.jpg \
  37.7749 \
  -122.4194 \
  2024-01-10T17:00:00 \
  2024-01-10T16:45:00 \
  --compartment-id <your-compartment-id> \
  --os-namespace <your-namespace> \
  --os-bucket <your-bucket>
```

## Troubleshooting

If you encounter permission errors:

1. **Check Dynamic Group Membership:** Ensure the function is properly added to the dynamic group
2. **Verify Policy Attachments:** Confirm policies are attached to the correct compartment
3. **Review Audit Logs:** Check OCI Audit logs for specific permission denials
4. **Test Individual Services:** Use OCI CLI to test each service independently

## Additional Notes

- The function uses the OCI SDK's default authentication mechanism
- Environment variables in the `.env` file configure the specific resources to access
- The function supports both live OCI operations and local testing modes
- All service calls are made from within the OCI Function runtime environment
