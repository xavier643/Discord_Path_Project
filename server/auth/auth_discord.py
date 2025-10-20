# server/auth_discord.py
import os
import time
import secrets
import base64
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
import requests
from flask import Blueprint, session, request, redirect, jsonify
from db import users_col
from functools import wraps
from db import users_col

bp = Blueprint("auth", __name__)
API = "https://discord.com/api/v10"


def cfg():
    """Read env at call-time (no stale globals)."""
    return {
        "DISCORD_CLIENT_ID":     os.getenv("DISCORD_CLIENT_ID", ""),
        "DISCORD_CLIENT_SECRET": os.getenv("DISCORD_CLIENT_SECRET", ""),
        "DISCORD_REDIRECT_URI":  os.getenv("DISCORD_REDIRECT_URI", ""),
        "DISCORD_BOT_TOKEN":     os.getenv("DISCORD_BOT_TOKEN", ""),
        "POST_LOGIN_REDIRECT": os.getenv("POST_LOGIN_REDIRECT", "/"),
    }


def _bot_guild_ids():
    C = cfg()
    h = {"Authorization": f"Bot {C['DISCORD_BOT_TOKEN']}"}
    r = requests.get(f"{API}/users/@me/guilds", headers=h, timeout=15)
    r.raise_for_status()
    return {g["id"] for g in r.json()}


def _user_token(code: str):
    C = cfg()
    data = {
        "client_id": C['DISCORD_CLIENT_ID'],
        "client_secret": C['DISCORD_CLIENT_SECRET'],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": C['DISCORD_REDIRECT_URI'],
    }
    r = requests.post(f"{API}/oauth2/token", data=data, timeout=15)
    r.raise_for_status()
    return r.json()


def _me(token: str):
    h = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API}/users/@me", headers=h, timeout=15)
    r.raise_for_status()
    return r.json()


def _me_guilds(token: str):
    h = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API}/users/@me/guilds", headers=h, timeout=15)
    r.raise_for_status()
    return r.json()


def login_required(fn):
    C = cfg()

    @wraps(fn)
    def inner(*a, **k):
        if "access_token" not in session or "user" not in session:
            return jsonify({"error": "unauthorized"}), 401
        return fn(*a, **k)
    return inner


@bp.get("/auth/discord/login")
def login():
    C = cfg()
    # quick sanity: make sure we actually have a client id
    if not C['DISCORD_CLIENT_ID']:
        return jsonify({"error": "server_misconfig", "missing": "DISCORD_CLIENT_ID"}), 500

    # (temporary) print so you can see it in the server console
    print(f"[oauth] client_id={C['DISCORD_CLIENT_ID']!r} redirect={C['DISCORD_REDIRECT_URI']!r}")

    state = secrets.token_urlsafe(24)
    session["oauth_state"] = state
    params = {
        "client_id": C['DISCORD_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": C['DISCORD_REDIRECT_URI'],
        "scope": "identify guilds",
        "state": state,
        "prompt": "none",
    }
    return redirect(f"https://discord.com/oauth2/authorize?{urlencode(params)}", 302)


@bp.get("/auth/discord/callback")
def callback():
    if request.args.get("state") != session.get("oauth_state"):
        return jsonify({"error": "invalid_state"}), 400
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "missing_code"}), 400

    tok = _user_token(code)
    access = tok["access_token"]
    user = _me(access)
    ug = _me_guilds(access)
    user_guild_ids = {g["id"] for g in ug}
    allowed = user_guild_ids & _bot_guild_ids()
    if not allowed:
        session.clear()
        return jsonify({"error": "forbidden", "message": "No shared bot guilds"}), 403

    if users_col is not None:
        users_col.update_one(
            {"discord_id": user["id"]},
            {"$set": {
                "discord_id": user["id"],
                "username": user.get("username"),
                "global_name": user.get("global_name"),
                "discriminator": user.get("discriminator"),
                "avatar": user.get("avatar"),
                "last_login": __import__("datetime").datetime.now(__import__("datetime").timezone.utc),
                "allowed_guild_ids": list(allowed)
            }},
            upsert=True
        )

    session["access_token"] = access
    session["user"] = {"id": user["id"], "username": user.get("username")}
    return redirect(cfg()["POST_LOGIN_REDIRECT"], 302)


@bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
