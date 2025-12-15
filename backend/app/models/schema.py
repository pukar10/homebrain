"""
backend/app/models/schemas.py

- Defines pydantic models

"""

from typing import Literal, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessage]
    thread_id: str


# class SessionSummary(BaseModel):
#     id: str
#     created_at: datetime


# class SessionDetail(BaseModel):
#     id: str
#     created_at: datetime
#     messages: List[ChatMessage]
