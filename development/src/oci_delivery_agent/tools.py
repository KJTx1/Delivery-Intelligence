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
        
        # Try OCI first if client exists and namespace/bucket are not test values
        if (self._client is not None and 
            self._config.object_storage.namespace != "test" and 
            self._config.object_storage.bucket_name != "test"):  # pragma: no cover - network interaction
            try:
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
            except Exception:
                # Fall back to local on any error
                pass

        # Use local fallback
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

    def _damage_json_prompt(self, caption_context: Optional[Dict[str, Any]] = None) -> str:
        """Return strict JSON-only prompt for damage assessment.
        
        Args:
            caption_context: Optional caption results to provide context about visible packages
        """
        # Get scoring thresholds from config
        scoring = self._config.damage_scoring
        
        # Build context section if caption was provided
        context_section = ""
        if caption_context:
            pkg_visible = caption_context.get("packageVisible", False)
            pkg_desc = caption_context.get("packageDescription", "")
            if pkg_visible and pkg_desc:
                context_section = (
                    f"CONTEXT: Prior analysis identified packages in this image: {pkg_desc}\n"
                    f"Your damage assessment should evaluate these identified items.\n\n"
                )
        
        return (
            "You are a delivery damage inspector. Analyze the provided image and produce ONLY a single JSON object (no markdown, no preface, no trailing text) with this exact structure:\n\n"
            "{\n"
            "  \"overall\": { \"severity\": \"none|minor|moderate|severe\", \"score\": 0.0-1.0, \"rationale\": \"string\" },\n"
            "  \"indicators\": {\n"
            "    \"boxDeformation\": { \"present\": true|false, \"severity\": \"none|minor|moderate|severe\", \"evidence\": \"string\" },\n"
            "    \"cornerDamage\":   { \"present\": true|false, \"severity\": \"none|minor|moderate|severe\", \"evidence\": \"string\" },\n"
            "    \"leakage\":        { \"present\": true|false, \"severity\": \"none|minor|moderate|severe\", \"evidence\": \"string\" },\n"
            "    \"packagingIntegrity\": { \"present\": true|false, \"severity\": \"none|minor|moderate|severe\", \"evidence\": \"string\" }\n"
            "  },\n"
            "  \"packageVisible\": true|false,\n"
            "  \"uncertainties\": \"string\"\n"
            "}\n\n"
            f"{context_section}"
            "Important: A 'package' includes ANY delivered items: cardboard boxes, plastic bags, envelopes, containers, parcels, or any other delivery items.\n\n"
            "Definitions:\n"
            "- boxDeformation: crushed corners, bent edges, bulging sides, structural collapse (applies to boxes, bags, containers).\n"
            "- cornerDamage: crushed/abraded/torn/dented corners (for any package type with corners).\n"
            "- leakage: liquid stains, wet spots, moisture damage (visible on or around any package).\n"
            "- packagingIntegrity: tears, holes, dents, scratches, tape failure, visible damage to any package surface.\n\n"
            "Rules:\n"
            "- FIRST, identify if ANY delivery items (boxes, bags, coolers, envelopes, containers, parcels) are visible.\n"
            "- If ANY delivery items are visible, set \"packageVisible\": true and assess damage on those items.\n"
            "- If absolutely NO delivery items are visible, set \"packageVisible\": false and \"overall.severity\": \"none\", \"overall.score\": 0.0 with rationale.\n"
            f"- If delivery items are visible but no damage is visible, set all indicators.present=false, severity=\"none\", evidence=\"none\", overall.severity=\"none\", overall.score<={scoring.none_max}.\n"
            f"- Calibrate score by worst indicator: severe ≈ {scoring.severe_min}, moderate ≈ {scoring.moderate_min}–{scoring.moderate_max}, minor ≈ {scoring.minor_min}–{scoring.minor_max}, none ≤ {scoring.none_max}.\n"
            "- Keep evidence short and visual (what/where). Be precise, no speculation.\n"
            f"- If any of these keywords are observed: crushed, bent, bulging, tear, hole, dent, leak, wet, stain → minimum severity is 'minor' and score ≥ {scoring.minor_min}.\n"
            "- For plastic bags and soft containers: assess tears, holes, and structural integrity instead of box deformation.\n"
            "- Output MUST be valid JSON, UTF-8, no trailing commas, no extra commentary.\n\n"
            "Now analyze the image and output the JSON only."
        )

    def _parse_damage_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Parse a JSON report from model text; try substring recovery if needed."""
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = [
                line for line in clean.splitlines()
                if not line.strip().startswith("```")
            ]
            clean = "\n".join(lines).strip()
        try:
            return json.loads(clean)
        except Exception:
            start = clean.find("{")
            end = clean.rfind("}")
            if start != -1 and end != -1 and end > start:
                snippet = clean[start : end + 1]
                try:
                    return json.loads(snippet)
                except Exception:
                    return None
            return None

    def _parse_caption_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Parse caption JSON from model text; try substring recovery if needed."""
        clean = raw_text.strip()
        
        # Remove markdown code blocks
        if clean.startswith("```"):
            lines = [
                line for line in clean.splitlines()
                if not line.strip().startswith("```")
            ]
            clean = "\n".join(lines).strip()
        
        # Try direct JSON parsing first
        try:
            return json.loads(clean)
        except Exception:
            pass
        
        # Try to find JSON object boundaries
        start = clean.find("{")
        end = clean.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = clean[start : end + 1]
            try:
                return json.loads(snippet)
            except Exception:
                pass
        
        # Try to find JSON array boundaries (in case it's wrapped in array)
        start = clean.find("[")
        end = clean.rfind("]")
        if start != -1 and end != -1 and end > start:
            snippet = clean[start : end + 1]
            try:
                parsed = json.loads(snippet)
                if isinstance(parsed, list) and len(parsed) > 0:
                    return parsed[0]  # Return first object if it's an array
            except Exception:
                pass
        
        # Try to extract JSON from common patterns
        import re
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, clean, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except Exception:
                continue
        
        return None

    def _caption_json_prompt(self) -> str:
        """Return structured JSON prompt for delivery scene caption."""
        return (
            "You are a delivery scene analyzer. Analyze the provided image and produce ONLY a single JSON object (no markdown, no preface, no trailing text) with this exact structure:\n\n"
            "{\n"
            "  \"sceneType\": \"delivery|package|entrance|other\",\n"
            "  \"packageVisible\": true|false,\n"
            "  \"packageDescription\": \"string\",\n"
            "  \"location\": {\n"
            "    \"type\": \"doorstep|porch|mailbox|driveway|entrance|inside|other\",\n"
            "    \"description\": \"string\"\n"
            "  },\n"
            "  \"environment\": {\n"
            "    \"weather\": \"clear|rainy|cloudy|snowy|unknown\",\n"
            "    \"timeOfDay\": \"morning|afternoon|evening|night|unknown\",\n"
            "    \"conditions\": \"string\"\n"
            "  },\n"
            "  \"safetyAssessment\": {\n"
            "    \"protected\": true|false,\n"
            "    \"visible\": true|false,\n"
            "    \"secure\": true|false,\n"
            "    \"notes\": \"string\"\n"
            "  },\n"
            "  \"overallDescription\": \"string\"\n"
            "}\n\n"
            "Definitions:\n"
            "- sceneType: primary scene category (delivery=package at destination, package=package only, entrance=door/entrance visible, other=none of these)\n"
            "- packageVisible: whether any package/box/parcel is visible in the image\n"
            "- packageDescription: short description of package(s) seen, or \"none\" if not visible\n"
            "- location.type: where the package/scene is located\n"
            "- location.description: brief description of the location (what you see)\n"
            "- environment.weather: apparent weather conditions from visual cues\n"
            "- environment.timeOfDay: estimated time based on lighting\n"
            "- environment.conditions: brief description of environmental factors\n"
            "- safetyAssessment.protected: is package sheltered from weather/elements\n"
            "- safetyAssessment.visible: is package visible from street/public view\n"
            "- safetyAssessment.secure: does location appear secure (not easily stolen)\n"
            "- safetyAssessment.notes: brief assessment of delivery safety\n"
            "- overallDescription: 2-3 sentence summary of the entire scene\n\n"
            "Rules:\n"
            "- If no package is visible, set packageVisible=false and packageDescription=\"none\", but still describe the scene.\n"
            "- Keep descriptions factual and visual. No speculation about contents or ownership.\n"
            "- For weather/time, use \"unknown\" if not clearly visible.\n"
            "- Output MUST be valid JSON, UTF-8, no trailing commas, no extra commentary.\n\n"
            "Now analyze the image and output the JSON only."
        )

    def generate_caption(self, image_bytes: bytes) -> str:
        """Generate structured delivery scene caption using OCI GenAI Vision."""
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
                return json.dumps({"error": "missing_credentials"})
            
            # Structured caption prompt
            text_content = oci.generative_ai_inference.models.TextContent()
            text_content.text = self._caption_json_prompt()
            
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
            
            # Chat request with lower temperature for structured output
            chat_request = oci.generative_ai_inference.models.GenericChatRequest()
            chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
            chat_request.messages = [message]
            chat_request.max_tokens = 800
            chat_request.temperature = 0.2
            chat_request.frequency_penalty = 0
            chat_request.presence_penalty = 0
            chat_request.top_p = 0.85
            chat_request.top_k = -1
            chat_request.is_stream = False
            
            # Serving mode
            serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
                endpoint_id=model_ocid
            )
            
            # Chat details
            chat_detail = oci.generative_ai_inference.models.ChatDetails()
            chat_detail.serving_mode = serving_mode
            chat_detail.chat_request = chat_request
            chat_detail.compartment_id = compartment_id
            
            # Get response
            response = client.chat(chat_detail)
            
            # Parse response and extract JSON
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
                
                caption_text = response.data.chat_response.choices[0].message.content[0].text
                
                # Try to parse as JSON
                caption_json = self._parse_caption_json(caption_text)
                if caption_json is not None:
                    return json.dumps(caption_json)
                else:
                    # Fallback: return raw text wrapped in JSON
                    return json.dumps({"unstructured": caption_text})
            else:
                return json.dumps({"error": "no_caption_generated"})
                
        except Exception as e:
            print(f"Error generating caption: {e}")
            return json.dumps({"error": str(e)})

    def detect_damage(self, image_bytes: bytes, caption_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Detect damage using GenAI with strict JSON output for indicators.
        
        Args:
            image_bytes: The image data to analyze
            caption_context: Optional caption results to provide context about visible packages
        """
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
                return {"error": "missing_credentials"}
            
            # Strict JSON prompt for robust downstream parsing
            text_content = oci.generative_ai_inference.models.TextContent()
            text_content.text = self._damage_json_prompt(caption_context)
            
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
            chat_request.max_tokens = 800
            chat_request.temperature = 0.1
            chat_request.frequency_penalty = 0
            chat_request.presence_penalty = 0
            chat_request.top_p = 0.85
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
            
            # Parse JSON and extract only indicators
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
                report = self._parse_damage_json(assessment)
                
                if report is not None:
                    # Return complete report
                    return report
                else:
                    # Fallback: return error if JSON parsing failed
                    return {"error": "json_parse_failed"}

            return {"error": "no_response"}
            
        except Exception as e:
            print(f"Error detecting damage: {e}")
            return {"error": str(e)}


def extract_exif(image_bytes: bytes) -> Dict[str, Any]:
    with Image.open(io.BytesIO(image_bytes)) as img:
        exif_data_raw = img._getexif() or {}

    raw_gps = None
    timestamp = None
    for tag_id, value in exif_data_raw.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo":
            raw_gps = value
        elif tag in {"DateTimeOriginal", "DateTime"} and not timestamp:
            timestamp = value

    def _to_float(component: Any) -> Optional[float]:
        if component is None:
            return None
        if isinstance(component, (int, float)):
            return float(component)
        if hasattr(component, "numerator") and hasattr(component, "denominator"):
            denom = component.denominator
            return component.numerator / denom if denom else None
        if isinstance(component, (tuple, list)):
            if len(component) == 2:
                numerator = _to_float(component[0])
                denominator = _to_float(component[1])
                if numerator is None or denominator in (None, 0):
                    return None
                return numerator / denominator
            return None
        if isinstance(component, str):
            try:
                return float(component)
            except ValueError:
                if "/" in component:
                    num, denom = component.split("/", 1)
                    try:
                        return float(num) / float(denom)
                    except (ValueError, ZeroDivisionError):
                        return None
                return None
        try:
            return float(component)
        except Exception:
            return None

    def _convert_to_degrees(values: List[Any]) -> Optional[float]:
        if not values or len(values) < 3:
            return None
        deg = _to_float(values[0])
        minutes = _to_float(values[1])
        seconds = _to_float(values[2])
        if None in (deg, minutes, seconds):
            return None
        return deg + minutes / 60 + seconds / 3600

    gps_payload: Dict[str, Any] = {}
    if raw_gps:
        gps_named = {
            ExifTags.GPSTAGS.get(key, key): value for key, value in raw_gps.items()
        }
        lat = _convert_to_degrees(gps_named.get("GPSLatitude", []))
        lon = _convert_to_degrees(gps_named.get("GPSLongitude", []))
        lat_ref = gps_named.get("GPSLatitudeRef")
        lon_ref = gps_named.get("GPSLongitudeRef")
        if lat is not None and lat_ref == "S":
            lat = -lat
        if lon is not None and lon_ref == "W":
            lon = -lon
        if lat is not None and lon is not None:
            gps_payload["latitude"] = lat
            gps_payload["longitude"] = lon
        altitude = _to_float(gps_named.get("GPSAltitude"))
        if altitude is not None:
            gps_payload["altitude"] = altitude

    clean_exif: Dict[str, Any] = {}
    if gps_payload:
        clean_exif["GPSInfo"] = gps_payload
    if timestamp:
        clean_exif["timestamp"] = timestamp

    return clean_exif


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
    description: str = "Generate structured delivery scene analysis as JSON (sceneType, package, location, environment, safetyAssessment)."

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
    description: str = "Extract per-indicator damage assessment as JSON (boxDeformation, cornerDamage, leakage, packagingIntegrity)."

    def __init__(self, config: WorkflowConfig):
        super().__init__()
        self._config = config
        self._client = VisionClient(config)

    def _run(self, encoded_payload: str, caption_context: Optional[str] = None) -> str:
        """Run damage detection, optionally using caption context.
        
        Args:
            encoded_payload: Base64-encoded image data
            caption_context: Optional JSON string with caption results for context
        """
        image_bytes = base64.b64decode(encoded_payload)
        
        # Parse caption context if provided
        context_dict = None
        if caption_context:
            try:
                context_dict = json.loads(caption_context)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse caption_context: {caption_context}")
        
        result = self._client.detect_damage(image_bytes, caption_context=context_dict)
        return json.dumps(result)

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
