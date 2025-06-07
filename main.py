import spacy
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# --- Setup ---
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="PrivChat Backend API")
nlp = spacy.load("en_core_web_sm")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Schema ---
class PromptRequest(BaseModel):
    prompt: str

# --- Endpoint ---
@app.post("/process")
async def process_prompt(request: PromptRequest):
    prompt_text = request.prompt
    logging.info(f"Received prompt: {prompt_text}")

    # Step 1: spaCy NER
    doc = nlp(prompt_text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    print("\n--- Detected Named Entities ---")
    print(entities)
    print("---------------------------------")

    # Step 2: Send prompt to local LLM (Ollama)
    ollama_url = "http://localhost:11434/api/generate"
    try:
        response = requests.post(
            ollama_url,
            json={"model": "llama3", "prompt": prompt_text, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        llm_response_text = response.json().get("response", "No response.")
    except Exception as e:
        llm_response_text = f"Error talking to Ollama: {e}"

    print("\n--- LLM Response ---")
    print(llm_response_text)
    print("--------------------\n")

    return {"entities": entities, "llm_response": llm_response_text}
