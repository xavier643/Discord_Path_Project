# Discord Path Project

## Overview
A web app + Discord bot that share one **MongoDB**.

- Users log in with **Discord OAuth2**.
- Backend issues **JWTs** for frontend sessions.
- Discord bot connects to the same MongoDB and syncs with backend state.

---

## Repo Structure
    Discord_Path_Project/
    ├─ client/                # Frontend (React + Apollo Client)
    │   ├─ public/            # Static assets
    │   ├─ src/               # React source code
    │   │   ├─ apollo/        # Apollo client setup
    │   │   ├─ components/    # Reusable components
    │   │   ├─ pages/         # Page-level views (Login, Dashboard, Guilds)
    │   │   ├─ styles/        # CSS or SCSS (if not using CSS-in-JS)
    │   │   └─ index.js
    │   └─ package.json
    │
    ├─ server/                # Backend (Flask + Ariadne)
    │   ├─ services/          # Feature-based modules
    │   │   ├─ auth/          # Discord OAuth, JWT handling
    │   │   ├─ users/         # User resolvers & models
    │   │   ├─ guilds/        # Guild resolvers & models
    │   │   └─ security/      # Logging, risk collection
    │   ├─ schema/            # GraphQL typeDefs & resolvers
    │   ├─ routes/            # REST endpoints (auth/login, callback, etc.)
    │   ├─ config.py          # Settings (env vars)
    │   ├─ app.py             # Flask entrypoint
    │   ├─ requirements.txt
    │   └─ manage.py          # CLI helper (init db, runserver, etc.)
    │
    ├─ bot/                   # Discord.py bot worker
    │   ├─ cogs/              # Bot commands & events (organized by feature)
    │   ├─ utils/             # Shared helpers (db connection, logging)
    │   ├─ main.py            # Bot entrypoint
    │   └─ requirements.txt
    │
    ├─ .gitignore
    ├─ LICENSE
    ├─ PROJECT_PLAN.md
    └─ README.md

---

## Setup

### Prerequisites
- Node.js (latest LTS)
- Python 3.12+
- MongoDB Atlas (or local)
- Discord Developer App (client ID/secret + bot token)

---

### 1. Frontend (client)
    cd client
    npm install
    npm run dev
Runs React frontend at http://localhost:5173.

---

### 2. Backend (server)
    cd server
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate

    pip install -r requirements.txt
    python app.py
Runs Flask backend at http://localhost:5000.

---

### 3. Bot (bot)
    cd bot
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate

    pip install -r requirements.txt
    python main.py
Runs the Discord bot with your bot token.

---

## Environment Variables
Create a `.env` file in both **server/** and **bot/**:

    MONGO_URL=mongodb+srv://...
    JWT_SECRET=your_jwt_secret
    DISCORD_CLIENT_ID=...
    DISCORD_CLIENT_SECRET=...
    DISCORD_BOT_TOKEN=...

---

## Roadmap
- [ ] Implement Discord OAuth login
- [ ] Issue JWTs & secure sessions
- [ ] Bot joins guilds & syncs to Mongo
- [ ] Web UI for guild settings
- [ ] Audit logging

---

## License
MIT
