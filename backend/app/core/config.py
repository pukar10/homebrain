"""
backend/app/core/config.py

- Load environment variables
- Define Homebrain system prompt
- Initialize shared LLM

"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. Load env variables
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")


# 2. System Prompt used by LangGraph node
SYSTEM_PROMPT = (
    "You are Homebrain, an AI assistant for a homelab. "
    "You help with Proxmox, Kubernetes (K3s), networking, and related tooling. "
    "Be concise but clear, and ask for clarification when needed."
)

# 3. Initialize shared LLM instance
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=2,
)
