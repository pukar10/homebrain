"""
app/agents/rag/vectorstore.py

Helper to get Chroma vectorstore instance for RAG agent.
"""

from pathlib import Path
from functools import lru_cache
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.config import settings

@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:

    embeddings = OllamaEmbeddings(model="snowflake-arctic-embed:s")

    vector_path = Path(settings.rag_vector_dir)

    vector_path.mkdir(parents=True, exist_ok=True)

    return Chroma(
        persist_directory=str(vector_path),
        embedding_function=embeddings,
    )