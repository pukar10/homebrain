"""
app/services/chat.py
"""
import logging
import uuid
from typing import Generator, Tuple
from fastapi import HTTPException
from langchain_core.messages import HumanMessage
from app.workflow.utils.messages import content_to_text, thread_config

log = logging.getLogger(__name__)

def chat_turn_stream(graph, thread_id: str | None, user_msg: str) -> Tuple[str, Generator[str, None, None]]:
    """
    Initiates a chat turn in streaming mode.

    Params:
    - thread_id: Optional thread ID for the chat session.
    - user_msg: The user's message to process.
    Returns: tid, token_generator
    """
    user_msg = user_msg.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message is not allowed.")

    tid = thread_id or str(uuid.uuid4())
    config = thread_config(tid)

    log.info("chat_turn_stream start", extra={"thread_id": tid, "msg_len": len(user_msg)})

    def token_generator() -> Generator[str, None, None]:
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
                yield text

                log.info(
                    "chat_turn_stream completed",
                    extra={"thread_id": tid, "emitted_any": emitted_any},
                )

        except HTTPException:
            log.warning("chat_turn_stream HTTPException", extra={"thread_id": tid})
            raise

        except Exception:
            log.exception("chat_turn_stream failed", extra={"thread_id": tid})
            yield "\n[error] Streaming failed\n"

    return tid, token_generator()

