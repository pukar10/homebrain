"""
app/agents/homebrain/state.py
"""
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


Route = Literal["personal", "projects", "homelab", "general"]

class HomebrainState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]

    route: Route
    route_confidence: float
    route_reason: str
    needs_human_review: bool

    retrieved_context: str
    tool_results: dict
    error: str
