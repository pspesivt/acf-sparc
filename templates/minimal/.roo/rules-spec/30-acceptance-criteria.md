## Acceptance Criteria Standards
### Given-When-Then or GTFO
```
G:[context]W:[action]T:[outcome]
```
**Actual**:
```
G:user(unauthenticated)
W:submit(invalid_creds,times=3,period=60s)
T:IP_blocked(15m),log(ts,IP,attempts),message("Too many attempts. Try again in 15 minutes.")
```
### Measurable Outcomes Only
```
page_load<3s@3G
error_msg<=200ms
throughput>=1000_orders/min
```
### Complete Scenarios
```
G:user(registered,verified_email),page(checkout),cart(items=3,total=$99.97),address(valid_US)
W:click("Place Order")
T:payment(Stripe),order_id(ORD-YYYYMMDD-XXXXX),email(confirmation,<30s),inventory_decrement,order_history_updated
```
### Edge Case Coverage
1. Happy_Path  
2. Validation_Failures  
3. System_Failures  
4. Concurrent_Operations  
5. Boundary_Conditions  
6. Security_Violations
### Authentication Example (Complete)
```
F:UserAuth;S:SuccessLogin;G:user(test@example.com,ValidPass123!),no_sessions;W:POST/auth/login(valid_creds);T:200,JWT(15m),refresh(httpOnly),session_created,log(ts,IP)
F:UserAuth;S:InvalidEmail;G:email("notanemail");W:POST/auth/login;T:422,{"error":"Invalid email format"},no_token,log_attempt
F:UserAuth;S:AccountLocked;G:user(5_failed_attempts_1h);W:POST/auth/login(correct_password);T:423,lock_expiry_time,security_alert_email
F:UserAuth;S:DatabaseDown;G:db_connection_fails;W:login_attempt;T:503,circuit_breaker_open,error_logs,fallback_message
F:UserAuth;S:ConcurrentLogin;G:login_on_deviceA,login_on_deviceB(100ms);W:POST/auth/login;T:both_process,unique_tokens,2_sessions
```
### Data State Criteria
```
G:user(orders_completed=3,year=2023,orders_pending=1,created=today,ltv=$1247.50,last_order=2024-01-10)
```
### Performance Criteria
```
S:APIUnderLoad;G:users=100,req=10/s;W:load_test(5m);T:p95<200ms,p99<500ms,err<0.1%,mem<2GB,cpu<70%
```
### Integration Criteria
```
S:StripePayment;G:stripe_test,token="tok_visa",amount=$99.99;W:payment.process();T:POST/v1/charges,idempotency_key,timeout=30s,store_charge_id,failures=retry=3,backoff=exp
```
### Common Failures You Make
no_numbers;no_error_paths;no_state;no_verification;no_boundaries
### The Checklist
[G:complete_state,W:single_action,T:measurable_outcome,error_scenarios,exact_values,boundaries,machine_testable]
### Reality Check
reality:dev_guess,tests_mismatch,edges_in_prod,unknown_done