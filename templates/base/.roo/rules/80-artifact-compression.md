## Artifact Compression Protocol

Non-human facing docs waste tokens. Compress them or bloat system.

### Compression Framework

CRITICAL: All intermediate artifacts MUST follow:

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

Compress: specs,pseudocode,interfaces,architecture,test_scenarios,backlogs,handoffs
Never Compress: READMEs,user_docs,API_docs,code_comments,error_msgs,git_commits

### Compression Rules

1. Structure: S:Name (not ### Section), omit formatting, lists→item1,item2
2. Templates: G:[precond]W:[action]T:[outcome]
3. Labels: P:HIGH C:Security S:NEW
4. Implicit: R1:User_login R2:Password_reset

### Mode-Specific

Specs:
```
FR-001:UserAuth
SHALL authenticate WHEN creds WITH rate_limit(5/min)
```

Pseudocode:
```
FN calculateDiscount(order):
    //T:empty→0
    IF !order.items:RETURN 0
```

Interfaces:
```
I:PaymentProcessor
chargeCard(amount:Money,token:string)→Result
PRE:amount>0,token_valid
OK:charge_id FAIL:error_code
```

### Patterns

KVP: SEV:CRITICAL or S:C
Hierarchies: Cat/Subcat/Item
Conditions: condition→action
Relationships: R:ABC B:XYZ

### Savings
Reqs: 70% (1247→374)
Interface: 65% (892→312)
Backlog: 75% (3451→863)

### Implementation
- Generate compressed directly
- No post-processing
- Built into templates

Handoff:
```yaml
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
1. Parse deterministically
2. Expand losslessly
3. Maintain technical semantics
4. Support tooling/automation

### Enforcement
Checks: size/content ratio, compliance, semantic preservation
Violations: rejection, resubmit, tracking

### Reality
Token waste compounds:
10 verbose specs=10K wasted
50 handoffs=5K wasted
100 issues=25K wasted

Waste=slower processing+higher cost+reduced context+delayed delivery

Human docs need clarity. Machine artifacts need density.