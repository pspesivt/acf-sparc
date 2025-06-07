## Tracking Schema

State persists in filesystem. `docs/backlog/` = task registry. `status` field = source of truth. Orchestrator's task map rebuilt by scanning directory.

Track minimum necessary.

### Handoff Log
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
```yaml
completed:
  - task_id: "API-001"
    completed: "2024-01-15T09:00:00Z"
  - task_id: "BUG-042"
    completed: "2024-01-15T11:30:00Z"
```

### NOT Tracked
- ❌ Time per task
- ❌ Mode efficiency
- ❌ Velocity metrics
- ❌ Burndown charts
- ❌ Success rates

### Session State
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
`<DOMAIN>-<NUMBER>`
Examples: `AUTH-001`, `PERF-042`, `BUG-137`
Domains: AUTH, API, PERF, BUG, DATA, UI, DEPLOY, TEST

### Refresh Protocol
Every 10 handoffs:
1. Archive completed
2. Prune handoff log
3. Review parked
4. Reset if >50 active

### Dependency Management
```yaml
dependency_rules:
  - Task starts when: depends_on=[] OR all deps completed
  - Update task file status when deps complete
  - Enable parallel execution of independent tasks
  - No circular dependencies
```

Flow:
1. AUTH-001 completes (update docs/backlog/AUTH-001.yaml status=COMPLETE)
2. Scan tasks for AUTH-001 dependencies
3. Update docs/backlog/AUTH-002.yaml status=READY
4. Delegate AUTH-002 to specialist

### Query Patterns
1. Ready? → status:NEW/READY AND all depends_on:COMPLETE
2. Active? → status:IN_PROGRESS
3. Blocked? → status:BLOCKED (waiting deps)
4. Stuck? → status:BLOCKED (missing resources)
5. Finished? → status:COMPLETE

Track less. Ship more.