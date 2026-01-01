"""
app/api/chat.py
- Utilize Depends() for dependency injections like LLM clients, tool registries, tenant policy, rate limiters, checkpointers, vector store clients.
"""
import json
import logging
import time
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.api.deps import get_graph
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
async def chat_stream(chat_request: ChatRequest, request: Request, graph=Depends(get_graph)) -> StreamingResponse:
    """
    Streams chat responses using Server-Sent Events (SSE).
    - SSE events are sent as JSON payloads
    - handles client disconnection
    - Heartbeat every 15s to keep connection alive (not async)
    Params:
    - chat_request: ChatRequest object containing thread_id and message.
    - request: FastAPI Request object to check for client disconnection.
    Returns: StreamingResponse object that streams tokens as they are generated.
    """
    thread_id, token_gen = chat_turn_stream(graph, chat_request.thread_id, chat_request.message)

    log.info("chat stream start", extra={"thread_id": thread_id, "msg_len": len(chat_request.message)})

    def sse(data: dict) -> str:
        return f"data: {json.dumps(data)}\n\n"

    async def event_stream():
        disconnected = False
        last_ping = time.monotonic()
        try:
            for chunk in token_gen:
                if await request.is_disconnected():
                    disconnected = True
                    log.info("SSE client disconnected", extra={"thread_id": thread_id})
                    break
                yield sse({"type": "token", "data": chunk})

            now = time.monotonic()
            if now - last_ping > 15:
                last_ping = now
                yield ": ping\n\n"

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