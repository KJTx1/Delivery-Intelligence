"""OCI Function handler orchestrating the delivery quality workflow."""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict

from langchain.llms import OCIModel

from .chains import DeliveryContext, run_quality_pipeline
from .config import (
    GeolocationConfig,
    ObjectStorageConfig,
    QualityIndexWeights,
    VisionConfig,
    WorkflowConfig,
)


def load_config() -> WorkflowConfig:
    return WorkflowConfig(
        object_storage=ObjectStorageConfig(
            namespace=os.environ.get("OCI_OS_NAMESPACE", ""),
            bucket_name=os.environ.get("OCI_OS_BUCKET", ""),
            delivery_prefix=os.environ.get("DELIVERY_PREFIX", "deliveries/"),
        ),
        vision=VisionConfig(
            compartment_id=os.environ.get("OCI_COMPARTMENT_ID", ""),
            image_caption_model_endpoint=os.environ.get("OCI_CAPTION_ENDPOINT", ""),
            damage_detection_model_endpoint=os.environ.get("OCI_DAMAGE_ENDPOINT"),
        ),
        geolocation=GeolocationConfig(
            max_distance_meters=float(os.environ.get("MAX_DISTANCE_METERS", "50")),
            geocoding_api_endpoint=os.environ.get("GEOCODING_ENDPOINT"),
        ),
        quality_weights=QualityIndexWeights(
            timeliness=float(os.environ.get("WEIGHT_TIMELINESS", "0.3")),
            location_accuracy=float(os.environ.get("WEIGHT_LOCATION", "0.3")),
            damage_score=float(os.environ.get("WEIGHT_DAMAGE", "0.4")),
        ),
        notification_topic_id=os.environ.get("NOTIFICATION_TOPIC_ID"),
        database_table=os.environ.get("QUALITY_TABLE", "delivery_quality_events"),
        local_asset_root=os.environ.get("LOCAL_ASSET_ROOT"),
    )


def build_llm(config: WorkflowConfig) -> OCIModel:
    return OCIModel(
        compartment_id=config.vision.compartment_id,
        model_id=os.environ.get("OCI_TEXT_MODEL_OCID", ""),
    )


def handler(ctx: Any, data: bytes) -> Dict[str, Any]:
    payload = json.loads(data.decode("utf-8"))
    object_name = payload["data"]["resourceName"]
    event_time = payload["eventTime"]

    context = DeliveryContext(
        object_name=object_name,
        expected_latitude=float(payload["additionalDetails"]["expectedLatitude"]),
        expected_longitude=float(payload["additionalDetails"]["expectedLongitude"]),
        promised_time_utc=datetime.fromisoformat(payload["additionalDetails"]["promisedTime"]),
        delivered_time_utc=datetime.fromisoformat(event_time),
    )

    config = load_config()
    llm = build_llm(config)
    workflow_output = run_quality_pipeline(
        config=config,
        llm=llm,
        context=context,
        object_name=object_name,
    )

    # Persist results (placeholder for Autonomous Data Warehouse interaction)
    store_quality_event(config, workflow_output)

    # Trigger notification if assessment indicates review
    if workflow_output["assessment"].get("status") == "Review":
        trigger_alert(config, workflow_output)

    return workflow_output


def store_quality_event(config: WorkflowConfig, workflow_output: Dict[str, Any]) -> None:
    # Placeholder for database insertion logic.
    pass


def trigger_alert(config: WorkflowConfig, workflow_output: Dict[str, Any]) -> None:
    # Placeholder for Notification service call.
    pass
