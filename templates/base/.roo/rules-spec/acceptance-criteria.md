## Acceptance Criteria Standards

Your acceptance criteria suck. Here's why and how to fix them.

### Given-When-Then or GTFO

Every single requirement gets GWT format. No exceptions.

```gherkin
Given [context/precondition]
When [action/trigger]
Then [observable outcome]
```

**Your Garbage**:
```
"System should handle errors gracefully"
"Login must be secure"
"Performance should be good"
```

**Actual Criteria**:
```gherkin
Given an unauthenticated user
When they submit invalid credentials 3 times in 60 seconds
Then their IP is blocked for 15 minutes
And a security event logs with timestamp, IP, and attempts
And they see "Too many attempts. Try again in 15 minutes."
```

### Measurable Outcomes Only

Can't measure it? Not acceptance criteria.

**Unmeasurable Trash**:
- "User experience should be smooth"
- "System should be fast"
- "Errors handled appropriately"

**Measurable Reality**:
- "Page loads in < 3 seconds on 3G connection"
- "Error message displays within 200ms of validation failure"
- "System processes 1000 orders/minute without degradation"

### Complete Scenarios

Your half-assed scenarios miss critical paths.

**Incomplete**:
```gherkin
Given a user
When they click submit
Then form submits
```

**Complete**:
```gherkin
Given a registered user with verified email
And they are on the checkout page
And cart contains 3 items totaling $99.97
And shipping address is valid US address
When they click "Place Order"
Then payment processes through Stripe
And order ID generates with format ORD-YYYYMMDD-XXXXX
And confirmation email sends within 30 seconds
And inventory decrements by ordered quantities
And order appears in user's order history
```

### Edge Case Coverage

Happy path only? Amateur hour.

**Required Scenarios Per Feature**:

1. **Happy Path** (everything works)
2. **Validation Failures** (each field)
3. **System Failures** (network, database)
4. **Concurrent Operations** (race conditions)
5. **Boundary Conditions** (limits, empty, null)
6. **Security Violations** (injection, overflow)

### Authentication Example (Complete)

```gherkin
Feature: User Authentication

# Happy Path
Scenario: Successful login
  Given a user "test@example.com" with password "ValidPass123!"
  And no active sessions exist
  When they POST to /auth/login with valid credentials
  Then response returns 200 OK
  And body contains JWT token valid for 15 minutes
  And refresh token sets as httpOnly cookie
  And user session creates in database
  And login event logs with timestamp and IP

# Validation Failures  
Scenario: Invalid email format
  Given login request with email "notanemail"
  When they POST to /auth/login
  Then response returns 422 Unprocessable Entity
  And body contains {"error": "Invalid email format"}
  And no token generates
  And failed attempt logs

Scenario: Account locked
  Given user with 5 failed attempts in last hour
  When they POST to /auth/login with correct password
  Then response returns 423 Locked
  And body contains lock expiration time
  And security alert emails to user

# System Failures
Scenario: Database unavailable
  Given database connection fails
  When user attempts login
  Then response returns 503 Service Unavailable
  And circuit breaker opens
  And error logs to monitoring
  And fallback message shows

# Concurrent Operations
Scenario: Simultaneous login attempts
  Given user actively logging in on Device A
  When same user attempts login on Device B within 100ms
  Then both requests process independently
  And both receive valid unique tokens
  And two sessions exist in database
```

### Data State Criteria

Define exact data states. Vague states = broken tests.

**Vague**: "Given a user with orders"

**Exact**:
```gherkin
Given user with:
  - 3 completed orders from 2023
  - 1 pending order created today
  - Total lifetime value: $1,247.50
  - Last order date: 2024-01-10
```

### Performance Criteria

Numbers. Always numbers.

```gherkin
Scenario: API performance under load
  Given 100 concurrent users
  And each user makes 10 requests/second
  When load test runs for 5 minutes
  Then 95th percentile response time < 200ms
  And 99th percentile response time < 500ms
  And error rate < 0.1%
  And memory usage < 2GB
  And CPU usage < 70%
```

### Integration Criteria

External systems = explicit contracts.

```gherkin
Scenario: Payment processing via Stripe
  Given Stripe test mode active
  And valid card token "tok_visa"
  And amount $99.99 USD
  When payment.process() calls
  Then Stripe API receives POST to /v1/charges
  And request includes idempotency key
  And timeout set to 30 seconds
  And successful response stores charge ID
  And failure response triggers 3 retries with exponential backoff
```

### Common Failures You Make

1. **No Numbers**: "Fast" isn't a number
2. **No Errors**: Only testing happy path
3. **No State**: Undefined starting conditions
4. **No Verification**: Can't prove it happened
5. **No Boundaries**: Ignoring limits

### The Checklist

Every acceptance criteria must:
- [ ] Start with Given (complete state)
- [ ] Have clear When (single action)
- [ ] Define Then (measurable outcome)
- [ ] Include error scenarios
- [ ] Specify exact values/thresholds
- [ ] Cover boundaries
- [ ] Be testable by machine

### Reality Check

Bad acceptance criteria kill projects slowly:
1. Developers guess implementation
2. Tests don't match requirements
3. Edge cases surface in production
4. Nobody knows what "done" means

Write criteria so clear that:
- Junior dev can implement
- QA can test without asking
- Customer support knows expected behavior
- You can verify 6 months later

Ambiguity is laziness. Precision is professionalism.

Choose wisely.
