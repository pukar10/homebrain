from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse, ChatMessage
from app.services.chat import generate_response


# Define API router
router = APIRouter(prefix="/api", tags=["chat"])


# Health check endpoint
@router.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "homebrain-backend",
    }



# Chat endpoint
@router.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    history = req.history or []

    reply, new_history = generate_response(history, req.message)

    return ChatResponse(reply=reply, history=new_history)
