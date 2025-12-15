

from langchain_core.tools import tool
from datetime import datetime, timezone


@tool("get_utc_time")
def get_utc_time() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()

def get_tools() -> list:
    return [get_utc_time]