"""
app/config.py
"""

from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_google_genai import ChatGoogleGenerativeAI

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


@cache
def get_gemini_llm() -> ChatGoogleGenerativeAI:
    s = get_settings()
    return ChatGoogleGenerativeAI(
        model=s.gemini_model,
        temperature=s.gemini_temperature,
        max_retries=s.gemini_max_retries,
        google_api_key=s.gemini_api_key,
    )