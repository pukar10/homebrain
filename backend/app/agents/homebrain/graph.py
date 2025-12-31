"""
app/agents/homebrain/graph.py

Build the top-level Homebrain graph (Supervisor + specialist agents) and compile it.
"""
import logging
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy
from app.persistence import get_checkpointer
from backend.app.agents.homebrain.state import HomebrainState
# Import nodes: ingest, router, finalize
# Import agents + prompts: personal, projects, homelab, general


log = logging.getLogger(__name__)


"""
Configuration object passed to build_graph().
- min_confidence and ambiguity: human-in-the-loop, can pause and ask user for clarification if router confidence is low.
- ReAct agent node: Register tools per agent. 
    - ReAct agent can reason what tools to use and repeat until confidence is high.
- homelab_interrupt_on: HITL middleware, certain tool calls can trigger human confirmation.
"""
@dataclass(frozen=True)
class GraphConfig:
    min_confidence: float = 0.55
    interrupt_on_ambiguity: bool = True

    personal_tools: Sequence[Any] = field(default_factory=tuple)
    projects_tools: Sequence[Any] = field(default_factory=tuple)
    homelab_tools: Sequence[Any] = field(default_factory=tuple)
    general_tools: Sequence[Any] = field(default_factory=tuple)

    homelab_interrupt_on: Mapping[str, Any] = field(default_factory=dict)


"""
Parent graph: ingest → router → specialist → finalize
- Agents are nodes
- Agents are ReAct-style (use tools, reason, act, observe, repeat until confidence is high enough)
"""
def build_graph(*, llm: Any, checkpointer: Any, cfg: GraphConfig | None = None):
    cfg = cfg or GraphConfig()

    router_node = make_router_node(
        llm=llm,
        min_confidence=cfg.min_confidence,
        interrupt_on_ambiguity=cfg.interrupt_on_ambiguity,
    )

    personal_node = make_personal_node(
        llm=llm,
        tools=cfg.personal_tools,
        system_prompt=PERSONAL_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    projects_node = make_projects_node(
        llm=llm,
        tools=cfg.projects_tools,
        system_prompt=PROJECTS_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    homelab_node = make_homelab_node(
        llm=llm,
        tools=cfg.homelab_tools,
        system_prompt=HOMELAB_SYSTEM_PROMPT,
        checkpointer=checkpointer,
        interrupt_on=cfg.homelab_interrupt_on or None,
    )
    general_node = make_general_node(
        llm=llm,
        tools=cfg.general_tools,
        system_prompt=GENERAL_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    # Build graph
    g = StateGraph(HomebrainState)

    # Retry transient router failures (LLM hiccups).
    router_retry = RetryPolicy(max_attempts=2, initial_interval=0.5)

    # Nodes
    g.add_node("ingest", ingest_node)
    g.add_node("router", router_node, retry_policy=router_retry)

    g.add_node("personal_agent", personal_node)
    g.add_node("projects_agent", projects_node)
    g.add_node("homelab_agent", homelab_node)
    g.add_node("general_agent", general_node)

    g.add_node("finalize", finalize_node)

    # Edges
    g.add_edge(START, "ingest")
    g.add_edge("ingest", "router")

    # router returns Command(goto=...), so specialists just flow to finalize
    g.add_edge("personal_agent", "finalize")
    g.add_edge("projects_agent", "finalize")
    g.add_edge("homelab_agent", "finalize")
    g.add_edge("general_agent", "finalize")

    g.add_edge("finalize", END)

    return g.compile(checkpointer=checkpointer)
