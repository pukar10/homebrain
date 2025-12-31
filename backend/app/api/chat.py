"""
app/api/chat.py
"""
import json
import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.schemas.api import ChatRequest
from app.services.chat import chat_turn_stream

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "homebrain-backend",
    }


@router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest, request: Request) -> StreamingResponse:
    """
    Streams chat responses using Server-Sent Events (SSE).
    - SSE events are sent as JSON payloads
    - handles client disconnection
    Params:
    - chat_request: ChatRequest object containing thread_id and message.
    - request: FastAPI Request object to check for client disconnection.
    Returns: StreamingResponse object that streams tokens as they are generated.
    """
    thread_id, token_gen = chat_turn_stream(chat_request.thread_id, chat_request.message)

    log.info("chat stream start", extra={"thread_id": thread_id, "msg_len": len(chat_request.message)})

    def sse(data: dict) -> str:
        return f"data: {json.dumps(data)}\n\n"

    async def event_stream():
        disconnected = False
        try:
            for chunk in token_gen:
                if await request.is_disconnected():
                    disconnected = True
                    log.info("SSE client disconnected", extra={"thread_id": thread_id})
                    break
                yield sse({"type": "token", "data": chunk})

            if not disconnected:
                log.info("SSE stream completed", extra={"thread_id": thread_id})
                yield sse({"type": "done", "thread_id": thread_id})

        except HTTPException as e:
            log.warning("SSE stream HTTPException", extra={"thread_id": thread_id, "status": e.status_code})
            yield sse({"type": "error", "message": e.detail})

        except Exception:
            log.exception("SSE stream failed", extra={"thread_id": thread_id})
            yield sse({"type": "error", "message": "stream failed"})

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }

    return StreamingResponse(event_stream(), media_type="text/event-stream", headers=headers)