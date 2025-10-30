import json
import base64
import io
from fdk import response
from PIL import Image
import numpy as np
import oci
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Check if OpenCV is available
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None


def get_oci_vision_client():
    """Get OCI Vision AI client with resource principal or config file authentication."""
    try:
        signer = None
        config: Dict[str, Any] = {}
        service_endpoint = "https://vision.aiservice.us-chicago-1.oci.oraclecloud.com"
        
        try:
            from oci.auth.signers import get_resource_principals_signer

            signer = get_resource_principals_signer()
            signer_region = getattr(signer, "region", None)
            resolved_region = os.environ.get("OCI_REGION") or signer_region or "us-chicago-1"
            config = {"region": resolved_region}
            if os.environ.get("DEBUG_VISION"):
                print(f"Using resource principal authentication for Vision client (region={resolved_region})")
                print(f"Vision API endpoint: {service_endpoint}")
        except Exception as rp_error:
            if os.environ.get("DEBUG_VISION"):
                print(f"Resource principal signer unavailable for Vision: {rp_error}")
            try:
                config = oci.config.from_file()
                if os.environ.get("DEBUG_VISION"):
                    print("Falling back to local OCI configuration for Vision")
                    print(f"Vision API endpoint: {service_endpoint}")
            except Exception as config_error:
                try:
                    config = oci.config.from_file("~/.oci/config")
                    if os.environ.get("DEBUG_VISION"):
                        print("Using ~/.oci/config for Vision client")
                        print(f"Vision API endpoint: {service_endpoint}")
                except Exception:
                    return None

        if signer is not None:
            return oci.ai_vision.AIServiceVisionClient(
                config=config, 
                signer=signer,
                service_endpoint=service_endpoint
            )
        return oci.ai_vision.AIServiceVisionClient(
            config=config,
            service_endpoint=service_endpoint
        )
    except Exception as e:
        print(f"Failed to initialize Vision client: {e}")
        return None


def detect_faces_with_oci_vision(image_bytes: bytes, compartment_id: str, vision_client) -> List[Dict[str, Any]]:
    """
    Detect faces using OCI Vision Face Detection API.
    
    Returns list of face bounding boxes with format:
    [{"x": x1, "y": y1, "width": w, "height": h, "confidence": conf}, ...]
    """
    try:
        # Load original image and optionally upscale small images to aid detection
        original_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        orig_width, orig_height = original_image.size
        min_dim_target = int(os.environ.get("VISION_MIN_DIMENSION", "600"))
        detection_image = original_image
        if min(orig_width, orig_height) < min_dim_target:
            scale = float(min_dim_target) / float(min(orig_width, orig_height))
            new_w = int(orig_width * scale)
            new_h = int(orig_height * scale)
            detection_image = original_image.resize((new_w, new_h), Image.BICUBIC)
            if os.environ.get("DEBUG_VISION"):
                print(f"Upscaled image for detection: {orig_width}x{orig_height} -> {new_w}x{new_h}")

        # Encode detection image to base64 (Vision returns normalized vertices, so coordinates remain valid)
        buf = io.BytesIO()
        detection_image.save(buf, format='JPEG', quality=95)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        # Create inline image details
        inline_image_details = oci.ai_vision.models.InlineImageDetails(
            source="INLINE",
            data=image_base64
        )
        
        # Create face detection feature (per docs)
        max_results_cfg = int(os.environ.get("VISION_MAX_RESULTS", "100"))
        return_landmarks_cfg = os.environ.get("VISION_RETURN_LANDMARKS", "true").lower() == "true"
        face_detection_feature = oci.ai_vision.models.FaceDetectionFeature(
            feature_type="FACE_DETECTION",
            max_results=max_results_cfg,
            should_return_landmarks=return_landmarks_cfg
        )

        # Create analyze image details
        analyze_image_details = oci.ai_vision.models.AnalyzeImageDetails(
            features=[face_detection_feature],
            image=inline_image_details,
            compartment_id=compartment_id
        )
        
        # Call the Vision API
        if os.environ.get("DEBUG_VISION"):
            print("Calling OCI Vision Face Detection API...")
        analyze_response = vision_client.analyze_image(analyze_image_details)
        
        # DEBUG: Inspect Vision response structure
        try:
            resp_dict = oci.util.to_dict(analyze_response.data) if hasattr(oci, 'util') else None
            if isinstance(resp_dict, dict):
                top_keys = list(resp_dict.keys())
                if os.environ.get("DEBUG_VISION"):
                    print(f"Vision AnalyzeImageResult keys: {top_keys}")
                if 'faces' in resp_dict and isinstance(resp_dict['faces'], list) and resp_dict['faces']:
                    sample_face = resp_dict['faces'][0]
                    if os.environ.get("DEBUG_VISION"):
                        print(f"Sample face keys: {list(sample_face.keys())}")
                    if 'bounding_polygon' in sample_face and sample_face['bounding_polygon']:
                        bp = sample_face['bounding_polygon']
                        if os.environ.get("DEBUG_VISION"):
                            print(f"Bounding polygon keys: {list(bp.keys())}; normalized_vertices count: {len(bp.get('normalized_vertices', []) )}")
                else:
                    if os.environ.get("DEBUG_VISION"):
                        print("Vision response has no 'faces' or it's empty.")
            else:
                if os.environ.get("DEBUG_VISION"):
                    print("Vision response could not be converted to dict for logging.")
        except Exception as _:
            if os.environ.get("DEBUG_VISION"):
                print("Failed to serialize Vision response for debug logging")
        
        # Parse face detection results (FaceDetectionFeature returns `faces`)
        faces = []
        img_width = orig_width
        img_height = orig_height
        
        confidence_threshold = float(os.environ.get("VISION_CONFIDENCE_THRESHOLD", "0.0"))
        
        if analyze_response.data:
            # Basic introspection for troubleshooting
            has_faces = hasattr(analyze_response.data, 'faces') and bool(getattr(analyze_response.data, 'faces'))
            has_detected_faces = hasattr(analyze_response.data, 'detected_faces') and bool(getattr(analyze_response.data, 'detected_faces'))
            has_objects = hasattr(analyze_response.data, 'image_objects') and bool(getattr(analyze_response.data, 'image_objects'))
            if os.environ.get("DEBUG_VISION"):
                print(f"Vision response fields -> faces: {has_faces}, detected_faces: {has_detected_faces}, image_objects: {has_objects}")
            # Primary per docs
            vision_faces = getattr(analyze_response.data, 'faces', None)
            # Some examples/blogs use `detected_faces`
            if not vision_faces:
                detected_faces = getattr(analyze_response.data, 'detected_faces', None)
                if detected_faces:
                    if os.environ.get("DEBUG_VISION"):
                        print(f"Vision returned {len(detected_faces)} detected_faces entries")
                    vision_faces = detected_faces
            # No embeddings in analyze_image for FACE_DETECTION
            if vision_faces:
                if os.environ.get("DEBUG_VISION"):
                    print(f"Vision returned {len(vision_faces)} face entries")
                for face_obj in vision_faces:
                    conf = getattr(face_obj, 'confidence', 1.0) or 1.0
                    if conf < confidence_threshold:
                        continue
                    # Try normalized polygon first
                    bounding_polygon = getattr(face_obj, 'bounding_polygon', None)
                    x1 = y1 = x2 = y2 = None
                    if bounding_polygon and getattr(bounding_polygon, 'normalized_vertices', None) and img_width and img_height:
                        normalized_vertices = bounding_polygon.normalized_vertices
                        x_coords = [v.x * img_width for v in normalized_vertices]
                        y_coords = [v.y * img_height for v in normalized_vertices]
                        x1 = max(0, int(min(x_coords)))
                        y1 = max(0, int(min(y_coords)))
                        x2 = min(img_width, int(max(x_coords)))
                        y2 = min(img_height, int(max(y_coords)))
                    # Fallback: absolute vertices
                    elif bounding_polygon and getattr(bounding_polygon, 'vertices', None):
                        vertices = bounding_polygon.vertices
                        x_coords = [int(v.x) for v in vertices]
                        y_coords = [int(v.y) for v in vertices]
                        x1 = max(0, min(x_coords))
                        y1 = max(0, min(y_coords))
                        x2 = min(img_width or max(x_coords), max(x_coords))
                        y2 = min(img_height or max(y_coords), max(y_coords))
                    # Fallback: bounding box structure (x,y,width,height)
                    elif hasattr(face_obj, 'bounding_box') and face_obj.bounding_box:
                        bb = face_obj.bounding_box
                        try:
                            x1 = max(0, int(bb.x))
                            y1 = max(0, int(bb.y))
                            x2 = x1 + max(0, int(bb.width))
                            y2 = y1 + max(0, int(bb.height))
                        except Exception:
                            pass
                    if x1 is None or y1 is None or x2 is None or y2 is None:
                        continue
                    width = max(0, x2 - x1)
                    height = max(0, y2 - y1)
                    if width == 0 or height == 0:
                        continue
                    face_info = {"x": x1, "y": y1, "width": width, "height": height, "confidence": conf}
                    faces.append(face_info)
                    if os.environ.get("DEBUG_VISION"):
                        print(f"Face detected at ({x1}, {y1}) size {width}x{height}, conf={conf:.2f}")
            else:
                # Fallback: some SDKs place results under image_objects with name 'face'
                image_objects = getattr(analyze_response.data, 'image_objects', None)
                if image_objects:
                    if os.environ.get("DEBUG_VISION"):
                        print(f"Vision returned {len(image_objects)} image_objects; scanning for 'face'")
                    for obj in image_objects:
                        name = (getattr(obj, 'name', '') or '').lower()
                        if name != 'face':
                            continue
                        conf = getattr(obj, 'confidence', 1.0) or 1.0
                        if conf < confidence_threshold:
                            continue
                        bounding_polygon = getattr(obj, 'bounding_polygon', None)
                        if not bounding_polygon or not getattr(bounding_polygon, 'normalized_vertices', None):
                            continue
                        if img_width is None or img_height is None:
                            continue
                        normalized_vertices = bounding_polygon.normalized_vertices
                        x_coords = [v.x * img_width for v in normalized_vertices]
                        y_coords = [v.y * img_height for v in normalized_vertices]
                        x1 = max(0, int(min(x_coords)))
                        y1 = max(0, int(min(y_coords)))
                        x2 = min(img_width, int(max(x_coords)))
                        y2 = min(img_height, int(max(y_coords)))
                        width = max(0, x2 - x1)
                        height = max(0, y2 - y1)
                        if width == 0 or height == 0:
                            continue
                        face_info = {"x": x1, "y": y1, "width": width, "height": height, "confidence": conf}
                        faces.append(face_info)
                        if os.environ.get("DEBUG_VISION"):
                            print(f"Face (fallback) at ({x1}, {y1}) size {width}x{height}, conf={conf:.2f}")
        
        if not faces and os.environ.get("DEBUG_VISION"):
            print("No faces detected by OCI Vision")
        
        return faces
        
    except Exception as e:
        print(f"Error during OCI Vision face detection: {e}")
        raise


def blur_faces_in_image(image_bytes: bytes, faces: List[Dict[str, Any]], blur_intensity: int = 51, 
                       padding: int = 10, adaptive_blur_factor: float = 0.4, 
                       max_blur_intensity: int = 299) -> bytes:
    """
    Blur detected faces in the image.
    
    Args:
        image_bytes: Original image bytes
        faces: List of face bounding boxes from OCI Vision
        blur_intensity: Base blur intensity
        padding: Padding around face region
        adaptive_blur_factor: Factor for adaptive blur based on face size
        max_blur_intensity: Maximum blur intensity
        
    Returns:
        Blurred image bytes
    """
    if not CV2_AVAILABLE:
        raise RuntimeError("OpenCV not available")
    
    # Convert bytes to PIL Image
    pil_image = Image.open(io.BytesIO(image_bytes))
    
    # Convert PIL Image to OpenCV format (BGR)
    image_rgb = np.array(pil_image.convert('RGB'))
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    # Blur each detected face
    for face in faces:
        x = face["x"]
        y = face["y"]
        w = face["width"]
        h = face["height"]
        
        # Add padding around the face for better blurring
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image_bgr.shape[1], x + w + padding)
        y2 = min(image_bgr.shape[0], y + h + padding)
        
        # Extract face region
        face_region = image_bgr[y1:y2, x1:x2]
        
        # Skip if face region is invalid
        if face_region.size == 0:
            continue
        
        # ADAPTIVE BLUR: Scale blur intensity based on face size
        face_size = max(w, h)
        adaptive_blur = max(int(face_size * adaptive_blur_factor), blur_intensity)
        if adaptive_blur % 2 == 0:
            adaptive_blur += 1  # Ensure odd number for Gaussian blur
        adaptive_blur = min(adaptive_blur, max_blur_intensity)
        
        print(f"Blurring face at ({x}, {y}) with blur intensity: {adaptive_blur}")
        
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
    
    return output_buffer.getvalue()


def get_oci_storage_client():
    """Get OCI Object Storage client using resource principal or config file."""
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
    Face blurring function with OCI Vision Face Detection and Object Storage.
    
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
        
        # Get OCI clients
        storage_client = get_oci_storage_client()
        if storage_client is None:
            return response.Response(
                ctx,
                response_data={"error": "Failed to initialize OCI Object Storage client"},
                status_code=500
            )
        
        vision_client = get_oci_vision_client()
        if vision_client is None:
            return response.Response(
                ctx,
                response_data={"error": "Failed to initialize OCI Vision client"},
                status_code=500
            )
        
        # OCI configuration from environment variables
        namespace = os.environ.get("OCI_OS_NAMESPACE", "")
        bucket_name = os.environ.get("OCI_OS_BUCKET", "")
        compartment_id = os.environ.get("OCI_COMPARTMENT_ID", "")
        
        if not compartment_id:
            return response.Response(
                ctx,
                response_data={"error": "OCI_COMPARTMENT_ID environment variable is required"},
                status_code=500
            )
        
        # Retrieve original image
        if os.environ.get("DEBUG_VISION"):
            print(f"Retrieving image: {object_name}")
        try:
            response_obj = storage_client.get_object(
                namespace_name=namespace,
                bucket_name=bucket_name,
                object_name=object_name
            )
            image_bytes = response_obj.data.content
            if os.environ.get("DEBUG_VISION"):
                print(f"Retrieved image: {len(image_bytes)} bytes")
        except Exception as e:
            return response.Response(
                ctx,
                response_data={"error": f"Failed to retrieve object {object_name}: {e}"},
                status_code=500
            )
        
        # Detect faces using OCI Vision
        if os.environ.get("DEBUG_VISION"):
            print("Detecting faces with OCI Vision...")
        try:
            faces = detect_faces_with_oci_vision(image_bytes, compartment_id, vision_client)
            num_faces = len(faces)
            if os.environ.get("DEBUG_VISION"):
                print(f"Face detection completed: {num_faces} faces detected")
        except Exception as e:
            return response.Response(
                ctx,
                response_data={"error": f"Face detection failed: {e}"},
                status_code=500
            )
        
        # Blur faces if any were detected
        if num_faces > 0:
            print("Blurring detected faces...")
            try:
                # Read blur parameters from environment variables
                blur_intensity = int(os.environ.get("BLUR_INTENSITY", "51"))
                padding = int(os.environ.get("BLUR_PADDING", "10"))
                adaptive_blur_factor = float(os.environ.get("BLUR_ADAPTIVE_FACTOR", "0.4"))
                max_blur_intensity = int(os.environ.get("BLUR_MAX_INTENSITY", "299"))
                
                blurred_bytes = blur_faces_in_image(
                    image_bytes,
                    faces,
                    blur_intensity=blur_intensity,
                    padding=padding,
                    adaptive_blur_factor=adaptive_blur_factor,
                    max_blur_intensity=max_blur_intensity
                )
                print(f"Face blurring completed")
            except Exception as e:
                return response.Response(
                    ctx,
                    response_data={"error": f"Face blurring failed: {e}"},
                    status_code=500
                )
        else:
            print("No faces detected, returning original image")
            blurred_bytes = image_bytes
        
        # Store blurred image
        blur_prefix = os.environ.get("BLUR_PREFIX", "blurred/")
        blurred_object_name = f"{blur_prefix}{object_name}"
        print(f"Storing blurred image: {blurred_object_name}")
        try:
            put_response = storage_client.put_object(
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
                "bucket": bucket_name,
                "detection_method": "oci_vision"
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return response.Response(
            ctx,
            response_data={"error": f"Unexpected error: {e}"},
            status_code=500
        )
