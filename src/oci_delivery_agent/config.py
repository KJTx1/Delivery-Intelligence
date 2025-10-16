"""Configuration models for the OCI delivery agent workflow."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ObjectStorageConfig:
    """Object Storage connection parameters."""

    namespace: str
    bucket_name: str
    delivery_prefix: str = ""


@dataclass
class VisionConfig:
    """Configuration for OCI Vision and custom models."""

    compartment_id: str
    image_caption_model_endpoint: str
    damage_detection_model_endpoint: Optional[str] = None
    confidence_threshold: float = 0.5


@dataclass
class GeolocationConfig:
    """Parameters for validating delivery coordinates."""

    max_distance_meters: float = 50.0
    geocoding_api_endpoint: Optional[str] = None


@dataclass
class QualityIndexWeights:
    """Weights applied when computing the delivery quality index."""

    timeliness: float = 0.3
    location_accuracy: float = 0.3
    damage_score: float = 0.4

    def normalized(self) -> Dict[str, float]:
        total = self.timeliness + self.location_accuracy + self.damage_score
        if total == 0:
            raise ValueError("At least one quality index weight must be positive.")
        return {
            "timeliness": self.timeliness / total,
            "location_accuracy": self.location_accuracy / total,
            "damage_score": self.damage_score / total,
        }


@dataclass
class WorkflowConfig:
    """Top level settings required by the agent workflow."""

    object_storage: ObjectStorageConfig
    vision: VisionConfig
    geolocation: GeolocationConfig = field(default_factory=GeolocationConfig)
    quality_weights: QualityIndexWeights = field(default_factory=QualityIndexWeights)
    notification_topic_id: Optional[str] = None
    database_table: str = "delivery_quality_events"
    local_asset_root: Optional[str] = None
