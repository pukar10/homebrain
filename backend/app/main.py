"""
app/main.py

- Initialize and share large components
    - Compiled graph (supervisor + agents)
- Initialize FastAPI, register routers, set basic app metadata
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.core import Base, engine
from app.agents.homebrain.graph import build_graph
from app.persistence import get_checkpointer
from app.config import get_settings


log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    checkpointer = get_checkpointer()
    app.state.checkpointer = checkpointer
    app.state.graph = build_graph(checkpointer=checkpointer)

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