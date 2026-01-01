"""
app/agents/homebrain/graph.py

Build the top-level Homebrain graph (Supervisor + specialist agents) and compile it.
"""
import logging
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from langgraph.graph import END, START, StateGraph 
from langgraph.types import RetryPolicy
from app.workflow.nodes.router import make_router_node
from app.workflow.nodes.ingest import ingest
from app.workflow.nodes.finalize import finalize
from app.workflow.agents.homebrain.state import HomebrainState
from langchain_core.language_models.chat_models import BaseChatModel

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
def build_graph(*, llm: BaseChatModel, checkpointer: Any, cfg: GraphConfig | None = None):
    cfg = cfg or GraphConfig()

    router_node = make_router_node(
        llm=llm,
        min_confidence=cfg.min_confidence,
        interrupt_on_ambiguity=cfg.interrupt_on_ambiguity,
    )

    # Build graph
    g = StateGraph(HomebrainState)

    # Retry transient router failures (LLM hiccups).
    router_retry = RetryPolicy(max_attempts=2, initial_interval=0.5)

    # Nodes
    g.add_node("ingest", ingest)
    g.add_node("router", router_node, retry_policy=router_retry)
    g.add_node("finalize", finalize)

    # Edges
    g.add_edge(START, "ingest")
    g.add_edge("ingest", "router")

    # router returns Command(goto=...), so specialists just flow to finalize
    g.add_edge("finalize", END)

    return g.compile(checkpointer=checkpointer)
