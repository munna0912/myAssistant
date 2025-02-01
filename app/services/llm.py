# app/services/llm.py
import requests

def query(prompt: str) -> str:
    # URL for the local LLM service (Ollama) - adjust the endpoint as required
    ollama_url = "http://127.0.0.1:11434/api/chat"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        # Assuming the response JSON contains a key "response"
        return response.json().get("response", "No response received.")
    except requests.RequestException as e:
        return f"LLM query error: {e}"
