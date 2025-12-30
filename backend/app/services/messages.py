"""
backend/app/services/format.py

Helper functions
"""

from typing import List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from app.models.schema import ChatMessage


def to_chat_messages(messages: List[BaseMessage]) -> List[ChatMessage]:
    
    chat_messages: List[ChatMessage] = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            continue
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "system"
        chat_messages.append(ChatMessage(role=role, content=str(msg.content)))
    return chat_messages




def thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}



def get_last_assistant_reply(messages) -> str:
    for msg in reversed(messages):
        if getattr(msg, "type", None) == "ai" and msg.content:
            return msg.content
    return ""
