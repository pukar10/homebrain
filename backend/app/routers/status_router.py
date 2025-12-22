import re
from typing import Literal, TypedDict
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from 

Route = Literal["status", "chat"]

HOST_RE = re.compile(r"\b(proxmox[1-3])\b", re.IGNORECASE)

class RouteDecision(TypedDict, total=False):
    route: Route
    target_host: str

ROUTER_PROMPT = (
    "You are a router. Decide if the user is asking to CHECK STATUS/UP-DOWN/REACHABILITY "
    "of a Proxmox host or VM. Only answer with 'status' or 'chat'.\n"
    "If they ask to probe/reach/check/up/down/online/offline/status/health => status.\n"
    "If they ask conceptual questions (how-to/why/what is) => chat."
)

def router_node(state, config: RunnableConfig, *, router_llm) -> RouteDecision:
    last_user_msg = state["messages"][-1]
    text = getattr(last_user_msg, "content", "") or ""
    if not isinstance(text, str):
        return {"route": "chat"}

    m = HOST_RE.search(text)
    if not m:
        return {"route": "chat"}

    host = m.group(1).lower()

    # LLM decides intent ONLY because host mention matched
    decision = router_llm.invoke(
        [SystemMessage(content=ROUTER_PROMPT), *state["messages"]],
        config=config,
    ).content.strip().lower()

    if "status" in decision:
        return {"route": "status", "target_host": host}

    return {"route": "chat"}
