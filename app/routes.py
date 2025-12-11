from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Root endpoint returning welcome message."""
    return jsonify({"message": "Welcome to Flask CI/CD Pipeline", "status": "running"})


@main_bp.route("/health")
def health():
    """Health check endpoint for container orchestration."""
    return jsonify({"status": "healthy"}), 200


@main_bp.route("/api/v1/info")
def info():
    """API info endpoint."""
    return jsonify({
        "app": "Flask CI/CD Demo",
        "version": "1.0.0",
        "endpoints": ["/", "/health", "/api/v1/info"],
    })
