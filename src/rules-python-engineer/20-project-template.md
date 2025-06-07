## Python Project Template

Stop creating inconsistent project structures. Here's the only template you need.

### Directory Structure

```
project-name/
├── .python-version         # uv reads this: 3.12.7
├── pyproject.toml          # Everything lives here
├── uv.lock                 # Never edit manually
├── README.md               # Basic docs or you're fired
├── .env.example            # Document your secrets
├── .gitignore              # Stop committing garbage
├── .github/
│   └── workflows/
│       └── ci.yml          # Automated testing
├── src/
│   └── project_name/       # Underscores, not hyphens
│       ├── __init__.py
│       ├── __main__.py     # Entry point
│       ├── api/
│       │   ├── __init__.py
│       │   ├── app.py      # FastAPI instance
│       │   ├── deps.py     # Dependency injection
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── routers/
│       │       │   ├── __init__.py
│       │       │   ├── auth.py
│       │       │   └── users.py
│       │       └── schemas/
│       │           ├── __init__.py
│       │           ├── auth.py
│       │           └── users.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py   # Settings management
│       │   ├── security.py # Auth utilities
│       │   └── exceptions.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── base.py     # SQLAlchemy base
│       │   ├── session.py  # Database connection
│       │   └── models.py   # All models here
│       ├── repositories/   # Data access layer
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/       # Business logic
│       │   ├── __init__.py
│       │   └── user.py
│       └── utils/
│           ├── __init__.py
│           └── logging.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Global fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── services/
│   │       └── test_user.py
│   └── integration/
│       ├── __init__.py
│       └── api/
│           └── test_auth.py
├── alembic/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/           # Migrations go here
├── scripts/
│   ├── dev.sh              # Development shortcuts
│   └── seed.py             # Database seeding
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

### File Templates

**pyproject.toml**:
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Stop writing vague descriptions"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "you@example.com" },
]
dependencies = [
    "fastapi[standard]>=0.115.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.30.0",
    "alembic>=1.16.0",
    "structlog>=24.0.0",
    "httpx>=0.28.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[dependency-groups]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "pytest-cov>=6.0.0",
    "mypy>=1.14.0",
    "ruff>=0.8.0",
    "bandit[toml]>=1.8.0",
    "factory-boy>=3.3.0",
    "pytest-mock>=3.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
managed = true
dev-dependencies = ["dependency-groups", "dev"]

[tool.ruff]
target-version = "py312"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D",      # Docstrings handled separately
    "ANN101", # Missing type annotation for self
    "ANN102", # Missing type annotation for cls
    "COM812", # Conflicts with formatter
    "ISC001", # Conflicts with formatter
]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-xvs --cov=src --cov-report=term-missing"

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

**.gitignore**:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
env/
venv/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# Environment
.env
.env.*
!.env.example

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project
*.log
*.db
*.sqlite3
alembic/versions/*.py
!alembic/versions/.gitkeep
```

**src/project_name/__init__.py**:
```python
"""Project name - Brief description."""

__version__ = "0.1.0"
```

**src/project_name/__main__.py**:
```python
"""Entry point for the application."""

import uvicorn

from project_name.core.config import settings


def main() -> None:
    """Run the application."""
    uvicorn.run(
        "project_name.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        },
    )


if __name__ == "__main__":
    main()
```

**src/project_name/core/config.py**:
```python
"""Application configuration."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API
    api_title: str = "Project Name API"
    api_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 0

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    # CORS
    backend_cors_origins: list[str] = []

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list):
            return v
        return []

    @property
    def async_database_url(self) -> str:
        """Convert sync URL to async."""
        return self.database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
```

**tests/conftest.py**:
```python
"""Global test configuration."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from project_name.api.app import app
from project_name.api.deps import get_db
from project_name.core.config import settings
from project_name.db.base import Base

# Test database
engine = create_async_engine(
    settings.async_database_url.replace("/project", "/project_test"),
    echo=False,
)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """Get test client."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
```

### Development Commands

**Initial Setup**:
```bash
# Clone and enter
git clone <repo>
cd project-name

# Setup Python with uv
uv python install 3.12.7
uv python pin 3.12.7
uv sync

# Setup database
docker-compose up -d postgres
uv run alembic upgrade head

# Run dev server
uv run python -m project_name
```

**Daily Workflow**:
```bash
# Format and lint
uv run ruff check --fix .
uv run ruff format .

# Type check
uv run mypy src/

# Test
uv run pytest

# Security scan
uv run bandit -r src/

# Update deps
uv add <package>@latest
uv lock
```

### CI Configuration

**.github/workflows/ci.yml**:
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v4
      with:
        version: "latest"
    
    - name: Setup Python
      run: |
        uv python install 3.12.7
        uv python pin 3.12.7
    
    - name: Install dependencies
      run: uv sync --frozen
    
    - name: Lint
      run: |
        uv run ruff check .
        uv run ruff format --check .
    
    - name: Type check
      run: uv run mypy src/
    
    - name: Security scan
      run: uv run bandit -r src/
    
    - name: Test
      env:
        DATABASE_URL: postgresql://test:test@localhost/test
      run: uv run pytest --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
```

### Reality Check

This template works. Deviating means:
- Inconsistent imports
- Missing test coverage
- Security vulnerabilities
- Deployment failures

Use it exactly as shown or enjoy debugging your snowflake structure at 3 AM.
