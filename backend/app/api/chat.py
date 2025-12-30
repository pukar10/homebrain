"""
app/api/chat.py

Frontend hits these endpionts to interact with Homebrain backend.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.app.schemas.api import ChatRequest, ChatResponse
from app.services.chat import chat_turn, chat_turn_stream


router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "homebrain-backend",
    }



@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    
    try:
        ai_reply, history, thread_id = chat_turn(req.thread_id, req.message)
    except HTTPException:
        raise
    except Exception as e:
        print(f"LLM error: {e!r}")
    
    return ChatResponse(
        reply=ai_reply, 
        history=history,
        thread_id=thread_id,
    )

@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    
    thread_id, token_gen = chat_turn_stream(req.thread_id, req.message)

    def event_stream():
        for chunk in token_gen:
            # SSE format; frontend can read via EventSource
            yield f"data: {chunk}\n\n"
        # Optional "done" marker that includes thread_id
        yield f"data: [DONE]|{thread_id}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )