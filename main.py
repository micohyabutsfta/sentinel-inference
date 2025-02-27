from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Llama.cpp endpoint
LLM_ENDPOINT = "https://j23fwcijsc3m3e-5000.proxy.runpod.net/v1/completions"
# LLM_ENDPOINT = "https://j23fwcijsc3m3e-8080.proxy.runpod.net/v1/completions"

# Define the Pydantic model for the request body
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 1.0
    top_p: float = 0.9

@app.get("/")
def home():
    return {"message": "Sentinel API is running!"}

@app.post("/generate")
async def generate_response(request: GenerateRequest):
    payload = {
        "prompt": request.prompt,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(LLM_ENDPOINT, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        result = response.json()
        return {"response": result["choices"][0]["text"]}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
