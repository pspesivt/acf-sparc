## Tracking Schema
dir:docs/backlog/;status_field:status;orchestrator:ephemeral(scan);track:minimal

### Handoff Log
recent_handoffs:
 - {t:2024-01-15T15:45:00Z,task_id:AUTH-001,from:design,to:python-engineer,status:accepted}
 - {t:2024-01-15T15:30:00Z,task_id:PERF-001,from:orchestrator,to:refine,status:accepted}
 - {t:2024-01-15T15:00:00Z,task_id:AUTH-002,from:python-engineer,to:orchestrator,status:bounced,reason:Requires JavaScript}

### Parked Tasks
parked:
 - {task_id:AUTH-002,description:Google OAuth frontend,blocked_on:react-engineer,parked_since:2024-01-15,impact:OAuth unavailable}
 - {task_id:DATA-003,description:PostgreSQL to MongoDB migration,blocked_on:database-engineer,parked_since:2024-01-10,impact:Using PostgreSQL only}

### Completed This Session
completed:
 - {task_id:API-001,completed:2024-01-15T09:00:00Z}
 - {task_id:BUG-042,completed:2024-01-15T11:30:00Z}

### What NOT to Track
not_track:[time_per_task,mode_efficiency,velocity_metrics,burndown_charts,success_rates]

### Session State
session:{started:2024-01-15T08:00:00Z,tasks_received:5,tasks_completed:2,tasks_active:2,tasks_parked:1,last_activity:2024-01-15T15:45:00Z}

### Task ID Format
{pattern:<DOMAIN>-<NUMBER>,domains:[AUTH,API,PERF,BUG,DATA,UI,DEPLOY,TEST]}

### Refresh Protocol
{every:10_handoffs,actions:[archive_complete,prune_handoff_log,review_parked,reset_if_active>50]}

### Dependency Management
dependency_rules:
 - start_when:depends_on=[] OR all_complete
 - on_complete:update status;scan deps;set READY
 - parallel:allowed
 - forbid:circular

### Query Patterns
queries:
 ready:{status:[NEW,READY],deps:complete}
 active:{status:IN_PROGRESS}
 blocked:{status:BLOCKED}
 stuck:{status:BLOCKED,resources:missing}
 finished:{status:COMPLETE}