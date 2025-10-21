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
class DamageTypeWeights:
    """Weights for different damage types in MVP scoring."""
    
    leakage: float = 0.4
    box_deformation: float = 0.3
    packaging_integrity: float = 0.2
    corner_damage: float = 0.1
    
    def normalized(self) -> Dict[str, float]:
        """Return normalized weights that sum to 1.0."""
        total = self.leakage + self.box_deformation + self.packaging_integrity + self.corner_damage
        if total == 0:
            raise ValueError("At least one damage type weight must be positive.")
        return {
            "leakage": self.leakage / total,
            "boxDeformation": self.box_deformation / total,
            "packagingIntegrity": self.packaging_integrity / total,
            "cornerDamage": self.corner_damage / total,
        }


@dataclass
class SeverityScores:
    """Configurable severity score mapping."""
    
    none: float = 0.05
    minor: float = 0.35
    moderate: float = 0.65
    severe: float = 0.9


@dataclass
class DamageScoringConfig:
    """Configuration for damage severity scoring thresholds."""

    none_max: float = 0.1
    minor_min: float = 0.3
    minor_max: float = 0.4
    moderate_min: float = 0.6
    moderate_max: float = 0.7
    severe_min: float = 0.9
    
    # MVP: Add damage type weights
    use_weighted_scoring: bool = True
    type_weights: DamageTypeWeights = field(default_factory=DamageTypeWeights)
    severity_scores: SeverityScores = field(default_factory=SeverityScores)

    def __post_init__(self):
        """Validate score thresholds."""
        if not (0.0 <= self.none_max < self.minor_min < self.minor_max <= self.moderate_min < self.moderate_max <= self.severe_min <= 1.0):
            raise ValueError(
                "Damage score thresholds must be ordered: "
                "0.0 <= none_max < minor_min < minor_max <= moderate_min < moderate_max <= severe_min <= 1.0"
            )


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
    damage_scoring: DamageScoringConfig = field(default_factory=DamageScoringConfig)
    notification_topic_id: Optional[str] = None
    database_table: str = "delivery_quality_events"
    local_asset_root: Optional[str] = None
