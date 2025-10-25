# server/auth_discord.py
import os
import time
import secrets
import base64
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
import requests
from flask import Blueprint, session, request, redirect, jsonify, current_app, make_response
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


def _user_token(code: str):
    r = requests.post(
        "https://discord.com/api/v10/oauth2/token",
        data={
            "client_id": cfg()["DISCORD_CLIENT_ID"],
            "client_secret": cfg()["DISCORD_CLIENT_SECRET"],
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": cfg()["DISCORD_REDIRECT_URI"],  # MUST match auth step exactly
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    if r.status_code != 200:
        current_app.logger.error(
            "discord token exchange failed",
            extra={"status": r.status_code, "body": r.text[:500]},
        )
        return None
    return r.json()


def _bot_guild_ids():
    C = cfg()
    h = {"Authorization": f"Bot {C['DISCORD_BOT_TOKEN']}"}
    r = requests.get(f"{API}/users/@me/guilds", headers=h, timeout=15)
    r.raise_for_status()
    return {g["id"] for g in r.json()}


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
    # 1) validate and CONSUME state
    if request.args.get("state") != session.get("oauth_state"):
        current_app.logger.warning("oauth_state mismatch", extra={"got": request.args.get("state"), "expected": session.get("oauth_state")})
        return jsonify({"error": "invalid_state"}), 400
    session.pop("oauth_state", None)  # important: consume

    code = request.args.get("code")
    if not code:
        return jsonify({"error": "missing_code"}), 400

    token_json = _user_token(code)
    if token_json is None:
        # don’t 500; bounce back with an error flag so UI can show a message
        return redirect(f'{cfg()["POST_LOGIN_REDIRECT"]}?auth=failed', 302)

    try:
        token = token_json.get("access_token")

        # 3) fetch user
        user_resp = requests.get("https://discord.com/api/users/@me",
                                 headers={"Authorization": f"Bearer {token}"},
                                 timeout=10)
        if user_resp.status_code != 200:
            current_app.logger.error("discord user fetch failed",
                                     extra={"status": user_resp.status_code, "body": safe_body(user_resp)})
            return redirect(f'{cfg()["POST_LOGIN_REDIRECT"]}?auth=failed', 302)

        user = user_resp.json()

        # 4) set session and redirect
        session["user"] = {"id": user["id"], "username": user["username"]}
        session["access_token"] = token
        return redirect(cfg()["POST_LOGIN_REDIRECT"], 302)

    except Exception as e:
        current_app.logger.exception("oauth callback exception")
        return redirect(f'{cfg()["POST_LOGIN_REDIRECT"]}?auth=failed', 302)


def safe_body(resp):
    # helper to avoid logging secrets; trims big payloads
    try:
        txt = resp.text
        return txt[:500]
    except Exception:
        return "<unreadable>"


@bp.get("/logout")
@bp.post("/logout")
def logout():
    session.clear()

    # mirror cookie attributes by environment
    env = os.getenv("ENV", "").lower()
    samesite = "None" if env == "prod" else "Lax"
    secure = (env == "prod")

    resp = redirect(cfg()["POST_LOGIN_REDIRECT"], 302)
    resp.delete_cookie(
        key=current_app.session_cookie_name,
        path="/",
        httponly=True,
        samesite=samesite,
        secure=secure,
    )
    return resp
