# Homebrain

### Local Dev

```bash
# Fontend React (port 4000)
npm run dev

# Backend python FastAPI (port 8001)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

    # Swagger Docs
    http://localhost:8001/docs

# Full Stack Start
docker compose up -d --build
```

### 🗺️ Roadmap / To-Do

### 🧱 Foundation
- [x] Traffic from Domain to Caddy Reverse Proxy to Compute VM in Homelab
- [x] React Fontend
- [x] FastAPI Backend
- [x] Expose backend routes
- [x] Backend response from LLM
---
### ⛓️ LangChain
- [x] Integrate LangChain chain
---
### 📊 LangGraph
- [x] Integrate LangGraph Node
- [x] Implement streaming (replace invoke)
---
### Memory

#### In-Memory (Postgres)
- [x] Multi-turn
- [x] History Awareness

#### Checkpointers (production solution) *
- [x] Short-term memory (multi-turn)
- [ ] Long-term memory (user/app data accross sessions)

---
### Containerize
- [x] Seperate frontend and backend
- [x] Dockerfile for frontend
- [x] Dockerfile for backend
- [x] Docker-compose.yaml 
---
### Sidebar
- [x] Add sidebar to frontend
- [x] Add button for new chat (Send new `session_id` with payload)
- [x] Show previous conversations by pulling `session_id` from backend store
- [ ] Conversation titles
    - [ ] Call LLM with summarization prompt (after first turn) to generate title
    - [ ] Save in PostgresDB with `thread_id`
    - [ ] Show on frontend
---
### Tool Node *
- [ ] Create LangChain `tool`
- [ ] Wrap with agent
- [ ] Call agent from LangGraph Node 
---
### RAG Agent *
- [ ] Implement Vector Database (Chunking -> Embedding -> Vector store) to ingest Documents (.md/markdown/.txt)
- [ ] Create Retriever tool
- [ ] Add Retriever tool to agent (Agent should decide Answer from prior context or call Retriever tool and ground answer)
- [ ] Upgrade documents to include .PDF
---
### 🐿️ Other
- [ ] Basic Auth
- [ ] Rate limit / abuse protection
- [ ] Cost tracker
- [ ] Homelab Statuses for various services
- [ ] Integrate Redis?
- [ ] Integrate kafka? 
---
### ☕︎ DevOps
- [ ] CI/CD with GitHub Actions
--- 


## Checkout

elevenlabs.io

## React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).
