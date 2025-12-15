"""
backend/app/core/config.py

- Central app settings using Pydantic BaseSettings
- Load env vars
- Define Homebrain system prompt
- Initialize/expose LLMs
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Database ---
    database_url: str
    langgraph_db_url: str

    # --- API keys ---
    gemini_api_key: str

    # --- RAG ---
    rag_docs_dir: str
    rag_vector_dir: str

    # --- Embeddings ---
    ollama_base_url: str
    ollama_embed_model: str

# Singleton
settings = Settings()


SYSTEM_PROMPT = (
    "You are Homebrain, a fun and nerdy AI assistant, created by Pukar Subedi, "
    "for Pukar Subedi's homelab. "
    "You help with VMs (Proxmox, vSphere, etc.), Kubernetes, Terraform, "
    "Ansible, Cloud, Networking, and related tooling/concepts. "
    "You also help explain Pukar's homelab to others that are interested. "
    "Try not to make your responses too long; keep them concise and to the point "
    "but still fun and engaging. "
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=2,
    google_api_key=settings.gemini_api_key,
)