"""
app/services/homebrain_brain.py

- Uses LangGraph's MessagesState to manage conversation history.
- Defines a one-node graph 
- Exposes generate_response for FastAPI routes to call.

"""

from typing import List
from fastapi import HTTPException
from app.core.config import gemini_llm, SYSTEM_PROMPT
from app.models.schemas import ChatMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)


######################################
#   Helper functions                 #
######################################

def build_lc_history(history: List[ChatMessage]) -> List[BaseMessage]:
    """
    Converts chat history into LangChain message objects.
    Error if unknown role found.
    """
    lc_messages: List[BaseMessage] = []
    for msg in history:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))
        else:
            raise ValueError(f"Unknown message role: {msg.role}")
    return lc_messages


def chat_model_node(state: MessagesState) -> dict:
    """
    Single LangGraph node that calls LLM with conversation history.
    """
    # 1. Build messages with system prompt + history
    messages: List[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    # 2. Call LLM
    ai_reply = gemini_llm.invoke(messages)

    # 3. return messages with updated state
    return {"messages": [ai_reply]}

######################################
#  Build LangGraph chat graph        #
######################################

# 1. LangGraph builder for chats
builder = StateGraph(MessagesState)

# 2. Add nodes
builder.add_node("chat_model", chat_model_node)

# 3. Define Starting edge to first node
builder.add_edge(START, "chat_model")

# 4. Define Ending edge from last node
builder.add_edge("chat_model", END)

# 5. Compile the graph
chat_graph = builder.compile()

######################################
#  Core                              #
######################################
def generate_response(history: List[ChatMessage], user_message: str,) -> tuple[str, List[ChatMessage]]:
    """
    Generates a response from the LLM using the LangGraph chat graph.
    """
    # 1. Normalize user message
    trimmed = user_message.strip()
    if not trimmed:
        return "You sent an empty message.", history

    # Dumb logic
    if "proxmox" in trimmed.lower():
        reply = (
            "I can't talk to Proxmox yet, "
            "but soon I'll query the cluster status."
        )
        new_history = history + [
            ChatMessage(role="user", content=trimmed),
            ChatMessage(role="assistant", content=reply),
        ]
        return reply, new_history

    # 2. Convert history to LangChain messages, build initial state by appending new user message
    lc_history = build_lc_history(history)

    initial_state: MessagesState = {
        "messages": [
            *lc_history,
            HumanMessage(content=trimmed),
        ]
    }

    # 3. Run LangGraph chat graph
    try:
        final_state = chat_graph.invoke(initial_state)
    except Exception as e:
        print(f"Homebrain LangGraph/LLM error: {e!r}")
        raise HTTPException(status_code=500, detail="LLM call failed") from e

    # 4. Checks if final state is valid
    messages: List[BaseMessage] = final_state["messages"]
    if not messages:
        raise HTTPException(status_code=500, detail="Empty LLM response")
    
    # 5. Extract reply
    last_msg = messages[-1]
    reply_text = last_msg.content

    new_history = history + [
        ChatMessage(role="user", content=trimmed),
        ChatMessage(role="assistant", content=reply_text),
    ]

    return reply_text, new_history
