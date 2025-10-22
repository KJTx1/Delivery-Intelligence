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
class PrivacyConfig:
    """Privacy protection settings for image processing."""
    
    enable_face_blurring: bool = True
    blur_intensity: int = 51
    # More sensitive defaults for better privacy protection (catches partial faces)
    face_detection_scale_factor: float = 1.05  # Was 1.1 - more thorough detection
    face_detection_min_neighbors: int = 3      # Was 5 - more sensitive
    face_detection_min_size: tuple = field(default=(20, 20))  # Was (30,30) - catch smaller faces
    strict_privacy_mode: bool = True  # Use aggressive detection by default
    
    def __post_init__(self):
        """Validate privacy settings and apply strict mode if enabled."""
        if self.blur_intensity % 2 == 0:
            raise ValueError("blur_intensity must be an odd number")
        if not 15 <= self.blur_intensity <= 99:
            raise ValueError("blur_intensity must be between 15 and 99")
        if not 1.01 <= self.face_detection_scale_factor <= 2.0:
            raise ValueError("face_detection_scale_factor must be between 1.01 and 2.0")
        if not 1 <= self.face_detection_min_neighbors <= 10:
            raise ValueError("face_detection_min_neighbors must be between 1 and 10")
        
        # Apply strict privacy mode settings if enabled
        if self.strict_privacy_mode:
            # Override with maximum privacy settings
            self.face_detection_scale_factor = min(self.face_detection_scale_factor, 1.05)
            self.face_detection_min_neighbors = min(self.face_detection_min_neighbors, 3)
            # Ensure minimum size catches smaller/partial faces
            if isinstance(self.face_detection_min_size, tuple) and self.face_detection_min_size[0] > 20:
                self.face_detection_min_size = (20, 20)


@dataclass
class WorkflowConfig:
    """Top level settings required by the agent workflow."""

    object_storage: ObjectStorageConfig
    vision: VisionConfig
    geolocation: GeolocationConfig = field(default_factory=GeolocationConfig)
    quality_weights: QualityIndexWeights = field(default_factory=QualityIndexWeights)
    damage_scoring: DamageScoringConfig = field(default_factory=DamageScoringConfig)
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    notification_topic_id: Optional[str] = None
    database_table: str = "delivery_quality_events"
    local_asset_root: Optional[str] = None
