# server/routes/me.py
from flask import Blueprint, jsonify, session
from auth.auth_discord import login_required, _me_guilds, _bot_guild_ids
from db import users_col

import requests
import sys

bp = Blueprint("me", __name__)


@bp.get("/me")
@login_required
def me():
    try:
        ipv4 = requests.get("https://api.ipify.org").text
        print(f"[DEBUG] Egress IPv4: {ipv4}", file=sys.stderr)
    except Exception as e:
        print(f"[DEBUG] Failed to get IPv4: {e}", file=sys.stderr)
    # Pull fresh guilds, filter by bot guilds, return minimal data
    access = session["access_token"]
    user_guilds = _me_guilds(access)
    allowed_ids = _bot_guild_ids() & {g["id"] for g in user_guilds}
    filtered = [{"id": g["id"], "name": g["name"]} for g in user_guilds if g["id"] in allowed_ids]

    # Optionally keep allowed guilds current in DB
    if users_col is not None:
        users_col.update_one(
            {"discord_id": session["user"]["id"]},
            {"$set": {"allowed_guild_ids": [g["id"] for g in filtered]}},
            upsert=True
        )

    return jsonify({
        "user": session["user"],
        "authorized_guilds": filtered
    })
