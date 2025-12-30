"""
app.agents.util.messages
"""
from __future__ import annotations
from typing import Any, Optional, Sequence, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage
from typing import Literal


ContentMode = Literal["stream", "debug"]


class ThreadConfig(TypedDict, total=False):
    """
    typed wrapper around RunnableConfig.
    attributes:
    - configurable used to pass runtime parameters to LangGraph nodes.
    - tags used for grouping/tracing runs.
    - metadata used for extra safe/non-sensitive info.
    Notes:
    - configurable.thread_id is the key used by LangGraph checkpointers for thread persistence.
    - tags/metadata are optional but useful for logging/observability.
    """
    configurable: dict[str, Any]
    tags: list[str]
    metadata: dict[str, Any]


def thread_config(thread_id: str, 
                *, 
                user_id: Optional[str] = None, 
                tags: Optional[Sequence[str]] = None, 
                metadata: Optional[dict[str, Any]] = None
                ) -> ThreadConfig:
    """
    Builds a RunnableConfig dict for LangGraph runs.

    Params:
        thread_id: identifier used for checkpointing and memory.
        user_id: Optional identifier for analytics/logging (avoid PII for public apps).
        tags: Optional tags to group/trace runs.
        metadata: Optional extra metadata (safe, non-sensitive).

    Returns:
        config Dict compatible with RunnableConfig.
    """
    cfg: ThreadConfig = {
        "configurable": {"thread_id": thread_id},
    }

    if user_id:
        cfg["configurable"]["user_id"] = user_id

    if tags:
        cfg["tags"] = list(tags)

    if metadata:
        cfg["metadata"] = dict(metadata)

    return cfg


def content_to_text(content:Any, *, mode: ContentMode = "stream") -> str:
    """
    Convert LangChain message content into plain text.

    mode="stream" (default):
      - strict + safe for user-facing streaming
      - avoids dumping dict/object reprs into the UI

    mode="debug":
      - best-effort for logs/diagnostics
      - falls back to str(content)
    """
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
                continue

            if isinstance(part, dict):
                if part.get("type") == "text":
                    text = part.get("text")
                    if isinstance(text, str):
                        parts.append(text)
                elif mode == "debug": 
                    text = part.get("text")
                    if isinstance(text, str):
                        parts.append(text)
        return "".join(parts) if mode == "stream" else "\n".join(parts)

    return "" if mode == "stream" else str(content)


def last_human_text(messages: list[AnyMessage]) -> str:
    """Return the most recent HumanMessage content as plain text."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return content_to_text(msg.content).strip()
    return ""
