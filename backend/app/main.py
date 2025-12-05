
from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(
    title="Homebrain Backend",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(chat_router)
