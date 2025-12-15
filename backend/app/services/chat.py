"""
app/services/chat.py

"""

from typing import List, Tuple, Generator
import uuid

from fastapi import HTTPException
from langchain_core.messages import BaseMessage, HumanMessage

from backend.app.services import formatting as fmt
from app.core.graph import graph
from backend.app.models.schema import ChatMessage


######################################
#  Core                              #
######################################

def chat_turn(thread_id: str | None, user_msg: str) -> Tuple[str, List[ChatMessage], str]:
    """
    Single non-streaming chat turn.
    Returns (ai_reply, new_history, tid)
    """

    user_msg = user_msg.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message is not allowed.")

    # Ensure thread_id
    tid = thread_id or str(uuid.uuid4())
    config = fmt.thread_config(tid)

    # Invoke the graph, send only new user message, config with thread_id
    try:
        final_state = graph.invoke(
            {"messages": [HumanMessage(content=user_msg)]},
            config=config,
        )
    except Exception as e:
        print(f"Homebrain LangGraph/LLM error: {e!r}")
        raise HTTPException(status_code=500, detail="LLM call failed") from e

    # checks final state for messages
    messages: List[BaseMessage] = final_state.get("messages", [])
    if not messages:
        raise HTTPException(status_code=500, detail="Empty LLM response")

    # Convert to ChatMessage schema
    new_history = fmt.to_chat_messages(messages)

    # Extract last assistant reply
    ai_reply = fmt.get_last_assistant_reply(new_history)
    if not ai_reply:
        raise HTTPException(status_code=502, detail="No assistant reply found")

    return ai_reply, new_history, tid


def chat_turn_stream(thread_id: str | None, user_msg: str) -> Tuple[str, Generator[str, None, None]]:
    """
    Similar to chat_turn, but returns a streaming response generator.

    Returns (tid, token_generator)
    """

    user_msg = user_msg.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message is not allowed.")

    # Ensure thread_id
    tid = thread_id or str(uuid.uuid4())
    config = fmt.thread_config(tid)

    # Token generator
    def token_generator() -> Generator[str, None, None]:
        try:
            # Invoke the graph in streaming mode
            for msg_chunk, metadata in graph.stream(
                {"messages": [HumanMessage(content=user_msg)]},
                config=config,
                stream_mode="messages",
            ):
                # Only stream from main agent node
                if metadata.get("langgraph_node") != "agent":
                    continue

                if metadata.get("langgraph_node") == "tools":
                    print("TOOLS NODE HIT")

                content = getattr(msg_chunk, "content", "")
                if not content:
                    continue

                # Normalize content to string
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    # LangChain content blocks
                    text = "".join(
                        block.get("text", "")
                        for block in content
                        if isinstance(block, dict) and block.get("type") == "text"
                    )
                else:
                    text = ""

                if text:
                    yield text

        except Exception as e:
            print(f"...{e!r}")
            yield "\n[error] Streaming failed\n"
            return

    return tid, token_generator()

