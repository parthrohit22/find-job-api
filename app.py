from pathlib import Path
import logging
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv

from routes.health import health_bp
from routes.jobs import jobs_bp


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


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

    app.register_blueprint(health_bp)
    app.register_blueprint(jobs_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)