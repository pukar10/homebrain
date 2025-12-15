"""
app/agents/rag/state.py

Defines the state structure for the RAG agent. 
"""

from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class RAGState(TypedDict):
    
    messages: Annotated[list[AnyMessage], add_messages]
