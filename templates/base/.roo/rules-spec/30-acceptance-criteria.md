## Acceptance Criteria Standards

### Given-When-Then or GTFO
Every requirement uses GWT format:
```
G:[context]W:[action]T:[outcome]
```

Bad:
```
"System should handle errors gracefully"
"Login must be secure"
"Performance should be good"
```

Good:
```
G:user(unauthenticated)
W:submit(invalid_creds,times=3,period=60s)
T:IP_blocked(15m),log(ts,IP,attempts),message("Too many attempts. Try again in 15 minutes.")
```

### Measurable Outcomes Only
Unmeasurable: "User experience should be smooth"
Measurable: "Page loads in < 3s on 3G connection"

### Complete Scenarios
Incomplete:
```
G:user
W:click(submit)
T:form_submits
```

Complete:
```
G:user(registered,verified_email),page(checkout),cart(items=3,total=$99.97),address(valid_US)
W:click("Place Order")
T:payment(Stripe),order_id(ORD-YYYYMMDD-XXXXX),email(confirmation,<30s),inventory_decrement,order_history_updated
```

### Edge Case Coverage
Required scenarios:
1. Happy Path
2. Validation Failures
3. System Failures
4. Concurrent Operations
5. Boundary Conditions
6. Security Violations

### Authentication Example
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
Vague: "Given a user with orders"
Exact: 
```
G:user(orders_completed=3,year=2023,orders_pending=1,created=today,ltv=$1247.50,last_order=2024-01-10)
```

### Performance Criteria
```
S:APIUnderLoad
G:users(100),requests(10/sec)
W:load_test(5min)
T:p95(<200ms),p99(<500ms),errors(<0.1%),memory(<2GB),cpu(<70%)
```

### Integration Criteria
```
S:StripePayment
G:stripe_test,token("tok_visa"),amount($99.99)
W:payment.process()
T:POST/v1/charges,idempotency_key,timeout(30s),store_charge_id,failures(retry=3,backoff=exp)
```

### Common Failures
1. No Numbers
2. No Errors
3. No State
4. No Verification
5. No Boundaries

### Checklist
- Start with Given (complete state)
- Clear When (single action)
- Define Then (measurable outcome)
- Include error scenarios
- Specify exact values/thresholds
- Cover boundaries
- Machine testable

### Reality Check
Bad criteria effects:
1. Developers guess implementation
2. Tests don't match requirements
3. Edge cases in production
4. Undefined "done"

Write criteria for:
- Junior dev implementation
- QA testing without questions
- Clear customer support expectations
- Future verification