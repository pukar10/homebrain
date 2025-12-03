from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "homebrain-backend"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message.strip()

    if not user_message:
        return ChatResponse(reply="You sent an empty message.")

    # For now, a very dumb "brain"
    if "proxmox" in user_message.lower():
        return ChatResponse(
            reply="I can't talk to Proxmox yet, but soon I'll query your cluster status."
        )

    return ChatResponse(
        reply=f'I received: "{user_message}". Later this will go through LangChain / LangGraph.'
    )
