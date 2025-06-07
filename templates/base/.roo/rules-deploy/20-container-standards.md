# Container Standards

## Dockerfile Standards

### Multi-Stage Builds

**Wrong**:
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**Right**:
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

FROM python:3.12-slim
WORKDIR /app
RUN useradd -r -u 1001 -s /bin/false appuser
COPY --from=builder /build/.venv /app/.venv
COPY --chown=appuser:appuser src/ ./src/
RUN chmod -R 555 /app
USER appuser
EXPOSE 8000
ENTRYPOINT ["/app/.venv/bin/python", "-m", "uvicorn"]
CMD ["src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Image Size Optimization

**Layer Caching Rules**:
```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
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
RUN useradd -r -u 1001 appuser
USER appuser
RUN apt-get install -y --no-install-recommends package-name
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN chmod -R 555 /app
FROM python:3.12.7-slim
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
```

**Security Scanning**:
```bash
docker build -t myapp .
trivy image --severity HIGH,CRITICAL myapp
if [ $? -ne 0 ]; then
  echo "Security vulnerabilities found"
  exit 1
fi
```

### Build Optimization

**Cache Mount for Package Managers**:
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.npm npm ci --only=production
RUN --mount=type=cache,target=/go/pkg/mod go build -o app
```

**BuildKit Features**:
```dockerfile
# syntax=docker/dockerfile:1.4
RUN <<EOF
#!/bin/bash
set -euo pipefail
apt-get update
apt-get install -y --no-install-recommends package1 package2
rm -rf /var/lib/apt/lists/*
EOF

RUN --mount=type=secret,id=github_token git clone https://$(cat /run/secrets/github_token)@github.com/private/repo
```

### Runtime Configuration

**Environment Variables**:
```dockerfile
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
```

**Resource Limits**:
```yaml
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
docker run -d --name app --restart unless-stopped --memory 512m --cpus 2.0 --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --cap-drop ALL --cap-add NET_BIND_SERVICE --security-opt no-new-privileges:true -p 127.0.0.1:8000:8000 myapp:latest
```

### Logging Standards

**Application Logs**:
```dockerfile
ENV LOG_LEVEL=info
CMD ["python", "-u", "app.py"]
ENV NODE_ENV=production
```

**Log Aggregation**:
```yaml
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
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
```

**Complex Check**:
```python
#!/usr/bin/env python3
import sys
import httpx
try:
    resp = httpx.get("http://localhost:8000/health", timeout=2)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("database", {}).get("connected"): sys.exit(1)
    if not data.get("cache", {}).get("connected"): sys.exit(2)
except Exception: sys.exit(1)
```

### Network Isolation

**Internal Services**:
```yaml
services:
  app:
    networks: [frontend, backend]
  db:
    networks: [backend]
  nginx:
    networks: [frontend]
    ports: ["80:80"]
networks:
  frontend:
  backend:
    internal: true
```

### Volume Management

**Data Persistence**:
```yaml
volumes:
  postgres_data:
    driver: local
  nginx_conf:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./nginx/conf.d
```

**Temporary Storage**:
```dockerfile
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m myapp
```

### Anti-Patterns to Avoid

1. Everything in One Layer
2. Secrets in Image
3. Running as Root
4. Using Latest Tags
5. Installing Unnecessary Tools

### Build Pipeline

```yaml
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
          MAX_SIZE=209715200
          if [ $SIZE -gt $MAX_SIZE ]; then
            echo "Image too large: $SIZE bytes"
            exit 1
          fi
```

### The Reality
Containers fail due to:
1. Laziness: FROM ubuntu when alpine works
2. Ignorance: Running as root
3. Bloat: 2GB images for 10MB code
4. Insecurity: Baked secrets, included tools
5. Complexity: Multi-service containers

Containers are process isolation:
- One process per container
- Minimal attack surface
- Immutable infrastructure
- Environment-based config
- Stdout/stderr logging