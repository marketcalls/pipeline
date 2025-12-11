# Development Guide

Guide for developing and contributing to the Flask CI/CD application.

## Development Environment Setup

### Requirements

- Python 3.11 or higher
- uv (Python package manager)
- Git
- Docker (optional, for containerized development)

### Install uv

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Initial Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/flask-cicd-app.git
cd flask-cicd-app

# Create virtual environment with uv
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install all dependencies (including dev)
uv pip install ".[dev]"
```

## Project Structure

```
flask-cicd-app/
├── app/                    # Application package
│   ├── __init__.py        # App factory
│   └── routes.py          # Route definitions
├── tests/                  # Test package
│   ├── conftest.py        # Pytest fixtures
│   └── test_routes.py     # Route tests
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD pipeline
├── Dockerfile             # Container definition
├── docker-compose.yml     # Local container orchestration
├── pyproject.toml         # Dependencies and tool config
└── run.py                 # Application entry point
```

## Running the Application

### Development Server

```bash
# Run with Flask development server
python run.py

# Or with flask command
flask --app run:app run --debug
```

### Production Server (Local)

```bash
# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 run:app
```

### Docker

```bash
# Using docker-compose
docker-compose up --build

# Using docker directly
docker build -t flask-cicd-app .
docker run -p 5000:5000 flask-cicd-app
```

## Code Style

This project uses automated code formatting and linting.

### Tools

| Tool | Purpose |
|------|---------|
| black | Code formatting |
| isort | Import sorting |
| flake8 | Linting |

### Format Code

```bash
# Format with black
black app/ tests/

# Sort imports
isort app/ tests/

# Check without modifying
black --check app/ tests/
isort --check-only app/ tests/
```

### Lint Code

```bash
# Run flake8
flake8 app/ tests/ --max-line-length=100
```

### Configuration

All tool configurations are in `pyproject.toml`:

```toml
[tool.black]
line-length = 100

[tool.isort]
profile = "black"
line_length = 100
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific test file
pytest tests/test_routes.py

# Run specific test
pytest tests/test_routes.py::test_health_check_returns_healthy
```

### Coverage

```bash
# Run with coverage
pytest --cov=app --cov-report=term-missing

# Generate HTML report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=80
```

### Writing Tests

Tests use pytest with the Flask test client:

```python
def test_example_endpoint(client):
    """Test description."""
    response = client.get("/endpoint")
    assert response.status_code == 200
    data = response.get_json()
    assert data["key"] == "expected_value"
```

## Security

### Static Analysis

```bash
# Run bandit security linter
bandit -r app/

# Check dependencies for vulnerabilities
safety check
```

### Best Practices

- Never commit secrets or credentials
- Use environment variables for configuration
- Keep dependencies updated
- Review security scan results in CI/CD

## Adding New Features

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Add Route

Edit `app/routes.py`:

```python
@main_bp.route("/api/v1/new-endpoint")
def new_endpoint():
    """Description of endpoint."""
    return jsonify({"data": "value"})
```

### 3. Add Tests

Edit `tests/test_routes.py`:

```python
def test_new_endpoint(client):
    """Test new endpoint."""
    response = client.get("/api/v1/new-endpoint")
    assert response.status_code == 200
```

### 4. Verify

```bash
# Run tests
pytest -v

# Check formatting
black --check app/ tests/
flake8 app/ tests/

# Run security scan
bandit -r app/
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add new endpoint feature"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

Open a PR on GitHub. The CI pipeline will automatically run checks.

## Debugging

### Flask Debug Mode

```bash
FLASK_DEBUG=1 python run.py
```

### Docker Logs

```bash
# View logs
docker-compose logs -f

# Enter container
docker-compose exec flask-app /bin/bash
```

## Dependency Management with uv

### Adding Dependencies

```bash
# Add production dependency - edit pyproject.toml [project.dependencies]
# Then reinstall:
uv pip install .

# Add dev dependency - edit pyproject.toml [project.optional-dependencies.dev]
# Then reinstall:
uv pip install ".[dev]"
```

### Updating Dependencies

```bash
# Update all packages
uv pip install --upgrade .

# Update specific package
uv pip install --upgrade flask
```

### Listing Installed Packages

```bash
uv pip list
```

### Creating Lock File (Optional)

```bash
# Generate requirements.txt from current environment
uv pip freeze > requirements.lock
```

## uv vs pip Comparison

| Task | pip | uv |
|------|-----|-----|
| Create venv | `python -m venv .venv` | `uv venv` |
| Install package | `pip install flask` | `uv pip install flask` |
| Install from pyproject.toml | `pip install .` | `uv pip install .` |
| Install with extras | `pip install ".[dev]"` | `uv pip install ".[dev]"` |
| List packages | `pip list` | `uv pip list` |
| Freeze | `pip freeze` | `uv pip freeze` |

uv is 10-100x faster than pip for most operations.
