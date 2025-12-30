"""
app.agents.personal.nodes.py
"""
from typing import Any, Sequence
from app.state import HomebrainState


def make_personal_node(*, llm: Any, tools: Sequence[Any], system_prompt: str, checkpointer: Any | None = None):
    """
    Personal specialist (ReAct-ready).
    - Uses create_agent (ReAct loop) if available
    - Falls back to single LLM call otherwise
    - Refuses private/sensitive info requests
    """
    agent = _try_create_agent(
        llm=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        middleware=None,
    )

    def personal_node(state: HomebrainState, config: RunnableConfig | None = None) -> dict:
        if state.get("needs_human_review"):
            return {
                "messages": [
                    AIMessage(
                        content=(
                            "I can’t help with private or sensitive personal information. "
                            "Ask about Pukar’s public/professional background or his work instead."
                        )
                    )
                ]
            }

        messages = state.get("messages") or []

        # ReAct agent path
        if agent is not None:
            out = agent.invoke({"messages": messages}, config=config)
            return {"messages": out.get("messages", messages)}

        # Simple fallback path
        reply = llm.invoke([SystemMessage(content=system_prompt), *messages])
        return {"messages": [reply] if isinstance(reply, AIMessage) else [AIMessage(content=str(reply))]}

    return personal_node