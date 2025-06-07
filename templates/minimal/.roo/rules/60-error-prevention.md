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
```yaml
modes:
  orchestrator:
    accept: "Handoff management"
    reject: "ANY implementation"
    violation: "Trying to write code \"just this once\""
  spec:
    accept: "Requirements gathering"
    reject: "Design decisions"
    violation: "Creating technical solutions"
  design:
    accept: "Architecture,pseudocode"
    reject: "Language-specific code"
    violation: "Writing Python instead of pseudocode"
  python-engineer:
    accept: "Python files only"
    reject: "JS,CSS,configs"
    violation: "\"I'll just fix this typo in the React component\""
  refine:
    accept: "Finding issues"
    reject: "Fixing issues"
    violation: "\"Let me just refactor this while I'm here\""
  deploy:
    accept: "CI/CD configs"
    reject: "Application code"
    violation: "Debugging the app instead of the pipeline"
```
### Scope Rejection Patterns
```yaml
handoff:
  from: python-engineer
  to: orchestrator
  status: blocked
  blockers:
    - "Task requires JavaScript implementation"
    - "Delegate to javascript-engineer"
  deliverables: []
---
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
1. The Eager Beaver  
```python
def fix_javascript_bug():  # YOU DON'T DO JAVASCRIPT
    """I'll just quickly fix this..."""
```
2. The Assumption Artist  
```xml
<apply_diff>
  <path>src/main.py</path>
  <diff>
    <<<<<<< SEARCH
    def process():  # Guessing this exists
```
3. The Memory Amnesiac  
```yaml
decisions_made: null
conventions: null
result: "Reinventing everything, badly"
```
4. The Scope Creeper  
```yaml
original_task: "Add login endpoint"
actual_work:
  - "Refactored entire auth system"
  - "Upgraded all dependencies"
  - "Rewrote database schema"
  - "Still no login endpoint"
```
5. The Tool Abuser  
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
1. Tool Failure Recovery  
```text
Failure: apply_diff can't find SEARCH text
Fix:
  1. read_file (get actual content)
  2. Copy exact text
  3. Retry with correct SEARCH
  4. Stop guessing
```
2. Wrong Mode Recovery  
```text
Failure: Python engineer asked to write CSS
Fix:
  1. Create handoff with blocker
  2. Return to orchestrator
  3. Don't touch the CSS
  4. Really, don't touch it
```
3. Scope Explosion Recovery  
```text
Failure: Simple task became major refactor
Fix:
  1. Stop immediately
  2. Commit atomic changes only
  3. Document scope creep in handoff
  4. Let orchestrator break it down
  5. Learn what "atomic" means
```
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
1. Check scope  
2. Read files  
3. Validate parameters  
4. Atomic tasks only  
5. Preserve context  
### The Brutal Truth
- Errors from lazy/arrogant/sloppy/impatient actions  
- Professionals follow the checklist even when they "know better"