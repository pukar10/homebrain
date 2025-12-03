"""
app/services/homebrain_brain.py

- Uses LangGraph's MessagesState to manage conversation history.
- Defines a one-node graph 
- Exposes generate_response(...) for FastAPI routes to call.

"""


from collections.abc import Sequence
from typing import List, Tuple
from fastapi import HTTPException
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langgraph.graph import StateGraph, START, END, MessagesState

from app.core.config import llm, SYSTEM_PROMPT
from app.models.chat import ChatMessage


def build_lc_history(history: List[ChatMessage]) -> List[BaseMessage]:
    """
    Converts chat history into LangChain message objects.
    """
    lc_messages: List[BaseMessage] = []
    for msg in history:
        if msg.role == "user":
            lc_messages.append(HumanMessage(msg.content))
        else:
            lc_messages.append(AIMessage(msg.content))
    return lc_messages


def generate_response(history: List[ChatMessage], user_message: str,) -> tuple[str, List[ChatMessage]]:
    """
    Generates a response from the LLM using the chain.
    """
    # 1. Normalize user message
    trimmed = user_message.strip()
    if not trimmed:
        return "You sent an empty message.", history

    # Dumb logic
    if "proxmox" in trimmed.lower():
        reply = "I can't talk to Proxmox yet, but soon I'll query your cluster status."
        new_history = history + [
            ChatMessage(role="user", content=trimmed),
            ChatMessage(role="assistant", content=reply),
        ]
        return reply, new_history

    # 2. Build LangChain Message History
    lc_history = build_lc_history(history)

    # 3. Call the chain, get response
    try:
        llm_response_raw = chain.invoke(
            {
                "history": lc_history,
                "input": trimmed,
            }
        )
    except Exception as e:
        print(f"Homebrain LLM error: {e}")
        raise HTTPException(status_code=500, detail="LLM call failed")

    llm_response = getattr(llm_response_raw, "text", None) or str(llm_response_raw)

    new_history = history + [
        ChatMessage(role="user", content=trimmed),
        ChatMessage(role="assistant", content=llm_response),
    ]

    return llm_response, new_history