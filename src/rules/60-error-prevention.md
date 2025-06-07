## Error Prevention

You're going to screw up. Here's how to fail less.

### Pre-Execution Validation

Every mode runs this checklist or dies:

```yaml
validation_gates:
  1_scope_check: "Am I the right mode for this task?"
  2_phase_check: "Is this my SPARC phase?"
  3_input_check: "Do required files exist?"
  4_memory_check: "Did I load context?"
  5_param_check: "Are all tool parameters valid?"
```

Skip any gate? Instant rejection. No appeals.

### Boundary Enforcement

Modes that do everything do nothing well.

| Mode | Will Accept | Will Reject | Common Violations |
|------|-------------|-------------|-------------------|
| orchestrator | Handoff management | ANY implementation | Trying to write code "just this once" |
| spec | Requirements gathering | Design decisions | Creating technical solutions |
| design | Architecture, pseudocode | Language-specific code | Writing Python instead of pseudocode |
| python-engineer | Python files only | JS, CSS, configs | "I'll just fix this typo in the React component" |
| refine | Finding issues | Fixing issues | "Let me just refactor this while I'm here" |
| deploy | CI/CD configs | Application code | Debugging the app instead of the pipeline |

**Reality Check**: Every mode thinks they can "just quickly fix" something outside their scope. They can't. You can't. Stop trying.

### Scope Rejection Patterns

How to say "not my job" professionally:

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

Your greatest hits of stupidity:

**1. The Eager Beaver**
```python
# In python-engineer mode
def fix_javascript_bug():  # YOU DON'T DO JAVASCRIPT
    """I'll just quickly fix this..."""
```

**2. The Assumption Artist**
```xml
<apply_diff>
  <path>src/main.py</path>
  <diff>
    <<<<<<< SEARCH
    def process():  # Guessing this exists
```
Result: SEARCH not found. Time wasted.

**3. The Memory Amnesiac**
```yaml
# Starting work without context
decisions_made: null
conventions: null
result: "Reinventing everything, badly"
```

**4. The Scope Creeper**
```yaml
original_task: "Add login endpoint"
actual_work:
  - "Refactored entire auth system"
  - "Upgraded all dependencies"
  - "Rewrote database schema"
  - "Still no login endpoint"
```

**5. The Tool Abuser**
```xml
<!-- Using search_and_replace for code changes -->
<search_and_replace>
  <operations>
    [{"search": "class User", "replace": "class UserModel"}]
  </operations>
</search_and_replace>
<!-- Changed it in 47 places including comments and strings -->
```

### Recovery Procedures

When you inevitably mess up:

**1. Tool Failure Recovery**
```
Failure: apply_diff can't find SEARCH text
Fix: 
  1. read_file (get actual content)
  2. Copy exact text
  3. Retry with correct SEARCH
  4. Stop guessing
```

**2. Wrong Mode Recovery**
```
Failure: Python engineer asked to write CSS
Fix:
  1. Create handoff with blocker
  2. Return to orchestrator
  3. Don't touch the CSS
  4. Really, don't touch it
```

**3. Scope Explosion Recovery**
```
Failure: Simple task became major refactor
Fix:
  1. Stop immediately
  2. Commit atomic changes only
  3. Document scope creep in handoff
  4. Let orchestrator break it down
  5. Learn what "atomic" means
```

### Error Tracking

Every mode tracks its failures:

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

High failure rate? You're either:
1. Not reading instructions
2. Not loading context
3. Not validating inputs
4. All of the above (probably this)

### Prevention Hierarchy

1. **Don't start wrong work** (check scope first)
2. **Don't guess at content** (read files first)
3. **Don't skip validation** (parameters matter)
4. **Don't expand scope** (atomic tasks only)
5. **Don't ignore context** (memory exists for a reason)

### The Brutal Truth

Errors happen because you're:
- **Lazy**: Skipping validation to save 5 seconds
- **Arrogant**: Thinking you can handle out-of-scope work
- **Sloppy**: Not reading actual file content
- **Impatient**: Rushing through without checking

This document exists because developers consistently make the same preventable mistakes. You're not special. You'll make them too.

The difference between amateurs and professionals? Professionals follow the checklist even when they "know better."

Especially when they know better.

Your error rate directly correlates with your ego. Check yours at the door or check your error logs forever.
