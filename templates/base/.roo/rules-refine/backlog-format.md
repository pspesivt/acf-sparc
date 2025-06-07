## Issue Reporting Structure

Your issue reports are worthless walls of text. Here's how to make them actionable.

### Standard Issue Format

```markdown
## [TYPE]-[NUMBER]: [One-Line Summary]

**Severity**: CRITICAL | HIGH | MEDIUM | LOW
**Category**: Performance | Security | Logic | Reliability | Maintainability
**Location**: [exact/file/path.py:line_numbers]
**Detected**: [timestamp]
**Status**: NEW | ACKNOWLEDGED | IN_PROGRESS | RESOLVED | WONT_FIX

### Description
[2-3 sentences max. What's broken, why it matters]

### Evidence
```
[Actual code/metrics/logs proving the issue exists]
```

### Impact Analysis
- **Users**: [How users experience this]
- **System**: [Technical consequences]
- **Business**: [Money/reputation cost]

### Root Cause
[One sentence. The actual problem, not symptoms]

### Reproduction Steps
1. [Exact step]
2. [With specific values]
3. [Observable failure]

### Suggested Resolution
[High-level approach. NO implementation code]

### Dependencies
- Blocks: [Issue IDs this prevents]
- Blocked by: [Issue IDs that must fix first]
```

Miss any section? Your issue gets ignored.

### Issue ID Convention

```
[CATEGORY]-[YYYY][MM][DD]-[SEQUENCE]

Examples:
SEC-20240115-001   # First security issue on Jan 15, 2024
PERF-20240115-047  # 47th performance issue same day
```

### Priority Matrix

| Severity | Response Time | Review Cycle | Escalation |
|----------|---------------|--------------|------------|
| CRITICAL | < 4 hours | Every 2 hours | Immediate |
| HIGH | < 24 hours | Daily | After 48h |
| MEDIUM | < 1 week | Weekly | After 2 weeks |
| LOW | < 1 month | Monthly | Never |

### Bulk Reporting Template

When you find 50+ issues (you will):

```yaml
---
scan_id: SCAN-20240115-1430
scan_type: security | performance | quality
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
    
  - id: SEC-20240115-002
    title: "Authentication bypass via header manipulation"
    location: middleware/auth.py:89
    
high_priority_patterns:
  - pattern: "Unbounded pagination"
    count: 8
    example_location: api/list_endpoints.py
    
  - pattern: "Missing rate limiting"
    count: 14
    example_location: api/public_routes.py

full_report: docs/quality/scan-20240115-1430.md
---
```

### Evidence Requirements

**Performance Issues**:
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

**Security Issues**:
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

**Logic Issues**:
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

Before creating an issue:

1. **Search existing**: `grep -r "same file:line"`
2. **Pattern match**: Is this instance of known pattern?
3. **Root cause match**: Different symptom, same cause?

**Duplicate Detection**:
```yaml
original: SEC-20240110-003
duplicate_attempt: SEC-20240115-001
reason: "Same SQL injection pattern, different parameter"
action: "Add location to original issue"
```

### Anti-Patterns in Reporting

**Your Garbage**:
```
"Something seems slow"
"Security might be an issue here"
"This code smells bad"
"Should probably refactor"
```

**Actual Reports**:
```
"API endpoint /users takes 3.8s under 100 concurrent requests"
"Password stored in plaintext in localStorage"
"Cyclomatic complexity 47 in process_order method"
"67% code duplication between UserService and AdminService"
```

### Batch Operations

```bash
# Generate report from scan results
./scripts/generate_backlog.py \
  --scan-results scan-20240115.json \
  --severity-threshold medium \
  --output-format markdown \
  > docs/quality/backlog-20240115.md

# Bulk update status
./scripts/update_issues.py \
  --pattern "SEC-202401*" \
  --status ACKNOWLEDGED \
  --assignee security-team
```

### Integration Formats

**Jira/Linear Export**:
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

Every issue must have:
- [ ] Unique ID following convention
- [ ] One-line summary under 80 characters
- [ ] Severity based on actual impact
- [ ] Exact file:line location
- [ ] Reproducible evidence
- [ ] Quantified impact
- [ ] Root cause (not symptoms)
- [ ] Dependencies mapped

### The Truth

Most issue reports fail because:
1. **Vague descriptions** ("It's broken")
2. **Missing evidence** (Trust me bro)
3. **Wrong severity** (Everything is CRITICAL)
4. **No reproduction** (Works on my machine)
5. **Solution focus** (Implementing before understanding)

Your report should let a developer who's never seen the code:
1. Understand the problem in 30 seconds
2. Reproduce it in 2 minutes
3. Verify their fix worked

Can't do that? Your report is noise.
