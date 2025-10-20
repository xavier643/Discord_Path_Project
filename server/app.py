
import os
from routes.me import bp as me_bp
from auth.auth_discord import bp as auth_bp
import os
import base64
import secrets
from flask import Flask
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name('.env'), override=False)
print("[debug] DISCORD_CLIENT_ID from env:", os.getenv("DISCORD_CLIENT_ID"))


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET") or base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    CORS(app, supports_credentials=True,
         resources={r"/*": {"origins": os.environ.get("ALLOWED_ORIGIN", "*")}})
    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)
    return app


app = create_app()

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("ENV", "dev") == "prod"  # True in prod (https)
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
