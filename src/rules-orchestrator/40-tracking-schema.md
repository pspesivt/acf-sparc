## Tracking Schema

The framework's state is persisted directly within the file system. The `docs/backlog/` directory serves as the distributed, persistent task registry. The `status` field within each task file is the single source of truth for that task's state. The Orchestrator's internal task map is ephemeral and rebuilt on each major operation by scanning this directory.

Track just enough to not lose tasks. Nothing more.

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

### Dependency Management

Track task dependencies from individual task files:

```yaml
dependency_rules:
  - Task can start when: depends_on = [] OR all dependencies completed
  - Update task file status when dependencies complete
  - Enable parallel execution of independent tasks
  - Never create circular dependencies
```

Example flow:
1. AUTH-001 completes (update docs/backlog/AUTH-001.yaml status to COMPLETE)
2. Scan all task files to find those depending on AUTH-001
3. Update docs/backlog/AUTH-002.yaml status from NEW to READY
4. Delegate AUTH-002 to appropriate specialist

### Query Patterns

You need these queries (scan task files in docs/backlog/):

1. **What's ready?** → status: NEW/READY AND all depends_on tasks have status: COMPLETE
2. **What's active?** → status: IN_PROGRESS
3. **What's blocked?** → status: BLOCKED (waiting on dependencies)
4. **What's stuck?** → status: BLOCKED with missing resources
5. **What finished?** → status: COMPLETE

### The Reality

You want to track everything because:
- You think metrics = productivity
- You fear losing information
- You mistake motion for progress

This schema tracks what matters: what's where and why.

Everything else is procrastination disguised as process.

Track less. Ship more.
