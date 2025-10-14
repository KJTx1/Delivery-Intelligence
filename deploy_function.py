#!/usr/bin/env python3
"""
OCI Function Deployment Script
Automates the deployment of the delivery quality function to OCI
"""

import os
import sys
import json
import zipfile
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load configuration from environment"""
    load_dotenv("local.env")
    
    return {
        'compartment_id': os.getenv("OCI_COMPARTMENT_ID"),
        'namespace': os.getenv("OCI_OS_NAMESPACE"),
        'bucket': os.getenv("OCI_OS_BUCKET"),
        'app_name': 'delivery-agent-app',
        'function_name': 'delivery-quality-function'
    }

def create_deployment_package():
    """Create deployment package for OCI Function"""
    print("📦 Creating deployment package...")
    
    # Create deployment directory
    deploy_dir = Path("function-deployment")
    if deploy_dir.exists():
        import shutil
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy source code
    src_dir = Path("src")
    if src_dir.exists():
        import shutil
        shutil.copytree(src_dir, deploy_dir / "src")
        print("   ✅ Source code copied")
    else:
        print("   ❌ Source directory not found")
        return False
    
    # Create requirements.txt for function
    requirements_content = """langchain==0.1.0
pillow
python-dotenv
oci
requests
"""
    
    with open(deploy_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    print("   ✅ Requirements.txt created")
    
    # Create function entry point
    entry_point = """import json
import sys
import os

# Add src to path
sys.path.append('/function/src')

def handler(ctx, data):
    try:
        from oci_delivery_agent.handlers import handler as delivery_handler
        return delivery_handler(ctx, data)
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
"""
    
    with open(deploy_dir / "func.py", "w") as f:
        f.write(entry_point)
    print("   ✅ Function entry point created")
    
    # Create zip file
    zip_path = "function.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arc_path)
    
    print(f"   ✅ Deployment package created: {zip_path}")
    return True

def check_oci_cli():
    """Check if OCI CLI is installed and configured"""
    print("🔍 Checking OCI CLI...")
    
    try:
        result = subprocess.run(['oci', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ OCI CLI installed: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ OCI CLI not found")
            return False
    except FileNotFoundError:
        print("   ❌ OCI CLI not installed")
        return False

def get_compartment_id():
    """Get compartment ID from user or environment"""
    config = load_config()
    
    if config['compartment_id']:
        print(f"   📍 Using compartment ID from environment: {config['compartment_id']}")
        return config['compartment_id']
    
    print("   ❓ Please provide your OCI compartment ID:")
    print("      You can find this in OCI Console → Identity → Compartments")
    compartment_id = input("   Compartment ID: ").strip()
    
    if not compartment_id:
        print("   ❌ Compartment ID is required")
        return None
    
    return compartment_id

def get_subnet_id():
    """Get subnet ID for function deployment"""
    print("   ❓ Please provide your VCN subnet ID:")
    print("      You can find this in OCI Console → Networking → Virtual Cloud Networks")
    subnet_id = input("   Subnet ID: ").strip()
    
    if not subnet_id:
        print("   ❌ Subnet ID is required")
        return None
    
    return subnet_id

def create_application(compartment_id, subnet_id):
    """Create OCI Function application"""
    print("🏗️  Creating OCI Function application...")
    
    app_name = "delivery-agent-app"
    
    # Check if application already exists
    try:
        result = subprocess.run([
            'oci', 'fn', 'application', 'list',
            '--compartment-id', compartment_id,
            '--query', f'data[?displayName==`{app_name}`]'
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip() != '[]':
            print(f"   ✅ Application '{app_name}' already exists")
            # Extract application ID from output
            import json
            apps = json.loads(result.stdout)
            if apps:
                return apps[0]['id']
    
    except Exception as e:
        print(f"   ⚠️  Could not check existing applications: {e}")
    
    # Create new application
    try:
        result = subprocess.run([
            'oci', 'fn', 'application', 'create',
            '--compartment-id', compartment_id,
            '--display-name', app_name,
            '--subnet-ids', f'["{subnet_id}"]',
            '--query', 'data.id',
            '--raw-output'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            app_id = result.stdout.strip()
            print(f"   ✅ Application created: {app_id}")
            return app_id
        else:
            print(f"   ❌ Failed to create application: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error creating application: {e}")
        return None

def create_function(app_id):
    """Create OCI Function"""
    print("⚡ Creating OCI Function...")
    
    function_name = "delivery-quality-function"
    
    # Check if function already exists
    try:
        result = subprocess.run([
            'oci', 'fn', 'function', 'list',
            '--application-id', app_id,
            '--query', f'data[?displayName==`{function_name}`]'
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip() != '[]':
            print(f"   ✅ Function '{function_name}' already exists")
            # Extract function ID from output
            import json
            functions = json.loads(result.stdout)
            if functions:
                return functions[0]['id']
    
    except Exception as e:
        print(f"   ⚠️  Could not check existing functions: {e}")
    
    # Create new function
    try:
        result = subprocess.run([
            'oci', 'fn', 'function', 'create',
            '--application-id', app_id,
            '--display-name', function_name,
            '--image', 'fnproject/python:3.9',
            '--memory-in-mbs', '512',
            '--timeout-in-seconds', '300',
            '--query', 'data.id',
            '--raw-output'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            function_id = result.stdout.strip()
            print(f"   ✅ Function created: {function_id}")
            return function_id
        else:
            print(f"   ❌ Failed to create function: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error creating function: {e}")
        return None

def deploy_function_code(function_id):
    """Deploy function code"""
    print("🚀 Deploying function code...")
    
    zip_path = "function.zip"
    if not Path(zip_path).exists():
        print(f"   ❌ Deployment package not found: {zip_path}")
        return False
    
    try:
        result = subprocess.run([
            'oci', 'fn', 'function', 'deploy',
            '--function-id', function_id,
            '--from-file', zip_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Function code deployed successfully")
            return True
        else:
            print(f"   ❌ Failed to deploy function: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error deploying function: {e}")
        return False

def set_environment_variables(function_id):
    """Set environment variables for the function"""
    print("🔧 Environment variables...")
    print("   ℹ️  All configuration must be set manually in OCI Console")
    print("   📋 Required variables: OCI_USER_OCID, OCI_FINGERPRINT, OCI_KEY_FILE,")
    print("      OCI_TENANCY_OCID, OCI_REGION, OCI_COMPARTMENT_ID, OCI_OS_BUCKET,")
    print("      OCI_OS_BUCKET_OCID, OCI_TEXT_MODEL_OCID, OCI_GENAI_HOSTNAME,")
    print("      OCI_CAPTION_ENDPOINT, OCI_DAMAGE_ENDPOINT, WEIGHT_TIMELINESS,")
    print("      WEIGHT_LOCATION, WEIGHT_DAMAGE, MAX_DISTANCE_METERS")

def create_test_event():
    """Create test event for function testing"""
    print("📝 Creating test event...")
    
    test_event = {
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
    
    with open("test-event.json", "w") as f:
        json.dump(test_event, f, indent=2)
    
    print("   ✅ Test event created: test-event.json")
    return True

def test_function(function_id):
    """Test the deployed function"""
    print("🧪 Testing deployed function...")
    
    if not Path("test-event.json").exists():
        print("   ❌ Test event file not found")
        return False
    
    try:
        result = subprocess.run([
            'oci', 'fn', 'function', 'invoke',
            '--function-id', function_id,
            '--file', 'test-event.json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Function test successful")
            print(f"   📊 Response: {result.stdout}")
            return True
        else:
            print(f"   ❌ Function test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing function: {e}")
        return False

def main():
    """Main deployment process"""
    print("🚀 OCI Function Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_oci_cli():
        print("\n❌ OCI CLI not available. Please install and configure OCI CLI first.")
        print("   Visit: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm")
        return
    
    # Create deployment package
    if not create_deployment_package():
        print("\n❌ Failed to create deployment package")
        return
    
    # Get configuration
    compartment_id = get_compartment_id()
    if not compartment_id:
        return
    
    subnet_id = get_subnet_id()
    if not subnet_id:
        return
    
    # Create application
    app_id = create_application(compartment_id, subnet_id)
    if not app_id:
        print("\n❌ Failed to create application")
        return
    
    # Create function
    function_id = create_function(app_id)
    if not function_id:
        print("\n❌ Failed to create function")
        return
    
    # Deploy code
    if not deploy_function_code(function_id):
        print("\n❌ Failed to deploy function code")
        return
    
    # Set environment variables
    set_environment_variables(function_id)
    
    # Create test event
    create_test_event()
    
    # Test function
    if test_function(function_id):
        print("\n🎉 Deployment successful!")
        print(f"   📍 Function ID: {function_id}")
        print(f"   📍 Application ID: {app_id}")
        print("\n🚀 Your OCI Function is ready for integration testing!")
    else:
        print("\n⚠️  Deployment completed but function test failed")
        print("   Check function logs for details:")
        print(f"   oci fn function logs --function-id {function_id}")

if __name__ == "__main__":
    main()
