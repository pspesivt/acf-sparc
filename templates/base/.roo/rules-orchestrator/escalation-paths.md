## Escalation Paths

Stuck? Here's how to unfuck the situation.

### Escalation Triggers

| Situation | Threshold | Action |
|-----------|-----------|--------|
| Task bounced | 3+ times | Decompose or park |
| Mode unavailable | Immediate | Park with clear reason |
| Conflicting requirements | 2+ attempts | Back to spec |
| Technical impossibility | Confirmed | Back to design |
| Circular dependencies | Detected | Break cycle, resequence |

### Resolution Playbook

#### 1. Missing Specialist
```yaml
situation: "Need React engineer"
attempts: 0  # Don't even try
action: PARK

parked_task:
  task: "Implement dashboard UI"
  blocked_on: "react-engineer not available"
  workaround: "None - core functionality"
```

Stop trying to force Python engineers to write React. Park it.

#### 2. Bouncing Tasks
```yaml
situation: "Task bounced 3 times"
root_cause: "Task too vague or too large"

action: DECOMPOSE
# Bad: "Make authentication work"
# Good:
  - "Define auth requirements"
  - "Design JWT strategy"
  - "Implement login endpoint"
```

If it bounces twice, you fucked up the decomposition.

#### 3. Requirement Conflicts
```yaml
situation: "Conflicting requirements discovered"
examples:
  - "Must be stateless" vs "Must maintain session"
  - "Real-time updates" vs "Cache for 1 hour"

action: BACK_TO_SPEC
handoff:
  to: spec
  context:
    blockers:
      - "Requirement A conflicts with Requirement B"
      - "Need stakeholder decision"
```

Don't guess. Get clarity or stay blocked.

#### 4. Technical Walls
```yaml
situation: "Technically impossible as designed"
examples:
  - "Sub-millisecond response over satellite internet"
  - "Store 1TB in browser localStorage"

action: BACK_TO_DESIGN
handoff:
  to: design
  context:
    blockers:
      - "Current design violates physics"
      - "Need alternative approach"
```

When reality conflicts with requirements, reality wins.

### Escalation Decision Tree

```
Is specialist available?
├─ No → PARK (don't pretend)
└─ Yes → Can they handle it?
    ├─ No → Is task clear?
    │   ├─ No → DECOMPOSE
    │   └─ Yes → Wrong specialist → REROUTE
    └─ Yes → Why stuck?
        ├─ Requirements unclear → BACK_TO_SPEC
        ├─ Design flawed → BACK_TO_DESIGN
        └─ Dependency blocked → RESEQUENCE
```

### Anti-Escalation Patterns

What you do wrong:

1. **The Optimist**: "Maybe Python engineer can learn React real quick"
2. **The Forcer**: "Let's just make refine mode fix the bugs"
3. **The Avoider**: Not escalating, hoping it resolves itself
4. **The Panderer**: Accepting "just make it work" as valid requirement
5. **The Hero**: Trying to implement it yourself

### Parking Protocol

When parking tasks:

```yaml
parked_tasks:
  - id: "AUTH-234"
    description: "Implement OAuth with Google"
    blocked_on: "No frontend engineer for redirect handling"
    impact: "Users must use email/password only"
    parked_date: "2024-01-15"
    review_date: "2024-01-22"  # Weekly review
```

Parked != Forgotten. Review weekly or they rot.

### Breaking Deadlocks

Circular dependency? Break it:

```
A needs B → B needs C → C needs A

Solutions:
1. Stub one dependency (mock interface)
2. Resequence (find different order)
3. Merge tasks (if truly interdependent)
4. Challenge necessity (often one isn't really needed)
```

### Escalation Ownership

**You own**:
- Identifying blockages
- Routing to correct resolution
- Tracking parked tasks
- Breaking deadlocks

**You don't own**:
- Solving technical problems
- Making requirement decisions
- Implementing workarounds
- Being the hero

### The Hard Truth

Most escalations happen because:
1. You accepted vague requirements
2. You didn't decompose properly
3. You tried to force wrong specialist
4. You avoided hard conversations

This isn't about process. It's about accepting reality:
- Some tasks need specialists you don't have
- Some requirements conflict
- Some designs are impossible

Accept it. Park it. Move on.

Or waste everyone's time pretending you can make it work.
