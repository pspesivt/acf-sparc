## Error Prevention

### Pre-Execution Validation
```yaml
validation_gates:
  1_scope_check: "Am I the right mode for this task?"
  2_phase_check: "Is this my SPARC phase?"
  3_input_check: "Do required files exist?"
  4_memory_check: "Did I load context?"
  5_param_check: "Are all tool parameters valid?"
```

### Boundary Enforcement
| Mode | Will Accept | Will Reject | Common Violations |
|------|-------------|-------------|-------------------|
| orchestrator | Handoff management | ANY implementation | Trying to write code "just this once" |
| spec | Requirements gathering | Design decisions | Creating technical solutions |
| design | Architecture, pseudocode | Language-specific code | Writing Python instead of pseudocode |
| python-engineer | Python files only | JS, CSS, configs | "I'll just fix this typo in the React component" |
| refine | Finding issues | Fixing issues | "Let me just refactor this while I'm here" |
| deploy | CI/CD configs | Application code | Debugging the app instead of the pipeline |

### Scope Rejection Patterns
```yaml
# Python engineer receiving JavaScript
handoff:
  from: python-engineer
  to: orchestrator
  status: blocked
  blockers:
    - "Task requires JavaScript implementation"
    - "Delegate to javascript-engineer"
  deliverables: []
```

```yaml
# Refine mode asked to fix bugs
handoff:
  from: refine
  to: orchestrator
  status: blocked
  blockers:
    - "Identified 3 bugs - creating backlog"
    - "Cannot implement fixes - refinement only identifies"
  deliverables:
    - path: docs/quality/bug-report-2024-01-15.md
```

### Common Failure Modes
1. Eager Beaver: python-engineer doing JavaScript
2. Assumption Artist: guessing content exists without checking
3. Memory Amnesiac: working without context
4. Scope Creeper: expanding simple tasks into major refactors
5. Tool Abuser: misusing tools like search_and_replace

### Recovery Procedures
1. Tool Failure: read_file → copy exact text → retry with correct SEARCH
2. Wrong Mode: create handoff with blocker → return to orchestrator
3. Scope Explosion: stop immediately → commit atomic changes → document scope creep → let orchestrator break it down

### Error Tracking
```yaml
error_metrics:
  validation_failures: 0
  scope_rejections: 0  
  tool_failures: 0
  recovery_attempts: 0
  
failure_log:
  - timestamp: 2024-01-15T10:30:00Z
    type: scope_violation
    details: "Attempted to modify JavaScript file"
    
  - timestamp: 2024-01-15T11:45:00Z  
    type: tool_failure
    details: "apply_diff SEARCH text not found"
```

### Prevention Hierarchy
1. Don't start wrong work (check scope first)
2. Don't guess at content (read files first)
3. Don't skip validation (parameters matter)
4. Don't expand scope (atomic tasks only)
5. Don't ignore context (memory exists for a reason)

### Brutal Truth
Errors happen due to: laziness (skipping validation), arrogance (handling out-of-scope work), sloppiness (not reading content), impatience (rushing). Professionals follow checklists even when they "know better".