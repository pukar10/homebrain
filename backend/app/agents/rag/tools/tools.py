"""
app/agents/rag/tools.py

Exports:
- 'search_rag_docs': A tool to search the RAG vectorstore for relevant documents.
- 'RAG_TOOLS': registry of tools
"""

from typing import List

from langchain_core.documents import Document
from langchain_core.tools import tool

from app.agents.rag.vectorstore import get_vectorstore


@tool
def search_rag_docs(query: str) -> str:
    """
    Search the RAG vectorstore for relevant documents based on the query.

    Use for questions about Pukar's homelab and documents. Skip for general knowledge questions.
    """
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 2})
    docs: List[Document] = retriever.invoke(query)

    if not docs:
        return "No relevant documents were found in the RAG index."

    chunks = []
    for i, d in enumerate(docs, start=1):
        chunks.append(f"[Chunk {i}]\n{d.page_content.strip()}")

    return "\n\n---\n\n".join(chunks)


RAG_TOOLS = [search_rag_docs]
