# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

This is an npm package for initializing SPARC-style projects:

```bash
# Initialize a new project with ACF-SPARC framework
npx acf-sparc init my-project

# Initialize .roo and .roomodes in current directory
npx acf-sparc init

# Lint code
npm run lint

# Format code (no script defined, use eslint directly)
npx eslint . --fix
```

There are no test scripts defined in package.json.

## High-Level Architecture

ACF-SPARC is a disciplined, AI-first software development framework that enforces the SPARC methodology through specialized AI agents.

### SPARC Methodology (6 Phases)

1. **Specification** → Extract requirements from vague user requests
2. **Pseudocode** → Design algorithms without language bias  
3. **Architecture** → Design system structure and interfaces
4. **Planning** → Decompose into atomic implementation tasks
5. **Refinement** → Implement, test, and iterate until production-ready
6. **Completion** → Deploy and establish operational excellence

Each phase has strict entry/exit criteria and deliverables. No phase can be skipped.

### Agent System

Specialized AI agents ("modes") handle different phases:

- **⚡ Zeus** - Orchestrator that routes tasks and enforces SPARC sequence
- **📋 Sherlock** - Extracts requirements and acceptance criteria
- **🏛️ Darwin** - Creates pseudocode and system architecture
- **🗺️ Pathfinder** - Decomposes architecture into atomic tasks
- **🐍 Monty** - Python/FastAPI implementation only
- **⚛️ Dexter** - React/TypeScript frontend only
- **🔍 Brutus** - Quality analysis (finds bugs, doesn't fix)
- **🚀 Maverick** - Deployment and CI/CD
- **📝 Scribe** - Documentation maintenance
- **🔥 Prometheus** - Creates new specialist modes when needed

### Key Directories

```
src/
├── rules/                    # Universal rules ALL agents follow
│   ├── 10-sparc-methodology.md    # Core SPARC phases and enforcement
│   ├── 20-mcp-integration.md      # MCP service requirements
│   └── ...                        # Other framework rules
├── rules-*/                  # Specialist-specific rules and templates
└── compile_markdown.sh       # Script to compile rules

templates/base/               # Project initialization template
├── AGENTS.md                # Agent descriptions
└── README.md                # Template project README

docs/                        # Documentation organized by SPARC phase
├── specifications/          # Requirements, constraints, acceptance criteria
├── design/                  # Pseudocode, test scenarios, flow diagrams  
├── architecture/            # System design, interfaces, API contracts
├── backlog/                 # Atomic task files (TASK-001.yaml, etc.)
└── deployment/              # Runbooks, monitoring, operational docs
```

### Critical Enforcement Rules

1. **Phase Gates**: Cannot proceed without meeting exit criteria
2. **Mode Boundaries**: Each agent strictly limited to their specialty  
3. **Document Partitioning**: Maximum 300 lines per file with navigation indices
4. **Handoff Protocol**: Formal work transfer via handoff.yaml files
5. **MCP Integration**: Mandatory use of OpenMemory, Context7, and Perplexity services
6. **API Contract Stability**: Contracts must be marked STABLE before implementation

### Python Stack (Non-Negotiable)

- **uv**: Package management (not pip/poetry/conda)
- **Ruff**: Formatting and linting
- **mypy**: Type checking with --strict
- **pytest**: Testing with 90% coverage minimum
- **FastAPI**: Async APIs only
- **SQLAlchemy 2.0**: Type-safe ORM
- **Alembic**: Database migrations

### Working with This Codebase

When modifying the framework:

1. Rules in `src/rules/` apply to ALL agents
2. Rules in `src/rules-<agent>/` are specialist-specific
3. Use the existing numeric prefixing (10-, 20-, etc.) for new rule files
4. The compile_markdown.sh script combines rules for distribution

When using the framework to build projects:

1. Always start with `npx acf-sparc init` to create proper structure
2. Follow SPARC phases strictly - no shortcuts
3. Use appropriate agents for each task
4. Maintain document partitioning (<300 lines per file)
5. Create incident reports (INC-*.md) for process failures