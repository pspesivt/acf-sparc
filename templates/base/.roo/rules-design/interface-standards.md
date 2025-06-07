## Interface Definition Standards

Your interfaces are ambiguous garbage. Here's how to fix them.

### Interface Anatomy

Every interface needs five things or it's worthless:

```yaml
Interface: ComponentName
Purpose: One sentence. What problem does this solve?
Contract:
  Methods: What operations are exposed
  Inputs: What goes in (with types and constraints)
  Outputs: What comes out (success and failure cases)
  Side Effects: What else happens (logs, events, state changes)
  Invariants: What never changes
```

Miss any part? Your integration fails in production.

### Method Specification

Stop with vague method names. Be explicit.

**Garbage**:
```
getUser(id)
processOrder(data)
handleRequest(req)
doStuff(thing)
```

**Actual Interfaces**:
```
Interface: UserRepository
  
  findById(userId: UUID) → User | null
    Precondition: userId is valid UUID
    Success: Returns User object with all fields
    Failure: Returns null if not found
    Side Effect: Logs query execution time
    Performance: < 10ms from cache, < 100ms from DB
  
  findByEmail(email: string) → User | null
    Precondition: email passes RFC 5322 validation
    Success: Returns User object
    Failure: Returns null if not found
    Side Effect: None
    Note: Case-insensitive search
  
  create(userData: CreateUserInput) → User | ValidationError
    Precondition: userData contains required fields
    Success: Returns created User with generated ID
    Failure: ValidationError with field-level errors
    Side Effect: Publishes UserCreated event
    Constraint: Email must be unique
```

### Input/Output Contracts

Define the shape precisely. No surprises.

```
TYPE CreateUserInput:
  email: string
    - REQUIRED
    - Must match RFC 5322
    - Max 255 characters
    - Lowercase normalized
  
  password: string
    - REQUIRED
    - Min 12 characters
    - Must contain: uppercase, lowercase, number, symbol
    - Max 128 characters
  
  name: string
    - OPTIONAL
    - Max 100 characters
    - Unicode allowed
    - Trimmed whitespace

TYPE User:
  id: UUID
    - Generated on creation
    - Immutable
  
  email: string
    - Unique across system
    - Immutable after verification
  
  name: string | null
    - Mutable
    - May be null
  
  createdAt: ISO8601DateTime
    - UTC timezone
    - Immutable
  
  status: "PENDING" | "ACTIVE" | "SUSPENDED" | "DELETED"
    - State machine rules apply
```

### Error Specification

Every failure mode documented or you're lying.

```
Interface: PaymentProcessor

chargeCard(amount: Money, cardToken: string) → ChargeResult

Success Cases:
  - CHARGED: Payment captured successfully
  - PENDING: Payment processing asynchronously

Failure Cases:
  - INSUFFICIENT_FUNDS: Card declined for NSF
    Response: {code: "insufficient_funds", retryable: false}
  
  - CARD_EXPIRED: Card expiration date passed
    Response: {code: "card_expired", retryable: false}
  
  - NETWORK_ERROR: Timeout or connection failure
    Response: {code: "network_error", retryable: true, retryAfter: 30}
  
  - RATE_LIMITED: Too many requests
    Response: {code: "rate_limited", retryable: true, retryAfter: 60}
  
  - INVALID_TOKEN: Token format invalid or expired
    Response: {code: "invalid_token", retryable: false}
```

### Async Interface Patterns

When operations take time, be explicit.

```
Interface: ReportGenerator

Sync Initiation:
  startReport(params: ReportParams) → {jobId: UUID, estimatedTime: seconds}
    - Returns immediately
    - Job queued for processing
    - estimatedTime based on historical data

Async Status:
  getStatus(jobId: UUID) → JobStatus
    JobStatus:
      - QUEUED: Position in queue provided
      - PROCESSING: Progress percentage if available
      - COMPLETED: Result URL provided
      - FAILED: Error details included
      - EXPIRED: Result no longer available

Result Retrieval:
  getResult(jobId: UUID) → ReportData | null
    - Returns null if not ready/expired
    - Result available for 24 hours
    - Large results paginated
```

### Event Contracts

Events aren't fire-and-forget. Define them.

```
Event: OrderPlaced
Version: 1
Schema:
  orderId: UUID
  customerId: UUID
  items: Array<{productId: UUID, quantity: integer, price: Money}>
  total: Money
  timestamp: ISO8601DateTime
  
Guarantees:
  - At-least-once delivery
  - Ordering within customer partition
  - 7-day retention
  
Consumers Must Handle:
  - Duplicate events (idempotency)
  - Out-of-order arrival
  - Schema version differences
```

### Interface Versioning

Because breaking changes are inevitable.

```
Interface: UserAPI

Version Strategy: URL-based (/v1/, /v2/)

v1 (Deprecated: 2024-03-01, Sunset: 2024-09-01):
  GET /v1/users/{id} → UserV1
  
v2 (Current):
  GET /v2/users/{id} → UserV2
  Changes:
    - Added: phoneNumber field
    - Removed: legacyId field
    - Changed: name split into firstName, lastName

Migration:
  - v1 continues working with adapter
  - Deprecation warnings in headers
  - Migration guide provided
```

### Performance Contracts

Numbers or GTFO.

```
Interface: SearchService

search(query: string, filters: FilterSet) → SearchResults

Performance Contract:
  - Response Time: p50 < 100ms, p99 < 500ms
  - Throughput: 1000 req/sec sustained
  - Availability: 99.9% monthly
  - Error Rate: < 0.1%
  
Degradation:
  - Over 1000 req/sec: Queue with backpressure
  - Over 10K results: Pagination required
  - Complex queries: May timeout at 30 seconds
```

### Integration Testing Boundaries

Define exactly what's mockable.

```
Interface: EmailService

Testing Support:
  - Mock Mode: Set via config flag
  - Test Addresses: *@test.example.com bypass sending
  - Sandbox Mode: Real SMTP, no delivery
  - Webhook Testing: POST to configurable endpoint

Contract Tests Required:
  1. Valid email accepted
  2. Invalid email rejected with specific error
  3. Rate limiting enforced
  4. Template substitution works
  5. Attachments under size limit accepted
```

### Common Interface Failures

1. **Optional Confusion**
   ```
   Wrong: user: User  // But sometimes null??
   Right: user: User | null  // Explicit optionality
   ```

2. **Error Swallowing**
   ```
   Wrong: save(data) → boolean  // What failed? Why?
   Right: save(data) → Success | ValidationError | DatabaseError
   ```

3. **Magic Parameters**
   ```
   Wrong: process(data, options)  // What options??
   Right: process(data, {timeout?: number, retries?: number})
   ```

4. **State Assumptions**
   ```
   Wrong: "Call init() before using"  // Hidden dependency
   Right: Interface enforces initialization in constructor
   ```

### The Contract Checklist

Every interface must specify:
- [ ] Each parameter's type and constraints
- [ ] All possible return values
- [ ] Every error condition
- [ ] Performance expectations
- [ ] Side effects and events
- [ ] Versioning strategy
- [ ] Testing approach

Skip any? Prepare for integration hell.

Interfaces are contracts. Contracts require precision. Ambiguity is negligence.

Write interfaces that lawyers would approve and developers can implement blindfolded.
