"""LangChain chains orchestrating the OCI delivery workflow."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional

from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM

from .config import WorkflowConfig, DamageTypeWeights, SeverityScores
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
        input_variables=["metadata", "caption_json"],
        template=(
            "You are validating proof-of-delivery photos. Given the delivery metadata\n"
            "{metadata}\nand the automated scene analysis\n{caption_json}\n"
            "Summarize the delivery scene in 2 sentences highlighting:\n"
            "- Package visibility and location\n"
            "- Safety and security concerns\n"
            "- Environmental conditions\n"
            "Be concise and focus on delivery quality assessment."
        ),
    )
    return LLMChain(prompt=prompt, llm=llm, output_key="caption_summary")


def compute_location_accuracy(exif: Mapping[str, Any], context: DeliveryContext, max_distance_meters: float) -> float:
    gps_info = exif.get("GPSInfo", {})
    if not gps_info:
        return 0.0
    lat = gps_info.get("latitude")
    lon = gps_info.get("longitude")
    if lat is None or lon is None:
        return 0.0

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
    return round(max(0.0, 1 - min(delay, 4) / 4), 3)


def compute_damage_score(damage_report: Mapping[str, Any], config: Optional[WorkflowConfig] = None) -> float:
    """Compute damage score from structured damage report JSON."""
    
    # MVP: If weighted scoring is enabled and we have indicators, use weighted calculation
    if (config and 
        config.damage_scoring.use_weighted_scoring and 
        damage_report.get("indicators")):
        
        return _compute_weighted_damage_score(damage_report, config.damage_scoring.type_weights, config.damage_scoring.severity_scores)
    
    # Fallback to original logic
    if isinstance(damage_report.get("overall"), dict):
        score = damage_report["overall"].get("score", 0.0)
        # Score is damage probability, so quality = 1 - damage
        return round(max(0.0, 1 - float(score)), 3)
    # Fallback: old format with "damage" key
    damage_prob = damage_report.get("damage", 0.0)
    return round(max(0.0, 1 - damage_prob), 3)


def _compute_weighted_damage_score(damage_report: Mapping[str, Any], type_weights: DamageTypeWeights, severity_scores: SeverityScores) -> float:
    """MVP: Compute weighted damage score from individual indicators."""
    
    indicators = damage_report.get("indicators", {})
    if not indicators:
        return 1.0  # No damage indicators = perfect quality
    
    # Get normalized weights
    weights = type_weights.normalized()
    
    # Convert severity to numeric score using configurable values
    def severity_to_score(severity: str) -> float:
        severity_map = {
            "none": severity_scores.none,
            "minor": severity_scores.minor,
            "moderate": severity_scores.moderate,
            "severe": severity_scores.severe
        }
        return severity_map.get(severity, 0.0)
    
    # Calculate weighted average of present damage indicators
    total_weighted_score = 0.0
    total_weight = 0.0
    
    for indicator_name, indicator_data in indicators.items():
        if indicator_data.get("present", False):
            severity = indicator_data.get("severity", "none")
            score = severity_to_score(severity)
            weight = weights.get(indicator_name, 0.0)
            
            total_weighted_score += score * weight
            total_weight += weight
    
    if total_weight == 0:
        return 1.0  # No active damage indicators
    
    # Calculate weighted average damage score
    weighted_damage_score = total_weighted_score / total_weight
    
    # Convert to quality score (1 - damage) and round to avoid precision errors
    return round(max(0.0, 1.0 - weighted_damage_score), 3)


def compute_quality_index(
    *,
    context: DeliveryContext,
    exif: Mapping[str, Any],
    damage_report: Mapping[str, Any],
    weights: Mapping[str, float],
    max_distance_meters: float,
    config: Optional[WorkflowConfig] = None,
) -> Dict[str, float]:
    location_accuracy = compute_location_accuracy(exif, context, max_distance_meters=max_distance_meters)
    timeliness = compute_timeliness_score(context)
    damage = compute_damage_score(damage_report, config)

    quality_index = round(
        weights["location_accuracy"] * location_accuracy
        + weights["timeliness"] * timeliness
        + weights["damage_score"] * damage, 3
    )
    return {
        "location_accuracy": round(location_accuracy, 3),
        "timeliness": timeliness,
        "package_quality": damage,  # Clear: this is quality score (0-1, higher is better)
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
            "'issues' (list of strings), and 'insights' (string).\n"
            "Output ONLY raw JSON (no code fences, no markdown, no extra commentary)."
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
    
    # Get structured caption JSON (do this first to provide context)
    caption_json = tools["caption"].run(encoded_payload)
    caption_dict = json.loads(caption_json)
    
    caption_summary = build_caption_chain(llm).invoke(
        {
            "metadata": json.dumps(retrieval_output["metadata"]),
            "caption_json": caption_json,
        }
    )["caption_summary"]
    
    # Get structured damage report JSON with caption context for consistency
    damage_report = json.loads(tools["damage"].run(
        encoded_payload,  # First positional argument
        caption_context=caption_json  # Pass caption results as context
    ))

    weights = config.quality_weights.normalized()
    quality_metrics = compute_quality_index(
        context=context,
        exif=exif_raw,
        damage_report=damage_report,
        weights=weights,
        max_distance_meters=config.geolocation.max_distance_meters,
        config=config,
    )

    workflow_chain = build_workflow_chain(config, llm)
    assessment = workflow_chain.invoke(
        {
            "metadata": json.dumps(retrieval_output["metadata"]),
            "caption_summary": caption_summary,
            "quality_metrics": json.dumps(quality_metrics),
        }
    )["agent_assessment"]
    assessment_clean = assessment.strip()
    if assessment_clean.startswith("```"):
        lines = [
            line for line in assessment_clean.splitlines()
            if not line.strip().startswith("```")
        ]
        assessment_clean = "\n".join(lines).strip()
    try:
        assessment_payload = json.loads(assessment_clean)
    except json.JSONDecodeError:
        assessment_payload = {
            "status": "Review",
            "issues": ["LLM returned non-JSON response"],
            "insights": assessment,
        }

    return {
        "metadata": retrieval_output["metadata"],
        "exif": exif_raw,
        "caption_json": caption_dict,  # Already parsed above
        "caption_summary": caption_summary,
        "damage_report": damage_report,
        "quality_metrics": quality_metrics,
        "assessment": assessment_payload,
    }
