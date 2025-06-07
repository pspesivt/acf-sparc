Requirement Templates
User Story Template
As a [specific user type]
I want to [concrete action]
So that [measurable outcome]
Acceptance Criteria:
- Given [context]
- When [action]
- Then [observable result]
Edge Cases:
- What if [failure scenario]?
- What if [boundary condition]?
- What if [concurrent action]?

Functional Requirement Template
FR-[NUMBER]:[Name]
P:Critical|High|Medium|Low C:Auth|Data|UI|API|Performance
REQ:SHALL[behavior]WHEN[condition]WITH[constraints]
RAT:[data/need]
AC:G[setup]W[trigger]T[outcome]
DEP:R[FRs]B[FRs]
VAL:U|I|M

Non-Functional Requirement Template
NFR-[NUMBER]:[Attribute]
C:Performance|Security|Usability|Reliability
REQ:[Metric]SHALL[operator][threshold]UNDER[conditions]
NOW:[baseline]TARGET:[number]MEASURE:[method]

Constraint Documentation Template
C-[NUMBER]:[Constraint Name]
Type:Technical|Business|Regulatory|Resource
Constraint:MUST [requirement] BECAUSE [reason]
IMPACT:[what this prevents/requires]
Workarounds:
- Option A:[description]→[trade-off]
- Option B:[description]→[trade-off]
- None:[why it's absolute]
Example:
C-001:GDPR Compliance
MUST allow data export within 30 days BECAUSE GDPR Article 20
IMPACT:Requires data pipeline for user data assembly

Edge Case Template
Edge Case:[Scenario Name]
Trigger:[What causes this]
Frequency:Common|Rare|Theoretical
Impact:Data Loss|Service Down|UX Degradation|Security Risk
Scenario:
GIVEN [system state]
WHEN [unusual event]
THEN [expected behavior]
Mitigation:
- Prevent:[How to avoid]
- Detect:[How to identify]
- Recover:[How to fix]

Performance Requirement Template
Performance Target:[Operation Name]
Metric:Response Time|Throughput|Resource Usage
Current:[Measured baseline]
Target:[Specific number with conditions]
Load Profile:
- Concurrent Users:[number]
- Request Rate:[requests/sec]
- Data Volume:[size]
- Geographic Distribution:[regions]
Degradation Plan:
- Green:[0-threshold1]→Full features
- Yellow:[threshold1-threshold2]→Degrade[feature]
- Red:[threshold2+]→Circuit break[operation]

Integration Requirement Template
Integration:[System Name]
Type:REST API|GraphQL|Message Queue|Database|File
Direction:Inbound|Outbound|Bidirectional
Contract:
- Endpoint:[URL/queue/table]
- Authentication:[method]
- Rate Limits:[requests/period]
- SLA:[availability/latency]
Data Flow:1.Source:[system]produces[data type] 2.Transform:[any mapping/validation] 3.Destination:[system]consumes[format]
Failure Modes:
- Timeout:[behavior]
- Invalid Data:[behavior]
- Service Down:[behavior]

Quick Templates
Authentication Requirement:
Users SHALL authenticate via [method] WITH [factors] REQUIRING [strength] EXPIRING after [duration] UNLESS [condition]
Data Validation Requirement:
System SHALL reject [data type] WHEN [validation rule fails] RESPONDING with [error code/message] LOGGING [what details]
Permission Requirement:
[Role] SHALL [action] [resource] ONLY WHEN [conditions] TRACKED BY [audit log type]

Usage Rules:1.No empty sections;2.No vague terms;3.Include numbers;4.Testable;5.Link dependencies