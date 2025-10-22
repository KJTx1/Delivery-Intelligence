"""CLI entry point for exercising the delivery quality LangChain workflow."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict

# from langchain.llms import OCIModel  # Commented out due to version compatibility
from langchain.llms.fake import FakeListLLM

from .chains import DeliveryContext, run_quality_pipeline
from .config import (
    DamageScoringConfig,
    GeolocationConfig,
    ObjectStorageConfig,
    QualityIndexWeights,
    VisionConfig,
    WorkflowConfig,
)


def _build_config(args: argparse.Namespace) -> WorkflowConfig:
    """Create a :class:`WorkflowConfig` from CLI arguments and env vars."""

    object_storage = ObjectStorageConfig(
        namespace=args.os_namespace or os.environ.get("OCI_OS_NAMESPACE", ""),
        bucket_name=args.os_bucket or os.environ.get("OCI_OS_BUCKET", ""),
        delivery_prefix=args.delivery_prefix
        or os.environ.get("DELIVERY_PREFIX", "deliveries/"),
    )
    vision = VisionConfig(
        compartment_id=args.compartment_id or os.environ.get("OCI_COMPARTMENT_ID", ""),
        image_caption_model_endpoint=args.caption_endpoint
        or os.environ.get("OCI_CAPTION_ENDPOINT", ""),
        damage_detection_model_endpoint=args.damage_endpoint
        or os.environ.get("OCI_DAMAGE_ENDPOINT"),
    )
    geolocation = GeolocationConfig(
        max_distance_meters=args.max_distance
        or float(os.environ.get("MAX_DISTANCE_METERS", "50")),
        geocoding_api_endpoint=args.geocoding_endpoint
        or os.environ.get("GEOCODING_ENDPOINT"),
    )
    quality_weights = QualityIndexWeights(
        timeliness=args.weight_timeliness
        or float(os.environ.get("WEIGHT_TIMELINESS", "0.3")),
        location_accuracy=args.weight_location
        or float(os.environ.get("WEIGHT_LOCATION", "0.3")),
        damage_score=args.weight_damage
        or float(os.environ.get("WEIGHT_DAMAGE", "0.4")),
    )
    damage_scoring = DamageScoringConfig(
        none_max=float(os.environ.get("DAMAGE_SCORE_NONE_MAX", "0.1")),
        minor_min=float(os.environ.get("DAMAGE_SCORE_MINOR_MIN", "0.3")),
        minor_max=float(os.environ.get("DAMAGE_SCORE_MINOR_MAX", "0.4")),
        moderate_min=float(os.environ.get("DAMAGE_SCORE_MODERATE_MIN", "0.6")),
        moderate_max=float(os.environ.get("DAMAGE_SCORE_MODERATE_MAX", "0.7")),
        severe_min=float(os.environ.get("DAMAGE_SCORE_SEVERE_MIN", "0.9")),
    )

    return WorkflowConfig(
        object_storage=object_storage,
        vision=vision,
        geolocation=geolocation,
        quality_weights=quality_weights,
        damage_scoring=damage_scoring,
        notification_topic_id=os.environ.get("NOTIFICATION_TOPIC_ID"),
        database_table=os.environ.get("QUALITY_TABLE", "delivery_quality_events"),
        local_asset_root=args.local_asset_root or os.environ.get("LOCAL_ASSET_ROOT"),
    )


def _build_context(args: argparse.Namespace) -> DeliveryContext:
    return DeliveryContext(
        object_name=args.object_name,
        expected_latitude=args.expected_latitude,
        expected_longitude=args.expected_longitude,
        promised_time_utc=datetime.fromisoformat(args.promised_time),
        delivered_time_utc=datetime.fromisoformat(args.delivered_time),
    )


def _build_llm(config: WorkflowConfig, args: argparse.Namespace):
    if args.dry_run:
        canned_response = json.dumps(
            {
                "status": "OK",
                "issues": [],
                "insights": "Dry-run response. Configure OCI Generative AI for live scoring.",
            }
        )
        return FakeListLLM(responses=[canned_response])

    # Use the same OCI GenAI implementation as handlers.py
    from .handlers import build_llm
    return build_llm(config)


def parse_args(argv: Any | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("object_name", help="Object name or path of the delivery photo")
    parser.add_argument("expected_latitude", type=float, help="Expected delivery latitude")
    parser.add_argument("expected_longitude", type=float, help="Expected delivery longitude")
    parser.add_argument("promised_time", help="ISO timestamp of the promised delivery time")
    parser.add_argument("delivered_time", help="ISO timestamp of when the delivery occurred")

    parser.add_argument("--dry-run", action="store_true", help="Use a fake LLM for offline testing")
    parser.add_argument("--model-ocid", dest="model_ocid", help="OCI Generative AI model OCID")
    parser.add_argument("--os-namespace", dest="os_namespace", help="OCI Object Storage namespace")
    parser.add_argument("--os-bucket", dest="os_bucket", help="OCI Object Storage bucket name")
    parser.add_argument("--delivery-prefix", dest="delivery_prefix", help="Delivery object prefix")
    parser.add_argument("--compartment-id", dest="compartment_id", help="OCI compartment OCID")
    parser.add_argument("--caption-endpoint", dest="caption_endpoint", help="Caption model endpoint URL")
    parser.add_argument("--damage-endpoint", dest="damage_endpoint", help="Damage model endpoint URL")
    parser.add_argument("--geocoding-endpoint", dest="geocoding_endpoint", help="Geocoding API endpoint")
    parser.add_argument("--max-distance", dest="max_distance", type=float, help="Max geolocation tolerance in meters")
    parser.add_argument("--weight-timeliness", dest="weight_timeliness", type=float, help="Timeliness weight")
    parser.add_argument("--weight-location", dest="weight_location", type=float, help="Location accuracy weight")
    parser.add_argument("--weight-damage", dest="weight_damage", type=float, help="Damage weight")
    parser.add_argument("--local-asset-root", dest="local_asset_root", help="Local directory for offline assets")

    return parser.parse_args(argv)


def main(argv: Any | None = None) -> Dict[str, Any]:
    args = parse_args(argv)
    config = _build_config(args)
    context = _build_context(args)
    llm = _build_llm(config, args)

    result = run_quality_pipeline(
        config=config,
        llm=llm,
        context=context,
        object_name=context.object_name,
    )
    print(json.dumps(result, indent=2, default=str))
    return result


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
