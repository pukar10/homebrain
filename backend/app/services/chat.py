"""
app/services/chat.py

- Uses LangGraph (checkpointer + postgres) to handle short- and long-term memory.
- Exposes chat_turn and chat_turn_stream for FastAPI routes to call.

"""

from __future__ import annotations
from typing import List, Tuple, Generator
import uuid
from fastapi import HTTPException
from app.models.schemas import ChatMessage
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from app.core.graph import graph

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
        elif isinstance(msg, SystemMessage):
            role = "system"
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







# def handle_chat_turn(history: List[ChatMessage], user_message: str,) -> tuple[str, List[ChatMessage]]:
#     """
#     Generates a response from the LLM using the LangGraph chat graph.
#     """
#     # 1. Normalize user message
#     user_message_trim = user_message.strip()
#     if not user_message_trim:
#         return "You sent an empty message.", history

#     # 2. Convert history to LangChain messages, build initial state by appending new user message to MessagesState object
#     lc_history = build_lc_history(history)

#     initial_state: MessagesState = {
#         "messages": [
#             *lc_history,
#             HumanMessage(content=user_message_trim),
#         ]
#     }

#     # 3. Run LangGraph
#     try:
#         final_state = chat_graph.invoke(initial_state)
#     except Exception as e:
#         print(f"Homebrain LangGraph/LLM error: {e!r}")
#         raise HTTPException(status_code=500, detail="LLM call failed") from e

#     # Checks if final state is valid
#     messages: List[BaseMessage] = final_state["messages"]
#     if not messages:
#         raise HTTPException(status_code=500, detail="Empty LLM response")
    
#     # Extract reply
#     last_msg = messages[-1]
#     LLM_reply = last_msg.content

#     # new_history = history + [
#     #     ChatMessage(role="user", content=user_message_trim),
#     #     ChatMessage(role="assistant", content=LLM_reply),
#     # ]

#     # 6. Build latest history
#     new_history: List[ChatMessage] = []
#     for msg in messages:
#         if isinstance(msg, HumanMessage):
#             new_history.append(ChatMessage(role="user", content=msg.content))
#         elif isinstance(msg, AIMessage):
#             new_history.append(ChatMessage(role="assistant", content=msg.content))
#         else:
#             raise ValueError(f"Unknown message type: {type(msg)}")

#     return LLM_reply, new_history


# def handle_session_chat_turn(session_id: str | None, user_message: str) -> Tuple[str, List[ChatMessage], str]:
#     """
#     High-level entrypoint: given an optional session_id and user message,
#     load history from DB, run one chat turn, save history to DB, and return:
#       (LLM_reply, new_history, resolved_session_id)
#     """
#     # 1. Get or create session
#     sid = get_or_create_session(session_id)

#     # 2. Load history for session
#     history = get_history_for_session(sid)

#     # 3. Run turn logic
#     LLM_reply, new_history = handle_chat_turn(history, user_message)

#     # 4. Save updated history back to session store
#     save_history_for_session(sid, new_history)

#     # 5. Return everything
#     return LLM_reply, new_history, sid