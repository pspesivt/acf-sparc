# Container Standards
## Dockerfile Standards
### Multi-Stage Builds
Wrong:```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python","app.py"]
```
Right:```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update&&apt-get install -y --no-install-recommends gcc&&rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
RUN pip install uv&&uv sync --frozen --no-dev

FROM python:3.12-slim
WORKDIR /app
RUN useradd -r -u1001 -s /bin/false appuser
COPY --from=builder /build/.venv /app/.venv
COPY --chown=appuser:appuser src/ ./src/
RUN chmod -R 555 /app
USER appuser
EXPOSE 8000
ENTRYPOINT ["/app/.venv/bin/python","-m","uvicorn"]
CMD ["src.main:app","--host","0.0.0.0","--port","8000"]
```
### Image Size Optimization
Layer Caching:```dockerfile
FROM python:3.12-slim
RUN apt-get update&&apt-get install -y --no-install-recommends libpq5&&rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
```
Size Targets:Python:python:3.12-slim<150MB/200MB;Node:node:20-alpine<100MB/150MB;Go:scratch<20MB/50MB;Static:nginx:alpine<30MB/50MB
### Security Standards
Checklist:```dockerfile
FROM python:3.12.7-slim
RUN useradd -r -u1001 appuser
USER appuser
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN chmod -R 555 /app
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health||exit 1
```
Scanning:```bash
docker build -t myapp .
trivy image --severity HIGH,CRITICAL myapp||exit 1
```
### Build Optimization
Cache Mounts:```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.npm npm ci --only=production
RUN --mount=type=cache,target=/go/pkg/mod go build -o app
```
BuildKit:```dockerfile
#syntax=docker/dockerfile:1.4
RUN <<EOF
set -euo pipefail
apt-get update&&apt-get install -y --no-install-recommends package1 package2&&rm -rf /var/lib/apt/lists/*
EOF
RUN --mount=type=secret,id=github_token git clone https://$(cat /run/secrets/github_token)@github.com/private/repo
```
### Runtime Configuration
Env:```dockerfile
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
```
Resources:```yaml
services:
  app:
    deploy:
      resources:
        limits:{cpus:'2.0',memory:512M}
        reservations:{cpus:'0.5',memory:256M}
```
Run:```bash
docker run -d --name app --restart unless-stopped --memory 512m --cpus 2.0 --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --cap-drop ALL --cap-add NET_BIND_SERVICE --security-opt no-new-privileges:true -p 127.0.0.1:8000:8000 myapp:latest
```
### Logging Standards
App:```dockerfile
ENV LOG_LEVEL=info
CMD ["python","-u","app.py"]
ENV NODE_ENV=production
```
Aggregation:```yaml
services:
  app:
    logging:{driver:"json-file",options:{max-size:"10m",max-file:"3",labels:"app_name,environment"}}
```
### Health Check Patterns
Simple:```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD curl -f http://localhost:8000/health||exit 1
```
Complex:```python
import sys,httpx
try:
 r=httpx.get("http://localhost:8000/health",timeout=2);r.raise_for_status()
 d=r.json()
 bool(d["database"]["connected"]) or sys.exit(1)
 bool(d["cache"]["connected"]) or sys.exit(2)
except:sys.exit(1)
```
### Network Isolation
```yaml
services:
  app:     networks:[frontend,backend]
  db:      networks:[backend]
  nginx:   networks:[frontend],ports:["80:80"]
networks:{frontend:{},backend:{internal:true}}
```
### Volume Management
Data:```yaml
volumes:{postgres_data:{driver:local},nginx_conf:{driver:local,driver_opts:{type:none,o:bind,device:./nginx/conf.d}}}
```
Tmp:```bash
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m myapp
```
### Anti-Patterns to Avoid
1:```dockerfile
RUN apt-get update&&apt-get install -y python3&&pip install -r requirements.txt&&cp config.json /etc/
```
2:```dockerfile
ENV API_KEY=secret123
COPY .env /app/
```
3:```dockerfile
USER root
CMD ["python","app.py"]
```
4:```dockerfile
FROM ubuntu:latest
```
5:```dockerfile
RUN apt-get install -y vim curl wget git make gcc
```
### Build Pipeline
```yaml
name:Docker Build
on:[push]
jobs:
  build:
    runs-on:ubuntu-latest
    steps:
    - uses:actions/checkout@v4
    - name:Set up Docker Buildx    uses:docker/setup-buildx-action@v3
    - run:|
        docker build --target production -t app:${{github.sha}} .
        trivy image --exit-code 1 --severity HIGH,CRITICAL app:${{github.sha}}
    - run:|
        S=$(docker image inspect app:${{github.sha}} --format='{{.Size}}');M=209715200;[ $S -gt $M ]&&exit 1
```
### The Reality
Laziness:FROM ubuntu vs alpine  
Ignorance:root  
Bloat:2GB for 10MB code  
Insecurity:secrets/tools included  
Complexity:multi-service  
One process/container;minimal attack surface;immutable infra;env config;stdout/stderr logging