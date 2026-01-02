"""
app/schemas/events.py
"""
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    data: str = Field(..., description="A streamed token/chunk")


class DoneEvent(BaseModel):
    type: Literal["done"] = "done"
    thread_id: str


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str
    thread_id: Optional[str] = None
    status: Optional[int] = None


StreamEvent = Union[TokenEvent, DoneEvent, ErrorEvent]