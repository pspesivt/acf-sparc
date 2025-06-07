# GitHub Actions Templates

Your pipelines are slow garbage. Here's what actually works.

## Base CI Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"
  NODE_VERSION: "20"

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      
      - name: Test
        run: |
          uv sync --frozen
          uv run pytest --cov --cov-report=xml
          uv run ruff check .
          uv run mypy src/
      
      - name: Upload coverage
        if: github.event_name == 'pull_request'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Deploy Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: production
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.image.outputs.image }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        id: image
        run: |
          IMAGE="ghcr.io/${{ github.repository }}:${{ github.sha }}"
          docker build --cache-from ghcr.io/${{ github.repository }}:latest \
            --tag $IMAGE --tag ghcr.io/${{ github.repository }}:latest \
            --push .
          echo "image=$IMAGE" >> $GITHUB_OUTPUT
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        env:
          IMAGE: ${{ needs.build.outputs.image }}
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: deploy
          key: ${{ secrets.DEPLOY_KEY }}
          envs: IMAGE
          script: |
            docker pull $IMAGE
            docker stop app || true
            docker run -d --name app --restart always \
              -p 127.0.0.1:8000:8000 \
              --env-file /etc/app/production.env \
              --health-cmd "curl -f http://localhost:8000/health || exit 1" \
              --health-interval 30s \
              $IMAGE
            docker system prune -f
```

## Release Pipeline

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Validate tag
        run: |
          if ! grep -q "^## \[${{ github.ref_name }}\]" CHANGELOG.md; then
            echo "Missing CHANGELOG entry for ${{ github.ref_name }}"
            exit 1
          fi
      
      - name: Build artifacts
        run: |
          docker build --target production -t release:${{ github.ref_name }} .
          docker create --name extract release:${{ github.ref_name }}
          docker cp extract:/app/dist ./dist
          tar -czf release-${{ github.ref_name }}.tar.gz dist/
      
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: release-*.tar.gz
          body_path: CHANGELOG.md
          fail_on_unmatched_files: true
```

## Security Scan

```yaml
# .github/workflows/security.yml
name: Security

on:
  schedule:
    - cron: '0 0 * * 1'
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'HIGH,CRITICAL'
          exit-code: '1'
      
      - name: SAST
        run: |
          pip install bandit safety
          bandit -r src/ -f json -o bandit.json
          safety check --json > safety.json
      
      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: security-results
          path: |
            bandit.json
            safety.json
```

## Reusable Workflows

```yaml
# .github/workflows/docker-build.yml
name: Docker Build

on:
  workflow_call:
    inputs:
      push:
        type: boolean
        default: false
    outputs:
      image:
        value: ${{ jobs.build.outputs.image }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.build.outputs.image }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        id: build
        run: |
          IMAGE="ghcr.io/${{ github.repository }}:${{ github.sha }}"
          docker build -t $IMAGE .
          
          if [[ "${{ inputs.push }}" == "true" ]]; then
            echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
            docker push $IMAGE
          fi
          
          echo "image=$IMAGE" >> $GITHUB_OUTPUT
```

## Performance Optimizations

### Dependency Caching
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
    cache-dependency-path: |
      requirements.txt
      requirements-dev.txt

# Or for uv
- name: Cache uv
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

### Docker Layer Caching
```yaml
- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Conditional Jobs
```yaml
test:
  if: |
    !contains(github.event.head_commit.message, '[skip ci]') &&
    !contains(github.event.pull_request.labels.*.name, 'skip-tests')
```

## Common Failures

**Your mistakes**:
1. **No timeouts**: Jobs running forever
2. **No concurrency control**: Deploying simultaneously
3. **Secrets in logs**: Echo $SECRET (genius move)
4. **No caching**: 5-minute dependency installs
5. **Sequential jobs**: Everything depends on everything

**Reality check**:
```yaml
# Bad: Your current mess
- run: |
    pip install -r requirements.txt
    python test.py
    python lint.py
    python deploy.py

# Good: Parallel, cached, measured
- run: uv sync --frozen
- run: |
    uv run pytest &
    uv run ruff check . &
    uv run mypy src/ &
    wait
```

## Matrix Strategy

```yaml
test:
  strategy:
    matrix:
      python: ["3.11", "3.12"]
      os: [ubuntu-latest]
      include:
        - python: "3.12"
          os: windows-latest
    fail-fast: false
  
  runs-on: ${{ matrix.os }}
```

## The Truth

Your pipelines fail because:
1. **Copy-paste engineering**: Using workflows you don't understand
2. **Kitchen sink approach**: Every action ever created
3. **No measurement**: "It runs" isn't a metric
4. **Security theater**: Scanning without fixing

Good pipelines:
- Run in < 5 minutes
- Cache everything cacheable
- Fail fast on critical issues
- Deploy without prayer

Stop making excuses. Ship working code.
