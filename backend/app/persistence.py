"""
app/persistence.py
"""
import logging
from dataclasses import dataclass
from typing import Any, cast
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from app.settings import Settings


log = logging.getLogger(__name__)

@dataclass
class CheckpointerResource:
    checkpointer: Any
    pool: Any | None = None

    def close(self) -> None:
        if self.pool is not None:
            try:
                self.pool.close()
            except Exception:
                log.exception("failed to close checkpointer pool")
            finally:
                self.pool = None

        close_fn = getattr(self.checkpointer, "close", None)
        if callable(close_fn):
            try:
                close_fn()
            except Exception:
                log.exception("failed to close checkpointer")


def create_checkpointer_resource(settings: Settings) -> CheckpointerResource:
    """
    - InMemorySaver if no DB URL.
    - PostgresSaver if langgraph_db_url is set.
    """
    db_url = getattr(settings, "langgraph_db_url", None)
    if not db_url:
        log.info("LangGraph: using InMemorySaver (no langgraph_db_url).")
        return CheckpointerResource(checkpointer=InMemorySaver())

    log.info("LangGraph checkpointer: using PostgresSaver.")
    pool = ConnectionPool(
        conninfo=db_url,
        max_size=10,
        max_idle=300,
        timeout=30,
        kwargs={"autocommit": True, "row_factory": dict_row},
    )
    cp = PostgresSaver(cast(Any, pool))
    return CheckpointerResource(checkpointer=cp, pool=pool)