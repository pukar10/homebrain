# Homebrain

### Local Dev

```bash
# Fontend React (port 4000)
npm run dev

# Backend python FastAPI (port 8001)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

    # Swagger Docs
    http://localhost:8001/docs

# Full Stack Start (prod/dev)
docker compose up -d --build
docker compose -f docker-compose.dev.yaml up -d --build

# Run ingestion job for RAG agent (prod/dev)
docker compose --profile jobs run --rm ingest
docker compose -f docker-compose.dev.yaml --profile jobs run --rm ingest
```

## Architecture

Placeholder

## Checkout

elevenlabs.io  
github.com/FareedKhan-dev/Multi-Agent-AI-System

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).
