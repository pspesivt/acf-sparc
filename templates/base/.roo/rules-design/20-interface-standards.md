## Interface Definition Standards

I:ComponentName
P:[problem]
M:[operations]
IN:[types,constraints]
OUT:[success|failure]
SE:[logs,events,state]
INV:[constants]

### Method Specification
Bad:
```
getUser(id)
processOrder(data)
handleRequest(req)
doStuff(thing)
```

Good:
```
I:UserRepository
findById(userId:UUID)→User|null
PRE:valid_UUID
OK:User(all_fields)
FAIL:null
SE:log(query_time)
PERF:cache<10ms,DB<100ms

findByEmail(email:string)→User|null
PRE:email_RFC5322
OK:User
FAIL:null
SE:none
NOTE:case_insensitive

create(userData:CreateUserInput)→User|ValidationError
PRE:required_fields
OK:User(with_generated_ID)
FAIL:ValidationError(field_errors)
SE:publish(UserCreated)
CON:email_unique
```

### Input/Output Contracts
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

### Testing Boundaries
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

### Common Failures
1. Optional Confusion
2. Magic Parameters: Wrong: process(data, options) vs Right: process(data, {timeout?: number, retries?: number})
3. State Assumptions: Wrong: "Call init() before using" vs Right: Interface enforces initialization in constructor

### Contract Checklist
- Parameter types/constraints
- All return values
- Every error condition
- Performance expectations
- Side effects/events
- Versioning strategy
- Testing approach