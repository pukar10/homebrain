"""
app/services/homebrain_brain.py

- Uses LangGraph's MessagesState to manage conversation history.
- Defines a one-node graph 
- Exposes generate_response for FastAPI routes to call.

"""

from typing import List, Tuple
from fastapi import HTTPException
from app.core.config import gemini_llm, SYSTEM_PROMPT
from app.models.schemas import ChatMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from app.services.session_store import (
    get_or_create_session,
    get_history_for_session,
    save_history_for_session,
)

######################################
#   Helpers                          #
######################################

def build_lc_history(history: List[ChatMessage]) -> List[BaseMessage]:
    """
    Converts chat history into LangChain message objects.
    Error if unknown role found.
    """
    lc_messages: List[BaseMessage] = []
    for msg in history:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))
        else:
            raise ValueError(f"Unknown message role: {msg.role}")
    return lc_messages


def generate_reply(state: MessagesState) -> dict:
    """
    Node that calls LLM with system prompt + history, returns updated messages state.
    """
    # 1. Build messages with system prompt + history
    messages: List[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    # 2. Call LLM
    ai_reply = gemini_llm.invoke(messages)

    # 3. return messages with updated state
    return {"messages": [ai_reply]}


# Initialize LangGraph builder
builder = StateGraph(MessagesState)
builder.add_node("agent", generate_reply)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)
chat_graph = builder.compile()


######################################
#  Core                              #
######################################
def handle_chat_turn(history: List[ChatMessage], user_message: str,) -> tuple[str, List[ChatMessage]]:
    """
    Generates a response from the LLM using the LangGraph chat graph.
    """
    # 1. Normalize user message
    user_message_trim = user_message.strip()
    if not user_message_trim:
        return "You sent an empty message.", history

    # 2. Convert history to LangChain messages, build initial state by appending new user message to MessagesState object
    lc_history = build_lc_history(history)

    initial_state: MessagesState = {
        "messages": [
            *lc_history,
            HumanMessage(content=user_message_trim),
        ]
    }

    # 3. Run LangGraph
    try:
        final_state = chat_graph.invoke(initial_state)
    except Exception as e:
        print(f"Homebrain LangGraph/LLM error: {e!r}")
        raise HTTPException(status_code=500, detail="LLM call failed") from e

    # Checks if final state is valid
    messages: List[BaseMessage] = final_state["messages"]
    if not messages:
        raise HTTPException(status_code=500, detail="Empty LLM response")
    
    # Extract reply
    last_msg = messages[-1]
    LLM_reply = last_msg.content

    # new_history = history + [
    #     ChatMessage(role="user", content=user_message_trim),
    #     ChatMessage(role="assistant", content=LLM_reply),
    # ]

    # 6. Build latest history
    new_history: List[ChatMessage] = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            new_history.append(ChatMessage(role="user", content=msg.content))
        elif isinstance(msg, AIMessage):
            new_history.append(ChatMessage(role="assistant", content=msg.content))
        else:
            raise ValueError(f"Unknown message type: {type(msg)}")

    return LLM_reply, new_history


def handle_session_chat_turn(session_id: str | None, user_message: str) -> Tuple[str, List[ChatMessage], str]:
    """
    High-level entrypoint: given an optional session_id and user message,
    load history from DB, run one chat turn, save history to DB, and return:
      (LLM_reply, new_history, resolved_session_id)
    """
    # 1. Get or create session
    sid = get_or_create_session(session_id)

    # 2. Load history for session
    history = get_history_for_session(sid)

    # 3. Run turn logic
    LLM_reply, new_history = handle_chat_turn(history, user_message)

    # 4. Save updated history back to session store
    save_history_for_session(sid, new_history)

    # 5. Return everything
    return LLM_reply, new_history, sid