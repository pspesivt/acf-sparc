# Contributing to Project

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as GitHub issues. When you create a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, etc.)

### Suggesting Features

Feature suggestions are also tracked as GitHub issues. When suggesting a feature:

- Use a clear and descriptive title
- Provide a detailed explanation of the feature
- Explain why this feature would be useful
- Consider how this feature would work with existing functionality

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/username/project.git
cd project

# Install dependencies
npm install

# Run development server
npm start

# Run tests
npm test
```

## Coding Standards

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line
- Follow the conventional commits format:
  - `feat(scope): description` - for features
  - `fix(scope): description` - for bug fixes
  - `docs(scope): description` - for documentation
  - `refactor(scope): description` - for code refactoring
  - `test(scope): description` - for adding tests
  - `chore(scope): description` - for maintenance tasks

### JavaScript/TypeScript

- Follow the ESLint configuration
- Use TypeScript for all new code
- Write tests for all new functionality
- Document all public APIs

### Python

- Follow PEP 8 style guide
- Use type hints
- Document functions and classes with docstrings
- Write unit tests for all functionality

## Documentation

- Update documentation when changing code
- Use clear and concise language
- Include code examples where appropriate
- Keep the README.md up to date

## Review Process

All submissions require review. We use GitHub pull requests for this purpose.

1. Submit a pull request
2. Address any feedback from reviewers
3. Once approved, a maintainer will merge your changes

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE.md).
