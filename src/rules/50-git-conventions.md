## Git Commit Conventions

Your commits are probably garbage. Here's how to fix them.

### Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Miss any part? Your commit is worthless for automation.

### Types (Non-Negotiable)

| Type | Use Case | Wrong? You're Probably... |
|------|----------|---------------------------|
| feat | New feature | Using 'add' or 'new' like an amateur |
| fix | Bug fix | Writing 'fixed' or 'fixes' (learn imperative mood) |
| docs | Documentation only | Mixing docs with code changes |
| style | Formatting, no logic change | Confusing with 'refactor' |
| refactor | Code restructure, same behavior | Breaking things and calling it refactor |
| test | Tests only | Not writing tests at all |
| chore | Build, tools, deps | Dumping everything here |

### The Rules

**Subject Line**:
- 50 characters max. Can't summarize in 50? Your commit does too much.
- Imperative mood: "add" not "added" or "adds"
- No period at end. It's not a sentence.
- Lowercase type, capitalize description

**Body** (when needed):
- Blank line after subject. Skip it? Tools break.
- 72 character wrap. Wider? Unreadable in terminals.
- Explain what and why. Never how. Code shows how.

**Breaking Changes**:
```
feat(api)!: change user endpoint response

BREAKING CHANGE: user endpoint now returns nested object
instead of flat structure
```

### Atomic Commits

One logical change per commit. Period.

**Wrong** (you do this):
```
feat: add auth, fix bugs, update docs, refactor db
```

**Right** (what professionals do):
```
feat(auth): add JWT token generation
fix(auth): validate token expiration correctly  
docs(auth): document authentication flow
refactor(db): extract connection pool logic
```

### Real Examples

**Garbage** (your current commits):
```
update stuff
fix
works now
asdfasdf
final fix (hopefully)
```

**Professional**:
```
feat(api): implement user registration endpoint

Add POST /users endpoint with email/password validation.
Includes rate limiting and duplicate email checks.

Closes #123
```

```
fix(auth): prevent timing attacks on password comparison

Switch from string equality to constant-time comparison
using hmac.compare_digest to prevent timing analysis.
```

### Commit Frequency

After every subtask. Not at end of day. Not "when you remember."

**Your workflow** (wrong):
1. Code for 8 hours
2. `git add .`
3. `git commit -m "did stuff"`

**Correct workflow**:
1. Write failing test: `test(user): add email validation test`
2. Make it pass: `feat(user): implement email validation`
3. Clean up: `refactor(user): extract validation helpers`

### Scope Guidelines

Be specific. Generic scopes are useless.

**Useless scopes**: `app`, `update`, `misc`, `various`

**Useful scopes**: `auth`, `database`, `user-api`, `payment`

### Code Comments

Stop leaving TODO comments that live forever.

```python
# TODO(auth): implement refresh token rotation - target: v2.1
# FIXME(db): connection leak under high load - critical
# HACK(cache): temporary workaround for Redis 7.0 bug - remove after upgrade
# NOTE(api): rate limits are per-IP, not per-user - by design
```

Include scope and context. "TODO: fix later" helps nobody.

### Validation

Your team should reject commits that violate these rules. Automate it:

```yaml
# .gitmessage
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']],
    'scope-empty': [2, 'never'],
    'subject-case': [2, 'always', 'sentence-case'],
  }
};
```

### Why This Matters

1. **Automation**: Semantic versioning, changelog generation
2. **Searchability**: `git log --grep "^fix"` finds all fixes
3. **Code Review**: Clear commits = faster reviews
4. **Debugging**: Bisect with confidence
5. **Professionalism**: Your git log isn't a diary

### Common Excuses (All Invalid)

"It's just a personal project" - Practice like you play
"I'll squash later" - Later never comes
"Nobody reads commits" - They do when debugging
"It slows me down" - Poor commits slow everyone down

### The Hard Truth

Your commit history reveals your engineering maturity. Sloppy commits indicate:
- Poor planning (can't break work into logical units)
- Lazy thinking (can't summarize your changes)  
- Disrespect for teammates (making history hard to navigate)

This isn't about following rules. It's about being a professional who values their team's time and the project's future maintainability.

Fix your commits or stay amateur. Your choice.
