# Setup Guide

Complete guide for setting up the Flask CI/CD pipeline.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- GitHub account
- Docker Hub account

## Step 1: Clone and Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/flask-cicd-app.git
cd flask-cicd-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## Step 2: Verify Local Setup

```bash
# Run tests
pytest -v

# Run the application
python run.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/info
```

## Step 3: Docker Hub Setup

### Create Access Token

1. Log in to [Docker Hub](https://hub.docker.com)
2. Go to **Account Settings** > **Security**
3. Click **New Access Token**
4. Name: `github-actions` (or any descriptive name)
5. Permissions: **Read, Write, Delete**
6. Click **Generate**
7. Copy the token immediately (you won't see it again)

## Step 4: GitHub Repository Setup

### Create Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `flask-cicd-app` (or your preferred name)
3. Keep it empty (no README, .gitignore, or license)

### Push Code

```bash
git init
git add .
git commit -m "Initial commit: Flask app with CI/CD pipeline"
git remote add origin https://github.com/YOUR_USERNAME/flask-cicd-app.git
git branch -M main
git push -u origin main
```

### Add Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Name | Value |
|------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | The access token from Step 3 |

## Step 5: Verify Pipeline

1. Make a small change to any file
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push
   ```
3. Go to **Actions** tab in your GitHub repository
4. Watch the pipeline execute

### Expected Pipeline Flow

```
Lint ─────┐
Security ─┼─> Build & Push ─> Docker Hub
Test ─────┘
```

## Step 6: Pull and Run from Docker Hub

After successful pipeline:

```bash
# Pull the image
docker pull YOUR_USERNAME/flask-cicd-app:latest

# Run the container
docker run -p 5000:5000 YOUR_USERNAME/flask-cicd-app:latest

# Verify
curl http://localhost:5000/health
```

## Troubleshooting

### Pipeline Fails at Lint Stage

```bash
# Fix formatting locally
black app/ tests/
isort app/ tests/

# Check linting
flake8 app/ tests/ --max-line-length=100
```

### Pipeline Fails at Test Stage

```bash
# Run tests locally with coverage
pytest --cov=app --cov-report=term-missing

# Ensure 80% coverage minimum
```

### Docker Build Fails

```bash
# Test build locally
docker build -t test-build .

# Check for errors in Dockerfile
```

### Authentication Errors

- Verify `DOCKERHUB_USERNAME` is correct (case-sensitive)
- Regenerate Docker Hub access token if expired
- Ensure token has write permissions

## Next Steps

- [API Documentation](API.md)
- [Development Guide](DEVELOPMENT.md)
- [Deployment Guide](DEPLOYMENT.md)
