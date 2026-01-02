"""
app/schemas/api.py
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


Role = Literal["user", "assistant", "system"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: Optional[str] = None

    @field_validator("message")
    @classmethod
    def strip_and_reject_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Empty message is not allowed.")
        return v


class ChatResponse(BaseModel):
    reply: str
    thread_id: str

