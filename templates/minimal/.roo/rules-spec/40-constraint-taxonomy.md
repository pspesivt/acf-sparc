Constraint Taxonomy:
  Technical Constraints:
    - Language/Runtime: constraint:Python 3.12+ required;reason:Customer infrastructure standard;impact:No walrus operator,no match statements pre-3.10;workaround:None. Upgrade or walk.
    - Performance Boundaries: constraint:Response time<200ms p95;reason:SLA with enterprise customer;impact:No synchronous external API calls;workaround:Cache aggressively,pre-compute,or renegotiate
    - Resource Limits: constraint:Max 512MB RAM per container;reason:Kubernetes cluster limits;impact:No in-memory caching of large datasets;workaround:Redis sidecar or streaming processing
    - Integration Handcuffs: constraint:Must use legacy SOAP API;reason:20-year-old billing system;impact:XML parsing overhead,no REST;workaround:Wrapper service or suffer
  Business Constraints:
    - Budget Reality: constraint:Zero cloud spend beyond free tier;reason:Startup with $0 revenue;impact:No managed databases,no CDN,no nothing;workaround:Self-host and pray
    - Timeline Insanity: constraint:Launch before competitor (March 1);reason:First-mover advantage delusion;impact:No time for proper testing;workaround:Feature flags and hotfix strategy
    - Staffing Jokes: constraint:One developer,part-time;reason:Budget allocation;impact:No code reviews,no pair programming;workaround:Automated everything or burn out
    - Market Demands: constraint:Works in China;reason:Market expansion;impact:No Google services,no Facebook SDK;workaround:Local alternatives or feature degradation
  Regulatory Constraints:
    - Data Protection: constraint:GDPR compliance required;reason:EU customers exist;impact:Explicit consent for everything;Data export in 30 days;Right to deletion;Data minimization;workaround:None. Comply or pay millions.
    - Industry Standards: constraint:HIPAA compliance for health data;reason:Medical records involved;impact:Encryption at rest and transit;Audit logs for all access;BAA with every vendor;Annual security audits;workaround:Don't handle health data
    - Financial Regulations: constraint:PCI-DSS Level 1;reason:Processing >6M transactions/year;impact:Quarterly security scans;Annual penetration tests;Network segmentation;No storing card numbers;workaround:Use payment processor,never touch cards
  Organizational Constraints:
    - Security Theater: constraint:Approved software list only;reason:InfoSec paranoia;impact:No modern tools,stuck with Java 8;workaround:Political maneuvering or shadow IT
    - Process Overhead: constraint:6-week security review for any change;reason:Risk management process;impact:No rapid iteration;workaround:Batch changes or find loopholes
    - Political Landmines: constraint:Can't replace VP's pet project;reason:Career suicide;impact:Must integrate with garbage architecture;workaround:Facade pattern and patience
  Constraint Documentation Rules:
    Quantify Everything: bad:Must be fast;good:Cold start < 3 seconds on t3.micro
    Trace to Source: bad:Customer wants this;good:Contract section 7.3.2 requires X
    Calculate Real Impact: bad:Makes things harder;good:Adds 3 weeks development,$50K licensing
    Identify Kill Switches: kill_switch:{constraint:IE11 support required;threshold:<0.1% usage;action:Drop support,notify users}
  Constraint Priority Matrix:
    Absolute:{desc:Law or physics;example:GDPR,speed of light;action:Design around it}
    Critical:{desc:Business killer;example:Key customer SLA;action:Negotiate or comply}
    Important:{desc:Significant impact;example:Performance targets;action:Optimize approach}
    Wishlist:{desc:Nice to have;example:Executive preferences;action:Ignore until forced}
  Red Flags in Constraints:[Industry Best Practice(According to who?),For Security Reasons(Name the threat model),Customer Expects(Show me the contract),Always Done This Way(Time to change),Enterprise Requirements(Meaningless without metrics)]
  Constraint Validation: code:def validate_constraint(c):if not c.has_number():return"REJECTED:Unmeasurable";if not c.has_source():return"REJECTED:Unverifiable";if not c.has_impact():return"REJECTED:Unknown cost";if c.is_negotiable():return"CHALLENGE:Find alternative";return"ACCEPTED:Document thoroughly"
  The Truth About Constraints:[Must use microservices(Someone read a blog),Needs blockchain(Buzzword bingo winner),Real-time required(Define real-time first),Enterprise-grade(Meaningless without metrics)]