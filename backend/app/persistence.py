"""
app/persistence.py
"""
import logging
from functools import cache
from typing import Optional
from psycopg import Connection
from psycopg.rows import dict_row, DictRow
from psycopg_pool import ConnectionPool

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from app.config import get_settings


logger = logging.getLogger(__name__)
pool: Optional[ConnectionPool[Connection[DictRow]]] = None


"""
Singleton checkpointer

- InMemorySaver if no DB URL.
- PostgresSaver in prod.
- .setup() only runs if enabled via settings.
"""
@cache
def get_checkpointer():
    global pool
    s = get_settings()

    db_url = getattr(s, "langgraph_db_url", None)
    if not db_url:
        logger.info("LangGraph: using InMemorySaver (no langgraph_db_url).")
        return InMemorySaver()

    logger.info("LangGraph: using PostgresSaver.")
    pool = ConnectionPool(
        conninfo=db_url,
        max_size=10,
        max_idle=300,
        timeout=30,
        kwargs={
            "autocommit": True,
            "row_factory": dict_row,
        },
    )

    cp = PostgresSaver(pool)

    if bool(getattr(s, "langgraph_init_db", False)):
        logger.info("LangGraph: running checkpointer.setup()")
        cp.setup()

    return cp


def close_checkpointer() -> None:
    global pool
    if pool is not None:
        pool.close()
        pool = None