"""
backend/app/core/config.py

- Load environment variables
- Define Homebrain system prompt
- Initialize shared LLM

"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# 1. Load env variables
load_dotenv()

if not os.getenv("GEMINI_API_KEY") or not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing API key(s) check your .env file.")



# 2. System Prompt used by LangGraph node
SYSTEM_PROMPT = (
    "You are Homebrain, a fun and nerdy AI assistant, Created by Pukar Subedi, for Pukar Subedi's homelab. "
    "You help with VMs (proxmox, vSphere, etc), Kubernetes, Terraform, Ansible, Cloud, Networking, and related tooling/concepts. "
    "You also help explain my homelab to others that are interested. "
    "Be concise but clear, and ask for clarification when needed. "
)

# 3. Expose LLM objects for other services to use
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_retries=2,
)

openai_llm = ChatOpenAI(
    model_name="gpt-5-nano",
    }
