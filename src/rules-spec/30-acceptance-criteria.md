## Acceptance Criteria Standards

Your acceptance criteria suck. Here's why and how to fix them.

### Given-When-Then or GTFO

Every single requirement gets GWT format. No exceptions.

```
G:[context]W:[action]T:[outcome]
```

**Your Garbage**:
```
"System should handle errors gracefully"
"Login must be secure"
"Performance should be good"
```

**Actual Criteria**:
```
G:user(unauthenticated)
W:submit(invalid_creds,times=3,period=60s)
T:IP_blocked(15m),log(ts,IP,attempts),message("Too many attempts. Try again in 15 minutes.")
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
```
G:user
W:click(submit)
T:form_submits
```

**Complete**:
```
G:user(registered,verified_email),page(checkout),cart(items=3,total=$99.97),address(valid_US)
W:click("Place Order")
T:payment(Stripe),order_id(ORD-YYYYMMDD-XXXXX),email(confirmation,<30s),inventory_decrement,order_history_updated
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

```
F:UserAuth
S:SuccessLogin
G:user(test@example.com,ValidPass123!),no_sessions
W:POST/auth/login(valid_creds)
T:200,JWT(15m),refresh(httpOnly),session_created,log(ts,IP)

S:InvalidEmail
G:email("notanemail")
W:POST/auth/login
T:422,{"error":"Invalid email format"},no_token,log_attempt

S:AccountLocked
G:user(5_failed_attempts_1h)
W:POST/auth/login(correct_password)
T:423,lock_expiry_time,security_alert_email

S:DatabaseDown
G:db_connection_fails
W:login_attempt
T:503,circuit_breaker_open,error_logs,fallback_message

S:ConcurrentLogin
G:login_on_deviceA,login_on_deviceB(100ms)
T:both_process,unique_tokens,two_sessions
```

### Data State Criteria

Define exact data states. Vague states = broken tests.

**Vague**: "Given a user with orders"

**Exact**:
```
G:user(orders_completed=3,year=2023,orders_pending=1,created=today,ltv=$1247.50,last_order=2024-01-10)
```

### Performance Criteria

Numbers. Always numbers.

```
S:APIUnderLoad
G:users(100),requests(10/sec)
W:load_test(5min)
T:p95(<200ms),p99(<500ms),errors(<0.1%),memory(<2GB),cpu(<70%)
```

### Integration Criteria

External systems = explicit contracts.

```
S:StripePayment
G:stripe_test,token("tok_visa"),amount($99.99)
W:payment.process()
T:POST/v1/charges,idempotency_key,timeout(30s),store_charge_id,failures(retry=3,backoff=exp)
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
