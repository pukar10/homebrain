from typing import Optional
from langchain_core.messages import HumanMessage

def last_human(state) -> Optional[HumanMessage]:
    return next(
        (m for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)),
        None,
    )

