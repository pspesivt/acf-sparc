## Python Security Checklist

Your code is probably a security disaster waiting to happen. Here's how to stop being an attack vector.

### Authentication & Authorization

**Password Storage**:
```python
# WRONG: Your amateur hour garbage
password_hash = hashlib.sha256(password.encode()).hexdigest()

# RIGHT: Use bcrypt with work factor
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password with bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time comparison."""
    return pwd_context.verify(plain, hashed)
```

**JWT Implementation**:
```python
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

# WRONG: Storing sensitive data in JWT
token_data = {"user_id": 123, "password": "hash", "ssn": "123-45-6789"}

# RIGHT: Minimal claims
def create_access_token(user_id: UserId) -> str:
    """Create JWT with minimal claims."""
    expire = datetime.now(UTC) + timedelta(minutes=15)
    claims = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "access",
    }
    return jwt.encode(claims, settings.secret_key, algorithm="HS256")
```

### Input Validation

**SQL Injection Prevention**:
```python
# WRONG: String concatenation = instant pwn
query = f"SELECT * FROM users WHERE email = '{email}'"

# RIGHT: Parameterized queries ALWAYS
from sqlalchemy import select

stmt = select(User).where(User.email == email)
result = await session.execute(stmt)
```

**Pydantic Validation**:
```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserInput(BaseModel):
    """Validate ALL user input."""
    
    email: EmailStr  # Automatic email validation
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    age: int = Field(..., ge=13, le=120)
    
    @field_validator("username")
    @classmethod
    def no_script_tags(cls, v: str) -> str:
        """Prevent basic XSS."""
        dangerous = ["<script", "javascript:", "onerror=", "onclick="]
        if any(d in v.lower() for d in dangerous):
            raise ValueError("Invalid characters in username")
        return v
```

### XSS Prevention

**Template Escaping**:
```python
# WRONG: Raw HTML injection
return f"<h1>Welcome {user_input}</h1>"

# RIGHT: Always escape
import html

return f"<h1>Welcome {html.escape(user_input)}</h1>"

# BETTER: Use template engine
from jinja2 import Environment, select_autoescape

env = Environment(autoescape=select_autoescape(["html", "xml"]))
```

**JSON Responses**:
```python
# WRONG: Manual JSON construction
response = f'{{"user": "{username}"}}'

# RIGHT: Use json module
import json
response = json.dumps({"user": username})
```

### CSRF Protection

```python
from secrets import token_urlsafe

class CSRFProtection:
    """CSRF token management."""
    
    @staticmethod
    def generate_token() -> str:
        """Generate CSRF token."""
        return token_urlsafe(32)
    
    @staticmethod
    def validate_token(
        session_token: str,
        request_token: str,
    ) -> bool:
        """Constant-time comparison."""
        return secrets.compare_digest(session_token, request_token)

# FastAPI middleware
@app.middleware("http")
async def csrf_protection(request: Request, call_next):
    """Validate CSRF for state-changing operations."""
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        session_token = request.session.get("csrf_token")
        request_token = request.headers.get("X-CSRF-Token")
        
        if not session_token or not request_token:
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF token missing"},
            )
        
        if not CSRFProtection.validate_token(session_token, request_token):
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF token invalid"},
            )
    
    return await call_next(request)
```

### Secret Management

**Environment Variables**:
```python
# WRONG: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"

# RIGHT: Environment variables with validation
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str  # Required, no default
    database_url: str
    api_key: str
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_strength(cls, v: str) -> str:
        """Ensure secret is strong."""
        if len(v) < 32:
            raise ValueError("Secret key too weak")
        return v
```

### File Upload Security

```python
import hashlib
import mimetypes
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def secure_file_upload(
    file: UploadFile,
    user_id: UserId,
) -> Path:
    """Secure file upload with validation."""
    # Size check
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    # Extension validation
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type: {extension}")
    
    # MIME type verification
    mime_type = mimetypes.guess_type(file.filename)[0]
    if mime_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise ValueError(f"Invalid MIME type: {mime_type}")
    
    # Generate safe filename
    file_hash = hashlib.sha256(contents).hexdigest()
    safe_name = f"{user_id}_{file_hash}{extension}"
    
    # Store outside web root
    upload_path = Path("/var/uploads") / safe_name
    upload_path.write_bytes(contents)
    
    return upload_path
```

### Rate Limiting

```python
from datetime import datetime, timedelta
from typing import Optional

import redis.asyncio as redis

class RateLimiter:
    """Redis-based rate limiting."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int,
    ) -> tuple[bool, Optional[int]]:
        """Check if request is allowed."""
        now = datetime.now().timestamp()
        window_start = now - window_seconds
        
        # Remove old entries
        await self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count recent requests
        request_count = await self.redis.zcard(key)
        
        if request_count >= max_requests:
            # Get oldest request time
            oldest = await self.redis.zrange(key, 0, 0, withscores=True)
            if oldest:
                retry_after = int(oldest[0][1] + window_seconds - now)
                return False, retry_after
            return False, window_seconds
        
        # Add current request
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

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Trusted host validation
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
)
```

### Dependency Scanning

**pyproject.toml additions**:
```toml
[tool.bandit]
targets = ["src"]
skip = ["B101"]  # Skip assert_used test

[dependency-groups]
security = [
    "bandit[toml]>=1.8.0",
    "safety>=3.0.0",
    "pip-audit>=2.7.0",
]
```

**Security commands**:
```bash
# Scan code for vulnerabilities
uv run bandit -r src/

# Check dependencies
uv run safety check
uv run pip-audit

# Update vulnerable packages
uv add --upgrade package-name@latest
```

### Logging Security

```python
import structlog
from typing import Any

# Configure secure logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        # Sanitize sensitive data
        lambda _, __, event_dict: sanitize_log(event_dict),
        structlog.processors.JSONRenderer(),
    ],
)

def sanitize_log(event_dict: dict[str, Any]) -> dict[str, Any]:
    """Remove sensitive data from logs."""
    sensitive_keys = {"password", "token", "secret", "api_key", "ssn"}
    
    for key in list(event_dict.keys()):
        if any(s in key.lower() for s in sensitive_keys):
            event_dict[key] = "***REDACTED***"
    
    return event_dict
```

### Common Vulnerabilities You Create

1. **Timing Attacks**: Using `==` for password comparison
2. **Mass Assignment**: Accepting all fields from user input
3. **Path Traversal**: Not validating file paths
4. **SSRF**: Following any URL without validation
5. **XXE**: Processing XML without disabling entities
6. **Insecure Deserialization**: Using pickle on untrusted data

### Security Audit Commands

```bash
# Full security audit
uv run bandit -r src/ -f json -o bandit-report.json
uv run safety check --json > safety-report.json
uv run pip-audit --format json > audit-report.json

# Git secrets scanning
git secrets --install
git secrets --scan
```

### The Reality

Most Python developers think:
- "It's internal only" (until it's not)
- "Nobody would do that" (they would)
- "We'll add security later" (you won't)

Security isn't a feature. It's the absence of stupidity.

Every item on this checklist prevents a real attack that's happened to someone who thought they were too smart to be hacked.

You're not.
