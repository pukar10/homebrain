"""
app/main.py
FastAPI: creates web app and connects it to runtime.
- Utilize lifespan for statup/shutdown + singletons like DB engine, Redis, vector store client, LLM client wrapper, HTTP client pools, 
model client pools, prompt catalogs, telemetry.
- attach to app.state.*
- register routers/middleware
"""
import logging 
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.core import Base, engine
from app.bootstrap import create_runtime
from app.settings import get_settings

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.settings = settings

    # Dev-friendly. In prod, replace with Alembic migrations.
    # consider wrapping in conditional to avoid running every startup
    Base.metadata.create_all(bind=engine)

    runtime = create_runtime(settings)
    app.state.runtime = runtime

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