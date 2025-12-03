"""
backend/app/core/config.py

- Construct LangChain Prompt Template
- Initializes Gemini chat model.
- Exposes a 'chain' object that other services can call to generate responses.

"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. Load API key from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")


# 2. Construct LangChain Prompt Template
SYSTEM_PROMPT = (
    "You are Homebrain, an AI assistant for a homelab. "
    "You help with Proxmox, Kubernetes (K3s), networking, and related tooling. "
    "Be concise but clear, and ask for clarification when needed."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{history}"),
        ("human", "{input}"),
    ]
)

# 3. Expose Chain object other services can use to generate responses
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=2,
)

chain = prompt | llm
