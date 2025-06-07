## Tool Configs, Thresholds

### Static Analysis Stack

**Python Security**:
```yaml
[bandit]
targets = src/
exclude = tests/,venv/
skips = B101
severity = medium

checks:
  - B102
  - B108
  - B201
  - B301
  - B302
  - B306
  - B307
  - B324
  - B501
  - B601
  - B602
```

**Dependency Scanning**:
```bash
safety check --json --output safety-report.json
pip-audit --desc --format json --output pip-audit.json
npm audit --json > npm-audit.json
snyk test --json > snyk-report.json
trivy image --format json --output trivy-report.json myapp:latest
```

**Secret Detection**:
```yaml
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
```

### Dynamic Analysis Configuration

**OWASP ZAP**:
```python
zap_config = {
    "spider": {
        "maxDuration": 10,
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
        "disable": [10015, 10098],
        "config": {
            40018: {"strength": "INSANE"},
            90019: {"strength": "HIGH"},
        }
    }
}
```

**Fuzzing Configurations**:
```yaml
afl_config:
  input_dir: "./fuzzing/inputs"
  output_dir: "./fuzzing/outputs"
  dictionary: "./fuzzing/dict/http.dict"
  timeout: 1000
  memory: 512
  
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
SQL_INJECTION_PATTERNS = [
    r'(SELECT|INSERT|UPDATE|DELETE).*?\+.*?(user_input|request\.|params)',
    r'f["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?\{.*?\}',
    r'["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?%[s|d].*?%.*?user',
    r'["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?\.format\(',
]

SAFE_PATTERNS = [
    r'execute\([^,]+,\s*\[.*?\]\)',
    r'session\.query\(.*?\)\.filter\(',
]
```

**XSS Detection**:
```yaml
contexts:
  - name: "HTML Context"
    dangerous: [innerHTML =, document.write(, .html(]
    safe: [.textContent =, .innerText =, escapeHtml(]
      
  - name: "JavaScript Context"
    dangerous: [eval(, Function(, setTimeout( + string]
    safe: [JSON.parse(, parseInt(]
      
  - name: "URL Context"
    dangerous: [href = user_input, location =]
    safe: [encodeURIComponent(, URL validation regex]
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

```dockerfile
ignored:
  - DL3008
  - DL3009

trustedRegistries:
  - docker.io
  - gcr.io
  
failure-threshold: warning

rules:
  - DL3001
  - DL3002
  - DL3003
  - DL3004
  - DL3007
  - DL3025
  - DL4006
  - SC2086
```

### API Security Testing

```yaml
{
  "info": {"name": "Security Test Suite"},
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
        "body": {"contains": ["unauthorized", "token required"]}
      }
    },
    {
      "name": "Expired Token",
      "request": {
        "url": "{{baseUrl}}/api/users",
        "method": "GET",
        "header": [{"key": "Authorization", "value": "Bearer {{expiredToken}}"}]
      },
      "expect": {"status": 401}
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
        "body": {"not_contains": ["error", "syntax", "SQL"]}
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
    manual_checks: ["Verify RBAC implementation", "Test privilege escalation paths"]
      
  A02_cryptographic_failures:
    tools: ["SSLyze", "testssl.sh"]
    checks: ["TLS 1.2 minimum", "No weak ciphers", "HSTS enabled"]
      
  A03_injection:
    tools: ["Bandit", "Semgrep", "SQLMap"]
    patterns: [sql_injection, command_injection, ldap_injection]
```

### Continuous Security Pipeline

```yaml
security:sast:
  stage: security
  script:
    - bandit -r src/ -f json -o bandit-report.json
    - safety check --json > safety-report.json
    - semgrep --config=auto --json -o semgrep-report.json src/
  artifacts:
    reports:
      sast: [bandit-report.json, safety-report.json, semgrep-report.json]

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
      dependency_scanning: [pip-audit.json, npm-audit.json]
```

### Finding Validation

```python
def validate_finding(finding):
    if finding.type == "hardcoded_password":
        if "example" in finding.file_path: return False
        if finding.value == "changeme": return False
            
    if finding.type == "sql_injection":
        if not is_user_controlled(finding.source): return False
            
    if finding.severity == "CRITICAL":
        if "denial of service" in finding.description:
            finding.severity = "HIGH"
            
    return True
```

### Reality
Security scanning: 60% false positives, 30% low-impact, 9% real vulns, 1% critical
Real security scanning: multiple tools, validated findings, tracked remediation, continuous monitoring