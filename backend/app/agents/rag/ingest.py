# app/services/ingest.py

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

# Where your homelab / Homebrain docs live
DOCS_DIR = Path(settings.rag_docs_dir)  # e.g. "data/homebrain_docs"
VECTOR_DIR = Path(settings.rag_vector_dir)  # e.g. "data/homebrain_chroma"


def build_vectorstore() -> None:
    """Ingest docs -> chunk -> embed -> persist to Chroma."""

    if not DOCS_DIR.exists():
        raise SystemExit(f"Docs directory does not exist: {DOCS_DIR}")

    print(f"Loading documents from {DOCS_DIR} ...")
    loader = DirectoryLoader(
        str(DOCS_DIR),
        glob="**/*.md",          # adjust: .md, .txt, .pdf with other loaders, etc.
        loader_cls=TextLoader,
        show_progress=True,
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
    )
    splits = splitter.split_documents(docs)
    print(f"Split into {len(splits)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"  # or your preferred Gemini embedding model
    )

    print(f"Indexing into Chroma at {VECTOR_DIR} ...")
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR),
    )

    print("✅ Ingestion complete.")


if __name__ == "__main__":
    build_vectorstore()
