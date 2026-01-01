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
from app.persistence import create_checkpointer, CheckpointerResource
from app.workflow.agents.homebrain.graph import build_graph
from app.settings import Settings

log = logging.getLogger(__name__)


@dataclass
class Runtime:
    settings: Settings
    llm: Any
    checkpointer: CheckpointerResource 
    graph: Any

    def close(self) -> None:
        self.checkpointer.close()


def create_runtime(settings: Settings) -> Runtime:
    llm = build_gemini_llm(settings)
    checkpointer = create_checkpointer(settings)
    graph = build_graph(llm=llm, checkpointer=checkpointer)

    return Runtime(settings=settings, llm=llm, checkpointer=checkpointer, graph=graph)
