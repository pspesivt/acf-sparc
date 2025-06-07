## Python Code Patterns

Your code patterns are probably outdated garbage from 2019. Here's what actually works in 2025.

### Import Organization

Stop your random import chaos. Order matters.

```python
# Standard library future imports FIRST
from __future__ import annotations

# Standard library imports
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Never, TypeAlias, assert_never
from uuid import UUID

# Third-party imports
import httpx
import structlog
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports  
from project_name.core import security
from project_name.db import models

# Type checking imports (zero runtime cost)
if TYPE_CHECKING:
    from collections.abc import Sequence
    from project_name.services import UserService
```

### Type Aliases

Stop typing the same complex types repeatedly.

```python
# Domain-specific aliases
UserId: TypeAlias = UUID
OrderId: TypeAlias = UUID
Money: TypeAlias = int  # ALWAYS cents, never floats
Email: TypeAlias = str  # Already validated by Pydantic

# Generic useful aliases
JsonDict: TypeAlias = dict[str, Any]
ErrorDict: TypeAlias = dict[str, str | list[str]]
```

### Async Patterns

Everything I/O bound is async. No exceptions.

**Database Operations**:
```python
async def get_user_by_email(
    session: AsyncSession,
    email: Email,
) -> models.User | None:
    """Get user by email, case-insensitive."""
    stmt = (
        select(models.User)
        .where(models.User.email == email.lower())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

**Concurrent Operations**:
```python
async def fetch_user_data(
    user_id: UserId,
    session: AsyncSession,
) -> UserComplete:
    """Fetch user with all related data concurrently."""
    # Fire all queries at once
    user_task = get_user(session, user_id)
    orders_task = get_user_orders(session, user_id)
    preferences_task = get_user_preferences(session, user_id)
    
    # Wait for all
    user, orders, preferences = await asyncio.gather(
        user_task,
        orders_task, 
        preferences_task,
    )
    
    if not user:
        raise UserNotFoundError(user_id)
    
    return UserComplete(
        user=user,
        orders=orders,
        preferences=preferences,
    )
```

### Error Handling

Exceptions are part of your API. Design them.

```python
# Base errors
class DomainError(Exception):
    """Base for all business logic errors."""
    
class ValidationError(DomainError):
    """Invalid input data."""
    
    def __init__(self, errors: ErrorDict) -> None:
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")

class NotFoundError(DomainError):
    """Resource doesn't exist."""
    
    def __init__(self, resource: str, identifier: Any) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} {identifier} not found")

# Specific errors
class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UserId) -> None:
        super().__init__("User", user_id)

# Usage pattern
async def get_user_strict(
    session: AsyncSession,
    user_id: UserId,
) -> models.User:
    """Get user or raise."""
    user = await get_user(session, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

### Dependency Injection

FastAPI dependencies done right.

```python
# deps.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: str = Depends(security.oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> models.User:
    """Get current authenticated user."""
    payload = security.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = await get_user(session, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

# Composite dependencies
class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
        cache: Redis = Depends(get_redis),
    ) -> None:
        self.session = session
        self.current_user = current_user
        self.cache = cache
```

### Repository Pattern

Isolate database queries. Always.

```python
class UserRepository:
    """User data access layer."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get(self, user_id: UserId) -> models.User | None:
        """Get user by ID."""
        return await self.session.get(models.User, user_id)
    
    async def get_by_email(self, email: Email) -> models.User | None:
        """Get user by email, case-insensitive."""
        stmt = select(models.User).where(
            models.User.email == email.lower()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, user_data: UserCreate) -> models.User:
        """Create new user."""
        user = models.User(
            email=user_data.email.lower(),
            hashed_password=security.hash_password(
                user_data.password.get_secret_value()
            ),
            name=user_data.name,
        )
        self.session.add(user)
        await self.session.flush()  # Get ID without commit
        return user
    
    async def exists_by_email(self, email: Email) -> bool:
        """Check if email already taken."""
        stmt = select(
            exists().where(models.User.email == email.lower())
        )
        result = await self.session.execute(stmt)
        return result.scalar()
```

### Service Layer

Business logic lives here. Not in routes. Not in models.

```python
class UserService:
    """User business logic."""
    
    def __init__(
        self,
        repo: UserRepository,
        email_service: EmailService,
        cache: Cache,
    ) -> None:
        self.repo = repo
        self.email_service = email_service
        self.cache = cache
    
    async def register_user(
        self,
        user_data: UserCreate,
    ) -> models.User:
        """Register new user with all checks."""
        # Check existing
        if await self.repo.exists_by_email(user_data.email):
            raise ValidationError(
                {"email": "Email already registered"}
            )
        
        # Create user
        user = await self.repo.create(user_data)
        
        # Side effects
        await self.email_service.send_welcome(user.email)
        await self.cache.delete(f"user_count:*")
        
        return user
```

### Structured Logging

Stop using print(). You're not debugging a toy script.

```python
logger = structlog.get_logger(__name__)

async def process_order(order_id: OrderId) -> None:
    """Process order with proper logging."""
    log = logger.bind(order_id=str(order_id))
    
    log.info("processing_order_started")
    
    try:
        order = await get_order(order_id)
        log = log.bind(
            user_id=str(order.user_id),
            total=order.total,
        )
        
        await validate_inventory(order)
        log.info("inventory_validated")
        
        payment = await charge_payment(order)
        log.info(
            "payment_processed",
            payment_id=payment.id,
            amount=payment.amount,
        )
        
    except Exception as e:
        log.error(
            "order_processing_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise
```

### Configuration

Environment-specific config with validation.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # API Settings
    api_title: str = "MyAPI"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 0
    
    # Security
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    
    # External services
    redis_url: str = "redis://localhost:6379"
    email_api_key: str | None = None
    
    @property
    def async_database_url(self) -> str:
        """Convert to async driver."""
        return self.database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

# Singleton
settings = Settings()
```

### Testing Patterns

Tests that actually catch bugs.

```python
# Fixtures
@pytest.fixture
async def user(session: AsyncSession) -> models.User:
    """Create test user."""
    user = models.User(
        email="test@example.com",
        hashed_password="hashed",
        name="Test User",
    )
    session.add(user)
    await session.commit()
    return user

# Service tests
async def test_register_user_success(
    user_service: UserService,
    session: AsyncSession,
) -> None:
    """Test successful user registration."""
    # Arrange
    user_data = UserCreate(
        email="new@example.com",
        password="ValidPass123!",
        name="New User",
    )
    
    # Act
    user = await user_service.register_user(user_data)
    
    # Assert
    assert user.id is not None
    assert user.email == "new@example.com"
    
    # Verify persisted
    db_user = await session.get(models.User, user.id)
    assert db_user is not None
    assert db_user.email == user.email

async def test_register_user_duplicate_email(
    user_service: UserService,
    user: models.User,  # Existing user fixture
) -> None:
    """Test registration with existing email."""
    # Arrange
    user_data = UserCreate(
        email=user.email,  # Duplicate
        password="ValidPass123!",
        name="Another User",
    )
    
    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        await user_service.register_user(user_data)
    
    assert "email" in exc_info.value.errors
```

### Performance Patterns

Stop writing slow code.

```python
# Bulk operations
async def bulk_create_users(
    session: AsyncSession,
    users_data: list[UserCreate],
) -> list[models.User]:
    """Create multiple users efficiently."""
    # Don't do N queries
    users = [
        models.User(
            email=data.email.lower(),
            hashed_password=security.hash_password(
                data.password.get_secret_value()
            ),
            name=data.name,
        )
        for data in users_data
    ]
    
    session.add_all(users)
    await session.flush()
    return users

# Eager loading
async def get_orders_with_items(
    session: AsyncSession,
    user_id: UserId,
) -> Sequence[models.Order]:
    """Get orders with items in single query."""
    stmt = (
        select(models.Order)
        .where(models.Order.user_id == user_id)
        .options(selectinload(models.Order.items))
        .order_by(models.Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()
```

### Reality Check

These patterns aren't suggestions. They're the minimum bar for professional Python in 2025.

Skip them and your code will be:
- Slow (no async)
- Buggy (no types)
- Unmaintainable (no structure)
- Insecure (no validation)

Your choice: Follow the patterns or write amateur code that gets rejected in review.
