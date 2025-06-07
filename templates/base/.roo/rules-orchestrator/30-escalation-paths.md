## Escalation Paths

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
attempts: 0
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
If bounces twice, decomposition failed.

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
Reality wins when conflicts with requirements.

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
1. **Optimist**: "Python engineer can learn React quick"
2. **Forcer**: "Make refine mode fix bugs"
3. **Avoider**: Not escalating, hoping self-resolution
4. **Panderer**: Accepting "just make it work" as requirement
5. **Hero**: Implementing yourself

### Parking Protocol
```yaml
parked_tasks:
  - id: "AUTH-234"
    description: "Implement OAuth with Google"
    blocked_on: "No frontend engineer for redirect handling"
    impact: "Users must use email/password only"
    parked_date: "2024-01-15"
    review_date: "2024-01-22"
```
Parked ≠ Forgotten. Review weekly.

### Breaking Deadlocks
```
A needs B → B needs C → C needs A

Solutions:
1. Stub dependency (mock interface)
2. Resequence (different order)
3. Merge tasks (if interdependent)
4. Challenge necessity
```

### Escalation Ownership
**Own**: Identifying blockages, Routing resolution, Tracking parked tasks, Breaking deadlocks
**Don't own**: Solving technical problems, Making requirement decisions, Implementing workarounds, Being hero

### Hard Truth
Most escalations from:
1. Accepting vague requirements
2. Poor decomposition
3. Forcing wrong specialist
4. Avoiding hard conversations

Accept reality:
- Some tasks need unavailable specialists
- Some requirements conflict
- Some designs impossible

Accept. Park. Move on.