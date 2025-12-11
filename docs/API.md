# API Documentation

Complete API reference for the Flask CI/CD application.

## Base URL

```
http://localhost:5000
```

## Endpoints

### Root Endpoint

Returns a welcome message and application status.

**Request**
```
GET /
```

**Response**
```json
{
  "message": "Welcome to Flask CI/CD Pipeline",
  "status": "running"
}
```

**Status Codes**
| Code | Description |
|------|-------------|
| 200 | Success |

**Example**
```bash
curl http://localhost:5000/
```

---

### Health Check

Health check endpoint for container orchestration and load balancers.

**Request**
```
GET /health
```

**Response**
```json
{
  "status": "healthy"
}
```

**Status Codes**
| Code | Description |
|------|-------------|
| 200 | Application is healthy |

**Example**
```bash
curl http://localhost:5000/health
```

**Use Cases**
- Kubernetes liveness/readiness probes
- Docker health checks
- Load balancer health checks
- Monitoring systems

---

### Application Info

Returns application metadata and available endpoints.

**Request**
```
GET /api/v1/info
```

**Response**
```json
{
  "app": "Flask CI/CD Demo",
  "version": "1.0.0",
  "endpoints": ["/", "/health", "/api/v1/info"]
}
```

**Status Codes**
| Code | Description |
|------|-------------|
| 200 | Success |

**Example**
```bash
curl http://localhost:5000/api/v1/info
```

---

## Error Responses

### 404 Not Found

Returned when accessing non-existent endpoints.

**Response**
```json
{
  "error": "Not Found"
}
```

### 500 Internal Server Error

Returned when an unexpected error occurs.

**Response**
```json
{
  "error": "Internal Server Error"
}
```

---

## Response Headers

All responses include:

| Header | Value |
|--------|-------|
| Content-Type | application/json |

---

## Testing with cURL

```bash
# Test all endpoints
curl -s http://localhost:5000/ | jq
curl -s http://localhost:5000/health | jq
curl -s http://localhost:5000/api/v1/info | jq

# Test with headers
curl -v http://localhost:5000/health
```

## Testing with Python

```python
import requests

base_url = "http://localhost:5000"

# Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# App info
response = requests.get(f"{base_url}/api/v1/info")
print(response.json())
```
