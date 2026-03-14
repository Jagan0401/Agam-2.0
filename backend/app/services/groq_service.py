import requests
import json
from app.config import get_groq_key, rotate_groq_key

class GroqService:
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.1-8b-instant"

    @staticmethod
    def generate_response(prompt: str, system_message: str = "You are Agam, an AI property assistant.") -> str:
        """
        Sends a request to Groq API with automatic key rotation on 429 errors.
        """
        max_retries = 10
        for _ in range(max_retries):
            api_key = get_groq_key()
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": GroqService.MODEL,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            try:
                response = requests.post(GroqService.API_URL, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                
                if response.status_code == 429:
                    # Rate limit exceeded, rotate and retry
                    rotate_groq_key()
                    continue
                
                # Other errors
                return f"Error: {response.status_code} - {response.text}"
            
            except Exception as e:
                return f"Exception: {str(e)}"
        
        return "Critical Error: All API keys exhausted or rate limited."
