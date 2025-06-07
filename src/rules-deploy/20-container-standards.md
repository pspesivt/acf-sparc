# Container Standards

Your containers are bloated security disasters. Fix them.

## Dockerfile Standards

### Multi-Stage Builds

**Wrong** (your current garbage):
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
2GB image, root user, build tools in production. Amateur hour.

**Right**:
```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build

# Install build deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim
WORKDIR /app

# Security: non-root user
RUN useradd -r -u 1001 -s /bin/false appuser

# Copy only runtime deps
COPY --from=builder /build/.venv /app/.venv
COPY --chown=appuser:appuser src/ ./src/

# Security: read-only root filesystem
RUN chmod -R 555 /app

USER appuser
EXPOSE 8000

# No shell, direct exec
ENTRYPOINT ["/app/.venv/bin/python", "-m", "uvicorn"]
CMD ["src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Image Size Optimization

**Layer Caching Rules**:
```dockerfile
# Order: least to most frequently changing

# 1. Base image (changes rarely)
FROM python:3.12-slim

# 2. System dependencies (changes monthly)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 3. Python dependencies (changes weekly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Application code (changes daily)
COPY src/ ./src/
```

**Size Targets**:
| Language | Base Image | Target Size | Max Size |
|----------|------------|-------------|----------|
| Python | python:3.12-slim | < 150MB | 200MB |
| Node.js | node:20-alpine | < 100MB | 150MB |
| Go | scratch | < 20MB | 50MB |
| Static | nginx:alpine | < 30MB | 50MB |

### Security Standards

**Mandatory Security Checklist**:
```dockerfile
# ✓ Non-root user
RUN useradd -r -u 1001 appuser
USER appuser

# ✓ No sudo/su
# Never install sudo. Period.

# ✓ Minimal packages
RUN apt-get install -y --no-install-recommends package-name

# ✓ Clean package cache
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ✓ Read-only filesystem
RUN chmod -R 555 /app

# ✓ No secrets in image
# Use runtime environment variables

# ✓ Specific versions
FROM python:3.12.7-slim  # Not :latest

# ✓ Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Security Scanning**:
```bash
# Scan during build
docker build -t myapp .
trivy image --severity HIGH,CRITICAL myapp

# Block if vulnerabilities found
if [ $? -ne 0 ]; then
  echo "Security vulnerabilities found"
  exit 1
fi
```

### Build Optimization

**Cache Mount for Package Managers**:
```dockerfile
# Python with pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Node with npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Go with module cache
RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o app
```

**BuildKit Features**:
```dockerfile
# syntax=docker/dockerfile:1.4

# Heredocs for complex scripts
RUN <<EOF
#!/bin/bash
set -euo pipefail
apt-get update
apt-get install -y --no-install-recommends \
    package1 \
    package2
rm -rf /var/lib/apt/lists/*
EOF

# Secret mounting (never bake into image)
RUN --mount=type=secret,id=github_token \
    git clone https://$(cat /run/secrets/github_token)@github.com/private/repo
```

### Runtime Configuration

**Environment Variables**:
```dockerfile
# Build-time defaults only
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Runtime config via docker run
# docker run -e DATABASE_URL=xxx myapp
```

**Resource Limits**:
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

**Production Run**:
```bash
docker run -d \
  --name app \
  --restart unless-stopped \
  --memory 512m \
  --cpus 2.0 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  -p 127.0.0.1:8000:8000 \
  myapp:latest
```

### Logging Standards

**Application Logs**:
```dockerfile
# Log to stdout/stderr only
ENV LOG_LEVEL=info

# Python
CMD ["python", "-u", "app.py"]  # -u for unbuffered

# Node.js
ENV NODE_ENV=production
```

**Log Aggregation**:
```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "app_name,environment"
```

### Health Check Patterns

**Simple HTTP**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Complex Check**:
```python
# healthcheck.py
#!/usr/bin/env python3
import sys
import httpx

try:
    # Check API
    resp = httpx.get("http://localhost:8000/health", timeout=2)
    resp.raise_for_status()
    
    # Check database
    data = resp.json()
    if not data.get("database", {}).get("connected"):
        sys.exit(1)
        
    # Check redis
    if not data.get("cache", {}).get("connected"):
        sys.exit(2)
        
except Exception:
    sys.exit(1)
```

### Network Isolation

**Internal Services**:
```yaml
# docker-compose.yml
services:
  app:
    networks:
      - frontend
      - backend
  
  db:
    networks:
      - backend  # No frontend access
  
  nginx:
    networks:
      - frontend
    ports:
      - "80:80"  # Only nginx exposed

networks:
  frontend:
  backend:
    internal: true  # No external access
```

### Volume Management

**Data Persistence**:
```yaml
volumes:
  # Named volumes for data
  postgres_data:
    driver: local
  
  # Bind mounts for config
  nginx_conf:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./nginx/conf.d
```

**Temporary Storage**:
```dockerfile
# Use tmpfs for ephemeral data
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m myapp
```

### Anti-Patterns to Avoid

**1. Everything in One Layer**:
```dockerfile
# WRONG - No cache reuse
RUN apt-get update && \
    apt-get install -y python3 && \
    pip install -r requirements.txt && \
    cp config.json /etc/
```

**2. Secrets in Image**:
```dockerfile
# WRONG - Visible in history
ENV API_KEY=secret123
COPY .env /app/
```

**3. Running as Root**:
```dockerfile
# WRONG - Security nightmare
USER root
CMD ["python", "app.py"]
```

**4. Using Latest Tags**:
```dockerfile
# WRONG - Non-reproducible
FROM ubuntu:latest
```

**5. Installing Unnecessary Tools**:
```dockerfile
# WRONG - Attack surface
RUN apt-get install -y vim curl wget git make gcc
```

### Build Pipeline

```yaml
# .github/workflows/docker.yml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Build and scan
        run: |
          docker build --target production -t app:${{ github.sha }} .
          trivy image --exit-code 1 --severity HIGH,CRITICAL app:${{ github.sha }}
      
      - name: Size check
        run: |
          SIZE=$(docker image inspect app:${{ github.sha }} --format='{{.Size}}')
          MAX_SIZE=209715200  # 200MB
          if [ $SIZE -gt $MAX_SIZE ]; then
            echo "Image too large: $SIZE bytes"
            exit 1
          fi
```

### The Reality

Your containers fail because:
1. **Laziness**: FROM ubuntu when alpine works
2. **Ignorance**: Running as root "because it's easier"
3. **Bloat**: 2GB images for 10MB of code
4. **Insecurity**: Secrets baked in, tools included
5. **Complexity**: Multi-service containers

Containers aren't VMs. They're process isolation. Treat them that way:
- One process per container
- Minimal attack surface
- Immutable infrastructure
- Environment-based config
- Stdout/stderr logging

Follow these standards or ship vulnerable bloatware. Your choice.
