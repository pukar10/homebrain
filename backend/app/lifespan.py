"""
app/lifespan.py
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from app.bootstrap import create_runtime
from app.db.core import Base, SQLengine
from app.settings import get_settings


log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    FastAPI lifespan handler.

    - Load settings once and attach to app.state
    - Initialize long-lived runtime resources (LLM, checkpointer, graph, etc.)
    - (Dev-only) Create DB tables if you aren't using migrations yet
    - Ensure clean shutdown (close pools, dispose engine)
    """
    settings = get_settings()
    app.state.settings = settings

    # Dev-friendly. In prod, replace with Alembic migrations.
    # Consider gating this behind a setting like settings.auto_create_tables.
    Base.metadata.create_all(bind=SQLengine)

    runtime = create_runtime(settings)
    app.state.runtime = runtime

    try:
        yield
    finally:
        try:
            runtime.close()
        except Exception:
            log.exception("shutdown: failed to close runtime")

        try:
            SQLengine.dispose()
        except Exception:
            log.exception("shutdown: failed to dispose engine")
