"""
app/services/homebrain_brain.py

Where LangChain + Gemini live. FastAPI route calls this function.

"""

from typing import List
from fastapi import HTTPException
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from app.core.config import chain
from app.models.chat import ChatMessage


def build_lc_history(history: List[ChatMessage]) -> List[BaseMessage]:
    lc_messages: List[BaseMessage] = []
    for msg in history:
        if msg.role == "user":
            lc_messages.append(HumanMessage(msg.content))
        else:
            lc_messages.append(AIMessage(msg.content))
    return lc_messages


def run_homebrain(
    history: List[ChatMessage],
    user_message: str,
) -> tuple[str, List[ChatMessage]]:
    """
    Main brain function: takes existing history + new user message,
    calls the LangChain+Gemini chain, returns (reply, new_history).
    """
    trimmed = user_message.strip()
    if not trimmed:
        return "You sent an empty message.", history

    # Proxmox easter egg example
    if "proxmox" in trimmed.lower():
        reply = "I can't talk to Proxmox yet, but soon I'll query your cluster status."
        new_history = history + [
            ChatMessage(role="user", content=trimmed),
            ChatMessage(role="assistant", content=reply),
        ]
        return reply, new_history

    lc_history = build_lc_history(history)

    try:
        ai_msg = chain.invoke(
            {
                "history": lc_history,
                "input": trimmed,
            }
        )
    except Exception as e:
        print(f"Homebrain LLM error: {e}")
        raise HTTPException(status_code=500, detail="LLM call failed")

    reply_text = getattr(ai_msg, "text", None) or str(ai_msg)

    new_history = history + [
        ChatMessage(role="user", content=trimmed),
        ChatMessage(role="assistant", content=reply_text),
    ]
    return reply_text, new_history