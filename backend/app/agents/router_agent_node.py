"""
app/agents/router_agent_node.py
- keeps routing output logged in state
"""
import logging
from typing import Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command, interrupt
from app.schemas.routing import RouteDecision
from backend.app.agents.homebrain.state import HomebrainState, Route
from app.agents.utils.messages import last_human_text


logger = logging.getLogger(__name__)


ROUTE_TO_NODE: dict[Route, str] = {
    "personal": "personal_agent",
    "projects": "projects_agent",
    "homelab": "homelab_agent",
    "general": "general_agent",
}



def make_router_node(*, llm:Any, min_confidence:float=0.55, interrupt_on_ambiguity:bool=True):
    """
    Factory that builds router node.
    - Creates a router node with an injected llm
    - Logs routing decision metadata in state for observability
    - Easier testing by isolating dependencies
    """
    structured_router = llm.with_structured_output(RouteDecision)

    def router_node(state: HomebrainState) -> Command[str]:
        """
        Classifies latest user message into a RouteDecision and routes.
        - Internal routing logic using Command()
        - writes routing metadata into state
        - human-in-the-loop if confidence is low
        """
        text = last_human_text(state.get("messages") or [])

        decision = classify(structured_router, text)

        # Optional: if model isn't confident, ask user to choose explicitly.
        if decision.confidence < min_confidence and interrupt_on_ambiguity:
            route = interrupt_for_route(text)
            decision = RouteDecision(
                route=route,
                confidence=0.99,
                reason="user_selected_route",
                needs_human_review=False,
            )

        # Compute destination node name
        goto = ROUTE_TO_NODE.get(decision.route, "general_agent")

        # Update state with decision info for logging/analytics/debugging.
        update = {
            "route": decision.route,
            "route_confidence": float(decision.confidence),
            "route_reason": decision.reason,
            "needs_human_review": bool(decision.needs_human_review),
        }

        return Command(update=update, goto=goto)

    return router_node


# -------------------------
# Helpers
# -------------------------
def classify(structured_router: Any, text: str) -> RouteDecision:
    """
    Calls the LLM router with an instruction prompt.
    Returns a safe fallback decision on failure.
    """

    ROUTER_PROMPT = """\
    You are a router for a personal assistant.

    Choose exactly one route:
    - personal: about Pukar (public/professional background)
    - projects: about Pukar's software projects
    - homelab: about Pukar's homelab/infra
    - general: everything else

    Set needs_human_review=true if the request asks for private identifiers
    (address, phone, DOB, passwords, tokens) or asks for risky/real-world actions.

    User message:
    {user_message}
    """

    try:
        decision: RouteDecision = structured_router.invoke(ROUTER_PROMPT.format(user_message=text))

        # Restrict confidence to [0,1]
        conf = max(0.0, min(1.0, float(decision.confidence)))
        if conf != decision.confidence:
            decision.confidence = conf

        # Defensive: if route is somehow missing, default to general.
        if decision.route not in ("personal", "projects", "homelab", "general"):
            return RouteDecision(
                route="general",
                confidence=0.1,
                reason="invalid_route_from_model",
                needs_human_review=False,
            )

        return decision

    except Exception as e:
        logger.exception("Router classify failed; falling back to general. Error=%s", e)
        return RouteDecision(
            route="general",
            confidence=0.1,
            reason=f"classify_error:{type(e).__name__}",
            needs_human_review=False,
        )




def interrupt_for_route(original_text: str) -> Route:
    """
    Human-in-the-loop: ask user to clarify which domain they mean.
    This pauses the graph. On resume, this function receives the chosen value.
    """
    choice = interrupt(
        {
            "message": "Quick clarification so I route you correctly:",
            "options": ["personal", "projects", "homelab", "general"],
            "original_text": original_text,
        }
    )

    if choice in ("personal", "projects", "homelab", "general"):
        return choice

    return "general"
