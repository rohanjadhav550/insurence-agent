from app.rags.insurence_chat import insurence_chat_ollama, insurence_chat_gemini
from fastapi import FastAPI
import os
import asyncio
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"response":"Hello World"}

@app.post("/api/insurance-chat")
def chat_endpoint(request: ChatRequest):
    prompt = request.prompt
    return StreamingResponse(
        insurence_chat_ollama(prompt),
        media_type="text/event-stream"
    )