# app/services/llm.py
from typing import List
import requests
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ReturnMeaasge(BaseModel):
    think: str
    reply: str

ollama_url = "http://127.0.0.1:11434/api/chat"

def query(messages: List[Message]) -> str:
    # URL for the local LLM service (Ollama) - adjust the endpoint as required
    payload = {
    "model": "deepseek-r1:1.5b",
    "messages": [
            {
                "role": "assistant",
                "content": "Hello, I am Camilla. I am here to help you with your learning journey, coding, and more. Also I can entertain you with some jokes. How can I help you today?"
            },
            {
                "role": "user",
                "content": "Okay, thanks for the introduction."
            }
        ],
        "stream": True
    }

    payload["messages"].extend(messages.to_dict())

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        # Assuming the response JSON contains a key "response"
        return response.json().get("response", "No response received.")
    except requests.RequestException as e:
        return f"LLM query error: {e}"
