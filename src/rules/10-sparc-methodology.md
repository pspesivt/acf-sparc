## SPARC Methodology

Six phases. Non-negotiable sequence. No shortcuts.

### Phase Definitions

#### 1. Specification
**Purpose**: Extract truth from vague requirements.

**Entry Criteria**:
- User request exists
- Orchestrator initiated handoff

**Activities**:
- Extract functional requirements
- Define acceptance criteria (Given-When-Then)
- Identify constraints (technical, business, regulatory)
- Document edge cases
- Set performance targets

**Deliverables**:
```
docs/specifications/
├── requirements/
│   ├── _index.md                    # Navigation index
│   ├── core-functional-01.md        # Core functionality (<300 lines)
│   ├── core-functional-02.md        # Continued if needed
│   ├── auth-requirements-01.md      # Authentication specific
│   └── api-requirements-01.md       # API specific
├── acceptance-criteria/
│   ├── _index.md
│   ├── auth-scenarios-01.md         # Login/logout scenarios
│   ├── api-validation-01.md         # API test scenarios
│   └── edge-cases-01.md             # Failure scenarios
├── constraints/
│   ├── technical-01.md              # Tech stack limits
│   ├── business-01.md               # Budget/timeline
│   └── regulatory-01.md             # Compliance
└── scope-boundaries/
    └── exclusions-01.md             # What we're NOT building
```

**Exit Criteria**:
- All requirements have acceptance criteria
- Constraints documented and validated
- Stakeholder approval (explicit or timeout)
- No file exceeds 300 lines

**Quality Gates**:
- No implementation details
- Measurable success criteria
- Complete constraint inventory
- Proper file partitioning

#### 2. Pseudocode
**Purpose**: Blueprint the solution without language bias.

**Entry Criteria**:
- Specification phase complete
- Requirements approved

**Activities**:
- Design algorithms
- Define data structures
- Add TDD anchors (//T:[behavior])
- Identify component boundaries
- Map functional flow

**Deliverables**:
```
docs/design/
├── pseudocode/
│   ├── _index.md
│   ├── auth-service-01.md           # Auth logic (<300 lines)
│   ├── auth-service-02.md           # Continued
│   ├── api-handlers-01.md           # API endpoint logic
│   ├── data-models-01.md            # Core data structures
│   └── business-logic-01.md         # Domain logic
├── test-scenarios/
│   ├── _index.md
│   ├── unit-tests-01.md             # Unit test cases
│   ├── integration-tests-01.md      # Integration scenarios
│   └── edge-case-tests-01.md        # Failure testing
└── flow-diagrams/
    ├── _index.md
    ├── auth-flow-01.md               # Authentication flow
    └── data-flow-01.md               # Data processing flow
```

**Exit Criteria**:
- All requirements mapped to pseudocode
- TDD anchors cover happy path + edge cases
- Component interfaces defined
- Each file under 300 lines with proper sequencing

**Quality Gates**:
- Technology agnostic
- Testable assertions
- Clear input/output contracts
- Logical file boundaries

#### 3. Architecture
**Purpose**: Design system structure and integration points.

**Entry Criteria**:
- Pseudocode complete
- Core algorithms validated

**Activities**:
- Component architecture design
- Interface definitions
- Technology selection rationale
- Integration patterns
- Deployment architecture

**Deliverables**:
```
docs/architecture/
├── system-design/
│   ├── _index.md
│   ├── overview-01.md               # High-level architecture
│   ├── components-01.md             # Component breakdown
│   └── interactions-01.md           # Component interactions
├── component-interfaces/
│   ├── _index.md
│   ├── api-gateway-01.md            # External API interface
│   ├── auth-service-01.md           # Auth service contracts
│   ├── data-layer-01.md             # Repository interfaces
│   └── external-apis-01.md          # Third-party integrations
├── api-contracts/                    # MANDATORY for multi-service systems
│   ├── _index.md
│   ├── v1.0.0/
│   │   ├── auth-api.yaml            # OpenAPI 3.1 spec
│   │   ├── user-api.yaml            # OpenAPI 3.1 spec
│   │   └── order-api.yaml           # OpenAPI 3.1 spec
│   └── contract-status.md           # Version status (DRAFT/STABLE)
├── technology-decisions/
│   ├── _index.md
│   ├── stack-selection-01.md        # Core technology choices
│   └── trade-offs-01.md             # Decision rationale
├── deployment-architecture/
│   ├── infrastructure-01.md         # Server/cloud setup
│   └── scaling-strategy-01.md       # Growth planning
└── diagrams/
    ├── _index.md
    ├── c4-context-01.md              # C4 Level 1
    ├── c4-container-01.md            # C4 Level 2
    └── c4-component-01.md            # C4 Level 3
```

**Exit Criteria**:
- All components have defined interfaces
- Technology stack selected and justified
- Deployment model specified
- No monolithic documents
- API contracts versioned and marked STABLE for all service boundaries

**Quality Gates**:
- Scalability addressed
- Security boundaries defined
- Performance targets mapped to components
- Clean file partitioning

#### 4. Planning
**Purpose**: Create detailed implementation backlog from architecture and specifications.

**Entry Criteria**:
- Architecture phase complete
- API contracts marked STABLE
- Component interfaces defined

**Activities**:
- Analyze all specification and architecture documents
- Decompose high-level design into atomic tasks
- Map dependencies between tasks
- Sequence tasks for parallel execution
- Assign specialists to each task

**Deliverables**:
```
docs/backlog/                    # Directory containing one YAML file per atomic implementation task
├── TASK-001.yaml               # Individual task file
├── TASK-002.yaml               # Individual task file
└── ...                         # Additional task files
```

**Exit Criteria**:
- All requirements mapped to implementation tasks
- Task dependencies identified
- Specialist assignments complete
- Execution sequence optimized

**Quality Gates**:
- Each task is atomic (completable in one handoff)
- Dependencies prevent blocking
- Parallel work maximized
- Clear specialist ownership

#### 5. Refinement
**Purpose**: Implement and iterate until production-ready.

**Entry Criteria**:
- Architecture approved
- Interfaces frozen
- API contracts marked STABLE for all dependent services

**Activities**:
- Implement code (delegated by tech stack)
- Write tests (TDD)
- Debug failures
- Optimize performance
- Security hardening
- Documentation

**Deliverables**:
```
src/                    # Implementation (language-specific structure)
tests/                  # Test suites (partitioned by module)
docs/
├── api/               
│   ├── _index.md
│   ├── endpoints-auth-01.md        # Auth endpoints
│   ├── endpoints-users-01.md       # User endpoints
│   └── endpoints-orders-01.md      # Order endpoints
├── user/              
│   ├── _index.md
│   ├── getting-started-01.md       # Setup guide
│   ├── tutorial-basic-01.md        # Basic usage
│   └── tutorial-advanced-01.md     # Advanced features
├── developer/         
│   ├── _index.md
│   ├── architecture-guide-01.md    # Dev architecture
│   ├── contribution-guide-01.md    # How to contribute
│   └── debugging-guide-01.md       # Troubleshooting
└── retro/             
    ├── _index.md
    └── INC-*.md                     # Incident reports
```

**Exit Criteria**:
- All tests passing
- Performance targets met
- Security scan clean
- Documentation complete
- All files < 300 lines

**Quality Gates**:
- 90%+ test coverage on business logic
- Zero high-severity vulnerabilities
- Performance within 10% of targets
- API documentation auto-generated
- No documentation monoliths

#### 6. Completion
**Purpose**: Deploy and establish operational excellence.

**Entry Criteria**:
- Refinement phase signed off
- Deployment artifacts ready

**Activities**:
- Configure CI/CD
- Deploy to environments
- Setup monitoring
- Configure alerts
- Operational handoff

**Deliverables**:
```
.github/workflows/      # CI/CD pipelines
k8s/                   # Kubernetes manifests (if applicable)
monitoring/            
├── dashboards/        # Grafana/similar
├── alerts/           # Alert rules
└── slo/              # Service level objectives
docs/deployment/       
├── _index.md
├── runbook-deploy-01.md            # Deployment procedures
├── runbook-rollback-01.md          # Rollback procedures
├── runbook-incidents-01.md         # Incident response
└── architecture-prod-01.md         # Production setup
```

**Exit Criteria**:
- Running in production
- Monitoring active
- Alerts configured
- Runbooks documented
- Document structure maintainable

**Quality Gates**:
- Zero-downtime deployment proven
- SLIs/SLOs defined and measured
- Rollback tested
- On-call documentation complete
- All operational docs < 300 lines

### Phase Transitions

| From | To | Trigger | Deliverable |
|------|----|---------|-------------|
| Start | Specification | New objective | `TASK-SPEC-001.yaml` created |
| Specification | Pseudocode | `TASK-SPEC-001` complete | `TASK-ARCH-001.yaml` created |
| Pseudocode | Architecture | `TASK-ARCH-001` complete | `TASK-PLAN-001.yaml` created |
| Architecture | Planning | `TASK-PLAN-001` complete | `docs/backlog/` populated by planner |
| Planning | Refinement | Implementation tasks ready | Orchestrator begins executing backlog |
| Refinement | Completion | All implementation tasks complete | `TASK-DEPLOY-001.yaml` created |
| Completion | End | Deployed and monitored | `TASK-DEPLOY-001` complete |

### Handoff and State Management Protocol

The SPARC framework operates on a "file system as state machine" principle. The state of the project is persisted in the files under `docs/`.

*   **Single Source of Truth**: The `docs/backlog/` directory is the canonical task registry. Each `.yaml` file within it represents an atomic task.
*   **State Management**: A task's current state is determined *exclusively* by the `status` field within its corresponding `.yaml` file (`status: NEW | READY | IN_PROGRESS | BLOCKED | COMPLETE`).
*   **Handoffs as Triggers**: A handoff from the Orchestrator to a specialist is a stateless trigger. It contains a `task_id` which acts as a pointer to the task's definition file in the backlog. It does not contain the task payload itself.
*   **Task Completion**: A specialist signals task completion by modifying the `status` field in the task's `.yaml` file to `COMPLETE`. This is the final action before handing back to the Orchestrator.

### Backflow Rules

Backflow allowed only for blocking issues:

| Phase | Can Return To | Valid Reasons |
|-------|---------------|---------------|
| Pseudocode | Specification | Missing requirements discovered |
| Architecture | Specification | Constraints make design impossible |
| Architecture | Pseudocode | Algorithm doesn't scale |
| Refinement | Architecture | Interface changes required |
| Refinement | Pseudocode | Logic flaws discovered |
| Completion | Refinement | Deployment blockers |

### Document Management

**Partitioning Requirements**:
- Maximum 300 lines per file
- Split at logical boundaries (features, components)
- Sequence with -01, -02 suffixes
- Every directory gets _index.md for navigation
- Cross-references between related documents

**Index File Format**:
```markdown
# Component Index

## Document Overview
Total documents: 4
Total lines: 1,125
Last updated: 2024-01-15

## Documents
1. [auth-service-01.md](auth-service-01.md) - Core authentication (295 lines)
2. [auth-service-02.md](auth-service-02.md) - OAuth integration (287 lines)
3. [auth-service-03.md](auth-service-03.md) - Session management (276 lines)
4. [auth-service-04.md](auth-service-04.md) - Security utilities (267 lines)

## Cross-References
- Implements: [requirements/auth-requirements-01.md](../../specifications/requirements/auth-requirements-01.md)
- Interfaces: [architecture/component-interfaces/auth-service-01.md](../../architecture/component-interfaces/auth-service-01.md)
```

### Enforcement

**Orchestrator Responsibilities**:
1. Enforce phase sequence
2. Validate exit criteria before transitions
3. Reject out-of-order requests
4. Track phase ownership
5. Monitor document sizes
6. Enforce partitioning

**Mode Responsibilities**:
1. Refuse out-of-phase work
2. Validate input completeness
3. Meet exit criteria
4. Formal handoff only
5. Split documents at 300 lines
6. Create incident reports on failure

**Violations**:
- Mode attempting work outside assigned phase: **Rejected**
- Skipping phases: **Blocked by orchestrator**
- Incomplete handoffs: **Returned to sender**
- Missing deliverables: **Phase not closeable**
- Documents over 300 lines: **Split required**
- Repeated failures without incident reports: **Process review triggered**

### The Refinement Loop

The bug-fixing cycle is a formal, iterative sub-process within the Refinement phase:

```yaml
refinement_loop:
  1_bug_identification:
    actor: refine
    action: Analyze code and identify issues
    output: Bug report with severity and location

  2_task_creation:
    actor: refine
    action: Generate a new task file (e.g., docs/backlog/BUG-ID.yaml) in the backlog
    output: A complete, atomic task file with all necessary context

  3_orchestrator_dispatch:
    actor: orchestrator
    action: Detect new bug task file and dispatch to appropriate specialist based on its content
    
  4_implementation_and_verification:
    # (Remains as previously defined)
```

**Loop Characteristics**:
- Runs within Refinement phase
- Does not restart entire SPARC cycle
- Priority-based execution
- Verification required for closure
- Maximum 3 iterations before escalation

**Bug Priority Mapping**:
| Severity | Priority | Response Time |
|----------|----------|---------------|
| Critical | Immediate | Drop current work |
| High | Next task | Within current sprint |
| Medium | Queued | Next available slot |
| Low | Backlog | As capacity allows |

**Escalation Path**: If the `refine` mode, during its analysis, determines that a resolution requires changes to a `STABLE` API contract or a modification to the core system design, it MUST NOT create a bug task for an implementer. Instead, it will generate a task for the `design` mode, detailing the required architectural change. This initiates a new, targeted `Architecture` -> `Planning` cycle for the affected components, ensuring architectural integrity is maintained through the formal process.

No exceptions. No shortcuts. The methodology exists to prevent chaos, not enable it.

Documents exist to be read and understood, not to impress with length. Keep them atomic or keep debugging why nobody can find anything.
