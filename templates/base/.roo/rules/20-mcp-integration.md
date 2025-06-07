## MCP Integration Requirements

### Mandatory Services

#### 1. OpenMemory
**Purpose**: Persistent context across sessions.

**Required Operations**:
```xml
<use_mcp_tool>
  <server_name>openmemory</server_name>
  <tool_name>search_memory</tool_name>
  <arguments>{"query": "*"}</arguments>
</use_mcp_tool>

<use_mcp_tool>
  <server_name>openmemory</server_name>
  <tool_name>add_memories</tool_name>
  <arguments>{"text": "[category]: [decision with rationale]"}</arguments>
</use_mcp_tool>
```

**Memory Categories**: PROJECT_CONVENTION, TECHNICAL_DECISION, USER_PREFERENCE, ERROR_RESOLUTION, CONSTRAINT

**Enforcement**: No memory load = invalid session; No decision save = work rejected

#### 2. Context7
**Purpose**: Official documentation.

**Required When**: Implementing libraries/frameworks, debugging integration, architecture decisions with external tools

**Operations**:
```xml
<use_mcp_tool>
  <server_name>github.com/upstash/context7-mcp</server_name>
  <tool_name>resolve-library-id</tool_name>
  <arguments>{"libraryName": "fastapi"}</arguments>
</use_mcp_tool>

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

**Violations**: Implementing without doc verification = code rejected; Assuming API behavior = implementation blocked

#### 3. Perplexity
**Purpose**: Current best practices.

**Required Triggers**: Error resolution after 2 fails, technology evaluation, security research, performance optimization, deprecation checking

**Operations**:
```xml
<use_mcp_tool>
  <server_name>perplexity-mcp</server_name>
  <tool_name>search</tool_name>
  <arguments>{
    "query": "FastAPI dependency injection vs Flask 2025",
    "detail_level": "detailed"
  }</arguments>
</use_mcp_tool>

<use_mcp_tool>
  <server_name>perplexity-mcp</server_name>
  <tool_name>get_documentation</tool_name>
  <arguments>{
    "query": "SQLAlchemy DetachedInstanceError async session",
    "context": "FastAPI background tasks"
  }</arguments>
</use_mcp_tool>

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
1. Start: Load memories (required)
2. Decision: Unknown library→Context7; Best approach→Perplexity; Save to memory
3. Error: Attempt1→Context7; Attempt2→Debug logs; Attempt3→Perplexity

### Non-Negotiable Rules
1. Memory load starts every session
2. Documentation beats assumptions
3. Research beats guessing
4. Save decisions immediately
5. Use defined memory categories only

Violations result in rejected output. No exceptions.