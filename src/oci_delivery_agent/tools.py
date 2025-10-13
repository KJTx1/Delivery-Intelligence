"""LangChain tools wrapping OCI services for the delivery workflow."""
from __future__ import annotations

import base64
import io
import json
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
            profile = self._config.object_storage.namespace or None
            oci_config = oci.config.from_file(profile_name=profile) if profile else oci.config.from_file()
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

    def generate_caption(self, image_bytes: bytes) -> str:
        # Placeholder for an OCI Vision Generative caption endpoint call.
        # An OCI Data Science deployment could also be called here.
        return "Package delivered at front door"

    def detect_damage(self, image_bytes: bytes) -> Dict[str, float]:
        # Simulated inference output: label -> confidence.
        return {"damage": 0.15, "no_damage": 0.85}


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
    name = "retrieve_delivery_photo"
    description = "Fetch delivery photo bytes and metadata from OCI Object Storage."

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
    name = "extract_exif"
    description = "Extract EXIF metadata including GPS coordinates from a delivery image."

    def _run(self, encoded_payload: str) -> str:
        image_bytes = base64.b64decode(encoded_payload)
        exif = extract_exif(image_bytes)
        return json.dumps(exif, default=str)

    async def _arun(self, encoded_payload: str) -> str:  # pragma: no cover - async not implemented
        raise NotImplementedError


class ImageCaptionTool(BaseTool):
    name = "caption_image"
    description = "Generate a textual caption for the delivery photo using OCI Vision."

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
    name = "detect_damage"
    description = "Predict package damage likelihood from the delivery photo."

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
