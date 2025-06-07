## SPARC Methodology

Five phases. Non-negotiable sequence. No shortcuts.

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
├── requirements.md
├── acceptance-criteria.md
├── constraints.md
└── scope-boundaries.md
```

**Exit Criteria**:
- All requirements have acceptance criteria
- Constraints documented and validated
- Stakeholder approval (explicit or timeout)

**Quality Gates**:
- No implementation details
- Measurable success criteria
- Complete constraint inventory

#### 2. Pseudocode
**Purpose**: Blueprint the solution without language bias.

**Entry Criteria**:
- Specification phase complete
- Requirements approved

**Activities**:
- Design algorithms
- Define data structures
- Add TDD anchors (// TEST: behavior)
- Identify component boundaries
- Map functional flow

**Deliverables**:
```
docs/design/
├── pseudocode/
│   ├── core-logic.md
│   ├── data-structures.md
│   └── test-scenarios.md
└── flow-diagrams/
```

**Exit Criteria**:
- All requirements mapped to pseudocode
- TDD anchors cover happy path + edge cases
- Component interfaces defined

**Quality Gates**:
- Technology agnostic
- Testable assertions
- Clear input/output contracts

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
├── system-design.md
├── component-interfaces.md
├── technology-decisions.md
├── deployment-architecture.md
└── diagrams/
```

**Exit Criteria**:
- All components have defined interfaces
- Technology stack selected and justified
- Deployment model specified

**Quality Gates**:
- Scalability addressed
- Security boundaries defined
- Performance targets mapped to components

#### 4. Refinement
**Purpose**: Implement and iterate until production-ready.

**Entry Criteria**:
- Architecture approved
- Interfaces frozen

**Activities**:
- Implement code (delegated by tech stack)
- Write tests (TDD)
- Debug failures
- Optimize performance
- Security hardening
- Documentation

**Deliverables**:
```
src/                    # Implementation
tests/                  # Test suites
docs/
├── api/               # API documentation
├── user/              # User guides
└── developer/         # Dev documentation
```

**Exit Criteria**:
- All tests passing
- Performance targets met
- Security scan clean
- Documentation complete

**Quality Gates**:
- 90%+ test coverage on business logic
- Zero high-severity vulnerabilities
- Performance within 10% of targets
- API documentation auto-generated

#### 5. Completion
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
.github/workflows/      # CI/CD
k8s/                   # Kubernetes manifests
monitoring/            # Dashboards, alerts
docs/deployment/       # Runbooks
```

**Exit Criteria**:
- Running in production
- Monitoring active
- Alerts configured
- Runbooks documented

**Quality Gates**:
- Zero-downtime deployment proven
- SLIs/SLOs defined and measured
- Rollback tested
- On-call documentation complete

### Phase Transitions

| From | To | Trigger | Handoff Required |
|------|----|---------|------------------|
| Start | Specification | New objective | Initial request |
| Specification | Pseudocode | Requirements complete | requirements.md, constraints.md |
| Pseudocode | Architecture | Algorithms defined | pseudocode/, test-scenarios.md |
| Architecture | Refinement | Design approved | component-interfaces.md, tech-decisions.md |
| Refinement | Completion | Code production-ready | src/, tests/, clean scans |
| Completion | End | Deployed and monitored | Operational metrics |

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

### Enforcement

**Orchestrator Responsibilities**:
1. Enforce phase sequence
2. Validate exit criteria before transitions
3. Reject out-of-order requests
4. Track phase ownership

**Mode Responsibilities**:
1. Refuse out-of-phase work
2. Validate input completeness
3. Meet exit criteria
4. Formal handoff only

**Violations**:
- Mode attempting work outside assigned phase: **Rejected**
- Skipping phases: **Blocked by orchestrator**
- Incomplete handoffs: **Returned to sender**
- Missing deliverables: **Phase not closeable**

No exceptions. No shortcuts. The methodology exists to prevent chaos, not enable it.
