"""
app/agents/homebrain/ingest.py
- Validate/normalize user input before passing to router
- Only raise Python errors not HTTP errors
- Clears out state fields that shouldn't be persisted (like route decisions)
"""
import logging
from typing import Any
from langchain_core.messages import AnyMessage, HumanMessage
from app.workflow.agents.homebrain.state import HomebrainState
from app.workflow.utils.messages import last_human_text

log = logging.getLogger(__name__)

def ingest(state: HomebrainState) -> dict[str, Any]:
    """
    Deterministic ingest step.
    - Ensures we have a sane user message for this turn (guards against things)
    - Clear fields each turn so old routing/tool info doesn't carry over
    Returns: partial state update dict
    """
    messages = state.get("messages") or []
    last_user_txt = last_human_text(messages)

    if not last_user_txt:
        log.warning("ingest: empty last user message", extra={"messages_count": len(messages)})
        raise ValueError("Empty user message")

    update: dict[str, Any] = {
        "error": "",
        "retrieved_context": "",
        "tool_results": {},
        "route_reason": "",
        "route_confidence": 0.0,
        "needs_human_review": False,
    }

    log.debug(
        "ingest: ok",
        extra={"messages_count": len(messages), "last_user_txt_len": len(last_user_txt)},
    )

    return update