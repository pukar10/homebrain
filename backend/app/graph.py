"""
app/core/graph.py

- Creates Postgres checkpointer
"""

from contextlib import ExitStack
from langgraph.checkpoint.postgres import PostgresSaver
from config import settings

life_stack = ExitStack()
checkpointer = life_stack.enter_context(
    PostgresSaver.from_conn_string(settings.langgraph_db_url)
)
checkpointer.setup()

# Builds Agentic RAG tool loop
#graph = build_rag_agent_graph(checkpointer=checkpointer)

