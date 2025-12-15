# app/agents/rag/graph.py

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.rag.state import RAGState
from app.agents.rag.nodes import rag_node
from app.agents.rag.tools import RAG_TOOLS


def build_rag_agent_graph(checkpointer=None):
    """
    Agentic RAG graph:
    - agent (LLM w/ tools)
    - tools (ToolNode executes requested tools)
    - loop until the LLM responds without tool_calls
    """
    builder = StateGraph(RAGState)

    builder.add_node("agent", rag_node)
    builder.add_node("tools", ToolNode(RAG_TOOLS))

    # Start -> agent
    builder.add_edge(START, "agent")

    # agent -> tools or END
    # If tools_codition returns "tools", go to tools; else END
    builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )

    # tools -> agent
    # After tools run, go back to agent (it will see ToolMessage content)
    builder.add_edge("tools", "agent")

    return builder.compile(checkpointer=checkpointer)
