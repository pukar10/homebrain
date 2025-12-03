# Homebrain

## Local Dev

```bash
# Start React Vite server (port 4000)
npm run dev

# Start Backend (FastAPI port 8001)
uvicorn main:app --reload --host 0.0.0.0 --port 8001
# Health check
curl http://localhost:8001/api/health 
# Test chat
curl -X POST http://localhost:8001/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "hello from curl"}'

```

## To Do

- [ ] Dockerize front end
- [ ] Fake React UI Frontend
- [ ] 


## React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).
