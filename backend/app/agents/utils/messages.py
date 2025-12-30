"""
app.agents.util.messages
"""
from __future__ import annotations
from typing import Any
from langchain_core.messages import AnyMessage, HumanMessage


def content_to_text(content: Any) -> str:
    """Best-effort: convert LangChain message content into plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)

    return str(content)


def last_human_text(messages: list[AnyMessage]) -> str:
    """Return the most recent HumanMessage content as plain text."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return content_to_text(msg.content).strip()
    return ""
