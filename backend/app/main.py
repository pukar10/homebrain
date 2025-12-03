from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
from typing import Literal, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


# Load env vars
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY is not set, Check your .env file.")

# Create Gemini client & model
geminiClient = genai.Client(api_key=gemini_api_key)
MODEL_NAME = "gemini-2.5-flash"

# Initialize FastAPI app
app = FastAPI()


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessage]


### Health check endpoint ###
@app.get("/api/health")
def health():
    return {"status": "ok", 
            "service": "homebrain-backend",
            "llm": MODEL_NAME,
            }


### Chat endpoint ###
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message.strip()

    # Handle empty message
    if not user_message:
        return ChatResponse(reply="You sent an empty message.")

    # Dumb response logic
    if "proxmox" in user_message.lower():
        return ChatResponse(
            reply="I can't talk to Proxmox yet, but soon I'll query your cluster status."
        )

    # Main LLM interaction
    try:
        response = geminiClient.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
        )
    
        return ChatResponse(reply=response.text)
    except Exception as e:
        print(f"LLM error: {e}")
        raise HTTPException(status_code=500, detail="LLM call failed")
