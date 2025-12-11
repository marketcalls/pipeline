# Deployment Guide

Guide for deploying the Flask application to various environments.

## Docker Hub Deployment

The CI/CD pipeline automatically deploys to Docker Hub on pushes to `main`/`master`.

### Image Tags

| Tag | Description |
|-----|-------------|
| `latest` | Most recent build from main branch |
| `<sha>` | Specific commit SHA |

### Pull and Run

```bash
# Pull latest image
docker pull YOUR_USERNAME/flask-cicd-app:latest

# Run container
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  --restart unless-stopped \
  YOUR_USERNAME/flask-cicd-app:latest
```

## Deployment Options

### Docker Compose (Simple)

For single-server deployments:

```yaml
# docker-compose.prod.yml
version: "3.8"

services:
  flask-app:
    image: YOUR_USERNAME/flask-cicd-app:latest
    ports:
      - "80:5000"
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

Example Kubernetes manifests:

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: YOUR_USERNAME/flask-cicd-app:latest
        ports:
        - containerPort: 5000
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### AWS ECS

Task definition example:

```json
{
  "family": "flask-app",
  "containerDefinitions": [
    {
      "name": "flask-app",
      "image": "YOUR_USERNAME/flask-cicd-app:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      },
      "memory": 256,
      "cpu": 256
    }
  ]
}
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name flask-app \
  --image YOUR_USERNAME/flask-cicd-app:latest \
  --ports 5000 \
  --dns-name-label flask-app-demo
```

### Google Cloud Run

```bash
gcloud run deploy flask-app \
  --image YOUR_USERNAME/flask-cicd-app:latest \
  --port 5000 \
  --allow-unauthenticated
```

## Environment Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |

### Secrets Management

For production, use your platform's secrets management:

- **Kubernetes**: Secrets or external secrets operator
- **AWS**: Secrets Manager or Parameter Store
- **Azure**: Key Vault
- **GCP**: Secret Manager

## Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        proxy_pass http://flask_app/health;
        access_log off;
    }
}
```

## SSL/TLS

### Using Certbot

```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Obtain certificate
certbot --nginx -d your-domain.com
```

### Using Traefik

```yaml
# docker-compose with Traefik
version: "3.8"

services:
  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=your@email.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./letsencrypt:/letsencrypt

  flask-app:
    image: YOUR_USERNAME/flask-cicd-app:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.flask.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.flask.tls.certresolver=letsencrypt"
```

## Monitoring

### Health Checks

The `/health` endpoint returns:
```json
{"status": "healthy"}
```

Use this for:
- Load balancer health checks
- Container orchestration probes
- Uptime monitoring services

### Logging

Container logs are available via:

```bash
# Docker
docker logs flask-app

# Kubernetes
kubectl logs deployment/flask-app

# Docker Compose
docker-compose logs -f flask-app
```

## Rollback

### Docker

```bash
# Pull specific version
docker pull YOUR_USERNAME/flask-cicd-app:<previous-sha>

# Stop current container
docker stop flask-app

# Start with previous version
docker run -d --name flask-app -p 5000:5000 YOUR_USERNAME/flask-cicd-app:<previous-sha>
```

### Kubernetes

```bash
# View rollout history
kubectl rollout history deployment/flask-app

# Rollback to previous version
kubectl rollout undo deployment/flask-app

# Rollback to specific revision
kubectl rollout undo deployment/flask-app --to-revision=2
```
