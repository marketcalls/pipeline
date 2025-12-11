"""Tests for Flask application routes."""


def test_index_returns_welcome_message(client):
    """Test root endpoint returns correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome to Flask CI/CD Pipeline"
    assert data["status"] == "running"


def test_health_check_returns_healthy(client):
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_info_endpoint_returns_app_info(client):
    """Test info endpoint returns application information."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "Flask CI/CD Demo"
    assert data["version"] == "1.0.0"
    assert "/" in data["endpoints"]
    assert "/health" in data["endpoints"]


def test_nonexistent_route_returns_404(client):
    """Test that non-existent routes return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
