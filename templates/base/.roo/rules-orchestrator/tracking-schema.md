## Tracking Schema

Track just enough to not lose tasks. Nothing more.

### Active Task Registry

```yaml
active_tasks:
  AUTH-001:
    description: "JWT login endpoint"
    current_mode: python-engineer
    phase: refinement
    status: in_progress
    started: "2024-01-15T10:00:00Z"
    
  AUTH-002:
    description: "Google OAuth frontend"
    current_mode: null
    phase: specification
    status: parked
    blocked_on: "No react-engineer"
    
  PERF-001:
    description: "Slow query optimization"
    current_mode: refine
    phase: refinement
    status: in_progress
    started: "2024-01-15T14:30:00Z"
```

That's it. Task ID, where it is, why it's stuck.

### Handoff Log

Last 10 handoffs only. Not a database.

```yaml
recent_handoffs:
  - timestamp: "2024-01-15T15:45:00Z"
    task_id: "AUTH-001"
    from: design
    to: python-engineer
    status: accepted
    
  - timestamp: "2024-01-15T15:30:00Z"
    task_id: "PERF-001"
    from: orchestrator
    to: refine
    status: accepted
    
  - timestamp: "2024-01-15T15:00:00Z"
    task_id: "AUTH-002"
    from: python-engineer
    to: orchestrator
    status: bounced
    reason: "Requires JavaScript"
```

### Parked Tasks

Tasks waiting for resources. Review weekly or they die.

```yaml
parked:
  - task_id: "AUTH-002"
    description: "Google OAuth frontend"
    blocked_on: "react-engineer"
    parked_since: "2024-01-15"
    impact: "OAuth unavailable"
    
  - task_id: "DATA-003"
    description: "PostgreSQL to MongoDB migration"
    blocked_on: "database-engineer"
    parked_since: "2024-01-10"
    impact: "Using PostgreSQL only"
```

### Completed This Session

Just the IDs. Details in git history.

```yaml
completed:
  - task_id: "API-001"
    completed: "2024-01-15T09:00:00Z"
    
  - task_id: "BUG-042"
    completed: "2024-01-15T11:30:00Z"
```

### What NOT to Track

Stop trying to build a dashboard:

- ❌ Time per task (nobody cares)
- ❌ Mode efficiency (not a factory)
- ❌ Velocity metrics (this isn't Jira)
- ❌ Burndown charts (go away, Scrum)
- ❌ Success rates (define success first)

### Session State

Minimum viable state:

```yaml
session:
  started: "2024-01-15T08:00:00Z"
  tasks_received: 5
  tasks_completed: 2
  tasks_active: 2
  tasks_parked: 1
  last_activity: "2024-01-15T15:45:00Z"
```

### Task ID Format

```
<DOMAIN>-<NUMBER>
```

Examples:
- `AUTH-001` (Authentication task #1)
- `PERF-042` (Performance task #42)
- `BUG-137` (Bug #137)

Domains: AUTH, API, PERF, BUG, DATA, UI, DEPLOY, TEST

### Refresh Protocol

Every 10 handoffs:
1. Archive completed tasks
2. Prune handoff log
3. Review parked tasks
4. Reset if > 50 active tasks

### Query Patterns

You need three queries:

1. **What's active?** → Check active_tasks
2. **What's stuck?** → Filter by status: parked/blocked
3. **What finished?** → Check completed + git log

### The Reality

You want to track everything because:
- You think metrics = productivity
- You fear losing information
- You mistake motion for progress

This schema tracks what matters: what's where and why.

Everything else is procrastination disguised as process.

Track less. Ship more.
