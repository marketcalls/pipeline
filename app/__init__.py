from flask import Flask


def create_app(config_name=None):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)

    if config_name == "testing":
        app.config["TESTING"] = True

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
