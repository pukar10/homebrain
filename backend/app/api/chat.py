"""
app/api/chat.py
"""
import json
import logging
import time
from typing import AsyncIterator
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.api.deps import get_graph
from app.schemas.api import ChatRequest
from app.schemas.events import StreamEvent, TokenEvent, DoneEvent, ErrorEvent
from app.services.chat import chat_turn_stream


log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "homebrain-backend",
    }


def sse(event: StreamEvent) -> str:
    payload = event.model_dump()
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest, request: Request, graph=Depends(get_graph)) -> StreamingResponse:
    thread_id, event_gen = chat_turn_stream(graph, chat_request.thread_id, chat_request.message)
    log.info("chat stream start", extra={"thread_id": thread_id, "msg_len": len(chat_request.message)})

    async def event_stream() -> AsyncIterator[str]:
        last_ping = time.monotonic()
        try:
            for event in event_gen:
                if await request.is_disconnected():
                    log.info("SSE client disconnected", extra={"thread_id": thread_id})
                    break
                yield sse(event)
                
            # Heartbeat useless make async and move outside loop
            now = time.monotonic()
            if now - last_ping > 15:
                last_ping = now
                yield ": ping\n\n"
        except Exception:
            log.exception("SSE stream failed", extra={"thread_id": thread_id})
            yield sse(ErrorEvent(message="stream failed", thread_id=thread_id))

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }

    return StreamingResponse(event_stream(), media_type="text/event-stream", headers=headers)