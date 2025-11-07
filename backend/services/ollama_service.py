import httpx
import json
from typing import Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
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
        system_prompt = "You are a helpful AI assistant."
        if context:
            system_prompt += f"\n\nUse the following context to answer questions:\n\n{context}\n\nIf the context doesn't contain relevant information, say so."
        
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

