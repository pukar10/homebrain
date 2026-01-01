"""
app/agents/homebrain/finalize.py
- Does not generate new assistant text
- Only deterministic finalization logic
"""
import logging
from typing import Any
from langchain_core.messages import AnyMessage
from app.workflow.agents.homebrain.state import HomebrainState
from app.workflow.utils.messages import last_ai_text


log = logging.getLogger(__name__)


def finalize(state: HomebrainState) -> dict[str, Any]:
    """
    Finalize step:
    - Extract last assistant text into state["final_answer"] for convenience.
    - Add lightweight metrics for logging/analytics/debugging.
    - Avoid mutating messages (important for streaming endpoints).
    """
    messages = state.get("messages") or []
    final_answer = last_ai_text(messages)

    log.debug(
        "finalize: turn complete",
        extra={
            "messages_count": len(messages),
            "route": state.get("route"),
            "route_confidence": state.get("route_confidence"),
            "needs_human_review": state.get("needs_human_review"),
            "has_final_answer": bool(final_answer),
            "has_error": bool(state.get("error")),
        },
    )

    return {
        "final_answer": final_answer,
        "final_message_count": len(messages),
    }