# Step 1: IAM Configuration Setup

## Prerequisites
Before configuring IAM policies, you need:
1. **OCI Compartment** where your resources will be deployed
2. **OCI Object Storage bucket** for delivery photos
3. **OCI Generative AI model** for text processing
4. **OCI Vision service** endpoints (optional for local testing)

## Required IAM Policies

### 1. Create Dynamic Group
First, create a dynamic group for your OCI Function:

**Dynamic Group Name:** `DeliveryAgent-DynamicGroup`

**Matching Rules:**
```
resource.type = 'fnfunc'
resource.compartment.id = '<your-compartment-id>'
```

### 2. Create IAM Policies

#### Policy 1: Object Storage Access
**Policy Name:** `DeliveryAgent-ObjectStorage-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to manage objects in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'
Allow dynamic-group DeliveryAgent-DynamicGroup to read buckets in compartment <compartment-name> where target.bucket.name='<delivery-bucket-name>'
```

#### Policy 2: AI Services Access
**Policy Name:** `DeliveryAgent-AI-Services-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-generative-family in compartment <compartment-name>
Allow dynamic-group DeliveryAgent-DynamicGroup to use ai-service-vision-family in compartment <compartment-name>
```

#### Policy 3: Notification Service Access
**Policy Name:** `DeliveryAgent-Notification-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to use ons in compartment <compartment-name>
```

#### Policy 4: Database Access (if using ADW)
**Policy Name:** `DeliveryAgent-Database-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to manage autonomous-database-family in compartment <compartment-name>
Allow dynamic-group DeliveryAgent-DynamicGroup to use database-family in compartment <compartment-name>
```

#### Policy 5: Compartment Access
**Policy Name:** `DeliveryAgent-Compartment-Policy`

```sql
Allow dynamic-group DeliveryAgent-DynamicGroup to read compartments in compartment <compartment-name>
```

## Step-by-Step Setup Instructions

### 1. Create Dynamic Group
1. Go to **Identity & Security** → **Dynamic Groups**
2. Click **Create Dynamic Group**
3. Name: `DeliveryAgent-DynamicGroup`
4. Description: `Dynamic group for OCI Delivery Agent Function`
5. Matching Rules: Add the rule above with your compartment ID
6. Click **Create**

### 2. Create Policies
1. Go to **Identity & Security** → **Policies**
2. Click **Create Policy**
3. For each policy above:
   - Name: Use the policy name provided
   - Description: Brief description of the policy
   - Policy Builder: Use the SQL statements provided
   - Click **Create**

### 3. Verify Setup
After creating all policies, verify:
- Dynamic group exists and has the correct matching rules
- All 5 policies are created and attached to the correct compartment
- Policies reference the correct dynamic group name

## Testing IAM Setup

Once configured, you can test the IAM setup by:
1. Deploying a simple OCI Function
2. Testing access to each service individually
3. Checking audit logs for any permission denials

## Next Steps
After IAM is configured, we'll move to Step 2: Environment Configuration.
