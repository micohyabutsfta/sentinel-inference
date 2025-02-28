from fastapi import FastAPI
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download

app = FastAPI()

# Load model from Hugging Face
repo_id = "micohyabutsfta/Sentinel-2.0"
model_path = snapshot_download(repo_id)  # Downloads the model files locally

model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

@app.post("/generate")
async def generate(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
