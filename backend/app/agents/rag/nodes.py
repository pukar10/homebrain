# app/agents/rag/nodes.py

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from app.core.config import SYSTEM_PROMPT, gemini_llm
from app.agents.rag.tools import RAG_TOOLS
from backend.app.agents.rag.state import RAGState


# Bind tools to the base Gemini chat model so it can emit tool_calls
# Returns ai reply
model_with_tools = gemini_llm.bind_tools(RAG_TOOLS)

def rag_node(state: RAGState, config: RunnableConfig):
    """LLM decides: call tool(s) or respond directly.

    Returns:
        {"messages": [ai_reply: AnyMessage]}
    """
    history = state["messages"]

    messages = [SystemMessage(content=SYSTEM_PROMPT), *history]

    ai_reply = model_with_tools.invoke(messages, config=config)

    return {"messages": [ai_reply]}