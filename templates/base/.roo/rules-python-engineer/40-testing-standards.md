## Python Testing Standards

Tests aren't a checkbox. They're your only defense against production disasters.

```yaml
minimum_coverage:
  overall: 80%
  business_logic: 90%
  api_endpoints: 85%
  utilities: 70%
  
excluded:
  - __main__.py
  - */migrations/*
  - */tests/*
```

If tests pass when code is broken, delete them.

### Test Structure

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── test_user_service.py
│   ├── repositories/
│   │   └── test_user_repository.py
│   └── utils/
│       └── test_security.py
├── integration/
│   ├── __init__.py
│   ├── api/
│   │   └── test_auth_endpoints.py
│   └── db/
│       └── test_transactions.py
└── e2e/
    └── test_user_flow.py
```

### Unit Test Patterns

AAA Pattern:
```python
async def test_user_registration_success(
    user_service: UserService,
    mock_email_service: Mock,
) -> None:
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

Edge Case Testing:
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
    user_data = UserCreate(
        email=email,
        password="ValidPass123!",
        name="Test",
    )
    
    with pytest.raises(ValidationError) as exc_info:
        await user_service.register_user(user_data)
    
    assert expected_error in str(exc_info.value)
```

### Fixture Patterns

Database Fixtures:
```python
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def user(db_session: AsyncSession) -> User:
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

Factory Fixtures:
```python
@pytest.fixture
def user_factory(db_session: AsyncSession):
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

```python
@pytest.fixture
def mock_stripe(mocker: MockerFixture) -> Mock:
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
    result = await payment_service.charge_card(
        amount=9999,
        token="tok_visa",
    )
    
    assert result.charge_id == "ch_test123"
    mock_stripe.assert_called_once_with(
        amount=9999,
        currency="usd",
        source="tok_visa",
        idempotency_key=ANY,
    )
```

### Async Testing

```python
@pytest_asyncio.fixture
async def http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client

async def test_external_api_call(
    service: ExternalService,
    http_client: httpx.AsyncClient,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"status": "ok", "data": [1, 2, 3]},
    )
    
    result = await service.fetch_external_data()
    
    assert result == [1, 2, 3]
```

### Integration Test Patterns

```python
async def test_user_registration_flow(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
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
    
    stmt = select(User).where(User.email == "newuser@test.com")
    user = await db_session.scalar(stmt)
    assert user is not None
    assert user.id == UUID(user_data["id"])
    
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
    import time
    
    users_data = [
        UserCreate(
            email=f"user{i}@test.com",
            password="TestPass123!",
            name=f"User {i}",
        )
        for i in range(100)
    ]
    
    start = time.perf_counter()
    users = await user_service.bulk_create(users_data)
    duration = time.perf_counter() - start
    
    assert len(users) == 100
    assert duration < 1.0, f"Bulk creation took {duration:.2f}s"
```

### Test Utilities

```python
def assert_datetime_recent(
    dt: datetime,
    max_age_seconds: int = 5,
) -> None:
    age = (datetime.now(UTC) - dt).total_seconds()
    assert age < max_age_seconds, f"Datetime {dt} is {age}s old"

def assert_valid_uuid(value: Any) -> None:
    try:
        UUID(str(value))
    except ValueError:
        pytest.fail(f"Invalid UUID: {value}")
```

```python
class UserBuilder:
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

### Common Test Failures vs Actual Tests

Bad:
```python
def test_user_model():
    user = User(email="test@test.com")
    assert user.email == "test@test.com"

async def test_get_all_users(db_session):
    users = await get_all_users(db_session)
    assert len(users) == 5

def test_password_uses_bcrypt():
    assert "bcrypt" in hash_password("test")
```

Good:
```python
async def test_duplicate_email_rejected(user_service, existing_user):
    with pytest.raises(DuplicateEmailError):
        await user_service.create_user(email=existing_user.email)

async def test_list_active_users(user_factory):
    active = await user_factory(is_active=True)
    inactive = await user_factory(is_active=False)
    
    users = await list_active_users()
    
    assert active in users
    assert inactive not in users

def test_password_hash_verifiable():
    password = "TestPass123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
```

### Test Execution

```bash
uv run pytest
uv run pytest --cov
uv run pytest -m "not slow"
uv run pytest -m integration
uv run pytest -n auto
uv run pytest -xvs --pdb
uv run pytest --cov --cov-report=html
```

Tests should: fail when code breaks, run fast, be deterministic, document behavior, cover edge cases.