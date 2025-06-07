## Tool Configs, Thresholds

Security "scanning" isn't running `npm audit` once. Here's actual security analysis.

### Static Analysis Stack

**Python Security**:
```yaml
# Bandit configuration (.bandit)
[bandit]
targets = src/
exclude = tests/,venv/
skips = B101  # assert_used - fine in tests
severity = medium

# Critical checks - NEVER skip
checks:
  - B102  # exec_used
  - B108  # hardcoded_tmp_directory
  - B201  # flask_debug_true
  - B301  # pickle_usage
  - B302  # marshal_usage
  - B306  # mktemp_q
  - B307  # eval_used
  - B324  # hashlib_insecure_hash
  - B501  # request_with_no_cert_validation
  - B601  # paramiko_calls
  - B602  # subprocess_popen_with_shell_equals_true
```

**Dependency Scanning**:
```bash
# Python dependencies
safety check --json --output safety-report.json
pip-audit --desc --format json --output pip-audit.json

# JavaScript dependencies  
npm audit --json > npm-audit.json
snyk test --json > snyk-report.json

# Container scanning
trivy image --format json --output trivy-report.json myapp:latest
```

**Secret Detection**:
```yaml
# .gitleaks.toml
[allowlist]
  description = "Allowlisted files"
  paths = [
    '''^\.?gitleaks\.toml$''',
    '''(.*?)(jpg|gif|png|doc|pdf|bin|mp4|tiff)$''',
    '''^vendor/''',
  ]

[[rules]]
  description = "AWS Access Key"
  regex = '''AKIA[0-9A-Z]{16}'''
  tags = ["aws", "credentials"]
  severity = "CRITICAL"

[[rules]]
  description = "Generic API Key"
  regex = '''(?i)(api_key|apikey|api-key)\s*[:=]\s*['\"][0-9a-zA-Z]{32,}['"]'''
  tags = ["api", "generic"]
  severity = "HIGH"

# Run with
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

### Dynamic Analysis Configuration

**OWASP ZAP**:
```python
# zap-config.py
zap_config = {
    "spider": {
        "maxDuration": 10,  # minutes
        "maxDepth": 10,
        "maxChildren": 50,
        "acceptCookies": True,
    },
    "scanner": {
        "attackStrength": "HIGH",
        "alertThreshold": "MEDIUM",
        "scanPolicyName": "SQL-Injection-Active",
    },
    "rules": {
        # Rule IDs to skip (false positives)
        "disable": [10015, 10098],  
        # Rules requiring special config
        "config": {
            40018: {"strength": "INSANE"},  # SQL injection
            90019: {"strength": "HIGH"},     # Server side code injection
        }
    }
}
```

**Fuzzing Configurations**:
```yaml
# AFL++ config
afl_config:
  input_dir: "./fuzzing/inputs"
  output_dir: "./fuzzing/outputs"
  dictionary: "./fuzzing/dict/http.dict"
  timeout: 1000  # ms
  memory: 512   # MB
  
# Target specific fuzzing
targets:
  - name: "JSON Parser"
    binary: "./build/json_parser"
    args: "@@"
    sanitizers: ["address", "undefined"]
    
  - name: "Auth Handler"
    binary: "./build/test_auth"
    args: "-f @@"
    sanitizers: ["address", "memory", "thread"]
```

### Vulnerability Patterns

**SQL Injection Detection**:
```python
# Pattern matching rules
SQL_INJECTION_PATTERNS = [
    # String concatenation
    r'(SELECT|INSERT|UPDATE|DELETE).*?\+.*?(user_input|request\.|params)',
    # F-string formatting
    r'f["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?\{.*?\}',
    # % formatting
    r'["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?%[s|d].*?%.*?user',
    # .format() 
    r'["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?\.format\(',
]

# Safe patterns (parameterized)
SAFE_PATTERNS = [
    r'execute\([^,]+,\s*\[.*?\]\)',  # Parameterized query
    r'session\.query\(.*?\)\.filter\(',  # SQLAlchemy ORM
]
```

**XSS Detection**:
```yaml
contexts:
  - name: "HTML Context"
    dangerous:
      - innerHTML =
      - document.write(
      - .html(
    safe:
      - .textContent =
      - .innerText =
      - escapeHtml(
      
  - name: "JavaScript Context"
    dangerous:
      - eval(
      - Function(
      - setTimeout( + string
    safe:
      - JSON.parse(
      - parseInt(
      
  - name: "URL Context"
    dangerous:
      - href = user_input
      - location = 
    safe:
      - encodeURIComponent(
      - URL validation regex
```

### Threshold Configuration

```yaml
security_gates:
  fail_build:
    - severity: CRITICAL
      count: 1
    - severity: HIGH
      count: 5
    - severity: MEDIUM
      count: 20
      
  require_review:
    - severity: HIGH
      count: 1
    - severity: MEDIUM  
      count: 10
    - new_dependencies: true
    
  alert_security_team:
    - authentication_bypass: true
    - sql_injection: true
    - remote_code_execution: true
    - secrets_exposed: true
```

### Container Security

**Dockerfile Scanning**:
```dockerfile
# hadolint config (.hadolint.yaml)
ignored:
  - DL3008  # Pin versions in apt get
  - DL3009  # Delete apt lists

trustedRegistries:
  - docker.io
  - gcr.io
  
failure-threshold: warning

rules:
  - DL3001  # No sudo
  - DL3002  # No switching users
  - DL3003  # No cd in WORKDIR
  - DL3004  # No sudo in RUN
  - DL3007  # No :latest tags
  - DL3025  # No JSON in CMD
  - DL4006  # No pipe without set -o pipefail
  - SC2086  # Double quote variables
```

### API Security Testing

```yaml
# postman-security-tests.json
{
  "info": {
    "name": "Security Test Suite"
  },
  "auth_tests": [
    {
      "name": "Missing Auth Token",
      "request": {
        "url": "{{baseUrl}}/api/users",
        "method": "GET",
        "header": []
      },
      "expect": {
        "status": 401,
        "body": {
          "contains": ["unauthorized", "token required"]
        }
      }
    },
    {
      "name": "Expired Token",
      "request": {
        "url": "{{baseUrl}}/api/users",
        "method": "GET",
        "header": [{
          "key": "Authorization",
          "value": "Bearer {{expiredToken}}"
        }]
      },
      "expect": {
        "status": 401
      }
    }
  ],
  "injection_tests": [
    {
      "name": "SQL Injection in Search",
      "request": {
        "url": "{{baseUrl}}/api/search?q=' OR '1'='1",
        "method": "GET"
      },
      "expect": {
        "status": 400,
        "response_time": "<1000ms",
        "body": {
          "not_contains": ["error", "syntax", "SQL"]
        }
      }
    }
  ]
}
```

### Compliance Mapping

```yaml
owasp_top_10_2021:
  A01_broken_access_control:
    tools: ["ZAP", "Burp"]
    rules: [40018, 40019, 40020]
    manual_checks:
      - "Verify RBAC implementation"
      - "Test privilege escalation paths"
      
  A02_cryptographic_failures:
    tools: ["SSLyze", "testssl.sh"]
    checks:
      - "TLS 1.2 minimum"
      - "No weak ciphers"
      - "HSTS enabled"
      
  A03_injection:
    tools: ["Bandit", "Semgrep", "SQLMap"]
    patterns:
      - sql_injection
      - command_injection
      - ldap_injection
```

### Continuous Security Pipeline

```yaml
# .gitlab-ci.yml security stages
security:sast:
  stage: security
  script:
    - bandit -r src/ -f json -o bandit-report.json
    - safety check --json > safety-report.json
    - semgrep --config=auto --json -o semgrep-report.json src/
  artifacts:
    reports:
      sast: 
        - bandit-report.json
        - safety-report.json
        - semgrep-report.json

security:secrets:
  stage: security
  script:
    - gitleaks detect --report-format json --report-path secrets-report.json
  artifacts:
    reports:
      secret_detection: secrets-report.json

security:dependency:
  stage: security
  script:
    - pip-audit --format json --desc -o pip-audit.json
    - npm audit --json > npm-audit.json
  artifacts:
    reports:
      dependency_scanning:
        - pip-audit.json
        - npm-audit.json
```

### Finding Validation

```python
def validate_finding(finding):
    """Not every tool finding is real."""
    
    # Check for false positive patterns
    if finding.type == "hardcoded_password":
        if "example" in finding.file_path:
            return False  # Examples are meant to have fake passwords
        if finding.value == "changeme":
            return False  # Placeholder, not real password
            
    # Verify exploitability
    if finding.type == "sql_injection":
        if not is_user_controlled(finding.source):
            return False  # Not exploitable if no user input
            
    # Check severity inflation
    if finding.severity == "CRITICAL":
        if "denial of service" in finding.description:
            finding.severity = "HIGH"  # DoS rarely critical
            
    return True
```

### The Reality

Security scanning finds:
- 60% False positives (tools are paranoid)
- 30% Low-impact issues (theoretical problems)
- 9% Real vulnerabilities (fix these)
- 1% Critical issues (fix NOW)

Most "security scanning" is:
- Running one tool once
- Ignoring the output
- Claiming "we scan for security"

Real security scanning:
1. Multiple tools (defense in depth)
2. Validated findings (not tool spam)
3. Tracked remediation (not just reports)
4. Continuous monitoring (not point-in-time)

Security isn't a checkbox. It's a process. Configure it properly or get pwned by script kiddies.
