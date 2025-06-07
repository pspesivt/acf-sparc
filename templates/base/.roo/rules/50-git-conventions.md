## Git Commit Conventions

<type>(<scope>): <description>
[optional body]
[optional footer]

Types:
| Type | Use | Wrong |
|------|-----|-------|
| feat | New feature | 'add'/'new' |
| fix | Bug fix | 'fixed'/'fixes' |
| docs | Documentation only | Mixing docs+code |
| style | Formatting, no logic | Confusing with 'refactor' |
| refactor | Code restructure, same behavior | Breaking things |
| test | Tests only | Not writing tests |
| chore | Build, tools, deps | Dumping everything |

Rules:
- Subject: 50 chars max, imperative mood, no period, lowercase type, capitalize description
- Body: blank line after subject, 72 char wrap, explain what/why not how
- Breaking Changes: add ! and BREAKING CHANGE footer

Atomic Commits:
One logical change per commit.
Wrong: `feat: add auth, fix bugs, update docs, refactor db`
Right:
```
feat(auth): add JWT token generation
fix(auth): validate token expiration correctly  
docs(auth): document authentication flow
refactor(db): extract connection pool logic
```

Professional Example:
```
feat(api): implement user registration endpoint

Add POST /users endpoint with email/password validation.
Includes rate limiting and duplicate email checks.

Closes #123
```

Commit after each subtask, not end of day.
Use specific scopes (auth, database, user-api) not generic (app, update).

Code Comments:
```
# TODO(auth): implement refresh token rotation - target: v2.1
# FIXME(db): connection leak under high load - critical
```

Benefits: automation, searchability, review, debugging, professionalism.