"""
app/llms/gemini.py
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import Settings


def build_gemini_llm(settings: Settings) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.gemini_temperature,
        max_retries=settings.gemini_max_retries,
        google_api_key=settings.gemini_api_key,
    )
