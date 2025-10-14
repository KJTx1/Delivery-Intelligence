#!/usr/bin/env python3
"""
Test OCI GenAI Vision using the exact structure from OCI console
"""

import os
import sys
import json
import base64
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_console_vision():
    """Test Vision using the exact OCI console structure"""
    print("👁️  Testing OCI GenAI Vision with Console Structure")
    print("=" * 60)
    
    try:
        # Load environment
        load_dotenv('.env')
        
        # Check if local image exists
        local_image_path = "/Users/zhizhyan/Desktop/Codex/local_assets/deliveries/sample.jpg"
        if not os.path.exists(local_image_path):
            print(f"❌ Local image not found: {local_image_path}")
            return False
        
        print(f"✅ Found local image: {local_image_path}")
        
        # Read and encode the image
        with open(local_image_path, 'rb') as f:
            image_data = f.read()
        
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        print(f"✅ Image encoded: {len(encoded_image)} characters")
        
        # Get configuration
        hostname = os.environ.get('OCI_GENAI_HOSTNAME')
        model_ocid = os.environ.get('OCI_TEXT_MODEL_OCID')
        compartment_id = os.environ.get('OCI_COMPARTMENT_ID')
        
        # Remove endpoint path if included in hostname
        if '/20231130/actions/generateText' in hostname:
            hostname = hostname.replace('/20231130/actions/generateText', '')
        
        # Import OCI modules
        import oci
        from oci.generative_ai_inference import GenerativeAiInferenceClient
        
        # Load OCI config
        print("📋 Loading OCI configuration...")
        oci_config = oci.config.from_file()
        print("✅ OCI config loaded")
        
        # Initialize client
        print("🔧 Initializing GenAI client...")
        client = GenerativeAiInferenceClient(
            config=oci_config,
            service_endpoint=hostname,
            retry_strategy=oci.retry.NoneRetryStrategy(),
            timeout=(10, 240)
        )
        print("✅ GenAI client initialized")
        
        # Test Vision with exact console structure
        print("👁️  Testing Vision with Console Structure...")
        
        # Create text content
        text_content = oci.generative_ai_inference.models.TextContent()
        text_content.text = "as an agent for delivery assurance, describe the delivery pic and ideally see where the package is placed and its condition."
        
        # Create image content using the console structure
        # Note: We need to use ImageUrl instead of ImageContent
        try:
            # Try to create ImageUrl structure
            image_url = oci.generative_ai_inference.models.ImageUrl()
            image_url.url = f"data:image/jpeg;base64,{encoded_image}"
            
            # Create image content with ImageUrl
            image_content = oci.generative_ai_inference.models.ImageContent()
            image_content.image_url = image_url
            
        except Exception as e:
            print(f"⚠️  ImageUrl structure not available: {e}")
            # Fallback to source method
            image_content = oci.generative_ai_inference.models.ImageContent()
            image_content.source = f"data:image/jpeg;base64,{encoded_image}"
        
        # Create message with both text and image content
        message = oci.generative_ai_inference.models.Message()
        message.role = "USER"
        message.content = [text_content, image_content]  # Both text and image
        
        # Create chat request with console structure
        chat_request = oci.generative_ai_inference.models.GenericChatRequest()
        chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
        chat_request.messages = [message]
        chat_request.max_tokens = 600
        chat_request.temperature = 1
        chat_request.frequency_penalty = 0
        chat_request.presence_penalty = 0
        chat_request.top_p = 0.75
        chat_request.top_k = -1
        chat_request.is_stream = False
        
        # Create serving mode with endpoint ID (using console structure)
        serving_mode = oci.generative_ai_inference.models.DedicatedServingMode(
            endpoint_id=model_ocid
        )
        
        # Create chat details
        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_detail.serving_mode = serving_mode
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = compartment_id
        
        # Call the chat API
        print("🚀 Calling OCI GenAI chat API with console structure...")
        response = client.chat(chat_detail)
        
        print("✅ Vision Analysis Response:")
        print(f"   Response type: {type(response.data)}")
        
        # Handle streaming response
        if hasattr(response.data, '__iter__'):
            print("📡 Processing streaming response...")
            full_response = ""
            
            try:
                for chunk in response.data:
                    if hasattr(chunk, 'data') and chunk.data:
                        print(f"   Chunk: {chunk.data}")
                        full_response += str(chunk.data)
                    elif hasattr(chunk, 'content') and chunk.content:
                        print(f"   Content: {chunk.content}")
                        full_response += str(chunk.content)
                    else:
                        print(f"   Raw chunk: {chunk}")
                        full_response += str(chunk)
                
                print(f"✅ Full streaming response: {full_response}")
                result = full_response
                
            except Exception as e:
                print(f"⚠️  Streaming error: {e}")
                result = str(response.data)
        else:
            print(f"   Non-streaming response: {response.data}")
            result = str(response.data)
        
        if result:
            # Check if the response indicates vision capabilities
            if "don't have the capability to visually see" in result.lower() or "can't see" in result.lower() or "don't see" in result.lower():
                print("\n⚠️  Model still indicates it cannot see images")
                print("💡 The API structure may need further adjustment")
            else:
                print("\n✅ Model appears to be analyzing the image!")
                print("🎉 Vision capabilities detected!")
        else:
            print("❌ No response generated")
            return False
        
        # Test with delivery-specific prompts
        print("\n📦 Testing delivery-specific vision analysis...")
        
        delivery_prompts = [
            "Describe the delivery scene in detail. What do you see?",
            "Where is the package placed? Is it in a safe location?",
            "What is the condition of the package? Any visible damage?",
            "Is this a successful delivery photo? What evidence supports this?",
            "Describe the environment where the package was delivered.",
            "Are there any safety concerns with this delivery?"
        ]
        
        for i, prompt in enumerate(delivery_prompts, 1):
            print(f"\n   Delivery Test {i}: {prompt}")
            
            # Update the text content
            text_content.text = prompt
            
            # Call the API
            response = client.chat(chat_detail)
            
            if (response.data and 
                hasattr(response.data, 'chat_response') and 
                response.data.chat_response and
                hasattr(response.data.chat_response, 'choices') and 
                response.data.chat_response.choices and
                len(response.data.chat_response.choices) > 0):
                
                result = response.data.chat_response.choices[0].message.content[0].text
                print(f"   Response: {result[:200]}...")
                
                # Check for vision capability indicators
                if "don't have the capability to visually see" in result.lower() or "can't see" in result.lower():
                    print("   ❌ No vision capability detected")
                else:
                    print("   ✅ Vision capability detected!")
            else:
                print("   ❌ No response")
        
        return True
        
    except Exception as e:
        print(f"❌ Console vision test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 OCI GenAI Console Vision API Test")
    print("=" * 60)
    
    success = test_console_vision()
    
    if success:
        print("\n🎉 Console vision test completed!")
        print("✅ Image content structure tested")
        print("✅ Vision capabilities explored")
    else:
        print("\n⚠️  Console vision test failed. Check your configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
