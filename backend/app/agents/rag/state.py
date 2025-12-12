# app/agents/rag/state.py

from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class RAGState(TypedDict):
    """State for the RAG agent: a running list of chat messages."""

    messages: Annotated[list[AnyMessage], add_messages]
