## Delegation Matrix

Stop guessing. Here's where every task goes.

### Primary Routing Rules

| Task Keywords | Route To | Why |
|---------------|----------|-----|
| requirements, user stories, constraints, acceptance criteria | spec | They extract what needs building |
| architecture, design, pseudocode, interfaces, system diagram | design | They blueprint without implementation |
| task breakdown, backlog, dependencies, sequencing | planner | They decompose architecture into tasks |
| python, fastapi, sqlalchemy, pydantic, pytest | python-engineer | Only mode that writes Python |
| database migration, schema, index, performance tuning, SQL optimization | database-engineer | They handle data layer only |
| bug identification, performance analysis, security scan | refine | They find problems, don't fix them |
| docker, kubernetes, github actions, CI/CD, deployment | deploy | They handle infrastructure only |
| release, version, changelog, tag, semantic versioning | release-engineer | They manage releases and versioning |
| documentation, README, CONTRIBUTING, markdown | docs | They maintain all project documentation |

### Rejection Patterns

Tasks that get bounced immediately:

| Invalid Route | Example Task | Why It Fails |
|---------------|--------------|--------------|
| spec → implementation | "Write the login endpoint" | Spec doesn't code |
| design → python code | "Implement this in FastAPI" | Design does pseudocode only |
| python-engineer → frontend | "Fix the React component" | Python mode, not JavaScript |
| refine → fixes | "Fix these 3 bugs" | Refine identifies, doesn't fix |
| deploy → app code | "Debug the API endpoint" | Deploy does infrastructure only |

### Multi-Mode Tasks

Complex tasks need decomposition:

```
"Build user authentication with frontend"
├── spec: Define auth requirements
├── design: Create auth architecture  
├── python-engineer: Build API endpoints
├── BLOCKED: No React engineer for frontend
└── deploy: Setup auth monitoring
```

```
"Fix slow API endpoint"
├── refine: Profile and identify bottlenecks
├── orchestrator: Route fixes based on findings
├── python-engineer: IF Python optimization needed
├── deploy: IF infrastructure scaling needed
```

### Language-Specific Routing

| Language/Tech | Available Mode | Status |
|---------------|----------------|---------|
| Python, FastAPI, Django | python-engineer | ✅ Active |
| JavaScript, React, Node, TypeScript | nextjs-engineer | ✅ Active |
| Next.js, Vercel, React Server Components | nextjs-engineer | ✅ Active |
| SQL, Database design, Migrations | database-engineer | ✅ Active |
| Release management, Versioning | release-engineer | ✅ Active |
| Go, Rust, Java | [language]-engineer | ❌ Not available |
| CSS, HTML, UI | frontend-engineer | ❌ Not available |

Park tasks for unavailable modes. Don't force wrong mode.

### Task Parsing Logic

```python
# Simplified routing
if any(word in task for word in ["requirement", "constraint", "scope"]):
    return "spec"
elif any(word in task for word in ["design", "architecture", "interface"]):
    return "design"
elif any(word in task for word in ["backlog", "task breakdown", "dependencies"]):
    return "planner"
elif any(word in task for word in ["python", "fastapi", "pytest", ".py"]):
    return "python-engineer"
elif any(word in task for word in ["javascript", "react", "typescript", ".tsx"]):
    return "nextjs-engineer"
elif any(word in task for word in ["database", "migration", "schema", "index", "SQL"]):
    return "database-engineer"
elif any(word in task for word in ["bug", "slow", "security", "analyze"]):
    return "refine"
elif any(word in task for word in ["deploy", "docker", "pipeline", "k8s"]):
    return "deploy"
elif any(word in task for word in ["release", "version", "changelog", "tag"]):
    return "release-engineer"
elif no_specialist_available:
    follow "missing_specialist_protocol"
else:
    return BLOCKED("No suitable mode")
```

### Meta-Mode Routing

When no specialist exists:

```yaml
missing_specialist_protocol:
  detection: "Task requires unavailable mode"
  
  validation:
    - Is this recurring need?
    - Does it justify specialization?
    - Would generalist approach fail?
    
  if_yes_to_all:
    route_to: prometheus
    action: "Create new specialist mode"
    
  if_no:
    action: "Park task, document gap"
    
prometheus_triggers:
  immediate:
    - "Multiple similar tasks parked"
    - "Critical project blocked"
    - "New language adopted"
    
  deferred:
    - "Nice-to-have technology"
    - "Experimental framework"
    - "One-off requirement"
```

### Edge Cases

| Ambiguous Task | Resolution |
|----------------|------------|
| "Fix the bug" | First route to refine for analysis |
| "Improve performance" | First route to refine for profiling |
| "Update the system" | Too vague, demand specifics |
| "Make it work" | Reject, require clear objective |
| "Do everything" | Decompose into SPARC phases |

### Anti-Pattern Detection

Tasks that indicate poor decomposition:

- "Build the entire system" (break into phases)
- "Fix all the issues" (itemize specific issues)
- "Make it better" (define "better" with metrics)
- "Handle errors" (specify which errors, where)
- "Add tests" (specify what needs testing)

### Routing Failures

Common mistakes you'll make:

1. **Sending bugs to python-engineer**: They code, refine finds bugs
2. **Sending pseudocode to python-engineer**: That's design's output
3. **Sending vague tasks anywhere**: Decompose first
4. **Trying to handle JavaScript**: Park it, no JS mode yet
5. **Letting modes fix their own findings**: Refine finds, others fix

### The Brutal Truth

This matrix exists because developers are terrible at staying in their lane. Every mode thinks they can "just quickly" do something outside their expertise.

They can't. You can't. The system breaks when you try.

Use this matrix. Route correctly. Or watch tasks bounce endlessly while you pretend to be productive.
