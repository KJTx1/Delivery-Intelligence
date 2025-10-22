import json
import base64
import io
from fdk import response
from PIL import Image
import numpy as np
import oci
import os
from datetime import datetime
from typing import Dict, Any

# Check if OpenCV is available
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

def blur_faces_in_image(image_bytes, blur_intensity=51, scale_factor=1.05, min_neighbors=3, min_face_size=(20, 20)):
    """Simple face blurring function"""
    if not CV2_AVAILABLE:
        raise RuntimeError("OpenCV not available")
    
    # Convert bytes to PIL Image
    pil_image = Image.open(io.BytesIO(image_bytes))
    
    # Convert PIL Image to OpenCV format (BGR)
    image_rgb = np.array(pil_image.convert('RGB'))
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    # Load pre-trained Haar Cascade for face detection
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        raise ValueError("Failed to load Haar Cascade classifier")
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_face_size,
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Blur each detected face
    for (x, y, w, h) in faces:
        # Add padding around the face for better blurring
        padding = 10
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image_bgr.shape[1], x + w + padding)
        y2 = min(image_bgr.shape[0], y + h + padding)
        
        # Extract face region
        face_region = image_bgr[y1:y2, x1:x2]
        
        # ADAPTIVE BLUR: Scale blur intensity based on face size
        face_size = max(w, h)
        adaptive_blur = max(int(face_size * 0.4), blur_intensity)  # 40% coverage, min 51px
        if adaptive_blur % 2 == 0:
            adaptive_blur += 1  # Ensure odd number for Gaussian blur
        adaptive_blur = min(adaptive_blur, 299)  # Cap blur intensity
        
        # Apply Gaussian blur
        blurred_face = cv2.GaussianBlur(
            face_region,
            (adaptive_blur, adaptive_blur),
            0
        )
        
        # Replace the face region with blurred version
        image_bgr[y1:y2, x1:x2] = blurred_face
    
    # Convert back to bytes
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    # Save to bytes
    output_buffer = io.BytesIO()
    pil_image.save(output_buffer, format='JPEG', quality=95)
    output_buffer.seek(0)
    
    return output_buffer.getvalue(), len(faces)

def get_oci_client():
    """Get OCI Object Storage client using the exact same pattern as main function"""
    try:
        signer = None
        config: Dict[str, Any] = {}
        try:
            from oci.auth.signers import get_resource_principals_signer

            signer = get_resource_principals_signer()
            signer_region = getattr(signer, "region", None)
            resolved_region = os.environ.get("OCI_REGION") or signer_region or "us-ashburn-1"
            config = {"region": resolved_region}
            print(f"Using resource principal authentication for Object Storage client (region={resolved_region})")
        except Exception as rp_error:
            print(f"Resource principal signer unavailable for Object Storage: {rp_error}")
            try:
                config = oci.config.from_file()
                print("Falling back to local OCI configuration for Object Storage")
            except Exception as config_error:
                try:
                    config = oci.config.from_file("~/.oci/config")
                    print("Using ~/.oci/config for Object Storage client")
                except Exception:
                    return None

        if signer is not None:
            return oci.object_storage.ObjectStorageClient(config=config, signer=signer)
        return oci.object_storage.ObjectStorageClient(config)
    except Exception:
        return None

def handler(ctx, data=None):
    """
    Face blurring function with OCI Object Storage.
    
    Input: {"objectName": "image.jpg"}
    Output: {"blurred_image_path": "oci://...", "faces_detected": 2}
    """
    try:
        # Parse input
        if data is None:
            return response.Response(
                ctx, 
                response_data={"error": "No input data provided"},
                status_code=400
            )
        
        # Normalize payload to a dictionary
        if hasattr(data, 'read'):
            try:
                data = data.read()
            except Exception:
                pass

        if isinstance(data, (bytes, bytearray)):
            try:
                data = data.decode('utf-8').strip()
            except Exception:
                return response.Response(
                    ctx,
                    response_data={"error": "Payload decode error"},
                    status_code=400
                )

        if isinstance(data, str):
            try:
                input_data = json.loads(data)
            except json.JSONDecodeError:
                from urllib.parse import parse_qsl
                fallback_data = dict(parse_qsl(data))
                if fallback_data:
                    input_data = fallback_data
                else:
                    return response.Response(
                        ctx,
                        response_data={"error": "Invalid JSON input"},
                        status_code=400
                    )
        elif isinstance(data, dict):
            input_data = data
        else:
            return response.Response(
                ctx,
                response_data={"error": "Invalid payload type"},
                status_code=400
            )
        
        object_name = input_data.get("objectName")
        if not object_name:
            return response.Response(
                ctx,
                response_data={"error": "objectName is required"},
                status_code=400
            )
        
        # Get OCI client
        client = get_oci_client()
        if client is None:
            return response.Response(
                ctx,
                response_data={"error": "Failed to initialize OCI client"},
                status_code=500
            )
        
        # OCI Object Storage configuration - read from environment variables (same as main function)
        namespace = os.environ.get("OCI_OS_NAMESPACE", "")
        bucket_name = os.environ.get("OCI_OS_BUCKET", "")
        
        # Retrieve original image
        print(f"Retrieving image: {object_name}")
        try:
            response_obj = client.get_object(
                namespace_name=namespace,
                bucket_name=bucket_name,
                object_name=object_name
            )
            image_bytes = response_obj.data.content
            print(f"Retrieved image: {len(image_bytes)} bytes")
        except Exception as e:
            return response.Response(
                ctx,
                response_data={"error": f"Failed to retrieve object {object_name}: {e}"},
                status_code=500
            )
        
        # Blur faces
        print("Processing image for face blurring...")
        try:
            # Read face blurring parameters from environment variables
            blur_intensity = int(os.environ.get("BLUR_INTENSITY", "51"))
            scale_factor = float(os.environ.get("BLUR_SCALE_FACTOR", "1.05"))
            min_neighbors = int(os.environ.get("BLUR_MIN_NEIGHBORS", "3"))
            min_face_size_str = os.environ.get("BLUR_MIN_FACE_SIZE", "20,20")
            min_face_size = tuple(map(int, min_face_size_str.split(',')))
            
            blurred_bytes, num_faces = blur_faces_in_image(
                image_bytes,
                blur_intensity=blur_intensity,
                scale_factor=scale_factor,
                min_neighbors=min_neighbors,
                min_face_size=min_face_size
            )
            print(f"Face blurring completed: {num_faces} faces detected")
        except Exception as e:
            return response.Response(
                ctx,
                response_data={"error": f"Face blurring failed: {e}"},
                status_code=500
            )
        
        # Store blurred image
        blur_prefix = os.environ.get("BLUR_PREFIX", "blurred/")
        blurred_object_name = f"{blur_prefix}{object_name}"
        print(f"Storing blurred image: {blurred_object_name}")
        try:
            put_response = client.put_object(
                namespace_name=namespace,
                bucket_name=bucket_name,
                object_name=blurred_object_name,
                put_object_body=blurred_bytes,
                content_type="image/jpeg"
            )
            blurred_image_path = f"oci://{namespace}/{bucket_name}/{blurred_object_name}"
            print(f"Blurred image stored: {blurred_image_path}")
        except Exception as e:
            return response.Response(
                ctx,
                response_data={"error": f"Failed to store blurred image: {e}"},
                status_code=500
            )
        
        # Return success response
        return response.Response(
            ctx,
            response_data={
                "status": "success",
                "blurred_image_path": blurred_image_path,
                "faces_detected": num_faces,
                "original_object": object_name,
                "blurred_object": blurred_object_name,
                "namespace": namespace,
                "bucket": bucket_name
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return response.Response(
            ctx,
            response_data={"error": f"Unexpected error: {e}"},
            status_code=500
        )