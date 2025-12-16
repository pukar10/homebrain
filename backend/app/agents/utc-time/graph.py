"""
app.agents.utc-time.graph.py
"""

from state import utcTimeState
from langgraph.graph import StateGraph
from tools import get_tools
from app.config import get_gemini_llm

def build_graph():
    model_with_tools = get_gemini_llm().bind_tools(get_tools())

    builder = StateGraph(utcTimeState)