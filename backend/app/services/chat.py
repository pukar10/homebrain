"""
app/services/chat.py
"""
import logging
import uuid
from typing import Generator, Tuple
from langchain_core.messages import HumanMessage
from app.workflow.utils.messages import content_to_text, thread_config
from app.schemas.events import (
    StreamEvent,
    TokenEvent,
    DoneEvent,
    ErrorEvent,
)


log = logging.getLogger(__name__)

def chat_turn_stream(graph, thread_id: str | None, user_msg: str) -> Tuple[str, Generator[StreamEvent, None, None]]:
    tid = thread_id or str(uuid.uuid4())
    config = thread_config(tid)

    log.info("chat_turn_stream start", extra={"thread_id": tid, "msg_len": len(user_msg)})

    def token_generator() -> Generator[StreamEvent, None, None]:
        emitted_any = False
        try:
            for msg_chunk, metadata in graph.stream(
                {"messages": [HumanMessage(content=user_msg)]},
                config=config,
                stream_mode="messages",
            ):
                node = metadata.get("langgraph_node") or metadata.get("node") or "unknown"
                if node == "tools":
                    log.debug("tools node executed", extra={"thread_id": tid})

                content = getattr(msg_chunk, "content", None)
                text = content_to_text(content)
                if not text:
                    continue

                emitted_any = True
                yield TokenEvent(data=text)
            
            log.info("chat_turn_stream completed", extra={"thread_id": tid, "emitted_any": emitted_any})
            yield DoneEvent(thread_id=tid)
            return
        except Exception:
            log.exception("chat_turn_stream failed", extra={"thread_id": tid})
            yield ErrorEvent(message="stream failed", thread_id=tid)
            return
        
    return tid, token_generator()

