import asyncio
import json
import time
from typing import Any, Dict, List

import httpx
import spacy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="PrivChat PII Detection API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except OSError:
    print("❌ spaCy model not found. Please install it with:")
    print("python -m spacy download en_core_web_sm")
    raise

# Pydantic models
class ProcessRequest(BaseModel):
    prompt: str

class EntityInfo(BaseModel):
    text: str
    label: str
    start: int
    end: int
    confidence: float

class ProcessResponse(BaseModel):
    original_prompt: str
    entities: List[EntityInfo]
    sanitized_prompt: str
    llm_response: str
    processing_time: float

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2"  # Change this to your preferred model

async def detect_entities(text: str) -> List[EntityInfo]:
    """Extract named entities using spaCy NER"""
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        # Map spaCy labels to our PII categories
        confidence = 0.85 + (hash(ent.text) % 15) / 100  # Simulate confidence
        
        entities.append(EntityInfo(
            text=ent.text,
            label=ent.label_,
            start=ent.start_char,
            end=ent.end_char,
            confidence=round(confidence, 2)
        ))
    
    return entities

def sanitize_prompt(text: str, entities: List[EntityInfo]) -> str:
    """Replace detected entities with placeholders"""
    sanitized = text
    
    # Sort entities by start position (reverse order to maintain indices)
    sorted_entities = sorted(entities, key=lambda x: x.start, reverse=True)
    
    for entity in sorted_entities:
        placeholder = f"[{entity.label}]"
        start = entity.start
        end = entity.end
        sanitized = sanitized[:start] + placeholder + sanitized[end:]
    
    return sanitized

async def call_ollama_api(prompt: str) -> str:
    """Call Ollama API for LLM response"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False
            }
            
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            else:
                return f"Error calling Ollama API: {response.status_code}"
                
    except httpx.RequestError as e:
        return f"Error connecting to Ollama: {str(e)}. Make sure Ollama is running on localhost:11434"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@app.get("/")
async def read_index():
    """Serve the main HTML page"""
    return FileResponse('index.html')

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "spacy_model": "en_core_web_sm",
        "ollama_url": OLLAMA_BASE_URL
    }

@app.post("/process")
async def process_message(request: ProcessRequest):
    """Main endpoint to process messages with PII detection and LLM response"""
    start_time = time.time()
    
    try:
        print(f"\n🔄 Processing message request...")
        print(f"📝 Input prompt: {request.prompt}")
        
        # Step 1: Detect named entities
        entities = await detect_entities(request.prompt)
        print(f"\n🔍 Detected entities:")
        for entity in entities:
            print(f"  - {entity.text} ({entity.label}) - {entity.confidence*100:.1f}%")
        
        # Step 2: Sanitize prompt for LLM
        sanitized_prompt = sanitize_prompt(request.prompt, entities)
        print(f"\n🧹 Sanitized prompt: {sanitized_prompt}")
        
        # Step 3: Get LLM response
        print(f"\n🤖 Calling Ollama API...")
        llm_response = await call_ollama_api(sanitized_prompt)
        print(f"📤 LLM Response: {llm_response}")
        
        processing_time = round((time.time() - start_time) * 1000)  # Convert to milliseconds
        print(f"\n⏱️ Total processing time: {processing_time}ms")
        
        return {
            "original_prompt": request.prompt,
            "entities": [entity.dict() for entity in entities],
            "sanitized_prompt": sanitized_prompt,
            "llm_response": llm_response,
            "processing_time": processing_time
        }
        
    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_ollama_models():
    """List available Ollama models"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Could not fetch models"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PrivChat API server...")
    print("📋 Make sure you have:")
    print("   1. Ollama running on localhost:11434")
    print("   2. A model pulled (e.g., 'ollama pull llama2')")
    print("   3. spaCy model installed ('python -m spacy download en_core_web_sm')")
    
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
