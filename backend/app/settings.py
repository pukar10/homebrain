"""
app/settings.py
"""
from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Database ---
    database_url: str
    langgraph_db_url: str

    # --- Gemini model config ---
    gemini_api_key: str
    gemini_model: str
    gemini_temperature: float
    gemini_max_retries: int


    # --- RAG ---
    rag_docs_dir: str
    rag_vector_dir: str

    # --- Embeddings ---


@cache
def get_settings() -> Settings:
    return Settings.model_validate({})