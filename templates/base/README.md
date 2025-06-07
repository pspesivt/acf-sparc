# ACF-SPARC Boilerplate

This project is initialized with ACF-SPARC framework. Your code is no longer a mess.

## What is SPARC?

**S**pecification → **P**seudocode → **A**rchitecture → **R**efinement → **C**ompletion

A framework that enforces discipline through specialized AI agents:

| Phase | Purpose | Agent |
|-------|---------|-------|
| **Specification** | Extract requirements, define acceptance criteria | 📋 Sherlock |
| **Pseudocode** | Create algorithm blueprints, define data structures | 🏗️ Darwin |
| **Architecture** | Design system structure, select technologies | 🏗️ Darwin |
| **Refinement** | Implement, test, optimize | 🐍 Monty + Others |
| **Completion** | Deploy, monitor, operationalize | 🚀 Maverick |

Zeus (⚡) orchestrates the entire process, ensuring each phase delivers quality outputs.

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

## Common Commands

```bash
# Run tests
npm test

# Build project
npm run build

# Start development server
npm start
```

See [AGENTS.md](./AGENTS.md) for detailed instructions for AI coding agents.

## License

MIT
