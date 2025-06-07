## Incident Reporting Protocol

Execution failed? Document it properly or repeat the failure forever.

### Incident Report Format
```markdown
# INC-[YYYY][MM][DD]-[HHMM]-[MODE]
**Mode**: [mode-name]
**Phase**: [current SPARC phase]
**Task**: [what was attempted]
**Timestamp**: [ISO 8601]
## Failure
[Single line: what broke]
## Context
[Max 3 lines: essential state when failure occurred]
## Root Cause
[Single line: why it failed]
## Recovery Path
[Numbered steps taken or needed]
## Handoff
Status: blocked
Blocker: [specific issue]
Next: [required action]
```

### Filename Convention
```
docs/retro/INC-YYYYMMDD-HHMM-MODE.md
Examples:
docs/retro/INC-20240115-1430-python-engineer.md
docs/retro/INC-20240115-1445-orchestrator.md
```

### Incident Triggers
**Immediate Report Required**:
- Tool execution failure after retry
- File not found when expected  
- Handoff rejection
- Constraint violation discovered
- Scope boundary hit
- Memory/context load failure
- API/integration timeout

**Not Incidents**:
- Normal validation rejections
- Expected bouncebacks
- Planned handoffs
- Successful retries

### Severity Levels
```yaml
CRITICAL: # Blocks all work
  - "Cannot load project memory"
  - "Core deliverable missing"
  - "Circular dependency detected"
HIGH: # Blocks current task
  - "Required tool unavailable"
  - "Integration API down"  
  - "File corruption detected"
MEDIUM: # Workaround exists
  - "Retry succeeded after 3 attempts"
  - "Fallback path used"
  - "Performance degradation"
```

### Required Sections
**Minimal**:
- Mode, Phase, Task, Timestamp
- Failure (1 line)
- Root Cause (1 line)
- Handoff status

**Extended** (HIGH/CRITICAL):
- Context (3 lines max)
- Recovery attempts
- Dependencies affected

### Examples
**Good**:
```markdown
# INC-20240115-1430-python-engineer
**Mode**: python-engineer
**Phase**: refinement
**Task**: Implement user authentication
**Timestamp**: 2024-01-15T14:30:00Z
## Failure
apply_diff failed: SEARCH text not found in auth.py
## Root Cause  
File structure changed since architecture phase
## Recovery Path
1. Read current file structure
2. Update implementation approach
3. Retry with correct paths
## Handoff
Status: blocked
Blocker: Outdated file references
Next: Re-read architecture docs
```

**Bad**:
```markdown
# Random incident
So I was trying to implement the authentication system and ran into some issues...
[200 more lines of diary entries]
```

### Incident Aggregation
Weekly rollup:
```markdown
# docs/retro/WEEK-2024-03.md
## Incident Summary Week 3, 2024
Total: 12
Critical: 1
High: 3
Medium: 8
### Patterns
1. File structure mismatches (4 incidents)
2. Tool parameter errors (3 incidents)
3. Memory load failures (2 incidents)
### Actions
1. Update file structure documentation
2. Add parameter validation
3. Improve memory error handling
```

### Auto-Generation
```python
def handle_failure(error, context):
    incident = {
        "id": f"INC-{timestamp}-{mode}",
        "mode": current_mode,
        "phase": current_phase,
        "task": current_task,
        "failure": str(error)[:80],
        "root_cause": analyze_error(error),
        "recovery": determine_recovery_path(error)
    }
    write_incident_report(incident)
    create_blocked_handoff(incident["root_cause"])
```

### The Reality
Most failures repeat because:
1. No documentation of what went wrong
2. No root cause analysis 
3. No recovery plan
4. No pattern detection
5. No learning

Every undocumented failure will happen again. Write it down or waste time forever.