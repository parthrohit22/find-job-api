from flask import Flask
from routes.health import health_bp
from routes.jobs import jobs_bp

app = Flask(__name__)
app.register_blueprint(health_bp)
app.register_blueprint(jobs_bp)

if __name__ == "__main__":
    app.run(debug=True)