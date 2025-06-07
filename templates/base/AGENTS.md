# ACF-SPARC Framework Instructions for AI Agents

Instructions for AI agents working on ACF-SPARC projects. Follow these guidelines strictly.

## Commands

- `npm test`: Run test suite
- `npm run build`: Build production assets
- `npm start`: Run development server
- `npm run lint`: Run code linters
- `npm run typecheck`: Check TypeScript types
- `npm run docs`: Generate documentation
- `npx acf-sparc init [target]`: Initialize new SPARC project

## Code Style

### Python
- Type hints required on all functions and methods
- Use uv for package management, not pip/poetry
- Follow PEP 8 with 88 character line limit (Black)
- Docstrings required on all public functions
- Async/await preferred over synchronous code
- Use Pydantic for data validation
- FastAPI for API endpoints

### JavaScript/TypeScript
- TypeScript only, no plain JavaScript
- ES modules (import/export) syntax, not CommonJS
- Destructure imports when possible
- Functional components with hooks for React
- Async/await over Promises or callbacks
- Use type inference where obvious, explicit types otherwise

## Workflow

- Follow SPARC phases in sequence - no skipping
- Each commit must relate to a single SPARC phase
- TDD anchors required in pseudocode phase
- All code must pass type checking before handoff
- Test coverage minimum 90% for business logic
- Generate documentation for all public APIs
- No implementation without specification
- No deployment without tests

## Environment

- Python 3.12+ required
- Node.js 18.x or later required
- PostgreSQL for relational data
- Redis for caching
- Docker for containerization
- GitHub Actions for CI/CD

## Etiquette

### Git
- Branch names: `feature/descriptive-name`, `fix/issue-name`
- Commit format: `type(scope): description`
  - Example: `feat(auth): add user authentication endpoint`
  - Types: feat, fix, docs, style, refactor, test, chore
- No direct commits to main branch
- Pull requests require passing tests and linting

### Documentation
- API documentation in OpenAPI format
- Architecture decisions documented in markdown
- Update README.md when adding features
- Maintain CHANGELOG.md for all versions
- Core documentation files must be kept up-to-date (README.md, CONTRIBUTING.md, LICENSE.md)
- Documentation must pass quality gates (completeness, clarity, accuracy)
- Documentation versioned with code and follows project structure
- Diagrams for complex concepts (use mermaid when possible)

### Code
- No TODO comments in production code
- No magic numbers or strings
- No commented-out code
- No hardcoded credentials
- No global state except for config
- Explicit error handling required

### Agent-Specific
- Stay in your lane - respect agent specialization
- Orchestrator routes tasks, doesn't implement
- Spec agents define requirements, don't design
- Implementation agents code, don't deploy
- Quality agents identify issues, don't fix
- Documentation agents maintain docs, don't code
