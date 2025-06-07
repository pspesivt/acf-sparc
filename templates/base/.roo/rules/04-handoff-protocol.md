## Handoff Protocol

Stop dropping the ball. Here's how modes transfer work.

### Handoff Format

```yaml
handoff:
  from: orchestrator
  to: spec
  phase: specification
  status: ready  # ready|blocked|partial
  
  deliverables:
    - path: docs/requirements.md
      type: specification
      state: complete  # complete|draft|missing
      
  context:
    decisions:
      - "Using FastAPI for API layer"
      - "PostgreSQL for persistence"
    blockers:
      - "Authentication method undefined"
    next_actions:
      - "Define user authentication flow"
      - "Specify rate limiting requirements"
```

That's it. No checksums. No signatures. No blockchain.

### Required Fields

Missing any of these? Handoff rejected.

| Field | Purpose | Valid Values |
|-------|---------|--------------|
| from | Who's handing off | Mode slug |
| to | Who's receiving | Mode slug |
| phase | Current SPARC phase | specification/pseudocode/architecture/refinement/completion |
| status | Work state | ready/blocked/partial |
| deliverables | What's being handed over | Array of files with type and state |
| context | Critical information | decisions, blockers, next_actions arrays |

### Handoff Rules

1. **Orchestrator initiates all handoffs**. Modes don't talk directly.
2. **Deliverables must exist**. No promises, only files.
3. **Blocked status stops execution**. Fix blockers first.
4. **Partial requires next_actions**. Be specific about gaps.

### Status Definitions

**ready**: Work complete, meet phase exit criteria.
```yaml
status: ready
blockers: []  # Must be empty
```

**blocked**: Cannot proceed without resolution.
```yaml
status: blocked
blockers:
  - "Missing API rate limits from stakeholder"
  - "Database connection string not provided"
```

**partial**: Some progress, gaps documented.
```yaml
status: partial
next_actions:
  - "Complete error handling in auth flow"
  - "Add test cases for edge scenarios"
```

### Validation by Receiver

Receiving mode MUST verify:

1. **Correct phase**: Am I supposed to work in this phase?
2. **Required inputs**: Do I have prerequisite deliverables?
3. **No blockers**: Is status 'ready' or are blockers resolved?
4. **File existence**: Do all deliverable paths exist?

Validation fails? Bounce back immediately.

### Bounce-Back Protocol

Wrong mode for the job? Send it back.

```yaml
handoff:
  from: python-engineer
  to: orchestrator
  phase: refinement
  status: blocked
  
  deliverables: []
  
  context:
    decisions: []
    blockers:
      - "Task requires JavaScript implementation"
      - "python-engineer does not handle frontend"
    next_actions:
      - "Route to javascript-engineer"
```

### Common Handoff Patterns

#### Spec → Design
```yaml
deliverables:
  - path: docs/specifications/requirements.md
    type: specification
    state: complete
  - path: docs/specifications/constraints.md
    type: specification
    state: complete
```

#### Design → Implementation
```yaml
deliverables:
  - path: docs/design/pseudocode/api-endpoints.md
    type: pseudocode
    state: complete
  - path: docs/architecture/component-interfaces.md
    type: interface
    state: complete
```

#### Implementation → Refine
```yaml
deliverables:
  - path: src/api/endpoints.py
    type: code
    state: complete
  - path: tests/test_endpoints.py
    type: test
    state: complete
```

### Anti-Patterns

**DON'T**: Handoff without files
```yaml
# WRONG
deliverables:
  - path: "Will create requirements.md soon"
    type: promise
    state: pending
```

**DO**: Only handoff completed work
```yaml
# RIGHT
deliverables:
  - path: docs/specifications/requirements.md
    type: specification
    state: complete
```

**DON'T**: Accept wrong-phase work
```yaml
# Python engineer receiving design work
phase: architecture  # WRONG - I do refinement only
```

**DO**: Bounce immediately
```yaml
blockers:
  - "python-engineer works in refinement phase only"
```

### Tracking

Orchestrator maintains handoff log:
```yaml
handoff_history:
  - timestamp: 2024-01-15T10:30:00Z
    from: spec
    to: design
    status: ready
    duration_minutes: 45
    
  - timestamp: 2024-01-15T11:15:00Z
    from: design
    to: orchestrator
    status: blocked
    blockers: ["Missing performance requirements"]
```

High bounce rate? Poor task assignment.
Long durations? Scope too large.
Many blockers? Poor specification.

### The Truth

Handoffs fail because:
1. **Laziness**: Not checking deliverables exist
2. **Assumptions**: Thinking partial work is acceptable  
3. **Ego**: Trying to do work outside expertise

This protocol isn't complex. It's a checklist.

Follow it or waste everyone's time with bounced work and failed implementations.

Your choice.
