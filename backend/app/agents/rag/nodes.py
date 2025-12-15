"""
app/agents/rag/nodes.py

Node fucntions for the RAG agent.
"""

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from app.config import SYSTEM_PROMPT, get_gemini_llm
from app.agents.rag.tools import get_tools
from app.agents.rag.state import RAGState

model_with_tools = get_gemini_llm().bind_tools(get_tools())

def rag_node(state: RAGState, config: RunnableConfig):
    """
    Returns an update for RAGState
    """
    history = state["messages"]

    messages = [SystemMessage(content=SYSTEM_PROMPT), *history]

    ai_reply = model_with_tools.invoke(messages, config=config)

    return {"messages": [ai_reply]}