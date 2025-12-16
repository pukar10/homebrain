# utc_time/node.py


from datetime import datetime, timezone
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from state import utcTimeState
from app.config import SYSTEM_PROMPT
from app.util.messages import last_human


def agent_node(state: utcTimeState, config: RunnableConfig) -> dict:

    messages = state["messages"]

    messages = [SYSTEM_PROMPT, *messages]

    now = datetime.now(timezone.utc).isoformat()

    return {"messages": [ai_reply]}


def capture_tool_results(state: utcTimeState) -> dict:
    """
    ToolNode returns ToolMessage(s) into `messages`.
    This node copies the most recent tool outputs into `last_tool_results`
    so the parent can easily return them in a strict JSON payload.
    """
    new_results = []
    # scan from end until messages stop being ToolMessages
    for m in reversed(state["messages"]):
        if isinstance(m, ToolMessage):
            new_results.append(m.content)
        else:
            break

    new_results.reverse()
    return {"last_tool_results": new_results}
