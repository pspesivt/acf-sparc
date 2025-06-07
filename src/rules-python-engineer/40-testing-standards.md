## Python Testing Standards

Your tests are probably worthless. Here's how to write tests that actually catch bugs.

### Testing Philosophy

Tests aren't a checkbox. They're your only defense against production disasters.

**Coverage Metrics**:
```yaml
minimum_coverage:
  overall: 80%  # Absolute minimum
  business_logic: 90%  # Services, domain logic
  api_endpoints: 85%  # All routes tested
  utilities: 70%  # Helper functions
  
excluded:
  - __main__.py
  - */migrations/*
  - */tests/*
```

If your tests pass when the code is broken, delete them.

### Test Structure

**File Organization**:
```
tests/
├── __init__.py
├── conftest.py              # Global fixtures
├── unit/                    # Fast, isolated
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── test_user_service.py
│   ├── repositories/
│   │   └── test_user_repository.py
│   └── utils/
│       └── test_security.py
├── integration/             # Database, external services
│   ├── __init__.py
│   ├── api/
│   │   └── test_auth_endpoints.py
│   └── db/
│       └── test_transactions.py
└── e2e/                    # Full system tests
    └── test_user_flow.py
```

### Unit Test Patterns

**The AAA Pattern** (Arrange, Act, Assert):
```python
async def test_user_registration_success(
    user_service: UserService,
    mock_email_service: Mock,
) -> None:
    """Test successful user registration."""
    # Arrange
    user_data = UserCreate(
        email="test@example.com",
        password="SecurePass123!",
        name="Test User",
    )
    mock_email_service.send_welcome.return_value = None
    
    # Act
    user = await user_service.register_user(user_data)
    
    # Assert
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    mock_email_service.send_welcome.assert_called_once_with("test@example.com")
```

**Edge Case Testing**:
```python
@pytest.mark.parametrize(
    "email,expected_error",
    [
        ("", "Email required"),
        ("notanemail", "Invalid email format"),
        ("@example.com", "Invalid email format"),
        ("user@", "Invalid email format"),
        ("a" * 256 + "@test.com", "Email too long"),
    ],
)
async def test_user_registration_invalid_email(
    user_service: UserService,
    email: str,
    expected_error: str,
) -> None:
    """Test registration with invalid emails."""
    # Arrange
    user_data = UserCreate(
        email=email,
        password="ValidPass123!",
        name="Test",
    )
    
    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        await user_service.register_user(user_data)
    
    assert expected_error in str(exc_info.value)
```

### Fixture Patterns

**Database Fixtures**:
```python
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Isolated database session for each test."""
    # Create test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Provide session
    async with TestSessionLocal() as session:
        yield session
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def user(db_session: AsyncSession) -> User:
    """Create test user."""
    user = User(
        email="fixture@example.com",
        hashed_password=hash_password("TestPass123!"),
        name="Fixture User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
```

**Factory Fixtures**:
```python
@pytest.fixture
def user_factory(db_session: AsyncSession):
    """Factory for creating test users."""
    created_users = []
    
    async def _create_user(
        email: str | None = None,
        name: str = "Test User",
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email or f"user{len(created_users)}@test.com",
            hashed_password=hash_password("TestPass123!"),
            name=name,
            is_active=is_active,
        )
        db_session.add(user)
        await db_session.commit()
        created_users.append(user)
        return user
    
    return _create_user
```

### Mocking Patterns

**External Services**:
```python
@pytest.fixture
def mock_stripe(mocker: MockerFixture) -> Mock:
    """Mock Stripe API calls."""
    mock = mocker.patch("stripe.Charge.create")
    mock.return_value = Mock(
        id="ch_test123",
        amount=9999,
        currency="usd",
        status="succeeded",
    )
    return mock

async def test_payment_processing(
    payment_service: PaymentService,
    mock_stripe: Mock,
) -> None:
    """Test payment processing with mocked Stripe."""
    # Act
    result = await payment_service.charge_card(
        amount=9999,
        token="tok_visa",
    )
    
    # Assert
    assert result.charge_id == "ch_test123"
    mock_stripe.assert_called_once_with(
        amount=9999,
        currency="usd",
        source="tok_visa",
        idempotency_key=ANY,  # Don't care about exact value
    )
```

### Async Testing

**Async Fixtures**:
```python
@pytest_asyncio.fixture
async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async HTTP client for tests."""
    async with httpx.AsyncClient() as client:
        yield client

async def test_external_api_call(
    service: ExternalService,
    http_client: httpx.AsyncClient,
    httpx_mock: HTTPXMock,
) -> None:
    """Test external API integration."""
    # Setup mock
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"status": "ok", "data": [1, 2, 3]},
    )
    
    # Act
    result = await service.fetch_external_data()
    
    # Assert
    assert result == [1, 2, 3]
```

### Integration Test Patterns

**API Testing**:
```python
async def test_user_registration_flow(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Test complete registration flow."""
    # Register
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "SecurePass123!",
            "name": "New User",
        },
    )
    assert response.status_code == 201
    user_data = response.json()
    
    # Verify in database
    stmt = select(User).where(User.email == "newuser@test.com")
    user = await db_session.scalar(stmt)
    assert user is not None
    assert user.id == UUID(user_data["id"])
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "newuser@test.com",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Performance Testing

```python
@pytest.mark.performance
async def test_bulk_user_creation_performance(
    user_service: UserService,
    db_session: AsyncSession,
) -> None:
    """Test bulk user creation stays under 1 second."""
    import time
    
    # Arrange
    users_data = [
        UserCreate(
            email=f"user{i}@test.com",
            password="TestPass123!",
            name=f"User {i}",
        )
        for i in range(100)
    ]
    
    # Act
    start = time.perf_counter()
    users = await user_service.bulk_create(users_data)
    duration = time.perf_counter() - start
    
    # Assert
    assert len(users) == 100
    assert duration < 1.0, f"Bulk creation took {duration:.2f}s"
```

### Test Utilities

**Custom Assertions**:
```python
def assert_datetime_recent(
    dt: datetime,
    max_age_seconds: int = 5,
) -> None:
    """Assert datetime is recent."""
    age = (datetime.now(UTC) - dt).total_seconds()
    assert age < max_age_seconds, f"Datetime {dt} is {age}s old"

def assert_valid_uuid(value: Any) -> None:
    """Assert value is valid UUID."""
    try:
        UUID(str(value))
    except ValueError:
        pytest.fail(f"Invalid UUID: {value}")
```

**Test Data Builders**:
```python
class UserBuilder:
    """Builder for test users."""
    
    def __init__(self) -> None:
        self._email = "test@example.com"
        self._name = "Test User"
        self._is_active = True
    
    def with_email(self, email: str) -> Self:
        self._email = email
        return self
    
    def inactive(self) -> Self:
        self._is_active = False
        return self
    
    def build(self) -> User:
        return User(
            email=self._email,
            name=self._name,
            is_active=self._is_active,
            hashed_password=hash_password("Test123!"),
        )
```

### Coverage Configuration

**pytest.ini**:
```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
minversion = "8.0"
addopts = """
    -xvs
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
"""
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "performance: marks performance tests",
]
```

### Common Test Failures

**Your Garbage Tests**:
```python
# Useless test
def test_user_model():
    user = User(email="test@test.com")
    assert user.email == "test@test.com"  # Testing Python, not your code

# No isolation
async def test_get_all_users(db_session):
    users = await get_all_users(db_session)
    assert len(users) == 5  # Assumes database state

# Testing implementation
def test_password_uses_bcrypt():
    assert "bcrypt" in hash_password("test")  # Who cares HOW
```

**Actual Tests**:
```python
# Tests behavior
async def test_duplicate_email_rejected(user_service, existing_user):
    with pytest.raises(DuplicateEmailError):
        await user_service.create_user(email=existing_user.email)

# Isolated
async def test_list_active_users(user_factory):
    active = await user_factory(is_active=True)
    inactive = await user_factory(is_active=False)
    
    users = await list_active_users()
    
    assert active in users
    assert inactive not in users

# Tests contract
def test_password_hash_verifiable():
    password = "TestPass123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
```

### Test Execution

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific markers
uv run pytest -m "not slow"
uv run pytest -m integration

# Run in parallel
uv run pytest -n auto

# Run with debugging
uv run pytest -xvs --pdb

# Generate coverage report
uv run pytest --cov --cov-report=html
open htmlcov/index.html
```

### The Reality

Bad tests are worse than no tests because they give false confidence.

Your tests should:
1. **Fail when code breaks** (not just pass when it works)
2. **Run fast** (< 5 seconds for unit tests)
3. **Be deterministic** (same result every time)
4. **Document behavior** (test names explain intent)
5. **Cover edge cases** (not just happy path)

Stop writing tests to hit coverage metrics. Write tests that would have caught your last production bug.

That's the only metric that matters.
