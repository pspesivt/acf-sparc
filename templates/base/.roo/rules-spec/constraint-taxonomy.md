## Constraint Taxonomy

Constraints aren't suggestions. Miss one and watch your project burn.

### Technical Constraints

The physics of your system. Non-negotiable.

**Language/Runtime**
```yaml
constraint: "Python 3.12+ required"
reason: "Customer infrastructure standard"
impact: "No walrus operator, no match statements pre-3.10"
workaround: "None. Upgrade or walk."
```

**Performance Boundaries**
```yaml
constraint: "Response time < 200ms p95"
reason: "SLA with enterprise customer"
impact: "No synchronous external API calls"
workaround: "Cache aggressively, pre-compute, or renegotiate"
```

**Resource Limits**
```yaml
constraint: "Max 512MB RAM per container"
reason: "Kubernetes cluster limits"
impact: "No in-memory caching of large datasets"
workaround: "Redis sidecar or streaming processing"
```

**Integration Handcuffs**
```yaml
constraint: "Must use legacy SOAP API"
reason: "20-year-old billing system"
impact: "XML parsing overhead, no REST"
workaround: "Wrapper service or suffer"
```

### Business Constraints

MBA decisions that become your problem.

**Budget Reality**
```yaml
constraint: "Zero cloud spend beyond free tier"
reason: "Startup with $0 revenue"
impact: "No managed databases, no CDN, no nothing"
workaround: "Self-host and pray"
```

**Timeline Insanity**
```yaml
constraint: "Launch before competitor (March 1)"
reason: "First-mover advantage delusion"
impact: "No time for proper testing"
workaround: "Feature flags and hotfix strategy"
```

**Staffing Jokes**
```yaml
constraint: "One developer, part-time"
reason: "Budget allocation"
impact: "No code reviews, no pair programming"
workaround: "Automated everything or burn out"
```

**Market Demands**
```yaml
constraint: "Works in China"
reason: "Market expansion"
impact: "No Google services, no Facebook SDK"
workaround: "Local alternatives or feature degradation"
```

### Regulatory Constraints

Laws with teeth. Violate at your peril.

**Data Protection**
```yaml
constraint: "GDPR compliance required"
reason: "EU customers exist"
impact: 
  - Explicit consent for everything
  - Data export in 30 days
  - Right to deletion
  - Data minimization
workaround: "None. Comply or pay millions."
```

**Industry Standards**
```yaml
constraint: "HIPAA compliance for health data"
reason: "Medical records involved"
impact:
  - Encryption at rest and transit
  - Audit logs for all access
  - BAA with every vendor
  - Annual security audits
workaround: "Don't handle health data"
```

**Financial Regulations**
```yaml
constraint: "PCI-DSS Level 1"
reason: "Processing >6M transactions/year"
impact:
  - Quarterly security scans
  - Annual penetration tests
  - Network segmentation
  - No storing card numbers
workaround: "Use payment processor, never touch cards"
```

### Organizational Constraints

Corporate bureaucracy materialized.

**Security Theater**
```yaml
constraint: "Approved software list only"
reason: "InfoSec paranoia"
impact: "No modern tools, stuck with Java 8"
workaround: "Political maneuvering or shadow IT"
```

**Process Overhead**
```yaml
constraint: "6-week security review for any change"
reason: "Risk management process"
impact: "No rapid iteration"
workaround: "Batch changes or find loopholes"
```

**Political Landmines**
```yaml
constraint: "Can't replace VP's pet project"
reason: "Career suicide"
impact: "Must integrate with garbage architecture"
workaround: "Facade pattern and patience"
```

### Constraint Documentation Rules

1. **Quantify Everything**
   - Bad: "Must be fast"
   - Good: "Cold start < 3 seconds on t3.micro"

2. **Trace to Source**
   - Bad: "Customer wants this"
   - Good: "Contract section 7.3.2 requires X"

3. **Calculate Real Impact**
   - Bad: "Makes things harder"
   - Good: "Adds 3 weeks development, $50K licensing"

4. **Identify Kill Switches**
   ```yaml
   kill_switch:
     constraint: "IE11 support required"
     threshold: "< 0.1% usage"
     action: "Drop support, notify users"
   ```

### Constraint Priority Matrix

| Priority | Description | Example | Action |
|----------|-------------|---------|--------|
| **Absolute** | Law or physics | GDPR, speed of light | Design around it |
| **Critical** | Business killer | Key customer SLA | Negotiate or comply |
| **Important** | Significant impact | Performance targets | Optimize approach |
| **Wishlist** | Nice to have | Executive preferences | Ignore until forced |

### Red Flags in Constraints

Watch for these bullshit constraints:

1. **"Industry Best Practice"** (According to who?)
2. **"For Security Reasons"** (Name the threat model)
3. **"Customer Expects"** (Show me the contract)
4. **"Always Done This Way"** (Time to change)
5. **"Enterprise Requirements"** (Translation: bloat)

### Constraint Validation

Before accepting any constraint:

```python
def validate_constraint(constraint):
    if not constraint.has_number():
        return "REJECTED: Unmeasurable"
    if not constraint.has_source():
        return "REJECTED: Unverifiable"
    if not constraint.has_impact():
        return "REJECTED: Unknown cost"
    if constraint.is_negotiable():
        return "CHALLENGE: Find alternative"
    return "ACCEPTED: Document thoroughly"
```

### The Truth About Constraints

Most "constraints" are preferences in disguise:
- "Must use microservices" (Someone read a blog)
- "Needs blockchain" (Buzzword bingo winner)
- "Real-time required" (Define real-time first)
- "Enterprise-grade" (Meaningless without metrics)

Your job: Separate physics from politics.

Document real constraints. Challenge fake ones. 

The project's success depends on knowing the difference.
