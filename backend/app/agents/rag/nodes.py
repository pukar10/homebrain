"""
app/agents/rag/nodes.py

Nodes for the RAG agent.
"""

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from app.core.config import SYSTEM_PROMPT, gemini_llm
from app.agents.rag.tools import RAG_TOOLS
from app.core.state import GraphState

model_with_tools = gemini_llm.bind_tools(RAG_TOOLS)

def rag_node(state: GraphState, config: RunnableConfig):
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