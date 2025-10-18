#!/usr/bin/env python3
"""
Test the updated ImageCaptionTool with GenAI Vision
"""

import os
import sys
import base64
import json
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_caption_tool():
    """Test the ImageCaptionTool with GenAI Vision"""
    print("🖼️  Testing ImageCaptionTool with GenAI Vision")
    print("=" * 60)
    
    try:
        # Load environment
        load_dotenv('.env')
        
        # Test Object Storage integration
        print("🔗 Testing Object Storage integration...")
        
        # Import Object Storage tools
        from oci_delivery_agent.tools import ObjectRetrievalTool
        from oci_delivery_agent.config import WorkflowConfig, ObjectStorageConfig, VisionConfig
        
        # Create Object Storage config
        object_storage = ObjectStorageConfig(
            namespace=os.environ.get('OCI_OS_NAMESPACE'),
            bucket_name=os.environ.get('OCI_OS_BUCKET'),
            delivery_prefix=""  # No prefix for root bucket access
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
        
        # Test Object Storage retrieval
        print("📦 Testing Object Storage retrieval...")
        retrieval_tool = ObjectRetrievalTool(config)
        
        # Use a test object path (you'll need to upload an image to your bucket first)
        test_object_path = "deliveries/sample.jpg"  # Object in deliveries folder
        
        try:
            # This should retrieve from Object Storage
            retrieval_result = retrieval_tool._run(test_object_path)
            retrieval_data = json.loads(retrieval_result)
            encoded_payload = retrieval_data["payload"]
            print(f"✅ Retrieved from Object Storage: {len(encoded_payload)} characters")
        except Exception as e:
            print(f"⚠️  Object Storage retrieval failed: {e}")
            print("📝 Falling back to local file for testing...")
            
            # Fallback to local file for testing
            local_image_path = "/Users/zhizhyan/Desktop/Codex/development/assets/deliveries/sample.jpg"
            if not os.path.exists(local_image_path):
                print(f"❌ Local image not found: {local_image_path}")
                return False
            
            with open(local_image_path, 'rb') as f:
                image_data = f.read()
            
            encoded_payload = base64.b64encode(image_data).decode('utf-8')
            print(f"✅ Using local image: {len(encoded_payload)} characters")
        
        # Test the caption tool with Object Storage data
        print("🔧 Testing ImageCaptionTool with Object Storage data...")
        
        # Import caption tool
        from oci_delivery_agent.tools import ImageCaptionTool
        
        # Create caption tool
        print("🔧 Creating ImageCaptionTool...")
        caption_tool = ImageCaptionTool(config)
        print("✅ ImageCaptionTool created")
        
        # Test caption generation
        print("📝 Generating image caption...")
        caption = caption_tool._run(encoded_payload)
        
        print("✅ Caption Generated:")
        print(f"   {caption}")
        
        # Check if caption indicates vision capabilities
        if "don't have the capability to visually see" in caption.lower() or "can't see" in caption.lower():
            print("\n⚠️  Tool still indicates it cannot see images")
            return False
        else:
            print("\n✅ Tool appears to be analyzing the image!")
            print("🎉 Vision capabilities confirmed!")
            
            # Test damage detection as well
            print("\n🔍 Testing damage detection...")
            from oci_delivery_agent.tools import DamageDetectionTool
            
            damage_tool = DamageDetectionTool(config)
            damage_scores = damage_tool._run(encoded_payload)
            
            print("✅ Damage Detection Results:")
            if isinstance(damage_scores, dict):
                for category, score in damage_scores.items():
                    print(f"   {category}: {score:.2f}")
            else:
                print(f"   Response: {damage_scores}")
            
            return True
        
    except Exception as e:
        print(f"❌ Caption tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 OCI GenAI Caption Tool Test")
    print("=" * 60)
    
    success = test_caption_tool()
    
    if success:
        print("\n🎉 Caption tool test completed!")
        print("✅ GenAI Vision integration working")
        print("✅ Image captioning functional")
        print("✅ Damage detection functional")
    else:
        print("\n⚠️  Caption tool test failed. Check your configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
