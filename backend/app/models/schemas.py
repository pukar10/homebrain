"""
backend/app/models/chat.py

- Defines pydantic models for chat messages, requests and responses.

"""

from typing import Literal, List, Optional
from datetime import datetime
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessage]
    session_id: str


class SessionSummary(BaseModel):
    id: str
    created_at: datetime


class SessionDetail(BaseModel):
    id: str
    created_at: datetime
    messages: List[ChatMessage]