# server/routes/me.py

import os
from flask import Blueprint, jsonify, session
from auth.auth_discord import login_required, _me_guilds, _me_member, _guild_roles_bot
from db import users_col

import requests
import sys

bp = Blueprint("me", __name__)


def cfg():
    """Read env at call-time (no stale globals)."""
    return {
        "DISCORD_GUILD_ID": os.getenv("DISCORD_GUILD_ID", ""),
    }


@bp.get("/me")
@login_required
def me():
    try:
        ipv4 = requests.get("https://api.ipify.org").text
        print(f"[DEBUG] Egress IPv4: {ipv4}", file=sys.stderr)
    except Exception as e:
        print(f"[DEBUG] Failed to get IPv4: {e}", file=sys.stderr)

    access = session["access_token"]
    user_guilds = _me_guilds(access)

    target_guild_id = cfg().get("DISCORD_GUILD_ID")
    if not target_guild_id:
        return jsonify({"error": "DISCORD_GUILD_ID is not set"}), 500

    match = next((g for g in user_guilds if g.get("id") == target_guild_id), None)
    authorized = match is not None

    guild = None
    if match:
        guild = {"id": match.get("id"), "name": match.get("name")}

    # Optional: keep status in DB
    if users_col is not None:
        users_col.update_one(
            {"discord_id": session["user"]["id"]},
            {"$set": {"is_member": authorized, "guild_id": target_guild_id}},
            upsert=True
        )

    is_owner = False

    if match:
        is_owner = bool(match.get("owner"))  # comes from /users/@me/guilds entries
        member = _me_member(access, target_guild_id)

    roles = []

    if authorized:
        if not member:
            return jsonify({
                "user": session["user"],
                "authorized": True,
                "guild": {"id": target_guild_id},
                "roles": [],
                "error": "member_fetch_failed"
            }), 200

        role_ids = set(member.get("roles", [])) if member else set()

        all_roles = _guild_roles_bot(target_guild_id)

        roles = [
            {"id": r["id"], "name": r["name"], "position": r["position"]}
            for r in all_roles
            if r["id"] in role_ids
        ]

    return jsonify({
        "user": session["user"],
        "authorized": authorized,
        "guild": guild,
        "is_owner": is_owner,
        "roles": roles,
    })
