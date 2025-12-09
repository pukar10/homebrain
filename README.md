# Homebrain

### Local Dev

```bash
# Fontend React (port 4000)
npm run dev
curl http://localhost:4000

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
- [x] Integrate LangChain
---
### 📊 LangGraph
- [x] Upgrade to LangGraph!
- [x] Multi-turn chat
- [x] History Awareness (send full history with `userQuery`)
- [ ] Multi-nodes! Add a tool node
- [ ] Add RAG Pipeline

#### 💾 Memory
- [x] Implement in-memory sessions using `session_id`
- [ ] Add Postgres DB
- [ ] Load prior history from store by `session_id`
- [ ] Sizebar with "New Chat" and saved chats
---
### 🐿️ Other
- [ ] Basic Auth
- [ ] Rate limit / abuse protection
- [ ] Cost tracker
- [ ] Homelab Statuses for various services
---
### ☕︎ DevOps
- [ ] Containerize frontend
- [ ] Containerize Backend
- [ ] Orchestration with Docker compose
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
