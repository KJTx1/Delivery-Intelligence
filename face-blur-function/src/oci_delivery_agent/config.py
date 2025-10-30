"""Configuration models for the face blur function."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectStorageConfig:
    """Object Storage connection parameters."""

    namespace: str
    bucket_name: str
    blur_prefix: str = "blurred/"


@dataclass
class VisionConfig:
    """Configuration for OCI Vision Face Detection."""

    compartment_id: str
    max_results: int = 100
    should_return_landmarks: bool = True
    confidence_threshold: float = 0.0


@dataclass
class BlurConfig:
    """Face blurring configuration."""

    blur_intensity: int = 51
    padding: int = 10
    adaptive_blur_factor: float = 0.4
    max_blur_intensity: int = 299

    def __post_init__(self):
        """Validate blur settings."""
        if self.blur_intensity % 2 == 0:
            raise ValueError("blur_intensity must be an odd number")
        if not 15 <= self.blur_intensity <= 99:
            raise ValueError("blur_intensity must be between 15 and 99")
        if self.max_blur_intensity % 2 == 0:
            self.max_blur_intensity += 1


@dataclass
class FaceBlurConfig:
    """Top level configuration for face blur function."""

    object_storage: ObjectStorageConfig
    vision: VisionConfig
    blur: BlurConfig
