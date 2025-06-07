## Bug Classification System

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

**Not Bugs**:
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