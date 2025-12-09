"""
FastAPI Entry Point

- Initialize FastAPI
- Create DB tables on startup (for dev)
- Registers API routers
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.sessions import router as sessions_router
from app.db.core import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager.

    Code before `yield` runs at startup.
    Code after `yield` runs at shutdown.
    """

    # Startup code: Create DB tables (dev)
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown code: (add any cleanup here if needed)


# Initialize FastAPI
app = FastAPI(
    title="Homebrain Backend",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


# Register routers
app.include_router(chat_router)
app.include_router(sessions_router)
