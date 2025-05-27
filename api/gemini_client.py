"""Gemini API client for EduBot."""

import requests
from typing import Dict, Any, List, Optional
from config.settings import Config

class GeminiAPI:
    """Gemini API client for generating responses."""
    
    def __init__(self, api_key: str) -> None:
        """Initialize the Gemini API client."""
        self.api_key = api_key
        self.base_url = Config.GEMINI_BASE_URL
    
    def generate_response(self, messages: List[Dict[str, str]], model: str = None,
                         max_tokens: int = None, temperature: float = None, 
                         image_data: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from Gemini API with optional image support."""
        
        # Use defaults from config if not provided
        model = model or Config.DEFAULT_MODEL
        max_tokens = max_tokens or Config.DEFAULT_MAX_TOKENS
        temperature = temperature or Config.DEFAULT_TEMPERATURE
        
        url = f"{self.base_url}/{model}:generateContent"
        params = {"key": self.api_key}
        
        # Convert messages to Gemini format
        contents = self._convert_messages_to_gemini_format(messages, image_data)
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 64
            },
            "safetySettings": Config.SAFETY_SETTINGS
        }
        
        try:
            response = requests.post(url, params=params, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return self._process_response(data)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _convert_messages_to_gemini_format(self, messages: List[Dict[str, str]], 
                                         image_data: Optional[str] = None) -> List[Dict]:
        """Convert messages to Gemini API format."""
        contents = []
        
        for msg in messages:
            role = "user" if msg['role'] == 'user' else "model"
            
            # Handle messages with images
            if image_data and msg['role'] == 'user' and msg == messages[-1]:
                contents.append({
                    "role": role,
                    "parts": [
                        {"text": msg['content']},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                })
            else:
                contents.append({
                    "role": role,
                    "parts": [{"text": msg['content']}]
                })
        
        return contents
    
    def _process_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the API response."""
        if 'candidates' not in data or not data['candidates']:
            return {"success": False, "error": "No response generated"}
        
        candidate = data['candidates'][0]
        
        if candidate.get('finishReason') == 'SAFETY':
            return {"success": False, "error": "Response blocked by safety filters"}
        
        if 'content' in candidate and 'parts' in candidate['content']:
            answer = candidate['content']['parts'][0].get('text', '')
            return {
                "success": True,
                "answer": answer,
                "usage": data.get('usageMetadata', {})
            }
        else:
            return {"success": False, "error": "Unexpected response format"}