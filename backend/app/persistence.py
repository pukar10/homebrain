"""
app/persistence.py
"""

from functools import lru_cache
from app.config import get_settings

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


@lru_cache(maxsize=1)
def get_checkpointer():
    """
    Create singleton checkpointer for whole app
    - Use InMemorySaver for local dev/testing (resets on restart).
    - Use PostgresSaver + ConnectionPool for production persistence.
    """
    s = get_settings()

    # “dev mode” toggle: if no URL, fall back to memory.
    if not getattr(s, "langgraph_db_url", None):
        return InMemorySaver()

    pool = ConnectionPool(
        conninfo=s.langgraph_db_url,
        max_size=10,
        max_idle=300.0,
        kwargs={"autocommit": True, "row_factory": dict_row},
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    return checkpointer