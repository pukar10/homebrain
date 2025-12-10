# app/core/graph.py

from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import SystemMessage
from app.core.config import SYSTEM_PROMPT, settings, gemini_llm


def agent_node(state: MessagesState) -> MessagesState:
    """
    Main Homebrain agent node.

    - `state["messages"]` comes from:
        - previous turns (loaded via checkpointer)
        - plus the newest HumanMessage for this turn (merged by MessagesState)
    - We prepend the system prompt, call the LLM, and append the AI reply.
    """

    history = state["messages"]   # list[BaseMessage]
    
    # System prompt is not stored in state, just used at call time
    messages = [SystemMessage(content= SYSTEM_PROMPT), *history]
    
    ai_reply = gemini_llm.invoke(messages)

    # Checkpointer will save this for the next turn.
    return {"messages": history + [ai_reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.set_entry_point("agent")
builder.set_finish_point("agent")

checkpointer = PostgresSaver.from_conn_string(settings.langgraph_db_url)
checkpointer.setup()

# Singleton
graph = builder.compile(checkpointer=checkpointer)
