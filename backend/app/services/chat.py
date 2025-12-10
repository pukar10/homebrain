"""
app/services/chat.py

- Uses LangGraph (checkpointer + postgres) to handle short- and long-term memory.
- Exposes chat_turn and chat_turn_stream for FastAPI routes to call.

"""

from typing import List, Tuple, Generator
import uuid

from fastapi import HTTPException
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from app.core.graph import graph
from app.models.schemas import ChatMessage

######################################
#   Helpers                          #
######################################

def to_chat_messages(messages: List[BaseMessage]) -> List[ChatMessage]:
    """
    Covert BaseMessage list to ChatMessage list (defining roles).
    Else block: For now, treat any other message types (ToolMessage, etc.) as "system" so they don't break the UI.
    """

    chat_messages: List[ChatMessage] = []

    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "system"
        chat_messages.append(ChatMessage(role=role, content=msg.content))

    return chat_messages


######################################
#  Core                              #
######################################

def chat_turn(thread_id: str | None, user_msg: str) -> Tuple[str, List[ChatMessage], str]:
    """
    Single non-streaming chat turn.

    - Ensures a thread_id (used as LangGraph thread_id).
    - Sends only the new user message to the graph.
    - Lets LangGraph + Postgres checkpointer handle history and persistence.
    - Returns (ai_reply, full_history, resolved_thread_id).
    """

    user_msg = user_msg.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message is not allowed.")

    tid = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}

    try:
        final_state = graph.invoke(
            {"messages": [HumanMessage(content=user_msg)]},
            config=config,
        )
    except Exception as e:
        print(f"Homebrain LangGraph/LLM error: {e!r}")
        raise HTTPException(status_code=500, detail="LLM call failed") from e

    messages: List[BaseMessage] = final_state.get("messages", [])
    if not messages:
        raise HTTPException(status_code=500, detail="Empty LLM response")

    new_history = to_chat_messages(messages)

    ai_reply = new_history[-1].content

    return ai_reply, new_history, tid


def chat_turn_stream(thread_id: str | None, user_msg: str) -> Tuple[str, Generator[str, None, None]]:
    """
    Similar to chat_turn, but returns a streaming response generator.

    Returns (resolved_thread_id, token_generator), where the generator
    yields text chunks (tokens/segments) from the agent node.
    """

    user_msg = user_msg.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Empty message is not allowed.")

    tid = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}

    def token_generator() -> Generator[str, None, None]:
        try:
            # stream_mode="messages" lets us stream message chunks from the graph.
            for msg_chunk, metadata in graph.stream(
                {"messages": [HumanMessage(content=user_msg)]},
                config=config,
                stream_mode="messages",
            ):
                # Only stream from main agent node
                if metadata.get("langgraph_node") != "agent":
                    continue

                content = getattr(msg_chunk, "content", "")

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
            print(f"Homebrain streaming error: {e!r}")
            raise HTTPException(status_code=500, detail="LLM streaming failed") from e

    return tid, token_generator()

