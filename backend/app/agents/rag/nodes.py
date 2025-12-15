"""
app/agents/rag/nodes.py

Nodes for the RAG agent.
"""

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from app.config import SYSTEM_PROMPT, gemini_llm
from backend.app.agents.rag.tools.tools import RAG_TOOLS
from app.agents.rag.state import RAGState

model_with_tools = gemini_llm.bind_tools(RAG_TOOLS)

def rag_node(state: RAGState, config: RunnableConfig):
    """
    Generates AI reply and returns an update for state.
`
    Returns:
        dict: Updated state with AI reply.
    """
    history = state["messages"]

    messages = [SystemMessage(content=SYSTEM_PROMPT), *history]

    ai_reply = model_with_tools.invoke(messages, config=config)

    return {"messages": [ai_reply]}