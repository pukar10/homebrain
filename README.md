# Homebrain

### Local Dev

```bash
# React Frontend (port 4000)
npm run dev

# FastAPI Python Backend (port 8001)
uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Swagger
http://localhost:8001/docs
```

### 🗺️ Roadmap / To-Do

### 🧱 Foundation
- [x] React Fontend
- [x] FastAPI Backend
- [x] Backend response from LLM
- [x] Frontend to backend
---
### ⛓️ LangChain
- [x] Integrate LangChain
---
### 📊 LangGraph
- [x] Upgrade to LangGraph!
- [x] Multi-turn chat
- [x] History Awareness (send full history with `userQuery`)
- [ ] Multi-nodes! Add a tool node
- [ ] Implement Memory
- [ ] Add RAG node

#### 💾 Memory
- [ ] Implement sessions using `session_id`
- [ ] Add backend store (Postgres)
- [ ] Load prior history from store by `session_id`
---
### 🐿️ Other
- [ ] Basic Auth
- [ ] Rate limit / abuse protection
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
