import runpod
import requests

# Your FastAPI server URL (inside RunPod)
FASTAPI_URL = "http://127.0.0.1:8000/generate"

def handler(event):
    input_data = event["input"]

    # Prepare request payload
    payload = {
        "prompt": input_data.get("prompt", "Default prompt"),
        "max_tokens": input_data.get("max_tokens", 200),
        "temperature": input_data.get("temperature", 1.0),
        "top_p": input_data.get("top_p", 0.9),
    }
    
    try:
        # Send request to FastAPI
        response = requests.post(FASTAPI_URL, json=payload)
        response.raise_for_status()
        return response.json()  # Return FastAPI response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
