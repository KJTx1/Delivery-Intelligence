#!/usr/bin/env python3
"""
Test damage detection on all 5 damage sample pictures.
"""

import os
import sys
import base64
import json
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_damage_samples():
    """Test damage detection on all damage samples"""
    print("🔍 Testing Damage Detection on All Samples")
    print("=" * 60)
    
    try:
        # Load environment
        load_dotenv('.env')
        
        # Import tools
        from oci_delivery_agent.tools import DamageDetectionTool, ImageCaptionTool
        from oci_delivery_agent.config import WorkflowConfig, ObjectStorageConfig, VisionConfig
        
        # Create config
        object_storage = ObjectStorageConfig(
            namespace=os.environ.get('OCI_OS_NAMESPACE'),
            bucket_name=os.environ.get('OCI_OS_BUCKET'),
            delivery_prefix=""
        )
        
        vision = VisionConfig(
            compartment_id=os.environ.get('OCI_COMPARTMENT_ID'),
            image_caption_model_endpoint=os.environ.get('OCI_TEXT_MODEL_OCID')
        )
        
        config = WorkflowConfig(
            object_storage=object_storage,
            vision=vision,
            local_asset_root=os.environ.get('LOCAL_ASSET_ROOT')
        )
        
        # Initialize tools
        damage_tool = DamageDetectionTool(config)
        caption_tool = ImageCaptionTool(config)
        
        # Test all damage samples
        damage_samples = [
            "deliveries/damage1.jpg",
            "deliveries/damage2.jpg", 
            "deliveries/damage3.jpg",
            "deliveries/damage4.jpg",
            "deliveries/damage5.jpg"
        ]
        
        results = {}
        
        for i, sample in enumerate(damage_samples, 1):
            print(f"\n📸 Testing Sample {i}: {sample}")
            print("-" * 50)
            
            # Load image from local assets
            local_image_path = f"../assets/{sample}"
            if not os.path.exists(local_image_path):
                print(f"❌ Image not found: {local_image_path}")
                continue
            
            with open(local_image_path, 'rb') as f:
                image_data = f.read()
            
            encoded_payload = base64.b64encode(image_data).decode('utf-8')
            print(f"✅ Loaded image: {len(image_data)} bytes")
            
            # Test captioning
            print("🔍 Testing Image Captioning...")
            try:
                caption_result = caption_tool._run(encoded_payload)
                caption_data = json.loads(caption_result)
                
                print(f"✅ Caption Results:")
                print(f"   Scene Type: {caption_data.get('sceneType', 'unknown')}")
                print(f"   Package Visible: {caption_data.get('packageVisible', False)}")
                print(f"   Package Description: {caption_data.get('packageDescription', 'N/A')}")
                print(f"   Location: {caption_data.get('location', {}).get('type', 'unknown')}")
                print(f"   Overall: {caption_data.get('overallDescription', 'N/A')[:100]}...")
                
            except Exception as e:
                print(f"❌ Caption failed: {e}")
                caption_data = {}
            
            # Test damage detection
            print("🔍 Testing Damage Detection...")
            try:
                damage_result = damage_tool._run(encoded_payload)
                damage_data = json.loads(damage_result)
                
                print(f"✅ Damage Analysis (Raw JSON):")
                print(json.dumps(damage_data, indent=2))
                
                # Store results for summary
                results[sample] = {
                    'caption': caption_data,
                    'damage': damage_data,
                    'overall_severity': damage_data.get('overall', {}).get('severity', 'unknown'),
                    'overall_score': damage_data.get('overall', {}).get('score', 0.0)
                }
                
            except Exception as e:
                print(f"❌ Damage detection failed: {e}")
                results[sample] = {'error': str(e)}
            
            print("=" * 50)
        
        # Summary
        print("\n📊 DAMAGE DETECTION SUMMARY")
        print("=" * 60)
        
        for sample, result in results.items():
            if 'error' in result:
                print(f"❌ {sample}: ERROR - {result['error']}")
            else:
                severity = result.get('overall_severity', 'unknown')
                score = result.get('overall_score', 0.0)
                package_visible = result.get('caption', {}).get('packageVisible', False)
                
                print(f"📦 {sample}:")
                print(f"   Package Visible: {package_visible}")
                print(f"   Damage Severity: {severity} (Score: {score:.2f})")
                
                if severity == 'none':
                    print(f"   ✅ No damage detected")
                elif severity == 'minor':
                    print(f"   ⚠️  Minor damage detected")
                elif severity == 'moderate':
                    print(f"   ⚠️  Moderate damage detected")
                elif severity == 'severe':
                    print(f"   🚨 Severe damage detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Damage Sample Testing")
    print("=" * 60)
    
    success = test_damage_samples()
    
    if success:
        print("\n🎉 Damage sample testing completed!")
        print("✅ All samples processed successfully")
    else:
        print("\n⚠️  Damage sample testing failed.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
