## Document Partitioning Protocol
### Partitioning Rules
Maximum Lines:300
Splitting Algorithm(Deterministic):
1.During generation if new content>300 lines STOP  
2.Search backwards to last semantic boundary:  
  - Markdown(.md):Level1/2 header  
  - Code(.py,.tsx):preceding fn/class  
  - YAML(.yaml):top-level key  
3.Split before boundary  
4.New file suffix -02 (incrementing)  
5.Add cross-refs: “Continues in:…”, “Continued from:…”  
6.Update corresponding _index.md

Naming Convention:
```
docs/{phase}/{type}/{component}-{subcomponent}-{sequence}.md
```
Examples:  
docs/specifications/requirements/auth-login-01.md  
docs/specifications/requirements/auth-oauth-02.md  
docs/design/pseudocode/api-users-01.md  
docs/design/pseudocode/api-orders-02.md  

### Required Splits by Document Type
Specifications(split by feature/module):
 docs/specifications/requirements:
  - auth-core-01.md#Core auth requirements  
  - auth-oauth-02.md#OAuth requirements  
  - api-users-01.md#User API requirements  
  - api-orders-01.md#Order API requirements  
 docs/specifications/acceptance-criteria:
  - auth-login-01.md#Login scenarios  
  - auth-logout-02.md#Logout scenarios  
  - api-validation-01.md#API validation rules  
 docs/specifications/constraints:
  - technical-01.md#Tech stack constraints  
  - regulatory-01.md#Compliance constraints  
  - business-01.md#Business rules  

Design(split by component):
 docs/design/pseudocode:
  - auth-service-01.md#Auth service logic  
  - auth-service-02.md#Continued  
  - data-models-01.md#User/Account models  
  - data-models-02.md#Order/Payment models  
 docs/design/flow-diagrams:
  - auth-flow-01.md#Login/logout flows  
  - order-flow-01.md#Order processing  
 docs/design/test-scenarios:
  - auth-tests-01.md#Auth test cases  
  - api-tests-01.md#API test cases  

Architecture(split by layer/service):
 docs/architecture/component-interfaces:
  - api-gateway-01.md#Gateway interfaces  
  - auth-service-01.md#Auth interfaces  
  - data-layer-01.md#Repository interfaces  
  - external-apis-01.md#Third-party integrations  

### Cross-Reference Index
```markdown
# docs/specifications/requirements/_index.md

## Requirements Index

### Authentication (auth-*)
- [auth-core-01.md](auth-core-01.md): Core auth requirements (lines:287)
- [auth-oauth-02.md](auth-oauth-02.md): OAuth integration (lines:234)

### API (api-*)
- [api-users-01.md](api-users-01.md): User management (lines:298)
- [api-orders-01.md](api-orders-01.md): Order processing (lines:276)
```

### Split Triggers
250→Plan split points; 280→Warning:prepare split; 300→STOP/Split required

### Mode Responsibilities
Generating:monitor line count;split<300 at boundaries;create/update index;add cross-refs  
Consuming:verify index;load docs by sequence;maintain context

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
DON'T: monolith >300 lines; random splits; lose context  
DO: split by feature/component; end each doc with “Continues in:[next-file]”; split at deterministic boundaries