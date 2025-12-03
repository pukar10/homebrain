"""
backend/app/models/chat.py

- Defines pydantic models for chat messages, requests and responses.

"""

from typing import Literal, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessage]
