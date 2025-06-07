## Document Partitioning Protocol

Your monolithic documents are unmanageable garbage. Split them or choke on complexity.

### Partitioning Rules

**Maximum Lines**: 300. Period. This is a hard limit.

**Splitting Algorithm (Deterministic)**:
1.  During generation, if adding new content will exceed 300 lines, STOP.
2.  Search backwards from the proposed insertion point to the last major semantic boundary.
    *   For Markdown (`.md`): The boundary is a Level 2 (`##`) or Level 1 (`#`) header.
    *   For Code (`.py`, `.tsx`): The boundary is the start of the preceding function or class definition.
    *   For YAML (`.yaml`): The boundary is the start of the preceding top-level key.
3.  Split the file immediately *before* this boundary.
4.  Create a new file with a `-02` (or incrementing) suffix.
5.  Add cross-reference links (`Continues in: ...`, `Continued from: ...`) at the split point.
6.  Update the corresponding `_index.md` file with the new document entry.

This is not a suggestion. It is a required, deterministic procedure.

**Naming Convention**:
```
docs/{phase}/{type}/{component}-{subcomponent}-{sequence}.md

Examples:
docs/specifications/requirements/auth-login-01.md
docs/specifications/requirements/auth-oauth-02.md
docs/design/pseudocode/api-users-01.md
docs/design/pseudocode/api-orders-02.md
docs/architecture/interfaces/payment-stripe-01.md
```

### Required Splits by Document Type

**Specifications** (Split by feature/module):
```
docs/specifications/
├── requirements/
│   ├── auth-core-01.md      # Core auth requirements
│   ├── auth-oauth-02.md     # OAuth requirements
│   ├── api-users-01.md      # User API requirements
│   └── api-orders-01.md     # Order API requirements
├── acceptance-criteria/
│   ├── auth-login-01.md     # Login scenarios
│   ├── auth-logout-02.md    # Logout scenarios
│   └── api-validation-01.md # API validation rules
└── constraints/
    ├── technical-01.md      # Tech stack constraints
    ├── regulatory-01.md     # Compliance constraints
    └── business-01.md       # Business rules
```

**Design** (Split by component):
```
docs/design/
├── pseudocode/
│   ├── auth-service-01.md   # Auth service logic
│   ├── auth-service-02.md   # Continued if >300 lines
│   ├── data-models-01.md    # User/Account models
│   └── data-models-02.md    # Order/Payment models
├── flow-diagrams/
│   ├── auth-flow-01.md      # Login/logout flows
│   └── order-flow-01.md     # Order processing
└── test-scenarios/
    ├── auth-tests-01.md     # Auth test cases
    └── api-tests-01.md      # API test cases
```

**Architecture** (Split by layer/service):
```
docs/architecture/
├── component-interfaces/
│   ├── api-gateway-01.md    # Gateway interfaces
│   ├── auth-service-01.md   # Auth interfaces
│   ├── data-layer-01.md     # Repository interfaces
│   └── external-apis-01.md  # Third-party integrations
```

### Cross-Reference Index

Every split document set needs an index:

```markdown
# docs/specifications/requirements/_index.md

## Requirements Index

### Authentication (auth-*)
- [auth-core-01.md](auth-core-01.md): Core auth requirements (lines: 287)
- [auth-oauth-02.md](auth-oauth-02.md): OAuth integration (lines: 234)

### API (api-*)
- [api-users-01.md](api-users-01.md): User management (lines: 298)
- [api-orders-01.md](api-orders-01.md): Order processing (lines: 276)
```

### Split Triggers

| Document Approaching | Action at Line | Hard Stop |
|---------------------|----------------|-----------|
| 250 lines | Plan split points | Continue |
| 280 lines | Warning: prepare split | Continue |
| 300 lines | STOP. Split required | Block write |

### Mode Responsibilities

**Generating Mode**:
1. Monitor line count during generation
2. Split at logical boundaries before 300
3. Create index file
4. Update references

**Consuming Mode**:
1. Check for index file
2. Load all related documents
3. Process in sequence order
4. Maintain context across splits

### Enforcement

```yaml
validation:
  check_line_count:
    - path: "docs/**/*.md"
    - max_lines: 300
    - action_on_violation: "reject_commit"
    
  check_index_exists:
    - for_each: "split_document_set"
    - required: "_index.md"
    - action_on_missing: "block_handoff"
```

### Anti-Patterns

**DON'T**: Create `requirements-final-v2-FINAL.md` (600 lines)
**DO**: Split into `auth-core-01.md`, `api-core-01.md`, etc.

**DON'T**: Lose context between splits
**DO**: End each doc with "Continues in: [next-file]"

**DON'T**: Random split points
**DO**: Split at component/feature boundaries

### The Reality

Large documents fail because:
1. **Context windows choke** on 1000+ line files
2. **Modes timeout** processing huge docs
3. **Humans can't navigate** document soup
4. **Git diffs become unreadable**
5. **Parallel work impossible** on monoliths

Split early. Split often. Split logically.

Your 2000-line specification isn't impressive. It's incompetent.
