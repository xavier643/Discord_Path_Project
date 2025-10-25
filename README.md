# Discord Path Project

Minimal full-stack template for a Discord-authenticated web app.

- Frontend: Vite + React + React Router
- Backend: Flask (Discord OAuth, session auth, CORS)
- DB: MongoDB (optional; currently skipped in dev)
- Auth: Only users who share a guild with your bot are allowed
- Deploy: API on Fly.io, frontend on any static host (Vercel/Netlify/etc.)

## Current Status (2025-10)

- Discord login works (identify + guilds).
- /me returns { user, authorized_guilds } (only guilds shared with the bot).
- Local dev: React on 3000, API on 5000; Vite proxy in dev.
- “invalid_state” fixed by using the same host for login + callback (localhost↔localhost or 127.0.0.1↔127.0.0.1).
- Mongo is disabled by default in dev via SKIP_MONGO=1.
- Next: enable Mongo writes, add GraphQL endpoint, migrate frontend to Apollo Client.

## Repo Structure

Discord_Path_Project/
├─ client/
│ ├─ index.html
│ └─ src/
│ ├─ main.jsx
│ ├─ App.jsx
│ ├─ components/
│ │ └─ RequireAuth.jsx
│ ├─ pages/
│ │ ├─ Login.jsx
│ │ ├─ Dashboard.jsx
│ │ └─ NotFound.jsx
│ └─ lib/
│ └─ api.js
│ ├─ vite.config.js
│ ├─ .env.development
│ └─ .env.production
│
└─ server/
├─ app.py
├─ auth_discord.py
├─ routes/
│ └─ me.py
├─ db.py
├─ requirements.txt
├─ Dockerfile
├─ fly.toml
└─ .env

## Environment Variables

### Backend (server/.env)

PORT=5000
SESSION_SECRET=<random>
ALLOWED_ORIGIN=http://localhost:3000
POST_LOGIN_REDIRECT=http://localhost:3000
DISCORD_CLIENT_ID=<Application ID>
DISCORD_CLIENT_SECRET=<Client Secret>
DISCORD_BOT_TOKEN=<Bot Token>
DISCORD_REDIRECT_URI=http://localhost:5000/auth/discord/callback
SKIP_MONGO=1

MONGO_URL=...
MONGO_DB=discord_path

### Frontend

client/.env.development
VITE_API_BASE=

client/.env.production
VITE_API_BASE=https://<your-api-app>.fly.dev

## Discord Developer Portal Setup

1. OAuth2 → General → Redirects:

- http://localhost:5000/auth/discord/callback
- https://<your-api-app>.fly.dev/auth/discord/callback

2. Use Application ID as DISCORD_CLIENT_ID.
3. Generate Client Secret → DISCORD_CLIENT_SECRET.
4. Bot → Reset Token → DISCORD_BOT_TOKEN.

## Running Locally

API

- cd server
- python -m venv venv
- venv/Scripts/pip install -r requirements.txt
- venv/Scripts/python app.py

## Frontend

- cd client
- npm install
- npm run dev

## Deploy

API (Fly)

- cd server
- type .env | fly secrets import
- fly deploy

Frontend

- cd client
- npm run build
- deploy dist/ to your static host

## API Endpoints

- GET /auth/discord/login
- GET /auth/discord/callback
- GET /me
- POST /logout
