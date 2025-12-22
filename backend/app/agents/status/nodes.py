# app/agents/proxmox_status/nodes.py

import re
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from state import statusState
from tools import tcp_probe

AGENT_SYSTEM_PROMPT = SystemMessage(
        "You help check homelab statuses. "
        "Be concise. If you can't determine the host, ask for the hostname/service. "
        "Keep reponses short and with ✅/❌ + evidence."
)

KNOWN_HOSTS = {"proxmox1", "proxmox2", "proxmox3"}  # optionally map to IPs

def extract_host_from_text(text: str) -> str | None:
    m = re.search(r"\b(proxmox[1-3])\b", text.lower())
    return m.group(1) if m else None

def extract_target_node(state: statusState, config: RunnableConfig) -> dict:
    last = state["messages"][-1] if state.get("messages") else None
    text = getattr(last, "content", "") if last else ""
    host = extract_host_from_text(text) if isinstance(text, str) else None
    return {"target_host": host} if host else {}

def check_status_node(state: statusState, config: RunnableConfig) -> dict:
    host = state.get("target_host")
    if not host:
        return {"messages": [AIMessage(content="Which Proxmox host should I check (proxmox1/proxmox2/proxmox3 or an IP)?")]}

    # If you have a DNS name -> IP mapping, apply it here.
    result = tcp_probe(host, port=8006, timeout_s=1.5)

    if result.up:
        msg = f"✅ {result.host} looks **UP** (TCP {result.port} reachable, ~{result.rtt_ms:.0f} ms)."
    else:
        msg = f"❌ {result.host} looks **DOWN** (TCP {result.port} unreachable: {result.error})."

    return {"messages": [AIMessage(content=msg)]}
