from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class GraphState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]

    # optional, add later when you need them:
    # rag_context: str
    # citations: list[str]
    # route: str
