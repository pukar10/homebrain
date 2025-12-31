"""
app/schemas/api.py
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field


Role = Literal["user", "assistant", "system"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    thread_id: str

