import runpod
import requests
import time

FASTAPI_URL = "http://127.0.0.1:8000/generate"

# Wait for FastAPI to be ready
def wait_for_fastapi():
    for _ in range(10):  # Try for 10 attempts (50 seconds max)
        try:
            response = requests.get("http://127.0.0.1:8000/")
            if response.status_code == 200:
                print("✅ FastAPI is running!")
                return
        except requests.exceptions.RequestException:
            pass
        print("⏳ Waiting for FastAPI to start...")
        time.sleep(5)  # Wait 5 seconds before retrying

wait_for_fastapi()

def handler(event):
    input_data = event["input"]

    payload = {
        "prompt": input_data.get("prompt", "Default prompt"),
        "max_tokens": input_data.get("max_tokens", 200),
        "temperature": input_data.get("temperature", 1.0),
        "top_p": input_data.get("top_p", 0.9),
    }
    
    try:
        response = requests.post(FASTAPI_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})
