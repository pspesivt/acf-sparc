## Artifact Compression Protocol

Non-human facing documents waste tokens. Compress them or bloat the system.

### Compression Framework

CRITICAL: All intermediate artifacts (specs, pseudocode, interfaces, backlogs) MUST follow this compression:

```
compress(input)->output:
  preserve_exact={global_headers,titles,paths,protocols,names,identifiers,values,code}
  preserve_semantic={structure,hierarchy,logic,relationships,content}
  remove={formatting(**,__,###),redundancy,filler,fluff,verbosity,human_markup,meta_commentary}
  apply={merge_similar,compact_syntax,implicit_structure}
  effort=ultrathink
  constraint=lossless_technical
  output_format=direct_start_no_preamble
  forbidden={introduction,commentary,evaluation,transition_text,acknowledgment}
  special_rule=preserve_first_line_if_title_or_header
  return=compressed_content_only_no_surrounding_text
```

### Scope

**Compress These** (machine-to-machine):
- Specification documents
- Pseudocode files
- Interface definitions
- Architecture documents
- Test scenarios
- Issue backlogs
- Handoff contexts

**Never Compress** (human-facing):
- README files
- User documentation
- API documentation
- Code comments
- Error messages
- Git commits

### Compression Rules

**1. Structure Markers**
```
BEFORE: ### Section Name
AFTER: S:Name

BEFORE: **Bold Text**
AFTER: [omit formatting]

BEFORE: - List item one
        - List item two
AFTER: item1,item2
```

**2. Verbose Templates**
```
BEFORE: Given [precondition]
        When [action]
        Then [outcome]
AFTER: G:[precondition]W:[action]T:[outcome]
```

**3. Redundant Labels**
```
BEFORE: Priority: HIGH
        Category: Security
        Status: NEW
AFTER: P:HIGH C:Security S:NEW
```

**4. Implicit Structure**
```
BEFORE: Requirements:
        - R1: User login
        - R2: Password reset
AFTER: R1:User_login R2:Password_reset
```

### Mode-Specific Compression

**Specification Documents**:
```
# Original
## Functional Requirement FR-001: User Authentication
The system SHALL authenticate users WHEN credentials provided
WITH rate limiting of 5 attempts per minute.

# Compressed
FR-001:UserAuth
SHALL authenticate WHEN creds WITH rate_limit(5/min)
```

**Pseudocode**:
```
# Original
FUNCTION calculateDiscount(order):
    // TEST: Empty order returns zero
    IF order.items IS EMPTY:
        RETURN 0

# Compressed
FN calculateDiscount(order):
    //T:empty→0
    IF !order.items:RETURN 0
```

**Interface Definitions**:
```
# Original
Interface: PaymentProcessor
Method: chargeCard(amount: Money, token: string) → Result
Precondition: amount > 0 and token valid
Success: Returns charge ID
Failure: Returns error code

# Compressed
I:PaymentProcessor
chargeCard(amount:Money,token:string)→Result
PRE:amount>0,token_valid
OK:charge_id FAIL:error_code
```

### Compression Patterns

**Key-Value Pairs**:
```
BEFORE: Severity: CRITICAL
AFTER: SEV:CRITICAL or S:C (if unambiguous)
```

**Hierarchies**:
```
BEFORE: Category > Subcategory > Item
AFTER: Cat/Subcat/Item
```

**Conditions**:
```
BEFORE: IF condition THEN action
AFTER: condition→action
```

**Relationships**:
```
BEFORE: Requires: ABC, Blocks: XYZ
AFTER: R:ABC B:XYZ
```

### Token Savings Examples

**Requirements Doc** (70% reduction):
```
Original: 1,247 tokens
Compressed: 374 tokens
```

**Interface Spec** (65% reduction):
```
Original: 892 tokens
Compressed: 312 tokens
```

**Issue Backlog** (75% reduction):
```
Original: 3,451 tokens
Compressed: 863 tokens
```

### Implementation

**At Generation**:
- Modes generate compressed format directly
- No post-processing needed
- Compression built into templates

**At Handoff**:
```yaml
# Compressed handoff
handoff:
  from:orchestrator to:spec phase:specification status:ready
  deliverables:
    docs/specs/reqs.md:specification:complete
  context:
    decisions:FastAPI,PostgreSQL
    blockers:auth_undefined
    next:define_auth,rate_limits
```

### Validation

Compressed artifacts must:
1. Parse deterministically
2. Expand losslessly (for humans when needed)
3. Maintain all technical semantics
4. Support tooling/automation

### Enforcement

**Orchestrator checks**:
- Artifact size vs content ratio
- Compression compliance
- Semantic preservation

**Violations**:
- Verbose artifacts rejected
- Mode must resubmit compressed
- Repeated violations tracked

### The Reality

Token waste compounds:
- 10 verbose specs = 10,000 wasted tokens
- 50 handoffs = 5,000 wasted tokens
- 100 issues = 25,000 wasted tokens

Every wasted token:
- Slows processing
- Increases cost
- Reduces context window
- Delays delivery

Compress or accept inefficiency. There's no middle ground.

Human documentation needs clarity. Machine artifacts need density.

Know the difference or waste everyone's resources.
