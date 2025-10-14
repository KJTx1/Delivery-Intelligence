"""LangChain chains orchestrating the OCI delivery workflow."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Mapping

from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM

from .config import WorkflowConfig
from .tools import toolset


@dataclass
class DeliveryContext:
    """Shared context across the workflow stages."""

    object_name: str
    expected_latitude: float
    expected_longitude: float
    promised_time_utc: datetime
    delivered_time_utc: datetime


def build_caption_chain(llm: BaseLLM) -> LLMChain:
    prompt = PromptTemplate(
        input_variables=["metadata", "caption"],
        template=(
            "You are validating proof-of-delivery photos. Given the delivery metadata\n"
            "{metadata}\nand the automated caption {caption}, summarize the scene in 2 sentences"
            " highlighting delivery location cues."
        ),
    )
    return LLMChain(prompt=prompt, llm=llm, output_key="caption_summary")


def compute_location_accuracy(exif: Mapping[str, Any], context: DeliveryContext, max_distance_meters: float) -> float:
    gps_info = exif.get("GPSInfo", {})
    if not gps_info:
        return 0.0

    def _convert_to_degrees(values: List[Any]) -> float:
        deg, minutes, seconds = values
        return deg[0] / deg[1] + minutes[0] / minutes[1] / 60 + seconds[0] / seconds[1] / 3600

    lat = _convert_to_degrees(gps_info["GPSLatitude"])
    lon = _convert_to_degrees(gps_info["GPSLongitude"])
    if gps_info.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps_info.get("GPSLongitudeRef") == "W":
        lon = -lon

    # Basic Haversine implementation
    from math import asin, cos, radians, sin, sqrt

    d_lat = radians(lat - context.expected_latitude)
    d_lon = radians(lon - context.expected_longitude)
    a = sin(d_lat / 2) ** 2 + cos(radians(context.expected_latitude)) * cos(radians(lat)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    earth_radius_m = 6371000
    distance = earth_radius_m * c
    return max(0.0, 1 - min(distance, max_distance_meters) / max_distance_meters)


def compute_timeliness_score(context: DeliveryContext) -> float:
    if context.delivered_time_utc <= context.promised_time_utc:
        return 1.0
    delay = (context.delivered_time_utc - context.promised_time_utc).total_seconds() / 3600
    return max(0.0, 1 - min(delay, 4) / 4)


def compute_damage_score(damage_predictions: Mapping[str, float]) -> float:
    damage_prob = damage_predictions.get("damage", 0.0)
    return max(0.0, 1 - damage_prob)


def compute_quality_index(
    *,
    context: DeliveryContext,
    exif: Mapping[str, Any],
    damage_predictions: Mapping[str, float],
    weights: Mapping[str, float],
    max_distance_meters: float,
) -> Dict[str, float]:
    location_accuracy = compute_location_accuracy(exif, context, max_distance_meters=max_distance_meters)
    timeliness = compute_timeliness_score(context)
    damage = compute_damage_score(damage_predictions)

    quality_index = (
        weights["location_accuracy"] * location_accuracy
        + weights["timeliness"] * timeliness
        + weights["damage_score"] * damage
    )
    return {
        "location_accuracy": location_accuracy,
        "timeliness": timeliness,
        "damage": damage,
        "quality_index": quality_index,
    }


def build_workflow_chain(config: WorkflowConfig, llm: BaseLLM) -> SequentialChain:
    prompt = PromptTemplate(
        input_variables=["metadata", "caption_summary", "quality_metrics"],
        template=(
            "Review the delivery metadata: {metadata}.\n"
            "Caption summary: {caption_summary}.\n"
            "Quality metrics: {quality_metrics}.\n"
            "Respond with a JSON object containing keys 'status' (OK or Review),\n"
            "'issues' (list of strings), and 'insights' (string)."
        ),
    )
    review_chain = LLMChain(prompt=prompt, llm=llm, output_key="agent_assessment")

    return SequentialChain(
        chains=[review_chain],
        input_variables=["metadata", "caption_summary", "quality_metrics"],
        output_variables=["agent_assessment"],
        verbose=True,
    )


def run_quality_pipeline(
    config: WorkflowConfig,
    llm: BaseLLM,
    context: DeliveryContext,
    object_name: str,
) -> Dict[str, Any]:
    tools = toolset(config)

    retrieval_output = json.loads(tools["retrieval"].run(object_name))
    encoded_payload = retrieval_output["payload"]

    exif_raw = json.loads(tools["exif"].run(encoded_payload))
    caption_summary = build_caption_chain(llm).run(
        metadata=json.dumps(retrieval_output["metadata"]),
        caption=tools["caption"].run(encoded_payload),
    )
    damage_predictions = json.loads(tools["damage"].run(encoded_payload))

    weights = config.quality_weights.normalized()
    quality_metrics = compute_quality_index(
        context=context,
        exif=exif_raw,
        damage_predictions=damage_predictions,
        weights=weights,
        max_distance_meters=config.geolocation.max_distance_meters,
    )

    workflow_chain = build_workflow_chain(config, llm)
    assessment = workflow_chain.run(
        metadata=json.dumps(retrieval_output["metadata"]),
        caption_summary=caption_summary,
        quality_metrics=json.dumps(quality_metrics),
    )
    try:
        assessment_payload = json.loads(assessment)
    except json.JSONDecodeError:
        assessment_payload = {
            "status": "Review",
            "issues": ["LLM returned non-JSON response"],
            "insights": assessment,
        }

    return {
        "metadata": retrieval_output["metadata"],
        "exif": exif_raw,
        "caption_summary": caption_summary,
        "damage_predictions": damage_predictions,
        "quality_metrics": quality_metrics,
        "assessment": assessment_payload,
    }
