# utc_time/node.py

from functools import lru_cache
from typing import Any, Dict

from app.config import SYSTEM_PROMPT, get_gemini_llm
from langchain_core.messages import SystemMessage, ToolMessage

@lru_cache(maxsize=1)
def get_model_with_tools(tools):
    # Cached so you don't re-init models constantly
    gemini_llm = get_gemini_llm()
    return gemini_llm.bind_tools(tools)  # tool_calls show up on AIMessage :contentReference[oaicite:1]{index=1}


def llm_node(state: Dict[str, Any], *, tools) -> dict:
    model_with_tools = get_model_with_tools(tuple(tools))  # tuple for cache key
    reply = model_with_tools.invoke([SystemMessage(content=SYSTEM_PROMPT), *state["messages"]])
    return {
        "messages": [reply],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


def capture_tool_results(state: Dict[str, Any]) -> dict:
    """
    ToolNode returns ToolMessage(s) into `messages`.
    This node copies the most recent tool outputs into `last_tool_results`
    so the parent can easily return them in a strict JSON payload.
    """
    new_results = []
    # scan from end until messages stop being ToolMessages
    for m in reversed(state["messages"]):
        if isinstance(m, ToolMessage):
            new_results.append(m.content)
        else:
            break

    new_results.reverse()
    return {"last_tool_results": new_results}
