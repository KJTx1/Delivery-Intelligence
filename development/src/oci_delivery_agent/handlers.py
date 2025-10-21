"""OCI Function handler orchestrating the delivery quality workflow."""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict

# from langchain.llms import OCIModel  # Commented out due to version compatibility

from .chains import DeliveryContext, run_quality_pipeline
from .config import (
    DamageScoringConfig,
    DamageTypeWeights,
    GeolocationConfig,
    ObjectStorageConfig,
    QualityIndexWeights,
    SeverityScores,
    VisionConfig,
    WorkflowConfig,
)


def load_config() -> WorkflowConfig:
    return WorkflowConfig(
        object_storage=ObjectStorageConfig(
            namespace=os.environ.get("OCI_OS_NAMESPACE", ""),
            bucket_name=os.environ.get("OCI_OS_BUCKET", ""),
            delivery_prefix=os.environ.get("DELIVERY_PREFIX", ""),
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
        damage_scoring=DamageScoringConfig(
            none_max=float(os.environ.get("DAMAGE_SCORE_NONE_MAX", "0.1")),
            minor_min=float(os.environ.get("DAMAGE_SCORE_MINOR_MIN", "0.3")),
            minor_max=float(os.environ.get("DAMAGE_SCORE_MINOR_MAX", "0.4")),
            moderate_min=float(os.environ.get("DAMAGE_SCORE_MODERATE_MIN", "0.6")),
            moderate_max=float(os.environ.get("DAMAGE_SCORE_MODERATE_MAX", "0.7")),
            severe_min=float(os.environ.get("DAMAGE_SCORE_SEVERE_MIN", "0.9")),
            use_weighted_scoring=os.environ.get("DAMAGE_USE_WEIGHTED_SCORING", "true").lower() == "true",
            type_weights=DamageTypeWeights(
                leakage=float(os.environ.get("DAMAGE_WEIGHT_LEAKAGE", "0.4")),
                box_deformation=float(os.environ.get("DAMAGE_WEIGHT_BOX_DEFORMATION", "0.3")),
                packaging_integrity=float(os.environ.get("DAMAGE_WEIGHT_PACKAGING_INTEGRITY", "0.2")),
                corner_damage=float(os.environ.get("DAMAGE_WEIGHT_CORNER_DAMAGE", "0.1")),
            ),
            severity_scores=SeverityScores(
                none=float(os.environ.get("SEVERITY_SCORE_NONE", "0.05")),
                minor=float(os.environ.get("SEVERITY_SCORE_MINOR", "0.35")),
                moderate=float(os.environ.get("SEVERITY_SCORE_MODERATE", "0.65")),
                severe=float(os.environ.get("SEVERITY_SCORE_SEVERE", "0.9")),
            ),
        ),
        notification_topic_id=os.environ.get("NOTIFICATION_TOPIC_ID"),
        database_table=os.environ.get("QUALITY_TABLE", "delivery_quality_events"),
        local_asset_root=os.environ.get("LOCAL_ASSET_ROOT"),
    )


def build_llm(config: WorkflowConfig) -> OCIModel:
    """Build OCI Generative AI client for chat API"""
    import oci
    from oci.generative_ai_inference import GenerativeAiInferenceClient
    
    # Get configuration from environment
    hostname = os.environ.get("OCI_GENAI_HOSTNAME")
    model_ocid = os.environ.get("OCI_TEXT_MODEL_OCID")
    compartment_id = os.environ.get("OCI_COMPARTMENT_ID")
    
    if not hostname:
        raise ValueError("OCI_GENAI_HOSTNAME must be set")
    
    if not model_ocid:
        print("Warning: OCI_TEXT_MODEL_OCID not set, using placeholder")
        model_ocid = "ocid1.test.oc1..<unique_ID>EXAMPLE-modelId-Value"
    
    if not compartment_id:
        raise ValueError("OCI_COMPARTMENT_ID must be set")
    
    # Remove endpoint path if included in hostname
    if '/20231130/actions/generateText' in hostname:
        hostname = hostname.replace('/20231130/actions/generateText', '')
    
    # Load OCI configuration with error handling
    try:
        oci_config = oci.config.from_file()
    except Exception as config_error:
        print(f"Warning: Could not load OCI config file: {config_error}")
        # Try environment variables as fallback
        try:
            oci_config = oci.config.from_file("~/.oci/config")
        except Exception as fallback_error:
            raise ValueError(f"Could not load OCI configuration: {config_error}, {fallback_error}")
    
    # Initialize Generative AI client
    try:
        client = GenerativeAiInferenceClient(
            config=oci_config,
            service_endpoint=hostname,
            retry_strategy=oci.retry.NoneRetryStrategy(),
            timeout=(10, 240)
        )
    except Exception as client_error:
        raise RuntimeError(f"Failed to initialize OCI Generative AI client: {client_error}")
    
    # Create custom LLM wrapper for OCI GenAI chat API
    from langchain_core.language_models import BaseLLM
    from langchain_core.callbacks import CallbackManagerForLLMRun
    from typing import Any, List, Optional
    
    class OCIGenAIModel(BaseLLM):
        client: Any = None
        model_ocid: str = ""
        compartment_id: str = ""
        
        def __init__(self, client, model_ocid, compartment_id):
            super().__init__(
                client=client,
                model_ocid=model_ocid,
                compartment_id=compartment_id
            )
        
        @property
        def _llm_type(self) -> str:
            return "oci_genai"
        
        def _generate(
            self,
            prompts: List[str],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> Any:
            """Generate responses for multiple prompts."""
            from langchain_core.outputs import LLMResult, Generation
            generations = []
            for prompt in prompts:
                text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
                generations.append([Generation(text=text)])
            return LLMResult(generations=generations)
        
        def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> str:
            """Generate text using OCI GenAI chat API"""
            try:
                # Create content and message
                content = oci.generative_ai_inference.models.TextContent()
                content.text = prompt
                
                message = oci.generative_ai_inference.models.Message()
                message.role = "USER"
                message.content = [content]
                
                # Create chat request
                chat_request = oci.generative_ai_inference.models.GenericChatRequest()
                chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
                chat_request.messages = [message]
                chat_request.max_tokens = kwargs.get('max_tokens', 300)
                chat_request.temperature = kwargs.get('temperature', 0.7)
                chat_request.frequency_penalty = kwargs.get('frequency_penalty', 0)
                chat_request.presence_penalty = kwargs.get('presence_penalty', 0)
                chat_request.top_p = kwargs.get('top_p', 0.75)
                
                # Create serving mode with endpoint ID
                serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
                    endpoint_id=self.model_ocid
                )
                
                # Create chat details
                chat_detail = oci.generative_ai_inference.models.ChatDetails()
                chat_detail.serving_mode = serving_mode
                chat_detail.chat_request = chat_request
                chat_detail.compartment_id = self.compartment_id
                
                # Call the chat API
                response = self.client.chat(chat_detail)
                
                # Extract text from response
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
                    return response.data.chat_response.choices[0].message.content[0].text
                else:
                    return "Error: No response generated"
                    
            except Exception as e:
                return f"Error generating text: {str(e)}"
    
    return OCIGenAIModel(client, model_ocid, compartment_id)


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
