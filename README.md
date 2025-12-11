# Flask CI/CD Pipeline

A production-ready Flask application with automated CI/CD pipeline that builds, tests, and deploys to Docker Hub.

## Features

- Flask REST API with health check endpoints
- Dockerized application with security best practices
- GitHub Actions CI/CD pipeline
- Automated testing with pytest
- Code quality checks (flake8, black, isort)
- Security scanning (bandit, safety, trivy)
- Automatic Docker Hub deployment

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask app factory
│   └── routes.py            # API endpoints
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── test_routes.py       # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline
├── Dockerfile               # Production container
├── docker-compose.yml       # Local development
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── run.py                   # Application entry point
└── pyproject.toml           # Tool configurations
```

## Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-dev.txt

# Run the application
python run.py
```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build manually
docker build -t flask-cicd-app .
docker run -p 5000:5000 flask-cicd-app
```

The application will be available at `http://localhost:5000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check for container orchestration |
| `/api/v1/info` | GET | Application information |

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Linting
flake8 app/ tests/

# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Security scan
bandit -r app/
```

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push and pull request to `main`/`master`:

### Pipeline Stages

1. **Lint** - Code quality checks
   - flake8 linting
   - black formatting verification
   - isort import ordering

2. **Security** - Vulnerability scanning
   - bandit static analysis
   - safety dependency check

3. **Test** - Unit tests
   - pytest with coverage
   - Minimum 80% coverage required

4. **Build & Push** - Docker deployment (main branch only)
   - Build Docker image
   - Push to Docker Hub
   - Trivy vulnerability scan

### Setup Requirements

Add these secrets to your GitHub repository:

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

## Docker Hub

After successful pipeline execution, the image is available at:

```bash
docker pull YOUR_USERNAME/flask-cicd-app:latest
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |

### Tool Configuration

Tool configurations are in `pyproject.toml`:
- black (code formatting)
- isort (import sorting)
- pytest (testing)
- bandit (security)

## License

MIT License
