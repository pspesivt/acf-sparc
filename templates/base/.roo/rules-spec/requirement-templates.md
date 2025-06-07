## Requirement Templates

Stop writing novels. Use these templates or requirements remain garbage.

### User Story Template

```markdown
As a [specific user type]
I want to [concrete action]
So that [measurable outcome]

Acceptance Criteria:
- Given [context]
- When [action]
- Then [observable result]

Edge Cases:
- What if [failure scenario]?
- What if [boundary condition]?
- What if [concurrent action]?
```

**Wrong**:
```
As a user, I want security so I feel safe.
```

**Right**:
```
As a registered customer
I want to enable 2FA on my account
So that unauthorized access risk drops by 99%

Acceptance Criteria:
- Given I have 2FA disabled
- When I scan QR code with authenticator app
- Then my account requires 6-digit code on next login
```

### Functional Requirement Template

```markdown
## FR-[NUMBER]: [Requirement Name]

**Priority**: Critical | High | Medium | Low
**Category**: Auth | Data | UI | API | Performance

**Requirement**:
The system SHALL [specific behavior] WHEN [condition] 
WITH [constraints].

**Rationale**:
[Why this matters, backed by data/user need]

**Acceptance**:
1. Given [setup]
2. When [trigger]
3. Then [outcome]

**Dependencies**:
- Requires: [Other FR numbers]
- Blocks: [Other FR numbers]

**Validation**:
- [ ] Unit testable
- [ ] Integration testable
- [ ] Manually verifiable
```

### Non-Functional Requirement Template

```markdown
## NFR-[NUMBER]: [Quality Attribute]

**Category**: Performance | Security | Usability | Reliability

**Requirement**:
[Metric] SHALL [operator] [threshold] UNDER [conditions]

**Current State**: [Baseline if known]
**Target State**: [Specific number]
**Measurement**: [How to verify]

**Example**:
NFR-001: API Response Time
The API SHALL respond in < 200ms for 95th percentile
UNDER normal load (1000 req/sec) 
EXCLUDING cold starts
```

### Constraint Documentation Template

```markdown
## C-[NUMBER]: [Constraint Name]

**Type**: Technical | Business | Regulatory | Resource

**Constraint**:
MUST [requirement] BECAUSE [reason]
IMPACT: [what this prevents/requires]

**Workarounds**: 
- Option A: [description] → [trade-off]
- Option B: [description] → [trade-off]
- None: [why it's absolute]

**Example**:
C-001: GDPR Compliance
MUST allow data export within 30 days BECAUSE GDPR Article 20
IMPACT: Requires data pipeline for user data assembly
```

### Edge Case Template

```markdown
## Edge Case: [Scenario Name]

**Trigger**: [What causes this]
**Frequency**: Common | Rare | Theoretical
**Impact**: Data Loss | Service Down | UX Degradation | Security Risk

**Scenario**:
GIVEN [system state]
WHEN [unusual event]
THEN [expected behavior]

**Mitigation**:
- Prevent: [How to avoid]
- Detect: [How to identify]
- Recover: [How to fix]
```

### Performance Requirement Template

```markdown
## Performance Target: [Operation Name]

**Metric**: Response Time | Throughput | Resource Usage
**Current**: [Measured baseline]
**Target**: [Specific number with conditions]

**Load Profile**:
- Concurrent Users: [number]
- Request Rate: [requests/sec]
- Data Volume: [size]
- Geographic Distribution: [regions]

**Degradation Plan**:
- Green: [0-threshold1] → Full features
- Yellow: [threshold1-threshold2] → Degrade [feature]
- Red: [threshold2+] → Circuit break [operation]
```

### Integration Requirement Template

```markdown
## Integration: [System Name]

**Type**: REST API | GraphQL | Message Queue | Database | File
**Direction**: Inbound | Outbound | Bidirectional

**Contract**:
- Endpoint: [URL/queue/table]
- Authentication: [method]
- Rate Limits: [requests/period]
- SLA: [availability/latency]

**Data Flow**:
1. Source: [system] produces [data type]
2. Transform: [any mapping/validation]
3. Destination: [system] consumes [format]

**Failure Modes**:
- Timeout: [behavior]
- Invalid Data: [behavior]
- Service Down: [behavior]
```

### Quick Templates for Common Patterns

**Authentication Requirement**:
```
Users SHALL authenticate via [method]
WITH [factors] REQUIRING [strength]
EXPIRING after [duration] UNLESS [condition]
```

**Data Validation Requirement**:
```
System SHALL reject [data type] 
WHEN [validation rule fails]
RESPONDING with [error code/message]
LOGGING [what details]
```

**Permission Requirement**:
```
[Role] SHALL [action] [resource]
ONLY WHEN [conditions]
TRACKED BY [audit log type]
```

### Usage Rules

1. **No empty sections**. Delete what doesn't apply.
2. **No vague terms**. "Fast", "secure", "user-friendly" = meaningless.
3. **Include numbers**. Every requirement needs measurable criteria.
4. **Test each requirement**. If you can't test it, rewrite it.
5. **Link dependencies**. Orphan requirements = integration hell.

Templates aren't bureaucracy. They're the difference between building what's needed and building what you assumed was needed.

Use them or enjoy your requirements meetings from hell.
