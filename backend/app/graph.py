"""
app/graph.py

Build the top-level Homebrain graph (Supervisor + specialist agents) and compile it.
"""

from app.persistence import get_checkpointer
from app.config import get_gemini_llm
from app.agents.supervisor.graph import build_supervisor_graph
from app.agents.registry import list_agent_factories

life_stack = ExitStack()
checkpointer = life_stack.enter_context(
    PostgresSaver.from_conn_string(settings.langgraph_db_url)
)
checkpointer.setup()


