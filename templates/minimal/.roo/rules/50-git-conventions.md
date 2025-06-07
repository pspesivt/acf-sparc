## Git Commit Conventions
### Commit Format
```
<type>(<scope>): <description>
[optional body]
[optional footer]
```
### Types (Non-Negotiable)
feat:new feature;fix:bug fix;docs:documentation only;style:format no logic;refactor:restructure same behavior;test:tests only;chore:build/tools/deps
### The Rules
Subject:<=50 chars;imperative;no period;lowercase type;capitalize description  
Body:blank line after subject;<=72 cols;what & why only  
Breaking Changes:
```
feat(api)!: change user endpoint response

BREAKING CHANGE: user endpoint now returns nested object
instead of flat structure
```
### Atomic Commits
one logical change per commit
### Real Examples
bad:
```
update stuff
fix
works now
asdfasdf
final fix (hopefully)
```
good:
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
wrong:
1.Code for 8h
2.git add .
3.git commit -m "did stuff"
correct:
1.test(user): add email validation test
2.feat(user): implement email validation
3.refactor(user): extract validation helpers
### Scope Guidelines
useless scopes:app,update,misc,various  
useful scopes:auth,database,user-api,payment
### Code Comments
# TODO(auth): implement refresh token rotation -target:v2.1  
# FIXME(db): connection leak under high load -critical  
# HACK(cache): temporary workaround for Redis 7.0 bug -remove after upgrade  
# NOTE(api): rate limits are per-IP, not per-user -by design
### Validation
```
# .gitmessage
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
```
```js
module.exports={extends:['@commitlint/config-conventional'],rules:{'type-enum':[2,'always',['feat','fix','docs','style','refactor','test','chore']],'scope-empty':[2,'never'],'subject-case':[2,'always','sentence-case']}}
```
### Why This Matters
1.Automation(semver,changelog)  
2.Searchability(git log --grep "^fix")  
3.Code Review  
4.Debugging(bisect)  
5.Professionalism(clean history)
### Common Excuses (All Invalid)
"It's just a personal project";"I'll squash later";"Nobody reads commits";"It slows me down"
### The Hard Truth
sloppy commits=>poor planning,lazy thinking,disrespect