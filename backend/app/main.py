"""
app/main.py

FastAPI entry point.
- Build the compiled LangGraph app once at startup
- Store it in app.state.graph
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.core import Base, engine
from app.persistence import get_checkpointer
from app.graph import build_main_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    checkpointer = get_checkpointer()
    app.state.checkpointer = checkpointer
    app.state.graph = build_main_graph(checkpointer=checkpointer)

    # Create tables on startup(sync SQLAlchemy):
    Base.metadata.create_all(bind=engine)

    yield

    # --- shutdown ---
    cp = getattr(app.state, "checkpointer", None)
    pool = getattr(cp, "pool", None)
    if pool is not None:
        pool.close()


app = FastAPI(
    title="Homebrain Backend",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


# Register routers
app.include_router(chat_router)