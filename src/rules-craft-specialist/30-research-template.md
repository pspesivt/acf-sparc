## Research Template for Mode Creation

Fill this completely before generating any mode. Half-assed research = half-assed specialist.

### Domain Profile

```yaml
domain:
  name: # e.g., "React Development"
  core_language: # e.g., "JavaScript/TypeScript"
  ecosystem_maturity: # startup|growing|mature|legacy
  complexity_level: # low|medium|high|extreme
  
primary_use_cases:
  - # e.g., "Single-page applications"
  - # e.g., "Reusable component libraries"
  - # e.g., "Progressive web apps"
```

### Technology Stack Research

```yaml
core_technologies:
  language:
    name:
    version: # minimum supported
    key_features: # that matter for this domain
    
  framework:
    name:
    version:
    alternatives: # considered but rejected
    
  build_tools:
    primary: # e.g., Vite
    why: # e.g., "Faster than webpack, better DX"
    configuration_complexity: # low|medium|high
    
  package_management:
    tool: # npm, yarn, pnpm, etc.
    lockfile_format:
    workspace_support:
```

### Best Practices Extraction

```yaml
coding_standards:
  style_guide: # e.g., "Airbnb JavaScript Style"
  type_safety: # none|optional|strict
  linting_tools:
    - tool:
      config:
      rules:
      
testing_practices:
  frameworks:
    unit: # e.g., "Vitest"
    integration: # e.g., "Cypress"
    e2e: # e.g., "Playwright"
  coverage_targets:
    minimum:
    business_logic:
    ui_components:
    
performance_standards:
  metrics:
    - name: # e.g., "First Contentful Paint"
      target: # e.g., "< 1.8s"
    - name: # e.g., "Time to Interactive"
      target: # e.g., "< 3.9s"
```

### Security Considerations

```yaml
common_vulnerabilities:
  - type: # e.g., "XSS in dangerouslySetInnerHTML"
    prevention:
    detection:
    
  - type: # e.g., "Prototype pollution"
    prevention:
    detection:
    
security_tools:
  static_analysis:
  dependency_scanning:
  runtime_protection:
```

### Anti-Pattern Catalog

```yaml
beginners_do_this:
  - pattern: # e.g., "Direct DOM manipulation"
    why_bad:
    correct_approach:
    
  - pattern: # e.g., "Mutating state directly"
    why_bad:
    correct_approach:
    
experts_still_do_this:
  - pattern: # e.g., "Over-engineering with Redux"
    why_bad:
    when_appropriate:
    
  - pattern: # e.g., "Premature optimization"
    why_bad:
    when_necessary:
```

### Integration Points

```yaml
handoff_boundaries:
  accepts_from:
    - mode: design
      deliverables: ["component specifications", "API contracts"]
      
  produces_for:
    - mode: refine
      deliverables: ["source code", "test suites"]
      
  never_touches:
    - "Backend API implementation"
    - "Database schemas"
    - "Deployment configurations"
```

### Validation Checklist

Before mode generation:
- [ ] Researched 10+ production codebases
- [ ] Read official documentation (not tutorials)
- [ ] Identified 5+ common failure patterns
- [ ] Found canonical test patterns
- [ ] Verified toolchain stability
- [ ] Confirmed security best practices
- [ ] Validated performance benchmarks

Skip any? Your mode will produce garbage.
