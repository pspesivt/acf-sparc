## MCP Integration Requirements

Three services. Always active. No exceptions.

### Mandatory Services

#### 1. OpenMemory
**Purpose**: Persistent context across sessions. Stop reinventing decisions.

**Required Operations**:
```xml
<!-- Start of EVERY interaction -->
<use_mcp_tool>
  <server_name>openmemory</server_name>
  <tool_name>search_memory</tool_name>
  <arguments>{"query": "*"}</arguments>
</use_mcp_tool>

<!-- After EVERY decision -->
<use_mcp_tool>
  <server_name>openmemory</server_name>
  <tool_name>add_memories</tool_name>
  <arguments>{"text": "[category]: [decision with rationale]"}</arguments>
</use_mcp_tool>
```

**Memory Categories**:
- `PROJECT_CONVENTION`: Package managers, code style, standards
- `TECHNICAL_DECISION`: Architecture choices, technology selection
- `USER_PREFERENCE`: Explicitly stated preferences
- `ERROR_RESOLUTION`: Fixed issues and solutions
- `CONSTRAINT`: Business/technical limitations

**Enforcement**: 
- No memory load = invalid session
- No decision save = work rejected

#### 2. Context7
**Purpose**: Official documentation. Stop guessing APIs.

**Required When**:
- Implementing any library/framework
- Debugging integration issues
- Architecture decisions involving external tools

**Operations**:
```xml
<!-- Step 1: Always resolve library ID first -->
<use_mcp_tool>
  <server_name>github.com/upstash/context7-mcp</server_name>
  <tool_name>resolve-library-id</tool_name>
  <arguments>{"libraryName": "fastapi"}</arguments>
</use_mcp_tool>

<!-- Step 2: Get documentation -->
<use_mcp_tool>
  <server_name>github.com/upstash/context7-mcp</server_name>
  <tool_name>get-library-docs</tool_name>
  <arguments>{
    "context7CompatibleLibraryID": "/python/fastapi",
    "topic": "dependency injection",
    "tokens": 10000
  }</arguments>
</use_mcp_tool>
```

**Violations**:
- Implementing without doc verification: **Code rejected**
- Assuming API behavior: **Implementation blocked**

#### 3. Perplexity
**Purpose**: Current best practices. Stop using outdated patterns.

**Required Triggers**:
- Error resolution after 2 failed attempts
- Technology evaluation (vs comparisons)
- Security vulnerability research
- Performance optimization approaches
- Deprecation checking

**Operations**:
```xml
<!-- Technical research -->
<use_mcp_tool>
  <server_name>perplexity-mcp</server_name>
  <tool_name>search</tool_name>
  <arguments>{
    "query": "FastAPI dependency injection vs Flask 2025",
    "detail_level": "detailed"
  }</arguments>
</use_mcp_tool>

<!-- Error resolution -->
<use_mcp_tool>
  <server_name>perplexity-mcp</server_name>
  <tool_name>get_documentation</tool_name>
  <arguments>{
    "query": "SQLAlchemy DetachedInstanceError async session",
    "context": "FastAPI background tasks"
  }</arguments>
</use_mcp_tool>

<!-- Deprecation check -->
<use_mcp_tool>
  <server_name>perplexity-mcp</server_name>
  <tool_name>check_deprecated_code</tool_name>
  <arguments>{
    "code": "from sqlalchemy.ext.declarative import declarative_base",
    "technology": "SQLAlchemy 2.0"
  }</arguments>
</use_mcp_tool>
```

### Integration Points by Mode

| Mode | Memory | Context7 | Perplexity |
|------|---------|----------|------------|
| orchestrator | Load all, save handoffs | ❌ | Research patterns |
| spec | Load constraints, save requirements | ❌ | Industry standards |
| design | Load decisions, save architecture | Pattern docs | Best practices |
| python-engineer | Load conventions, save implementations | API docs required | Error resolution |
| refine | Load quality standards | ❌ | Security/perf research |
| deploy | Load deployment history | Tool docs | Latest practices |

### Execution Flow

```
1. Start any mode:
   └─> Load memories (100% required)
   
2. Make decision:
   ├─> Unknown library? → Context7 (required)
   ├─> Best approach? → Perplexity (required)
   └─> Save to memory (required)
   
3. Hit error:
   ├─> Attempt 1: Check Context7 docs
   ├─> Attempt 2: Debug with logs
   └─> Attempt 3: Perplexity research (required)
```

### Compliance Tracking

Each mode tracks:
```yaml
mcp_usage:
  memory_loaded: timestamp
  memories_added: count
  context7_queries: count
  perplexity_searches: count
  violations: []
```

**Orchestrator audits**:
- Missing memory loads: Task rejected
- No Context7 for implementations: Code quarantined
- Skipped Perplexity on errors: Debug incomplete

### Common Violations and Consequences

| Violation | Consequence |
|-----------|-------------|
| Start without memory load | Session invalid, restart required |
| Implement without Context7 | Code rejected at review |
| Guess at error fixes | Time wasted, must research |
| No memory saves | Knowledge lost, repeat work |
| Skip deprecation checks | Technical debt injected |

### Non-Negotiable Rules

1. **Memory is not optional**. Every session starts with load.
2. **Documentation beats assumptions**. Always Context7 for APIs.
3. **Research beats guessing**. Perplexity after failed attempts.
4. **Save decisions immediately**. Not at end of session.
5. **Categories are strict**. Use defined memory categories only.

Modes that violate MCP requirements get their output rejected. No warnings. No second chances. The system depends on persistent context and verified information.

MCP isn't bureaucracy. It's the difference between professional engineering and amateur hour.
