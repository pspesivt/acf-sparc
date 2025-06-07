## SPARC Methodology

6 phases. Sequential. No shortcuts.

### Phase Definitions

#### 1. Specification
**Purpose**: Extract truth from vague requirements.

**Entry**: User request exists, Orchestrator handoff
**Activities**: Extract requirements, Define acceptance criteria, Identify constraints, Document edge cases, Set performance targets

**Deliverables**:
```
docs/specifications/
├── requirements/
│   ├── _index.md
│   ├── core-functional-01.md
│   ├── core-functional-02.md
│   ├── auth-requirements-01.md
│   └── api-requirements-01.md
├── acceptance-criteria/
│   ├── _index.md
│   ├── auth-scenarios-01.md
│   ├── api-validation-01.md
│   └── edge-cases-01.md
├── constraints/
│   ├── technical-01.md
│   ├── business-01.md
│   └── regulatory-01.md
└── scope-boundaries/
    └── exclusions-01.md
```

**Exit**: All requirements have criteria, Constraints documented, Stakeholder approval, Files <300 lines
**Quality Gates**: No implementation details, Measurable criteria, Complete constraints, Proper file partitioning

#### 2. Pseudocode
**Purpose**: Blueprint solution without language bias.

**Entry**: Specification complete, Requirements approved
**Activities**: Design algorithms, Define data structures, Add TDD anchors, Identify component boundaries, Map functional flow

**Deliverables**:
```
docs/design/
├── pseudocode/
│   ├── _index.md
│   ├── auth-service-01.md
│   ├── auth-service-02.md
│   ├── api-handlers-01.md
│   ├── data-models-01.md
│   └── business-logic-01.md
├── test-scenarios/
│   ├── _index.md
│   ├── unit-tests-01.md
│   ├── integration-tests-01.md
│   └── edge-case-tests-01.md
└── flow-diagrams/
    ├── _index.md
    ├── auth-flow-01.md
    └── data-flow-01.md
```

**Exit**: Requirements mapped to pseudocode, TDD anchors cover paths, Component interfaces defined, Files <300 lines
**Quality Gates**: Technology agnostic, Testable assertions, Clear contracts, Logical file boundaries

#### 3. Architecture
**Purpose**: Design system structure and integration points.

**Entry**: Pseudocode complete, Algorithms validated
**Activities**: Component design, Interface definitions, Technology selection, Integration patterns, Deployment architecture

**Deliverables**:
```
docs/architecture/
├── system-design/
│   ├── _index.md
│   ├── overview-01.md
│   ├── components-01.md
│   └── interactions-01.md
├── component-interfaces/
│   ├── _index.md
│   ├── api-gateway-01.md
│   ├── auth-service-01.md
│   ├── data-layer-01.md
│   └── external-apis-01.md
├── api-contracts/
│   ├── _index.md
│   ├── v1.0.0/
│   │   ├── auth-api.yaml
│   │   ├── user-api.yaml
│   │   └── order-api.yaml
│   └── contract-status.md
├── technology-decisions/
│   ├── _index.md
│   ├── stack-selection-01.md
│   └── trade-offs-01.md
├── deployment-architecture/
│   ├── infrastructure-01.md
│   └── scaling-strategy-01.md
└── diagrams/
    ├── _index.md
    ├── c4-context-01.md
    ├── c4-container-01.md
    └── c4-component-01.md
```

**Exit**: Defined interfaces, Tech stack justified, Deployment specified, No monoliths, API contracts STABLE
**Quality Gates**: Scalability addressed, Security defined, Performance mapped, Clean partitioning

#### 4. Planning
**Purpose**: Create implementation backlog from architecture.

**Entry**: Architecture complete, API contracts STABLE, Interfaces defined
**Activities**: Analyze docs, Decompose to atomic tasks, Map dependencies, Sequence tasks, Assign specialists

**Deliverables**:
```
docs/backlog/
├── TASK-001.yaml
├── TASK-002.yaml
└── ...
```

**Exit**: Requirements mapped to tasks, Dependencies identified, Assignments complete, Sequence optimized
**Quality Gates**: Atomic tasks, Dependencies prevent blocking, Parallel work maximized, Clear ownership

#### 5. Refinement
**Purpose**: Implement until production-ready.

**Entry**: Architecture approved, Interfaces frozen, API contracts STABLE
**Activities**: Implement code, Write tests, Debug, Optimize, Security hardening, Documentation

**Deliverables**:
```
src/
tests/
docs/
├── api/
│   ├── _index.md
│   ├── endpoints-auth-01.md
│   ├── endpoints-users-01.md
│   └── endpoints-orders-01.md
├── user/
│   ├── _index.md
│   ├── getting-started-01.md
│   ├── tutorial-basic-01.md
│   └── tutorial-advanced-01.md
├── developer/
│   ├── _index.md
│   ├── architecture-guide-01.md
│   ├── contribution-guide-01.md
│   └── debugging-guide-01.md
└── retro/
    ├── _index.md
    └── INC-*.md
```

**Exit**: Tests passing, Performance targets met, Security clean, Docs complete, Files <300 lines
**Quality Gates**: 90%+ test coverage, Zero high vulnerabilities, Performance within 10%, API docs auto-generated

#### 6. Completion
**Purpose**: Deploy and establish operational excellence.

**Entry**: Refinement signed off, Deployment artifacts ready
**Activities**: Configure CI/CD, Deploy, Setup monitoring, Configure alerts, Operational handoff

**Deliverables**:
```
.github/workflows/
k8s/
monitoring/
├── dashboards/
├── alerts/
└── slo/
docs/deployment/
├── _index.md
├── runbook-deploy-01.md
├── runbook-rollback-01.md
├── runbook-incidents-01.md
└── architecture-prod-01.md
```

**Exit**: Running in production, Monitoring active, Alerts configured, Runbooks documented, Structure maintainable
**Quality Gates**: Zero-downtime proven, SLIs/SLOs defined, Rollback tested, On-call docs complete, Docs <300 lines

### Phase Transitions

| From | To | Trigger | Deliverable |
|------|----|---------|-------------|
| Start | Specification | New objective | `TASK-SPEC-001.yaml` |
| Specification | Pseudocode | `TASK-SPEC-001` complete | `TASK-ARCH-001.yaml` |
| Pseudocode | Architecture | `TASK-ARCH-001` complete | `TASK-PLAN-001.yaml` |
| Architecture | Planning | `TASK-PLAN-001` complete | `docs/backlog/` populated |
| Planning | Refinement | Tasks ready | Orchestrator executes backlog |
| Refinement | Completion | Implementation complete | `TASK-DEPLOY-001.yaml` |
| Completion | End | Deployed and monitored | `TASK-DEPLOY-001` complete |

### Handoff Protocol

- **Source of Truth**: `docs/backlog/` directory is task registry
- **State Management**: Task state in `status` field (`NEW|READY|IN_PROGRESS|BLOCKED|COMPLETE`)
- **Handoffs**: Stateless triggers with `task_id` pointing to definition file
- **Completion**: Specialist sets `status: COMPLETE` before handoff

### Backflow Rules

| Phase | Can Return To | Valid Reasons |
|-------|---------------|---------------|
| Pseudocode | Specification | Missing requirements |
| Architecture | Specification | Impossible constraints |
| Architecture | Pseudocode | Algorithm scaling issues |
| Refinement | Architecture | Interface changes needed |
| Refinement | Pseudocode | Logic flaws found |
| Completion | Refinement | Deployment blockers |

### Document Management

- Max 300 lines per file
- Split at logical boundaries
- Sequence with -01, -02 suffixes
- Every directory needs _index.md
- Cross-reference related docs

### Enforcement

**Orchestrator Duties**:
1. Enforce phase sequence
2. Validate exit criteria
3. Reject out-of-order requests
4. Track ownership
5. Monitor doc sizes
6. Enforce partitioning

**Mode Duties**:
1. Refuse out-of-phase work
2. Validate inputs
3. Meet exit criteria
4. Formal handoffs
5. Split at 300 lines
6. Create incident reports

### Refinement Loop

Bug-fix cycle within Refinement:
1. Identify bugs
2. Create task file
3. Dispatch to specialist
4. Implement and verify

**Priority Handling**:
- Critical: Drop current work
- High: Next task
- Medium: Queued
- Low: Backlog

**Escalation**: If changes needed to STABLE API or core design, create task for `design` mode, not implementer.

No exceptions. No shortcuts. Methodology prevents chaos.