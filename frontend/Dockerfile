# frontend/Dockerfile

# ---- Build stage ----
FROM node:22-alpine AS build

WORKDIR /app

# Install deps
COPY package*.json ./
RUN npm install

# Copy Vite/React source
COPY vite.config.* ./
COPY tsconfig*.json ./
COPY index.html ./
COPY public ./public
COPY src ./src

# Build production bundle
RUN npm run build

# ---- Runtime stage ----
FROM nginx:alpine AS runtime

# Copy built assets into nginx's web root
COPY --from=build /app/dist /usr/share/nginx/html

# Optional: you can add a custom nginx.conf later if needed

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
