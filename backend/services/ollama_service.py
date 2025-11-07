import httpx
import json
import base64
from typing import Optional, Dict, List
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2", vision_model: Optional[str] = None):
        self.base_url = base_url
        self.model = model
        self.vision_model = vision_model or os.getenv("OLLAMA_VISION_MODEL", "llava")
        self.conversations: Dict[str, list] = {}
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
    
    async def chat(
        self,
        user_message: str,
        context: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, str]:
        """Send a chat message to Ollama with optional context"""
        
        # Build system prompt with context if provided
        if context and context.strip():
            # Strict mode: Only answer from provided context
            system_prompt = """You are a helpful AI assistant that ONLY answers questions based on the provided context documents. 

CRITICAL RULES:
1. You MUST ONLY use information from the provided context to answer questions.
2. If the question cannot be answered using the provided context, you MUST respond with: "I can only answer questions based on the documents provided. The information needed to answer this question is not available in the provided documents."
3. Do NOT use any knowledge outside of the provided context.
4. Do NOT make up information or infer beyond what is explicitly stated in the context.
5. If the context is empty or doesn't contain relevant information, clearly state that you cannot answer the question.

Provided context:
{context}

Remember: Only answer if the information is in the context above. Otherwise, politely decline.""".format(context=context)
        else:
            # No context available - refuse to answer
            system_prompt = """You are a helpful AI assistant, but you can ONLY answer questions based on documents that have been provided. 

Since no relevant documents are available, you must respond with: "I can only answer questions based on the documents provided. No relevant documents are available to answer this question. Please upload relevant documents first."

Do NOT attempt to answer questions without document context."""
        
        # Get or create conversation history
        if conversation_id and conversation_id in self.conversations:
            messages = self.conversations[conversation_id]
        else:
            conversation_id = conversation_id or f"conv_{len(self.conversations)}"
            messages = []
            self.conversations[conversation_id] = messages
        
        # Add system message if this is a new conversation
        if not messages:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare request
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract assistant response
                assistant_message = result.get("message", {}).get("content", "")
                
                # Add assistant response to conversation history
                messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                return {
                    "message": assistant_message,
                    "conversation_id": conversation_id
                }
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def get_available_models(self) -> list:
        """Get list of available Ollama models"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except:
            return []
    
    def check_vision_model_available(self) -> bool:
        """Check if vision model is available"""
        available_models = self.get_available_models()
        return any(self.vision_model in model for model in available_models)
    
    async def describe_image(self, image_path: Path, prompt: Optional[str] = None) -> str:
        """Use vision model to describe an image
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt (default: detailed description prompt)
        
        Returns:
            Description of the image as text
        """
        if not image_path.exists():
            return ""
        
        # Read and encode image
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Default prompt for technical drawings
        default_prompt = """Describe this image in detail, focusing on:
- All visible text, labels, dimensions, and annotations
- The type of drawing or diagram (technical drawing, schematic, blueprint, etc.)
- Key components, parts, or elements shown
- Relationships between elements if visible
- Any measurements, specifications, or technical details
- The overall purpose or context of what is shown

Provide a comprehensive description that would help someone understand what is in this image."""
        
        user_prompt = prompt or default_prompt
        
        # Prepare message with image
        messages = [
            {
                "role": "user",
                "content": user_prompt,
                "images": [image_base64]
            }
        ]
        
        payload = {
            "model": self.vision_model,
            "messages": messages,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:  # Longer timeout for vision
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                description = result.get("message", {}).get("content", "")
                return description
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to Ollama vision model: {str(e)}")
        except Exception as e:
            raise Exception(f"Error describing image: {str(e)}")
    
    async def describe_images_batch(self, image_paths: List[Path], prompt: Optional[str] = None) -> List[str]:
        """Describe multiple images (processes sequentially to avoid overwhelming the model)"""
        descriptions = []
        for i, image_path in enumerate(image_paths):
            try:
                print(f"Describing image {i+1}/{len(image_paths)}: {image_path.name}")
                description = await self.describe_image(image_path, prompt)
                descriptions.append(description)
            except Exception as e:
                print(f"Error describing {image_path.name}: {str(e)}")
                descriptions.append("")  # Empty description on error
        return descriptions

