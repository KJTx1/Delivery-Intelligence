#!/usr/bin/env python3
"""
OCI Function Build and Deploy Script
Automates the complete build and deployment process for the OCI Delivery Agent
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load configuration from environment"""
    load_dotenv(".env")
    
    return {
        'compartment_id': os.getenv("OCI_COMPARTMENT_ID"),
        'namespace': os.getenv("OCI_OS_NAMESPACE"),
        'bucket': os.getenv("OCI_OS_BUCKET"),
        'app_name': 'delivery-agent-app',
        'function_name': 'delivery-quality-function'
    }

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("   ❌ .env file not found. Please copy env.example to .env and configure it.")
        return False
    
    # Check if source code exists
    if not Path("src/oci_delivery_agent").exists():
        print("   ❌ Source code not found in src/oci_delivery_agent/")
        return False
    
    # Check if delivery-function directory exists
    if not Path("delivery-function").exists():
        print("   ❌ delivery-function directory not found")
        return False
    
    print("   ✅ Prerequisites check passed")
    return True

def sync_source_code():
    """Sync source code from src/ to delivery-function/src/"""
    print("🔄 Syncing source code...")
    
    try:
        # Remove existing src directory in delivery-function
        if Path("delivery-function/src").exists():
            shutil.rmtree("delivery-function/src")
        
        # Copy source code
        shutil.copytree("src", "delivery-function/src")
        print("   ✅ Source code synced to delivery-function/src/")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to sync source code: {e}")
        return False

def check_fn_cli():
    """Check if Fn Project CLI is installed"""
    print("🔍 Checking Fn Project CLI...")
    
    try:
        result = subprocess.run(['fn', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Fn Project CLI installed: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Fn Project CLI not found")
            return False
    except FileNotFoundError:
        print("   ❌ Fn Project CLI not installed")
        return False

def install_fn_cli():
    """Install Fn Project CLI"""
    print("📦 Installing Fn Project CLI...")
    
    try:
        # Download and install Fn Project CLI
        result = subprocess.run([
            'curl', '-LSs', 'https://raw.githubusercontent.com/fnproject/cli/master/install'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Fn Project CLI installation script downloaded")
            print("   ℹ️  Please run: curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh")
            return False
        else:
            print("   ❌ Failed to download Fn Project CLI")
            return False
            
    except Exception as e:
        print(f"   ❌ Error installing Fn Project CLI: {e}")
        return False

def setup_fn_context():
    """Set up Fn Project CLI context for OCI"""
    print("🔧 Setting up Fn Project CLI context...")
    
    config = load_config()
    
    try:
        # Create context
        result = subprocess.run([
            'fn', 'create', 'context', 'oci',
            '--api-url', 'https://functions.us-ashburn-1.oci.oraclecloud.com'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ⚠️  Context may already exist: {result.stderr}")
        
        # Use context
        result = subprocess.run(['fn', 'use', 'context', 'oci'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ Failed to use context: {result.stderr}")
            return False
        
        # Update registry
        result = subprocess.run([
            'fn', 'update', 'context', 'registry', 'iad.ocir.io/orasenatdpltintegration03'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Failed to set registry: {result.stderr}")
            return False
        
        # Update compartment
        result = subprocess.run([
            'fn', 'update', 'context', 'compartment-id', config['compartment_id']
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Failed to set compartment: {result.stderr}")
            return False
        
        print("   ✅ Fn Project context configured")
        return True
        
    except Exception as e:
        print(f"   ❌ Error setting up context: {e}")
        return False

def deploy_function():
    """Deploy function using Fn Project CLI"""
    print("🚀 Deploying function...")
    
    config = load_config()
    
    try:
        # Change to function directory
        os.chdir('delivery-function')
        
        # Deploy function
        result = subprocess.run([
            'fn', '-v', 'deploy', '--app', config['app_name']
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Function deployed successfully")
            print(f"   📊 Output: {result.stdout}")
            return True
        else:
            print(f"   ❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error deploying function: {e}")
        return False
    finally:
        # Change back to parent directory
        os.chdir('..')

def get_function_id():
    """Get function ID from OCI"""
    print("🔍 Getting function ID...")
    
    config = load_config()
    
    try:
        result = subprocess.run([
            'oci', 'fn', 'function', 'list',
            '--application-id', 'ocid1.fnapp.oc1.iad.amaaaaaawe6j4fqacp4fg46c2xk4zyxv7nctku422mui3lg7yhhhonwscrlq',
            '--query', f'data[?displayName==`{config["function_name"]}`].id',
            '--raw-output'
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            function_id = result.stdout.strip()
            print(f"   ✅ Function ID: {function_id}")
            return function_id
        else:
            print("   ❌ Function not found")
            return None
            
    except Exception as e:
        print(f"   ❌ Error getting function ID: {e}")
        return None

def configure_function(function_id):
    """Configure function environment variables"""
    print("🔧 Configuring function...")
    
    config = load_config()
    
    # Required environment variables
    env_vars = {
        'OCI_COMPARTMENT_ID': config['compartment_id'],
        'OCI_OS_NAMESPACE': config['namespace'],
        'OCI_OS_BUCKET': config['bucket'],
        'OCI_TEXT_MODEL_OCID': os.getenv('OCI_TEXT_MODEL_OCID'),
        'OCI_GENAI_HOSTNAME': os.getenv('OCI_GENAI_HOSTNAME'),
        'WEIGHT_TIMELINESS': '0.3',
        'WEIGHT_LOCATION': '0.3',
        'WEIGHT_DAMAGE': '0.4',
        'MAX_DISTANCE_METERS': '100'
    }
    
    success_count = 0
    total_count = len(env_vars)
    
    for key, value in env_vars.items():
        if value:
            try:
                result = subprocess.run([
                    'oci', 'fn', 'function', 'update',
                    '--function-id', function_id,
                    '--config', f'{key}={value}'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ Set {key}")
                    success_count += 1
                else:
                    print(f"   ⚠️  Failed to set {key}: {result.stderr}")
            except Exception as e:
                print(f"   ⚠️  Error setting {key}: {e}")
    
    print(f"   📊 Configured {success_count}/{total_count} environment variables")
    return success_count > 0

def create_test_event():
    """Create test event for function testing"""
    print("📝 Creating test event...")
    
    test_event = {
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
    
    with open("test-event.json", "w") as f:
        json.dump(test_event, f, indent=2)
    
    print("   ✅ Test event created: test-event.json")
    return True

def test_function(function_id):
    """Test the deployed function"""
    print("🧪 Testing function...")
    
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
    """Main build and deploy process"""
    print("🚀 OCI Function Build and Deploy Script")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    if not config['compartment_id']:
        print("❌ OCI_COMPARTMENT_ID not found in environment")
        print("   Please configure your .env file")
        return
    
    print(f"📍 Using compartment: {config['compartment_id']}")
    print(f"📍 Application: {config['app_name']}")
    print(f"📍 Function: {config['function_name']}")
    print()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed")
        return
    
    # Step 2: Sync source code
    if not sync_source_code():
        print("\n❌ Failed to sync source code")
        return
    
    # Step 3: Check Fn Project CLI
    if not check_fn_cli():
        print("\n📦 Installing Fn Project CLI...")
        if not install_fn_cli():
            print("\n❌ Please install Fn Project CLI manually:")
            print("   curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh")
            return
    
    # Step 4: Set up context
    if not setup_fn_context():
        print("\n❌ Failed to set up Fn Project context")
        return
    
    # Step 5: Deploy function
    if not deploy_function():
        print("\n❌ Failed to deploy function")
        return
    
    # Step 6: Get function ID
    function_id = get_function_id()
    if not function_id:
        print("\n❌ Failed to get function ID")
        return
    
    # Step 7: Configure function
    if not configure_function(function_id):
        print("\n⚠️  Function deployed but configuration may need manual setup")
    
    # Step 8: Create test event
    create_test_event()
    
    # Step 9: Test function
    if test_function(function_id):
        print("\n🎉 Build and deployment successful!")
        print(f"   📍 Function ID: {function_id}")
        print(f"   📍 Application ID: ocid1.fnapp.oc1.iad.amaaaaaawe6j4fqacp4fg46c2xk4zyxv7nctku422mui3lg7yhhhonwscrlq")
        print("\n🚀 Your OCI Function is ready!")
        print("\n📋 Next steps:")
        print("   1. Set authentication variables in OCI Console")
        print("   2. Monitor function logs")
        print("   3. Test with real Object Storage events")
    else:
        print("\n⚠️  Deployment completed but function test failed")
        print("   Check function logs for details:")
        print(f"   oci fn function logs --function-id {function_id}")

if __name__ == "__main__":
    main()
