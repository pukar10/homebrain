# Homebrain

### Local Dev

```bash
# Fontend React (port 4000)
npm run dev

# Backend dev setup
uv sync --frozen --extra dev

# Run tests
uv run pytest

# Start local Backend (port 8001)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

    # Swagger Docs
    http://localhost:8001/docs

# Full Stack Start (prod/dev)
docker compose up -d --build
docker compose -f docker-compose.dev.yaml up -d --build
```

## Architecture

```bash
START
  ↓
ingest_message  (normalize input, append to messages)
  ↓
router          (classify route + confidence + “needs review?”)
  ├─→ personal_react_agent
  ├─→ projects_react_agent
  ├─→ homelab_react_agent   (tools + RAG + approvals)
  └─→ general_react_agent
  ↓
finalize        (format answer + redact/deny sensitive requests)
  ↓
END
```

## Checkout

elevenlabs.io  
github.com/FareedKhan-dev/Multi-Agent-AI-System

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).
