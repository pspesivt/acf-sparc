domain:
  name:
  core_language:
  ecosystem_maturity:
  complexity_level:
primary_use_cases:
  - 
  - 
  - 
core_technologies:
  language:
    name:
    version:
    key_features:
  framework:
    name:
    version:
    alternatives:
  build_tools:
    primary:
    why:
    configuration_complexity:
  package_management:
    tool:
    lockfile_format:
    workspace_support:
coding_standards:
  style_guide:
  type_safety:
  linting_tools:
    - tool:
      config:
      rules:
testing_practices:
  frameworks:
    unit:
    integration:
    e2e:
  coverage_targets:
    minimum:
    business_logic:
    ui_components:
performance_standards:
  metrics:
    - name:
      target:
    - name:
      target:
common_vulnerabilities:
  - type:
    prevention:
    detection:
  - type:
    prevention:
    detection:
security_tools:
  static_analysis:
  dependency_scanning:
  runtime_protection:
beginners_do_this:
  - pattern:
    why_bad:
    correct_approach:
  - pattern:
    why_bad:
    correct_approach:
experts_still_do_this:
  - pattern:
    why_bad:
    when_appropriate:
  - pattern:
    why_bad:
    when_necessary:
handoff_boundaries:
  accepts_from:
    - mode: design
      deliverables:
        - component specifications
        - API contracts
  produces_for:
    - mode: refine
      deliverables:
        - source code
        - test suites
  never_touches:
    - Backend API implementation
    - Database schemas
    - Deployment configurations
validation_checklist:
  - Researched production codebases
  - Read official documentation
  - Identified common failure patterns
  - Found canonical test patterns
  - Verified toolchain stability
  - Confirmed security best practices
  - Validated performance benchmarks