# server/db.py
import os
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING

SKIP_MONGO = os.getenv("SKIP_MONGO", "1") == "1"  # default: skip while testing

if SKIP_MONGO:
    # Stubs so other files can import without blowing up
    db = None
    users_col = None
    guilds_col = None
    sessions_col = None
    items_col = None
else:
    MONGO_URL = os.environ["MONGO_URL"]
    DB_NAME = os.environ.get("MONGO_DB", "discord_path")

    _client = MongoClient(MONGO_URL, uuidRepresentation="standard", serverSelectionTimeoutMS=2000)
    db = _client[DB_NAME]

    users_col = db["users"]
    guilds_col = db["guilds"]
    sessions_col = db["sessions"]
    items_col = db["items"]

    # Only attempt indexes when a server responds
    try:
        _client.admin.command("ping")
        users_col.create_index([("discord_id", ASCENDING)], unique=True)
        guilds_col.create_index([("guild_id", ASCENDING)], unique=True)
        items_col.create_index([("guild_id", ASCENDING), ("created_at", ASCENDING)])
    except Exception:
        pass
