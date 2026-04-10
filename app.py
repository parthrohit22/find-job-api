from pathlib import Path
import logging
import os
from flask import Flask, send_from_directory
from flasgger import Swagger
from dotenv import load_dotenv

from routes.auth import auth_bp
from routes.health import health_bp
from routes.jobs import jobs_bp
from services.user_store import init_user_db


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist" / "frontend" / "browser"
env_path = BASE_DIR / ".env"
load_dotenv(env_path)
APP_PORT = int(os.getenv("APP_PORT", "5001"))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def create_app():
    app = Flask(__name__)

    app.config["SWAGGER"] = {
        "title": "Job Search API",
        "uiversion": 3
    }

    Swagger(app)
    init_user_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(jobs_bp)

    register_frontend_routes(app)

    return app


def register_frontend_routes(app: Flask):
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def frontend(path: str):
        if path == "api" or path.startswith(("api/", "auth/", "health", "apidocs", "flasgger_static")):
            return {"error": "not found"}, 404

        if FRONTEND_DIST.exists():
            asset_path = FRONTEND_DIST / path

            if path and asset_path.is_file():
                return send_from_directory(FRONTEND_DIST, path)

            return send_from_directory(FRONTEND_DIST, "index.html")

        if not path:
            return {
                "status": "API alive",
                "frontend": "build not found",
                "message": "Run the Angular build to serve the frontend from Flask."
            }

        return {"error": "not found"}, 404


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=APP_PORT)
