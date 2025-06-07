# ACF-SPARC Project

This project is initialized with ACF-SPARC framework. Your code is no longer a mess.

## What is SPARC?

**S**pecification → **P**seudocode → **A**rchitecture → **R**efinement → **C**ompletion

A framework that enforces discipline through specialized AI agents.

> **Note**: The SPARC methodology was derived and implemented based on the public work of [ruvnet](https://github.com/ruvnet). This framework represents a practical implementation of those concepts.

### Core Agents:

| Phase | Purpose | Primary Agent | Supporting Agents |
|-------|---------|--------------|------------------|
| **Specification** | Extract requirements, define acceptance criteria | 📋 Sherlock | 📚 Scribe (docs) |
| **Pseudocode** | Create algorithm blueprints, define data structures | 🏗️ Darwin | 📚 Scribe (docs) |
| **Architecture** | Design system structure, select technologies | 🏗️ Darwin | 🗺️ Pathfinder (planning) |
| **Planning** | Break down into atomic tasks | 🗺️ Pathfinder | ⚡ Zeus (routing) |
| **Refinement** | Implement, test, optimize | 🐍 Monty, ⚛️ Dexter, 🔨 Hephaestus | 🔧 Brutus (quality) |
| **Completion** | Deploy, monitor, operationalize | 🚀 Maverick, 🚢 Janus | 📚 Scribe (docs) |

⚡ Zeus orchestrates the entire process, ensuring each phase delivers quality outputs. When expertise gaps are identified, 🔥 Prometheus creates new specialized agents to fill them.

## Getting Started

### 1. Install RooCode Extension

1. Open VS Code
2. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS)
3. Search for "RooCode"
4. Click Install

### 2. Initialize ACF-SPARC Workflow

Your project is already initialized with ACF-SPARC framework. Start working with Zeus:

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "RooCode: Start Chat"
3. Select "⚡ Zeus (SPARC Orchestrator)" mode
4. Describe what you want to build:

```
I need to build [your project description]
```

Zeus will:
1. Break down work into SPARC phases
2. Route tasks to specialized agents
3. Track progress through completion

## Project Structure

```
.roo/                   # Framework rules
├── rules/              # Universal rules ALL agents follow
├── rules-orchestrator/ # Zeus-specific rules
├── rules-spec/         # Sherlock-specific rules
└── ...                 # Other agent rules

docs/                   # Project documentation
└── specifications/     # Requirements and constraints

src/                    # Implementation code
tests/                  # Test suites
```

## Available Agents

- **⚡ Zeus** - Orchestrator that breaks down objectives and routes to specialists
- **📋 Sherlock** - Specification analyst for requirements extraction
- **🏗️ Darwin** - Solution designer for architecture and pseudocode
- **🗺️ Pathfinder** - Planning specialist that creates atomic task backlogs
- **🐍 Monty** - Python engineer (FastAPI, SQLAlchemy, type-safe async)
- **⚛️ Dexter** - Next.js engineer (TypeScript, App Router, Server Components)
- **🔨 Hephaestus** - Database engineer (migrations, optimization, complex queries)
- **🔧 Brutus** - Quality engineer (finds bugs, doesn't fix them)
- **🚀 Maverick** - Deployment engineer (Docker, K8s, CI/CD)
- **🚢 Janus** - Release engineer (versioning, changelogs, releases)
- **📚 Scribe** - Documentation engineer (comprehensive project docs)
- **🔥 Prometheus** - Mode generator (creates new specialists when needed)

## Common Commands

```bash
# Python projects (if using Python)
python -m pytest  # Run tests
uv sync          # Install dependencies
ruff check .     # Lint code
mypy .          # Type check

# Next.js projects (if using Next.js)  
npm test        # Run tests
npm run build   # Build project
npm run dev     # Start development server

# General
git status      # Check changes
git commit -m "feat: your message"  # Commit with conventional format
```

See [AGENTS.md](./AGENTS.md) for detailed instructions for AI coding agents.

## License

MIT
