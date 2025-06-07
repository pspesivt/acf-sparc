## Python Security Checklist

### Authentication & Authorization

**Password Storage**:
```python
# WRONG: hashlib.sha256(password.encode()).hexdigest()
# RIGHT: Use bcrypt with work factor
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(plain: str, hashed: str) -> bool: return pwd_context.verify(plain, hashed)
```

**JWT Implementation**:
```python
from datetime import UTC, datetime, timedelta
from jose import JWTError, jwt
# WRONG: token_data = {"user_id": 123, "password": "hash", "ssn": "123-45-6789"}
# RIGHT: Minimal claims
def create_access_token(user_id: UserId) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=15)
    claims = {"sub": str(user_id), "exp": expire, "iat": datetime.now(UTC), "type": "access"}
    return jwt.encode(claims, settings.secret_key, algorithm="HS256")
```

### Input Validation

**SQL Injection Prevention**:
```python
# WRONG: query = f"SELECT * FROM users WHERE email = '{email}'"
# RIGHT: Parameterized queries
from sqlalchemy import select
stmt = select(User).where(User.email == email)
result = await session.execute(stmt)
```

**Pydantic Validation**:
```python
from pydantic import BaseModel, EmailStr, Field, field_validator
class UserInput(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    age: int = Field(..., ge=13, le=120)
    @field_validator("username")
    @classmethod
    def no_script_tags(cls, v: str) -> str:
        dangerous = ["<script", "javascript:", "onerror=", "onclick="]
        if any(d in v.lower() for d in dangerous): raise ValueError("Invalid characters in username")
        return v
```

### XSS Prevention

**Template Escaping**:
```python
# WRONG: f"<h1>Welcome {user_input}</h1>"
# RIGHT: Always escape
import html
return f"<h1>Welcome {html.escape(user_input)}</h1>"
# BETTER: Use template engine
from jinja2 import Environment, select_autoescape
env = Environment(autoescape=select_autoescape(["html", "xml"]))
```

**JSON Responses**:
```python
# WRONG: f'{{"user": "{username}"}}'
# RIGHT: Use json module
import json
response = json.dumps({"user": username})
```

### CSRF Protection

```python
from secrets import token_urlsafe
class CSRFProtection:
    @staticmethod
    def generate_token() -> str: return token_urlsafe(32)
    @staticmethod
    def validate_token(session_token: str, request_token: str) -> bool:
        return secrets.compare_digest(session_token, request_token)

@app.middleware("http")
async def csrf_protection(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        session_token = request.session.get("csrf_token")
        request_token = request.headers.get("X-CSRF-Token")
        if not session_token or not request_token:
            return JSONResponse(status_code=403, content={"detail": "CSRF token missing"})
        if not CSRFProtection.validate_token(session_token, request_token):
            return JSONResponse(status_code=403, content={"detail": "CSRF token invalid"})
    return await call_next(request)
```

### Secret Management

```python
# WRONG: API_KEY = "sk-1234567890abcdef"
# RIGHT: Environment variables with validation
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    secret_key: str
    database_url: str
    api_key: str
    @field_validator("secret_key")
    @classmethod
    def validate_secret_strength(cls, v: str) -> str:
        if len(v) < 32: raise ValueError("Secret key too weak")
        return v
```

### File Upload Security

```python
import hashlib, mimetypes
from pathlib import Path
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
async def secure_file_upload(file: UploadFile, user_id: UserId) -> Path:
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE: raise ValueError("File too large")
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS: raise ValueError(f"Invalid file type: {extension}")
    mime_type = mimetypes.guess_type(file.filename)[0]
    if mime_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise ValueError(f"Invalid MIME type: {mime_type}")
    file_hash = hashlib.sha256(contents).hexdigest()
    safe_name = f"{user_id}_{file_hash}{extension}"
    upload_path = Path("/var/uploads") / safe_name
    upload_path.write_bytes(contents)
    return upload_path
```

### Rate Limiting

```python
from datetime import datetime
import redis.asyncio as redis
class RateLimiter:
    def __init__(self, redis_client: redis.Redis): self.redis = redis_client
    async def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, Optional[int]]:
        now = datetime.now().timestamp()
        window_start = now - window_seconds
        await self.redis.zremrangebyscore(key, 0, window_start)
        request_count = await self.redis.zcard(key)
        if request_count >= max_requests:
            oldest = await self.redis.zrange(key, 0, 0, withscores=True)
            if oldest: return False, int(oldest[0][1] + window_seconds - now)
            return False, window_seconds
        await self.redis.zadd(key, {str(now): now})
        await self.redis.expire(key, window_seconds)
        return True, None
```

### Security Headers

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
app.add_middleware(CORSMiddleware, allow_origins=settings.backend_cors_origins, 
                  allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
```

### Dependency Scanning

**pyproject.toml**:
```toml
[tool.bandit]
targets = ["src"]
skip = ["B101"]
[dependency-groups]
security = ["bandit[toml]>=1.8.0", "safety>=3.0.0", "pip-audit>=2.7.0"]
```

**Security commands**:
```bash
uv run bandit -r src/
uv run safety check
uv run pip-audit
uv add --upgrade package-name@latest
```

### Logging Security

```python
import structlog
structlog.configure(processors=[
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    lambda _, __, event_dict: sanitize_log(event_dict),
    structlog.processors.JSONRenderer(),
])
def sanitize_log(event_dict: dict[str, Any]) -> dict[str, Any]:
    sensitive_keys = {"password", "token", "secret", "api_key", "ssn"}
    for key in list(event_dict.keys()):
        if any(s in key.lower() for s in sensitive_keys): event_dict[key] = "***REDACTED***"
    return event_dict
```

### Common Vulnerabilities
1. Timing Attacks: Using `==` for password comparison
2. Mass Assignment: Accepting all fields from user input
3. Path Traversal: Not validating file paths
4. SSRF: Following any URL without validation
5. XXE: Processing XML without disabling entities
6. Insecure Deserialization: Using pickle on untrusted data

### Security Audit Commands
```bash
uv run bandit -r src/ -f json -o bandit-report.json
uv run safety check --json > safety-report.json
uv run pip-audit --format json > audit-report.json
git secrets --install
git secrets --scan
```