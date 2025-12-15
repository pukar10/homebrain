"""
app.agents.utc-time.state


"""

from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class utcTimeState(TypedDict):
    
    messages: Annotated[list[AnyMessage], add_messages]
    llm_calls: int
