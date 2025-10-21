import fdk
import json
import sys
import os

# Ensure src/ modules are importable when running in OCI Functions
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(CURRENT_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

def handler(ctx, data=None):
    """
    OCI Function handler for delivery quality assessment.
    Processes delivery images and returns quality analysis using GenAI.
    """
    import json  # Ensure json is available in function scope
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
        
        # Handle empty data
        if len(data_bytes) == 0:
            return json.dumps({"error": "Empty data received", "status": "error"})
        
        try:
            request = json.loads(data_bytes.decode("utf-8"))
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"JSON decode error: {e}", "status": "error", "data_preview": data_bytes[:100].decode('utf-8', errors='ignore')})
        
        test_type = request.get("test_type", "basic")
        
        if test_type == "basic":
            # Basic connectivity test
            return json.dumps({
                "message": "Function is working!",
                "status": "success",
                "version": "0.0.20",
                "test_type": "basic",
                "langchain_available": True
            })
        
        elif test_type == "imports":
            # Test individual imports
            try:
                import oci
                from oci.generative_ai_inference import GenerativeAiInferenceClient
                from oci.object_storage import ObjectStorageClient
                from langchain.chains import LLMChain
                from langchain_core.language_models import BaseLLM
                
                return json.dumps({
                    "message": "All imports successful!",
                    "status": "success",
                    "test_type": "imports",
                    "imports": {
                        "oci": "✅",
                        "generative_ai": "✅", 
                        "object_storage": "✅",
                        "langchain": "✅",
                        "langchain_core": "✅"
                    }
                })
            except Exception as e:
                return json.dumps({
                    "error": str(e),
                    "status": "error",
                    "test_type": "imports"
                })
        
        elif test_type == "auth":
            # Test Resource Principal authentication with timeout
            try:
                import signal
                from oci.auth.signers import get_resource_principals_signer
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Resource Principal authentication timed out")
                
                # Set a 10-second timeout
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                print("Testing Resource Principal authentication...")
                signer = get_resource_principals_signer()
                print("✅ Resource Principal signer created successfully!")
                _ = signer.region  # Access attribute to ensure signer is fully initialized
                
                # Cancel the alarm
                signal.alarm(0)
                
                return json.dumps({
                    "message": "Resource Principal authentication successful!",
                    "status": "success", 
                    "test_type": "auth",
                    "auth_method": "resource_principal"
                })
            except TimeoutError:
                print("❌ Resource Principal authentication timed out")
                return json.dumps({
                    "error": "Resource Principal authentication timed out after 10 seconds",
                    "status": "error",
                    "test_type": "auth"
                })
            except Exception as e:
                print(f"❌ Resource Principal failed: {e}")
                return json.dumps({
                    "error": f"Resource Principal authentication failed: {e}",
                    "status": "error",
                    "test_type": "auth"
                })
        
        elif test_type == "extract":
            from oci_delivery_agent.handlers import load_config
            from oci_delivery_agent.tools import ObjectRetrievalTool, ExifExtractionTool

            object_name = (
                request.get("object_name")
                or request.get("data", {}).get("resourceName")
            )
            if not object_name:
                return json.dumps({
                    "error": "object_name missing from request",
                    "status": "error",
                    "test_type": "extract",
                })

            config = load_config()
            retrieval_tool = ObjectRetrievalTool(config)
            retrieval_result = json.loads(retrieval_tool._run(object_name))

            exif_tool = ExifExtractionTool()
            exif_data = json.loads(exif_tool._run(retrieval_result["payload"]))

            gps_info = exif_data.get("GPSInfo", {})

            return json.dumps({
                "status": "success",
                "test_type": "extract",
                "object_name": object_name,
                "metadata": retrieval_result["metadata"],
                "gps": gps_info,
                "exif": exif_data,
            })

        else:
            # Full delivery agent test
            from oci_delivery_agent.handlers import handler as delivery_handler
            
            # Create a proper Object Storage event structure for testing
            test_event = {
                "eventTime": "2024-01-15T10:30:00Z",
                "data": {
                    "resourceName": request.get("data", {}).get("resourceName", "sample.jpg")
                },
                "additionalDetails": {
                    "expectedLatitude": 40.7128,
                    "expectedLongitude": -74.0060,
                    "promisedTime": "2024-01-15T10:00:00Z"
                }
            }
            
            # Convert to bytes for the handler
            event_bytes = json.dumps(test_event).encode('utf-8')
            
            result = delivery_handler(ctx, event_bytes)
            # Ensure the result is JSON formatted
            if isinstance(result, dict):
                return json.dumps(result)
            return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return json.dumps({
            "error": str(e),
            "status": "error",
            "message": "Function processing failed",
            "traceback": error_details
        })

if __name__ == "__main__":
    fdk.handle(handler)
