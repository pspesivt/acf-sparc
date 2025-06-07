project-name/.python-version=3.12.7
project-name/pyproject.toml=[project]name="project-name";version="0.1.0";description="Stop writing vague descriptions";readme="README.md";requires-python=">=3.12";license={text="MIT"};authors=[{name="Your Name",email="you@example.com"}];dependencies=["fastapi[standard]>=0.115.0","pydantic>=2.9.0","pydantic-settings>=2.6.0","sqlalchemy>=2.0.0","asyncpg>=0.30.0","alembic>=1.16.0","structlog>=24.0.0","httpx>=0.28.0","python-jose[cryptography]>=3.3.0","passlib[bcrypt]>=1.7.4"];[dependency-groups.dev]=["pytest>=8.3.0","pytest-asyncio>=0.25.0","pytest-cov>=6.0.0","mypy>=1.14.0","ruff>=0.8.0","bandit[toml]>=1.8.0","factory-boy>=3.3.0","pytest-mock>=3.14.0"];[build-system]requires=["hatchling"];build-backend="hatchling.build";[tool.uv]managed=true;dev-dependencies=["dependency-groups","dev"];[tool.ruff]target-version="py312";line-length=88;src=["src","tests"];[tool.ruff.lint]select=["ALL"];ignore=["D","ANN101","ANN102","COM812","ISC001"];[tool.mypy]python_version="3.12";strict=true;plugins=["pydantic.mypy"];[tool.pytest.ini_options]testpaths=["tests"];asyncio_mode="auto";addopts="-xvs --cov=src --cov-report=term-missing";[tool.coverage.run]branch=true;source=["src"];[tool.coverage.report]exclude_lines=["pragma: no cover","if TYPE_CHECKING:","raise NotImplementedError"]
project-name/.gitignore=__pycache__/;*.py[cod];*$py.class;*.so;.Python;.venv/;env/;venv/;.pytest_cache/;.mypy_cache/;.coverage;htmlcov/;*.egg-info/;dist/;build/;.env;!.env.example;.vscode/;.idea/;*.swp;*.swo;*~;*.log;*.db;*.sqlite3;alembic/versions/*.py;!alembic/versions/.gitkeep
project-name/.env.example=
project-name/README.md=
project-name/uv.lock=
project-name/.github/workflows/ci.yml=name=CI;on=push[branches=[main]]+pull_request[branches=[main]];jobs.test.runs-on=ubuntu-latest;services.postgres={image:postgres:16,env:{POSTGRES_USER:test,POSTGRES_PASSWORD:test,POSTGRES_DB:test},options:"--health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5",ports:[5432:5432]};steps:[uses:actions/checkout@v4,uses:astral-sh/setup-uv@v4{version:"latest"},run:["uv python install 3.12.7","uv python pin 3.12.7","uv sync --frozen"],run:["uv run ruff check .","uv run ruff format --check ."],run:uv run mypy src/,run:uv run bandit -r src/,env:{DATABASE_URL:postgresql://test:test@localhost/test};run:uv run pytest --cov-report=xml,uses:codecov/codecov-action@v4{token:${{secrets.CODECOV_TOKEN}}}]
project-name/src/project_name/__init__.py=__version__="0.1.0"
project-name/src/project_name/__main__.py=import uvicorn;from project_name.core.config import settings;def main():uvicorn.run("project_name.api.app:app",host="0.0.0.0",port=8000,reload=settings.debug,log_config={"version":1,"disable_existing_loggers":False,"formatters":{"default":{"format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},"handlers":{"default":{"formatter":"default","class":"logging.StreamHandler","stream":"ext://sys.stderr"}},"root":{"level":"INFO","handlers":["default"]}});if __name__=="__main__":main()
project-name/src/project_name/core/config.py=from functools import lru_cache;from pydantic import field_validator;from pydantic_settings import BaseSettings,SettingsConfigDict;class Settings(BaseSettings):model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",case_sensitive=False);api_title:str="Project Name API";api_version:str="1.0.0";debug:bool=False;database_url:str;database_echo:bool=False;database_pool_size:int=20;database_max_overflow:int=0;secret_key:str;algorithm:str="HS256";access_token_expire_minutes:int=15;refresh_token_expire_days:int=30;backend_cors_origins:list[str]=[];@field_validator("backend_cors_origins",mode="before");@classmethod;def assemble_cors_origins(cls,v:str|list[str])->list[str]:return [i.strip() for i in v.split(",")] if isinstance(v,str) and not v.startswith("[") else v if isinstance(v,list) else [];@property;def async_database_url(self)->str:return self.database_url.replace("postgresql://","postgresql+asyncpg://");@lru_cache;def get_settings()->Settings:return Settings();settings=get_settings()
project-name/src/project_name/api/app.py=
project-name/src/project_name/api/deps.py=
project-name/src/project_name/api/v1/routers/auth.py=
project-name/src/project_name/api/v1/routers/users.py=
project-name/src/project_name/api/v1/schemas/auth.py=
project-name/src/project_name/api/v1/schemas/users.py=
project-name/src/project_name/core/security.py=
project-name/src/project_name/core/exceptions.py=
project-name/src/project_name/db/base.py=
project-name/src/project_name/db/session.py=
project-name/src/project_name/db/models.py=
project-name/src/project_name/repositories/user.py=
project-name/src/project_name/services/user.py=
project-name/src/project_name/utils/logging.py=
project-name/tests/conftest.py=import asyncio;import pytest;import pytest_asyncio;from httpx import AsyncClient;from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine;from project_name.api.app import app;from project_name.api.deps import get_db;from project_name.core.config import settings;from project_name.db.base import Base;engine=create_async_engine(settings.async_database_url.replace("/project","/project_test"),echo=False);TestSessionLocal=async_sessionmaker(engine,expire_on_commit=False);@pytest.fixture(scope="session");def event_loop():loop=asyncio.get_event_loop_policy().new_event_loop();yield loop;loop.close();@pytest_asyncio.fixture;async def db_session():async with engine.begin() as conn:await conn.run_sync(Base.metadata.create_all);async with TestSessionLocal() as session:yield session;async with engine.begin() as conn:await conn.run_sync(Base.metadata.drop_all);@pytest_asyncio.fixture;async def client(db_session):async def override_get_db():yield db_session;app.dependency_overrides[get_db]=override_get_db;async with AsyncClient(app=app,base_url="http://test") as ac:yield ac;app.dependency_overrides.clear()
project-name/tests/unit/services/test_user.py=
project-name/tests/integration/api/test_auth.py=
project-name/alembic/alembic.ini=
project-name/alembic/env.py=
project-name/alembic/script.py.mako=
project-name/alembic/versions/=
project-name/scripts/dev.sh=git clone <repo>;cd project-name;uv python install 3.12.7;uv python pin 3.12.7;uv sync;docker-compose up -d postgres;uv run alembic upgrade head;uv run python -m project_name
project-name/scripts/seed.py=
project-name/docker/Dockerfile=
project-name/docker/docker-compose.yml=