## Issue Reporting Structure

### Standard Issue Format
```
[TYPE]-[NUMBER]:[Summary]
SEV:CRITICAL|HIGH|MEDIUM|LOW CAT:Performance|Security|Logic|Reliability|Maintainability
LOC:[path:lines]DET:[timestamp]STAT:NEW|ACK|WIP|DONE|WONT
DESC:[broken,why_matters]
EVID:[code/metrics/logs]
IMP:U[user_exp]S[tech]B[cost]
ROOT:[actual_problem]
REPRO:1[step]2[values]3[failure]
FIX:[approach]
DEP:BLOCKS[IDs]BY[IDs]
```
Missing sections = ignored

### Issue ID Convention
```
[CATEGORY]-[YYYY][MM][DD]-[SEQUENCE]
Examples:
SEC-20240115-001
PERF-20240115-047
```

### Priority Matrix
| Severity | Response | Review | Escalation |
|----------|----------|--------|------------|
| CRITICAL | <4h | 2h | Immediate |
| HIGH | <24h | Daily | After 48h |
| MEDIUM | <1w | Weekly | After 2w |
| LOW | <1m | Monthly | Never |

### Bulk Reporting Template
```yaml
---
scan_id: SCAN-20240115-1430
scan_type: security|performance|quality
total_issues: 127
critical: 3
high: 22
medium: 67
low: 35

summary: |
  Scanned 10,450 lines across 127 files.
  3 SQL injection vectors require immediate attention.
  N+1 query pattern found in 15 endpoints.

critical_issues:
  - id: SEC-20240115-001
    title: "SQL injection in user search"
    location: handlers/user.py:45
    
high_priority_patterns:
  - pattern: "Unbounded pagination"
    count: 8
    example_location: api/list_endpoints.py

full_report: docs/quality/scan-20240115-1430.md
---
```

### Evidence Requirements
Performance:
```yaml
evidence:
  baseline_metric: 45ms
  current_metric: 3,847ms
  degradation: 8449%
  sample_size: 1000
  conditions: "Production load"
  profiler_output: |
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1000    3.567    0.004    3.567    0.004 database.py:89(fetch_user)
```

Security:
```yaml
evidence:
  vulnerability_class: "A03:2021 – Injection"
  cvss_score: 9.8
  exploit_difficulty: "Script kiddie level"
  poc: |
    curl -X POST https://api.example.com/search \
      -d "q='; DROP TABLE users; --"
  affected_users: "All"
```

Logic:
```yaml
evidence:
  expected: "Order total: $99.99"
  actual: "Order total: $-0.01"
  test_case: |
    order = Order()
    order.add_item(price=-100.00, quantity=1)
    order.add_discount(percent=1)
    assert order.total == -0.01  # PASSES - BAD
```

### Deduplication Rules
Before creating:
1. Search existing: `grep -r "same file:line"`
2. Pattern match: Instance of known pattern?
3. Root cause match: Different symptom, same cause?

```yaml
original: SEC-20240110-003
duplicate_attempt: SEC-20240115-001
reason: "Same SQL injection pattern, different parameter"
action: "Add location to original issue"
```

### Anti-Patterns vs Actual Reports
Bad: "Something seems slow"
Good: "API endpoint /users takes 3.8s under 100 concurrent requests"

### Batch Operations
```bash
./scripts/generate_backlog.py \
  --scan-results scan-20240115.json \
  --severity-threshold medium \
  --output-format markdown \
  > docs/backlog/security-backlog-20240115.md

./scripts/update_issues.py \
  --pattern "SEC-202401*" \
  --status ACKNOWLEDGED \
  --assignee security-team
```

### Integration Formats
```json
{
  "issueType": "Bug",
  "summary": "[PERF-20240115-001] N+1 query in order listing",
  "description": "See: docs/quality/issues/PERF-20240115-001.md",
  "priority": "High",
  "labels": ["performance", "database", "sparc-refine"],
  "customFields": {
    "severity": "HIGH",
    "detectedBy": "brutus",
    "sparkPhase": "refinement"
  }
}
```

### Review Readiness Checklist
- Unique ID following convention
- One-line summary <80 chars
- Severity based on actual impact
- Exact file:line location
- Reproducible evidence
- Quantified impact
- Root cause (not symptoms)
- Dependencies mapped

### Common Failures
1. Vague descriptions
2. Missing evidence
3. Wrong severity
4. No reproduction
5. Solution focus before understanding

Good report lets dev:
1. Understand in 30s
2. Reproduce in 2min
3. Verify fix worked