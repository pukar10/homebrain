# app/agents/proxmox_status/tools.py

import socket
import time
from dataclasses import dataclass

@dataclass(frozen=True)
class HostCheckResult:
    host: str
    port: int
    up: bool
    rtt_ms: float | None
    error: str | None = None

def tcp_probe(host: str, port: int = 8006, timeout_s: float = 1.5) -> HostCheckResult:
    """
    TCP proble to check if a host is up on a given port.
    """
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            rtt = (time.perf_counter() - start) * 1000.0
            return HostCheckResult(host=host, port=port, up=True, rtt_ms=rtt)
    except OSError as e:
        return HostCheckResult(host=host, port=port, up=False, rtt_ms=None, error=str(e))
