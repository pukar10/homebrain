"""
app/agents/utils/messages.py
"""
from __future__ import annotations
from typing import Any, Iterable, Optional, Sequence, TypedDict
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, ToolMessage
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
    mode="stream" (default): strict + safe for user streaming
    mode="debug": logs/diagnostics, falls back to str(content)
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


def message_text(msg: AnyMessage) -> str:
    return content_to_text(getattr(msg, "content", None)).strip()


def last_human_text(messages: list[AnyMessage]) -> str:
    """Return the most recent HumanMessage content as plain text."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return content_to_text(msg.content).strip()
    return ""


def last_ai_text(messages: Iterable[AnyMessage]) -> str:
    """Return the last AIMessage text (trimmed) or ''."""
    msg = last_ai_message(messages)
    return message_text(msg) if msg is not None else ""


def last_human_message(messages: Iterable[AnyMessage]) -> Optional[HumanMessage]:
    """Return the last HumanMessage in the iterable, if any."""
    for msg in reversed(list(messages)):
        if isinstance(msg, HumanMessage):
            return msg
    return None


def last_ai_message(messages: Iterable[AnyMessage]) -> Optional[AIMessage]:
    """Return the last AIMessage in the iterable, if any."""
    for msg in reversed(list(messages)):
        if isinstance(msg, AIMessage):
            return msg
    return None


def last_tool_message(messages: Iterable[AnyMessage]) -> Optional[ToolMessage]:
    """Return the last ToolMessage in the iterable, if any."""
    for msg in reversed(list(messages)):
        if isinstance(msg, ToolMessage):
            return msg
    return None


def has_messages(state: dict[str, Any]) -> bool:
    msgs = state.get("messages")
    return isinstance(msgs, list) and len(msgs) > 0