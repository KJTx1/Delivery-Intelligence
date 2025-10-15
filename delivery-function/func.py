import fdk
import json
import sys
import os

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
            return {"error": "Empty data received", "status": "error"}
        
        try:
            request = json.loads(data_bytes.decode("utf-8"))
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {e}", "status": "error", "data_preview": data_bytes[:100]}
        
        test_type = request.get("test_type", "basic")
        
        if test_type == "basic":
            # Basic connectivity test
            return {
                "message": "Function is working!",
                "status": "success",
                "version": "0.0.20",
                "test_type": "basic",
                "langchain_available": True
            }
        
        elif test_type == "imports":
            # Test individual imports
            try:
                import oci
                from oci.generative_ai_inference import GenerativeAiInferenceClient
                from oci.object_storage import ObjectStorageClient
                from langchain.chains import LLMChain
                from langchain_core.language_models import BaseLLM
                
                return {
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
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "status": "error",
                    "test_type": "imports"
                }
        
        elif test_type == "auth":
            # Test Instance Principal authentication with timeout
            try:
                import signal
                from oci.auth.signers import InstancePrincipalsSecurityTokenSigner
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Instance Principal authentication timed out")
                
                # Set a 10-second timeout
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                print("Testing Instance Principal authentication...")
                signer = InstancePrincipalsSecurityTokenSigner()
                print("✅ Instance Principal signer created successfully!")
                
                # Cancel the alarm
                signal.alarm(0)
                
                return {
                    "message": "Instance Principal authentication successful!",
                    "status": "success", 
                    "test_type": "auth",
                    "auth_method": "instance_principal"
                }
            except TimeoutError:
                print("❌ Instance Principal authentication timed out")
                return {
                    "error": "Instance Principal authentication timed out after 10 seconds",
                    "status": "error",
                    "test_type": "auth"
                }
            except Exception as e:
                print(f"❌ Instance Principal failed: {e}")
                return {
                    "error": f"Instance Principal authentication failed: {e}",
                    "status": "error",
                    "test_type": "auth"
                }
        
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
            return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "error": str(e),
            "status": "error",
            "message": "Function processing failed",
            "traceback": error_details
        }

if __name__ == "__main__":
    fdk.handle(handler)
