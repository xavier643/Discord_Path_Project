
from flask_cors import CORS
from flask import Flask
import secrets
import base64
import preload_env
from auth.auth_discord import bp as auth_bp
from routes.me import bp as me_bp
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET") or base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    CORS(app, supports_credentials=True,
         resources={r"/*": {"origins": os.environ.get("ALLOWED_ORIGIN", "*")}})
    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)
    return app


app = create_app()

env = os.getenv("ENV", "").lower()

app.config.update(
    SESSION_COOKIE_NAME=os.getenv("SESSION_COOKIE_NAME", "session"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None" if env == "prod" else "Lax",
    SESSION_COOKIE_SECURE=(env == "prod")
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
