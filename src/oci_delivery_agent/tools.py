"""LangChain tools wrapping OCI services for the delivery workflow."""
from __future__ import annotations

import base64
import io
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from langchain.tools import BaseTool
from PIL import Image, ExifTags

from .config import WorkflowConfig

try:  # pragma: no cover - optional dependency for real OCI calls
    import oci
except Exception:  # pragma: no cover - fall back to local mode when OCI SDK missing
    oci = None


class ObjectStorageClient:
    """Wrapper that prefers live OCI access but supports local testing."""

    def __init__(self, config: WorkflowConfig):
        self._config = config
        self._client = self._build_oci_client()

    def _build_oci_client(self):  # pragma: no cover - requires OCI SDK & credentials
        if oci is None:
            return None
        try:
            oci_config = oci.config.from_file()
            return oci.object_storage.ObjectStorageClient(oci_config)
        except Exception:
            return None

    def _resolve_object_name(self, object_name: str) -> str:
        prefix = self._config.object_storage.delivery_prefix or ""
        if object_name.startswith(prefix):
            return object_name
        return f"{prefix}{object_name}" if prefix else object_name

    def _load_local_file(self, object_name: str) -> Optional[Dict[str, Any]]:
        root = Path(self._config.local_asset_root or ".")
        candidate = root / object_name
        if not candidate.exists():
            candidate = root / self._resolve_object_name(object_name)
        if not candidate.exists():
            return None
        payload = candidate.read_bytes()
        return {
            "data": payload,
            "metadata": {
                "content_type": "image/jpeg",
                "size": len(payload),
                "object_name": str(candidate),
                "retrieved_at": datetime.utcnow().isoformat(),
                "source": "local",
            },
        }

    def get_object(self, object_name: str) -> Dict[str, Any]:
        resolved_name = self._resolve_object_name(object_name)
        if self._client is not None:  # pragma: no cover - network interaction
            response = self._client.get_object(
                namespace_name=self._config.object_storage.namespace,
                bucket_name=self._config.object_storage.bucket_name,
                object_name=resolved_name,
            )
            payload = response.data.content
            metadata = {
                "content_type": response.headers.get("Content-Type", "application/octet-stream"),
                "size": len(payload),
                "object_name": resolved_name,
                "retrieved_at": datetime.utcnow().isoformat(),
                "source": "oci",
            }
            return {"data": payload, "metadata": metadata}

        local = self._load_local_file(resolved_name)
        if local is None:
            raise FileNotFoundError(
                f"Could not locate {resolved_name}. Set LOCAL_ASSET_ROOT or provide a valid OCI configuration."
            )
        return local


class VisionClient:
    """Wrapper around OCI Vision deployments."""

    def __init__(self, config: WorkflowConfig):
        self._config = config
        self._client = None

    def _get_genai_client(self):
        """Initialize OCI GenAI client for vision"""
        if self._client is None:
            try:
                import oci
                from oci.generative_ai_inference import GenerativeAiInferenceClient
                
                # Load OCI configuration
                try:
                    oci_config = oci.config.from_file()
                except Exception as config_error:
                    print(f"Warning: Could not load OCI config file: {config_error}")
                    oci_config = oci.config.from_file("~/.oci/config")
                
                # Get GenAI configuration from environment
                hostname = os.environ.get('OCI_GENAI_HOSTNAME')
                if not hostname:
                    raise ValueError("OCI_GENAI_HOSTNAME must be set")
                
                # Remove endpoint path if included in hostname
                if '/20231130/actions/generateText' in hostname:
                    hostname = hostname.replace('/20231130/actions/generateText', '')
                
                # Initialize GenAI client
                self._client = GenerativeAiInferenceClient(
                    config=oci_config,
                    service_endpoint=hostname,
                    retry_strategy=oci.retry.NoneRetryStrategy(),
                    timeout=(10, 240)
                )
                
            except Exception as e:
                print(f"Error initializing OCI GenAI client: {e}")
                raise RuntimeError(f"Failed to initialize OCI GenAI client: {e}")
        
        return self._client

    def generate_caption(self, image_bytes: bytes) -> str:
        """Generate image caption using OCI GenAI Vision - EXACT copy from working console test"""
        try:
            import oci
            import base64
            
            # Get GenAI client
            client = self._get_genai_client()
            
            # Encode image to base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # Get configuration
            model_ocid = os.environ.get('OCI_TEXT_MODEL_OCID')
            compartment_id = os.environ.get('OCI_COMPARTMENT_ID')
            
            if not model_ocid or not compartment_id:
                return "Error: OCI_TEXT_MODEL_OCID and OCI_COMPARTMENT_ID must be set"
            
            # EXACT COPY from working console test
            text_content = oci.generative_ai_inference.models.TextContent()
            text_content.text = "Describe the delivery scene in detail. What do you see?"
            
            # EXACT COPY from working console test - try ImageUrl first, fallback to source
            try:
                # Try to create ImageUrl structure (from console test)
                image_url = oci.generative_ai_inference.models.ImageUrl()
                image_url.url = f"data:image/jpeg;base64,{encoded_image}"
                
                # Create image content with ImageUrl
                image_content = oci.generative_ai_inference.models.ImageContent()
                image_content.image_url = image_url
                
            except Exception as e:
                print(f"⚠️  ImageUrl structure not available: {e}")
                # Fallback to source method (from console test)
                image_content = oci.generative_ai_inference.models.ImageContent()
                image_content.source = f"data:image/jpeg;base64,{encoded_image}"
            
            # EXACT COPY from working console test
            message = oci.generative_ai_inference.models.Message()
            message.role = "USER"
            message.content = [text_content, image_content]  # Both text and image
            
            # EXACT COPY from working console test
            chat_request = oci.generative_ai_inference.models.GenericChatRequest()
            chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
            chat_request.messages = [message]
            chat_request.max_tokens = 600
            chat_request.temperature = 1
            chat_request.frequency_penalty = 0
            chat_request.presence_penalty = 0
            chat_request.top_p = 0.75
            chat_request.top_k = -1
            chat_request.is_stream = False
            
            # EXACT COPY from working console test
            serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
                endpoint_id=model_ocid
            )
            
            # EXACT COPY from working console test
            chat_detail = oci.generative_ai_inference.models.ChatDetails()
            chat_detail.serving_mode = serving_mode
            chat_detail.chat_request = chat_request
            chat_detail.compartment_id = compartment_id
            
            # EXACT COPY from working console test
            response = client.chat(chat_detail)
            
            # EXACT COPY from working console test response parsing
            if (response.data and 
                hasattr(response.data, 'chat_response') and 
                response.data.chat_response and
                hasattr(response.data.chat_response, 'choices') and 
                response.data.chat_response.choices and
                len(response.data.chat_response.choices) > 0 and
                hasattr(response.data.chat_response.choices[0], 'message') and
                response.data.chat_response.choices[0].message and
                hasattr(response.data.chat_response.choices[0].message, 'content') and
                response.data.chat_response.choices[0].message.content and
                len(response.data.chat_response.choices[0].message.content) > 0):
                
                caption = response.data.chat_response.choices[0].message.content[0].text
                return caption
            else:
                return "No caption generated"
                
        except Exception as e:
            print(f"Error generating caption: {e}")
            return "Error generating caption"

    def detect_damage(self, image_bytes: bytes) -> Dict[str, float]:
        """Detect damage in image using OCI GenAI Vision - EXACT copy from working console test"""
        try:
            import oci
            import base64
            import re
            
            # Get GenAI client
            client = self._get_genai_client()
            
            # Encode image to base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # Get configuration
            model_ocid = os.environ.get('OCI_TEXT_MODEL_OCID')
            compartment_id = os.environ.get('OCI_COMPARTMENT_ID')
            
            if not model_ocid or not compartment_id:
                return {"damage": 0.0, "no_damage": 1.0}
            
            # EXACT COPY from working console test
            text_content = oci.generative_ai_inference.models.TextContent()
            text_content.text = "Describe the delivery scene in detail. What do you see?"
            
            # EXACT COPY from working console test - try ImageUrl first, fallback to source
            try:
                # Try to create ImageUrl structure (from console test)
                image_url = oci.generative_ai_inference.models.ImageUrl()
                image_url.url = f"data:image/jpeg;base64,{encoded_image}"
                
                # Create image content with ImageUrl
                image_content = oci.generative_ai_inference.models.ImageContent()
                image_content.image_url = image_url
                
            except Exception as e:
                print(f"⚠️  ImageUrl structure not available: {e}")
                # Fallback to source method (from console test)
                image_content = oci.generative_ai_inference.models.ImageContent()
                image_content.source = f"data:image/jpeg;base64,{encoded_image}"
            
            # EXACT COPY from working console test
            message = oci.generative_ai_inference.models.Message()
            message.role = "USER"
            message.content = [text_content, image_content]  # Both text and image
            
            # EXACT COPY from working console test
            chat_request = oci.generative_ai_inference.models.GenericChatRequest()
            chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
            chat_request.messages = [message]
            chat_request.max_tokens = 600
            chat_request.temperature = 1
            chat_request.frequency_penalty = 0
            chat_request.presence_penalty = 0
            chat_request.top_p = 0.75
            chat_request.top_k = -1
            chat_request.is_stream = False
            
            # EXACT COPY from working console test
            serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
                endpoint_id=model_ocid
            )
            
            # EXACT COPY from working console test
            chat_detail = oci.generative_ai_inference.models.ChatDetails()
            chat_detail.serving_mode = serving_mode
            chat_detail.chat_request = chat_request
            chat_detail.compartment_id = compartment_id
            
            # EXACT COPY from working console test
            response = client.chat(chat_detail)
            
            # EXACT COPY from working console test response parsing
            damage_scores = {"damage": 0.0, "no_damage": 1.0}
            
            if (response.data and 
                hasattr(response.data, 'chat_response') and 
                response.data.chat_response and
                hasattr(response.data.chat_response, 'choices') and 
                response.data.chat_response.choices and
                len(response.data.chat_response.choices) > 0 and
                hasattr(response.data.chat_response.choices[0], 'message') and
                response.data.chat_response.choices[0].message and
                hasattr(response.data.chat_response.choices[0].message, 'content') and
                response.data.chat_response.choices[0].message.content and
                len(response.data.chat_response.choices[0].message.content) > 0):
                
                assessment = response.data.chat_response.choices[0].message.content[0].text
                
                # Parse damage assessment from response
                assessment_lower = assessment.lower()
                
                # Look for damage indicators
                if "damaged" in assessment_lower or "damage" in assessment_lower:
                    if "severely" in assessment_lower:
                        damage_scores = {"damage": 0.9, "no_damage": 0.1}
                    elif "moderately" in assessment_lower:
                        damage_scores = {"damage": 0.6, "no_damage": 0.4}
                    elif "slightly" in assessment_lower:
                        damage_scores = {"damage": 0.3, "no_damage": 0.7}
                    else:
                        damage_scores = {"damage": 0.5, "no_damage": 0.5}
                elif "intact" in assessment_lower or "good condition" in assessment_lower or "no damage" in assessment_lower:
                    damage_scores = {"damage": 0.1, "no_damage": 0.9}
                elif "not visible" in assessment_lower or "no package" in assessment_lower:
                    # If no package is visible, assume no damage
                    damage_scores = {"damage": 0.0, "no_damage": 1.0}
                
            return damage_scores
            
        except Exception as e:
            print(f"Error detecting damage: {e}")
            return {"damage": 0.0, "no_damage": 1.0}


def extract_exif(image_bytes: bytes) -> Dict[str, Any]:
    with Image.open(io.BytesIO(image_bytes)) as img:
        exif_data_raw = img._getexif() or {}

    exif_data: Dict[str, Any] = {}
    for tag_id, value in exif_data_raw.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        exif_data[tag] = value

    gps_info = exif_data.get("GPSInfo", {})
    if gps_info:
        gps_data = {}
        for key, val in gps_info.items():
            decoded_key = ExifTags.GPSTAGS.get(key, key)
            gps_data[decoded_key] = val
        exif_data["GPSInfo"] = gps_data

    return exif_data


class ObjectRetrievalTool(BaseTool):
    name: str = "retrieve_delivery_photo"
    description: str = "Fetch delivery photo bytes and metadata from OCI Object Storage."

    def __init__(self, config: WorkflowConfig):
        super().__init__()
        self._config = config
        self._client = ObjectStorageClient(config)

    def _run(self, object_name: str) -> str:
        result = self._client.get_object(object_name)
        payload = base64.b64encode(result["data"]).decode("utf-8")
        return json.dumps({"payload": payload, "metadata": result["metadata"]})

    async def _arun(self, object_name: str) -> str:  # pragma: no cover - async not implemented
        raise NotImplementedError


class ExifExtractionTool(BaseTool):
    name: str = "extract_exif"
    description: str = "Extract EXIF metadata including GPS coordinates from a delivery image."

    def _run(self, encoded_payload: str) -> str:
        image_bytes = base64.b64decode(encoded_payload)
        exif = extract_exif(image_bytes)
        return json.dumps(exif, default=str)

    async def _arun(self, encoded_payload: str) -> str:  # pragma: no cover - async not implemented
        raise NotImplementedError


class ImageCaptionTool(BaseTool):
    name: str = "caption_image"
    description: str = "Generate a textual caption for the delivery photo using OCI Vision."

    def __init__(self, config: WorkflowConfig):
        super().__init__()
        self._client = VisionClient(config)

    def _run(self, encoded_payload: str) -> str:
        image_bytes = base64.b64decode(encoded_payload)
        caption = self._client.generate_caption(image_bytes)
        return caption

    async def _arun(self, encoded_payload: str) -> str:  # pragma: no cover
        raise NotImplementedError


class DamageDetectionTool(BaseTool):
    name: str = "detect_damage"
    description: str = "Predict package damage likelihood from the delivery photo."

    def __init__(self, config: WorkflowConfig):
        super().__init__()
        self._config = config
        self._client = VisionClient(config)

    def _run(self, encoded_payload: str) -> str:
        image_bytes = base64.b64decode(encoded_payload)
        predictions = self._client.detect_damage(image_bytes)
        return json.dumps(predictions)

    async def _arun(self, encoded_payload: str) -> str:  # pragma: no cover
        raise NotImplementedError


def toolset(config: WorkflowConfig) -> Dict[str, BaseTool]:
    """Factory returning all tools keyed by workflow stage."""

    return {
        "retrieval": ObjectRetrievalTool(config),
        "exif": ExifExtractionTool(),
        "caption": ImageCaptionTool(config),
        "damage": DamageDetectionTool(config),
    }
