import fdk
import json
import sys
import os
import base64
from typing import Dict, Any

def handler(ctx, data=None):
    """
    Test individual components of the delivery agent.
    """
    try:
        # Parse the test request
        if hasattr(data, 'read'):
            data_bytes = data.read()
        elif isinstance(data, bytes):
            data_bytes = data
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = str(data).encode('utf-8')
        
        request = json.loads(data_bytes.decode("utf-8"))
        test_type = request.get("test_type", "all")
        
        # Import the delivery agent components
        from oci_delivery_agent.tools import ObjectRetrievalTool, ExifExtractionTool, ImageCaptionTool, DamageDetectionTool
        from oci_delivery_agent.config import WorkflowConfig, ObjectStorageConfig, VisionConfig
        
        # Initialize configuration
        config = WorkflowConfig(
            object_storage=ObjectStorageConfig(
                namespace=os.getenv('OCI_OS_NAMESPACE', 'test'),
                bucket_name=os.getenv('OCI_OS_BUCKET', 'test'),
                delivery_prefix=""
            ),
            vision=VisionConfig(
                caption_endpoint=os.getenv('OCI_TEXT_MODEL_OCID', ''),
                damage_endpoint=os.getenv('OCI_TEXT_MODEL_OCID', '')
            )
        )
        
        # Initialize tools
        object_tool = ObjectRetrievalTool(config=config)
        exif_tool = ExifExtractionTool()
        caption_tool = ImageCaptionTool(config=config)
        damage_tool = DamageDetectionTool(config=config)
        
        results = {}
        
        # Test Object Storage retrieval
        if test_type in ["all", "object_storage"]:
            try:
                print("Testing Object Storage retrieval...")
                object_name = request.get("object_name", "sample.jpg")
                retrieval_result = object_tool.run(object_name)
                results["object_storage"] = {
                    "status": "success",
                    "object_name": object_name,
                    "data_size": len(retrieval_result.get("payload", "")) if isinstance(retrieval_result, dict) else len(str(retrieval_result))
                }
            except Exception as e:
                results["object_storage"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test EXIF extraction
        if test_type in ["all", "exif"]:
            try:
                print("Testing EXIF extraction...")
                # Use a sample image for testing
                sample_image_path = "/function/sample.jpg"  # We'll need to add a sample image
                if os.path.exists(sample_image_path):
                    with open(sample_image_path, "rb") as f:
                        image_data = f.read()
                    exif_result = exif_tool.run(image_data)
                    results["exif"] = {
                        "status": "success",
                        "exif_data": exif_result
                    }
                else:
                    results["exif"] = {
                        "status": "skipped",
                        "reason": "No sample image available"
                    }
            except Exception as e:
                results["exif"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test Image Captioning
        if test_type in ["all", "caption"]:
            try:
                print("Testing Image Captioning...")
                # Use a sample image for testing
                sample_image_path = "/function/sample.jpg"
                if os.path.exists(sample_image_path):
                    with open(sample_image_path, "rb") as f:
                        image_data = f.read()
                    caption_result = caption_tool.run(image_data)
                    results["caption"] = {
                        "status": "success",
                        "caption": caption_result
                    }
                else:
                    results["caption"] = {
                        "status": "skipped",
                        "reason": "No sample image available"
                    }
            except Exception as e:
                results["caption"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Test Damage Detection
        if test_type in ["all", "damage"]:
            try:
                print("Testing Damage Detection...")
                # Use a sample image for testing
                sample_image_path = "/function/sample.jpg"
                if os.path.exists(sample_image_path):
                    with open(sample_image_path, "rb") as f:
                        image_data = f.read()
                    damage_result = damage_tool.run(image_data)
                    results["damage"] = {
                        "status": "success",
                        "damage_analysis": damage_result
                    }
                else:
                    results["damage"] = {
                        "status": "skipped",
                        "reason": "No sample image available"
                    }
            except Exception as e:
                results["damage"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "message": "Individual component testing completed",
            "status": "success",
            "test_type": test_type,
            "results": results
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "error": str(e),
            "status": "error",
            "message": "Component testing failed",
            "traceback": error_details
        }

if __name__ == "__main__":
    fdk.handle(handler)
