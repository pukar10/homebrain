from app.api.deps import get_graph
from app.schemas.events import TokenEvent, DoneEvent

def fake_chat_turn_stream(graph, thread_id, message):
    tid = thread_id or "test-thread"
    def gen():
        yield TokenEvent(data="hi")
        yield DoneEvent(thread_id=tid)
    return tid, gen()

def test_chat_stream_sends_sse_events(monkeypatch, client):
    # override graph dep on the app behind the client
    app = client.app
    app.dependency_overrides[get_graph] = lambda: object()

    import app.api.chat as chat_module
    monkeypatch.setattr(chat_module, "chat_turn_stream", fake_chat_turn_stream)

    with client.stream("POST", "/api/chat/stream", json={"message": "hello", "thread_id": None}) as resp:
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")

        body = ""
        for chunk in resp.iter_text():
            body += chunk
            if '"type":"done"' in body or '"type": "done"' in body:
                break

    assert '"token"' in body
    assert '"data"' in body
    assert '"done"' in body
