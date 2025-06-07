## Bug Classification System

Stop calling everything a "bug". Here's what you're actually finding.

### Primary Classification Hierarchy

```
BUG
├── LOGIC ERRORS
│   ├── Incorrect Computation
│   ├── Wrong Conditional
│   ├── State Corruption
│   └── Race Condition
├── INTEGRATION FAILURES  
│   ├── API Contract Violation
│   ├── Data Format Mismatch
│   ├── Protocol Error
│   └── Timeout Handling
├── RESOURCE ISSUES
│   ├── Memory Leak
│   ├── Handle Leak
│   ├── Connection Pool Exhaustion
│   └── Unbounded Growth
├── SECURITY VULNERABILITIES
│   ├── Injection
│   ├── Authentication Bypass
│   ├── Authorization Failure
│   └── Data Exposure
└── RELIABILITY DEFECTS
    ├── Crash
    ├── Hang
    ├── Data Loss
    └── Corruption
```

### Severity Classification

**CRITICAL** (Production Down):
```yaml
criteria:
  - Data loss occurring
  - Security breach active
  - Complete service failure
  - Financial computation errors
  
examples:
  - "Payment processor charges wrong amounts"
  - "Authentication bypass allows any password"
  - "Database corruption on concurrent writes"
  
sla: Fix within 4 hours
```

**HIGH** (Major Degradation):
```yaml
criteria:
  - Feature completely broken
  - Performance degraded >10x
  - Security vulnerability exploitable
  - Data accuracy compromised
  
examples:
  - "Search returns empty for valid queries"
  - "API timeout after 30 seconds"
  - "XSS in user comments"
  
sla: Fix within 24 hours
```

**MEDIUM** (Functionality Impaired):
```yaml
criteria:
  - Feature partially broken
  - Performance degraded 2-10x
  - Workaround available
  - Non-critical data issues
  
examples:
  - "Pagination skips records"
  - "Slow query on large datasets"
  - "Error messages expose stack traces"
  
sla: Fix within 1 week
```

**LOW** (Annoyance):
```yaml
criteria:
  - Cosmetic issues
  - Minor performance impact
  - Edge cases only
  - Documentation mismatch
  
examples:
  - "Tooltip shows wrong format"
  - "Unnecessary database call"
  - "Typo in error message"
  
sla: Fix when convenient
```

### Bug Patterns and Root Causes

**Logic Errors**:
```yaml
pattern: Off-by-one
locations: [loops, array access, pagination]
root_causes:
  - Inclusive vs exclusive bounds confusion
  - Zero vs one-based indexing
  - Forgetting array.length - 1
example: |
  for i in range(len(items) + 1):  # BOOM on items[i]
```

```yaml
pattern: Null/None handling
locations: [API responses, database queries, optional configs]
root_causes:
  - Missing null checks
  - Assuming optional always present
  - Null vs empty confusion
example: |
  user.profile.settings.theme  # profile might be None
```

**State Corruption**:
```yaml
pattern: Concurrent modification
locations: [shared state, cache updates, session data]
root_causes:
  - Missing locks/synchronization
  - Read-modify-write without atomicity
  - Stale data overwrites
example: |
  balance = get_balance()
  # Another thread updates here
  set_balance(balance - amount)  # Lost update
```

**Resource Leaks**:
```yaml
pattern: Connection leak
locations: [database, HTTP clients, file handles]
root_causes:
  - Missing finally/close
  - Exception before cleanup
  - Circular references
example: |
  conn = db.connect()
  result = conn.query(sql)  # Exception here
  conn.close()  # Never reached
```

### Detection Patterns

**Static Analysis Indicators**:
```python
# Complexity bombs
def process_order(order, user, inventory, payment, shipping, tax_config, 
                  promo_codes, loyalty_points, gift_cards, store_credit):
    # 500 lines of nested ifs
    # Cyclomatic complexity: 73
    # Bug probability: 100%

# Missing error handling
def critical_operation():
    data = external_api.fetch()  # What if this fails?
    return process(data)

# Type confusion
def calculate_total(items):
    return sum(item.price for item in items)  # What if price is string?
```

**Runtime Indicators**:
```yaml
memory_leak:
  symptom: "RSS grows 100MB/hour"
  pattern: "Objects created but not freed"
  detection: |
    import tracemalloc
    # Snapshot comparison shows growing allocations

race_condition:
  symptom: "Intermittent test failures"
  pattern: "Success depends on timing"
  detection: |
    Run with threading sanitizer
    Add random delays to expose

performance_cliff:
  symptom: "Fast until exactly 1000 items"
  pattern: "Algorithm complexity explosion"
  detection: |
    Profile with increasing N
    Look for O(n²) or worse
```

### Classification Decision Tree

```
Is data corrupted/lost?
├─ Yes → CRITICAL
└─ No → Does feature work at all?
    ├─ No → HIGH
    └─ Yes → Is workaround reasonable?
        ├─ No → MEDIUM
        └─ Yes → LOW
```

### Bug Relationship Mapping

```yaml
root_bug: LOGIC-20240115-001
  causes:
    - INTEG-20240115-023  # API returns invalid data
    - PERF-20240115-045   # Retry storm from errors
  
symptom_cluster: "Login failures"
  underlying_bugs:
    - SEC-20240115-002   # Session token corruption
    - LOGIC-20240115-007 # Race in session creation
    - RES-20240115-001   # Connection pool exhausted
```

### False Positive Patterns

**Not Bugs** (stop reporting these):
```yaml
- pattern: "Slow on my machine"
  reason: "Local environment issue"
  
- pattern: "Works differently than I expected"
  reason: "Requirement misunderstanding"
  
- pattern: "Could be optimized"
  reason: "That's enhancement, not bug"
  
- pattern: "Old library version"
  reason: "If it works, it's technical debt, not bug"
```

### Reproduction Requirements

**Minimal Reproduction**:
```python
"""
Bug: Order total calculation wrong with discounts
Category: LOGIC
Severity: CRITICAL
"""

def test_reproduction():
    # Setup
    order = Order()
    order.add_item(price=100, quantity=2)  # $200
    order.add_discount(percent=10)          # -$20
    order.add_discount(amount=15)           # -$15
    
    # Bug manifests
    assert order.total == 165  # FAILS: actual is 150
    
    # Root cause: Discounts applied to already-discounted total
```

### Impact Scoring

```python
def calculate_bug_priority(bug):
    severity_score = {
        "CRITICAL": 1000,
        "HIGH": 100,
        "MEDIUM": 10,
        "LOW": 1
    }[bug.severity]
    
    user_impact = bug.affected_users / total_users
    frequency = bug.occurrences_per_day
    
    priority = severity_score * user_impact * frequency
    
    return {
        "priority_score": priority,
        "fix_order": "IMMEDIATE" if priority > 100 else "QUEUED"
    }
```

### The Reality

You'll find bugs in these ratios:
- 40% Logic errors (developer can't think)
- 30% Integration failures (assumptions wrong)
- 20% Resource issues (forgot to clean up)
- 10% Security vulnerabilities (didn't think about evil users)

Most "critical" bugs are actually medium. Most "bugs" are actually feature requests.

Learn the difference or waste everyone's time.
```

## .roo/rules-refine/performance-metrics.md

```markdown
## What to Measure, How

Your performance "monitoring" is probably `print(f"Time: {end-start}")`. Here's actual measurement.

### Core Metrics Hierarchy

```yaml
latency:
  definition: "Time from request start to response complete"
  
  percentiles:
    p50: "Median - your happy path"
    p95: "Reality for 1 in 20 users"  
    p99: "Your actual SLA"
    p99.9: "When shit hits fan"
    
  breakdown:
    - Network RTT
    - Queue time
    - Processing time
    - I/O wait
    - Serialization

throughput:
  definition: "Operations completed per time unit"
  
  measurements:
    requests_per_second: "RPS at various percentiles"
    transactions_per_second: "Business operations"
    bytes_per_second: "Data transfer rate"
    
  constraints:
    saturation_point: "Where latency goes exponential"
    bottleneck_resource: "CPU, memory, I/O, or network"

resource_utilization:
  definition: "Percentage of available capacity used"
  
  targets:
    cpu: "< 70% sustained, < 90% peak"
    memory: "< 80% including cache"
    disk_io: "< 60% to avoid queuing"
    network: "< 50% to handle bursts"
```

### Measurement Points

**Application Level**:
```python
# WRONG: Measuring nothing useful
start = time.time()
result = do_something()
print(f"Took {time.time() - start}")

# RIGHT: Structured metrics
from prometheus_client import Histogram, Counter

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint', 'status']
)

@request_duration.time()
def handle_request(request):
    # Automatic timing with labels
    pass

# OR with context manager
with request_duration.labels(
    method='POST',
    endpoint='/api/users',
    status='200'
).time():
    process_user_creation()
```

**Database Level**:
```sql
-- Query analysis
EXPLAIN (ANALYZE, BUFFERS) 
SELECT u.*, o.* 
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- Key metrics:
-- Execution Time: 234.567 ms
-- Planning Time: 0.123 ms
-- Shared Buffer Hits: 8932
-- Shared Buffer Misses: 234 (BAD - disk I/O)
-- Rows Removed by Filter: 10000 (BAD - poor index)
```

**System Level**:
```bash
# CPU profiling
perf record -F 99 -p $(pgrep python) -- sleep 30
perf report

# Memory profiling  
tracemalloc + memory_profiler for Python
valgrind --tool=massif for C/C++

# I/O profiling
iotop -o -P -a
iostat -x 1

# Network profiling
ss -i | grep -E 'cwnd|ssthresh|rtt'
tcpdump -i eth0 -w capture.pcap
```

### Metric Collection Patterns

**Pull vs Push**:
```yaml
pull_metrics:  # Prometheus style
  pros:
    - Service discovery
    - No metric loss if collector down
    - Standardized endpoints
  cons:
    - Need accessible endpoint
    - Polling interval limits
    
push_metrics:  # StatsD style
  pros:
    - Fire and forget
    - Works behind firewall
    - Real-time streaming
  cons:
    - Metric loss if collector down
    - No standard format
```

**Sampling Strategies**:
```python
# Adaptive sampling based on importance
def should_sample(request):
    # Always sample errors
    if request.status >= 400:
        return True
    
    # Sample 10% of normal traffic
    if random.random() < 0.1:
        return True
        
    # Sample all slow requests
    if request.duration > 1.0:
        return True
        
    return False
```

### Load Testing Profiles

**Steady State**:
```yaml
profile: steady_state
duration: 3600s
users: 1000
ramp_up: 300s
scenario:
  - endpoint: /api/users
    method: GET
    weight: 70
  - endpoint: /api/orders
    method: POST
    weight: 30
```

**Stress Test**:
```yaml
profile: stress_test
stages:
  - duration: 300s
    target_users: 100
  - duration: 600s
    target_users: 1000  
  - duration: 600s
    target_users: 5000
  - duration: 300s
    target_users: 100
success_criteria:
  error_rate: "< 1%"
  p95_latency: "< 500ms"
```

**Spike Test**:
```yaml
profile: spike_test
baseline_users: 100
spike_users: 10000
spike_duration: 60s
recovery_time: "< 120s"
```

### Analysis Patterns

**Latency Breakdown**:
```python
@trace_execution
def api_endpoint(request):
    with trace_span("validation"):
        validate_request(request)  # 2ms
    
    with trace_span("database"):
        user = fetch_user(request.user_id)  # 45ms
        
    with trace_span("business_logic"):
        result = process_business_rules(user)  # 5ms
        
    with trace_span("serialization"):
        return jsonify(result)  # 1ms

# Total: 53ms
# Bottleneck: Database (85% of time)
```

**Throughput Analysis**:
```python
def analyze_throughput(metrics):
    # Little's Law: L = λ × W
    # L = number in system
    # λ = arrival rate  
    # W = time in system
    
    concurrency = metrics.concurrent_requests
    arrival_rate = metrics.requests_per_second
    latency = metrics.average_latency_seconds
    
    theoretical_max = concurrency / latency
    actual_throughput = arrival_rate
    
    utilization = actual_throughput / theoretical_max
    
    if utilization > 0.8:
        return "SATURATED: Add capacity or optimize"
```

### Bottleneck Identification

**CPU Bound**:
```yaml
symptoms:
  - CPU usage at 100%
  - Low I/O wait
  - Linear scaling with cores
profiling:
  - Flame graphs show hot functions
  - High user CPU time
solutions:
  - Algorithm optimization
  - Parallel processing
  - Caching computation results
```

**I/O Bound**:
```yaml
symptoms:
  - High I/O wait
  - Low CPU usage
  - Disk/network saturation
profiling:
  - strace shows blocking on read/write
  - High system CPU time
solutions:
  - Async I/O
  - Batching
  - Better indexes
  - Connection pooling
```

**Memory Bound**:
```yaml
symptoms:
  - High memory usage
  - Swap activity
  - GC pressure
profiling:
  - Heap dumps show large objects
  - Allocation profiler shows churn
solutions:
  - Object pooling
  - Streaming processing
  - Memory-efficient data structures
```

### Performance Budgets

```yaml
page_load_budget:
  total: 3000ms
  breakdown:
    dns_lookup: 50ms
    tcp_connection: 100ms
    tls_negotiation: 150ms
    server_response: 200ms
    content_download: 500ms
    parsing: 200ms
    rendering: 800ms
    javascript_execution: 1000ms

api_endpoint_budget:
  total: 200ms
  breakdown:
    request_parsing: 5ms
    authentication: 10ms
    authorization: 5ms
    business_logic: 50ms
    database_queries: 100ms
    response_serialization: 10ms
    network_overhead: 20ms
```

### Alerting Thresholds

```yaml
alerts:
  - name: "High Latency"
    condition: "p95 > 500ms for 5 minutes"
    severity: "warning"
    
  - name: "Very High Latency"
    condition: "p95 > 1000ms for 2 minutes"
    severity: "critical"
    
  - name: "Error Rate"
    condition: "5xx errors > 1% for 3 minutes"
    severity: "critical"
    
  - name: "Saturation"
    condition: "CPU > 90% for 10 minutes"
    severity: "warning"
```

### Common Measurement Failures

**Wrong Metrics**:
```yaml
vanity_metrics:
  - Total requests served (who cares without time context)
  - Average latency (p50/p95/p99 matter more)
  - Server uptime (available != working)
  
real_metrics:
  - Requests per second at p99 < 200ms
  - Error rate by error type
  - Time to first byte (TTFB)
```

**Bad Instrumentation**:
```python
# WRONG: Measuring the measurement
start = time.time()
metrics.record("db.query", time.time() - start)  # Includes metric recording time!

# RIGHT: Measure only the operation
start = time.time()
result = db.query(sql)
duration = time.time() - start
metrics.record("db.query", duration)
return result
```

### The Truth

90% of "performance monitoring" is:
- `console.log` with timestamps
- Checking Task Manager when it's slow
- Blaming the database without evidence
- Adding cache without measuring

Real performance work:
1. Measure everything
2. Find the actual bottleneck (not guess)
3. Fix the biggest problem first
4. Measure again to verify

Most performance problems are in your code, not the framework. Measure first, optimize second, or waste time optimizing the wrong thing.
