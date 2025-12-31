"""
app/bootstrap.py
Holds AI application runtime: Build and return long-lived stuff agents need, once per process.
- construct heavyweight clients (LLM, checkpointer/store, vectorstore, etc)
- compile the LangGraph graph (supervisor + agents)
- expose a single object (runtime) that holds these components
- provide a close()/aclose() to cleanup resources on shutdown (pools/connections)
returns Runtime
"""
import logging
from dataclasses import dataclass
from typing import Any
from app.llms.gemini import build_gemini_llm
from app.persistence import get_checkpointer
from app.agents.homebrain.graph import build_graph
from backend.app.settings import Settings

log = logging.getLogger(__name__)


@dataclass
class Runtime:
    settings: Settings
    llm: Any
    checkpointer: Any
    graph: Any

    def close(self) -> None:
        cp = self.checkpointer
        if cp is None:
            return
        
        pool = getattr(cp, "pool", None)
        if pool is not None:
            try:
                pool.close()
            except Exception:
                log.exception("failed to close checkpointer pool")

        close_fn = getattr(cp, "close", None)
        if callable(close_fn):
            try:
                close_fn()
            except Exception:
                log.exception("failed to close checkpointer")


def create_runtime(settings: Settings) -> Runtime:
    llm = build_gemini_llm(settings)
    checkpointer = get_checkpointer()
    graph = build_graph(llm=llm, checkpointer=checkpointer)

    return Runtime(settings=settings, llm=llm, checkpointer=checkpointer, graph=graph)
