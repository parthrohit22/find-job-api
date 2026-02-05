from flask import Flask
from flasgger import Swagger
from routes.health import health_bp
from routes.jobs import jobs_bp

app = Flask(__name__)

# Initialize Swagger ONCE
swagger = Swagger(app)

# Register blueprints AFTER Swagger
app.register_blueprint(health_bp)
app.register_blueprint(jobs_bp)

if __name__ == "__main__":
    # 🔑 Disable reloader to prevent double Swagger registration
    app.run(debug=True, use_reloader=False)