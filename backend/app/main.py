"""
app/main.py
Holds FastAPI app wiring: creates web app and connects it to runtime.
- Create FastAPI instance
- register routers/middleware
- run startup/shutdown (lifespan) to initialize runtime and store in app.homebrain.state
- 
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.core import Base, engine
from app.agents.homebrain.graph import build_graph
from app.persistence import get_checkpointer
from backend.app.bootstrap import create_runtime
from backend.app.settings import get_settings

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.settings = settings

    # Dev-friendly. In prod, replace with Alembic migrations.
    Base.metadata.create_all(bind=engine)

    runtime = create_runtime(settings)
    app.state.runtime = runtime
    app.state.graph = runtime.graph

    try:
        yield
    finally:
        runtime.close()
        try:
            engine.dispose()
        except Exception:
            log.exception("shutdown: failed to dispose engine")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Homebrain Backend",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(chat_router)
    return app


app = create_app()