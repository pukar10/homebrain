"""
backend/app/core/config.py
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_core.messages import SystemMessage


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
    ollama_base_url: str
    ollama_embed_model: str


def get_settings() -> Settings:
    return Settings()


SYSTEM_PROMPT_TEXT = (
    "You are Homebrain, a fun and nerdy AI assistant, created by Pukar Subedi, "
    "for Pukar Subedi's homelab. "
    "You help with VMs (Proxmox, vSphere, etc.), Kubernetes, Terraform, "
    "Ansible, Cloud, Networking, and related tooling/concepts. "
    "You also help explain Pukar's homelab to others that are interested. "
    "Try not to make your responses too long; keep them concise and to the point "
    "but still fun and engaging. "
)

SYSTEM_PROMPT = SystemMessage(content=SYSTEM_PROMPT_TEXT)

@lru_cache(maxsize=1)
def get_gemini_llm() -> ChatGoogleGenerativeAI:
    """Create the Gemini LLM client once per process."""
    s = get_settings()
    return ChatGoogleGenerativeAI(
        model=s.gemini_model,
        temperature=s.gemini_temperature,
        max_retries=s.gemini_max_retries,
        google_api_key=s.gemini_api_key,
    )

@lru_cache(maxsize=1)
def get_ollama_embeddings() -> OllamaEmbeddings:
    """Create the embedding client once per process."""
    s = get_settings()
    return OllamaEmbeddings(
        base_url=s.ollama_base_url,
        model=s.ollama_embed_model,
    )