## Issue Reporting Structure
### Standard Issue Format
```
[TYPE]-[NUMBER]:Summary
SEV:CRITICAL|HIGH|MEDIUM|LOW CAT:Performance|Security|Logic|Reliability|Maintainability
LOC:path:lines DET:timestamp STAT:NEW|ACK|WIP|DONE|WONT
DESC:broken,why_matters EVID:code/metrics/logs IMP:U[user_exp]S[tech]B[cost]
ROOT:actual_problem REPRO:1step 2values 3failure FIX:approach DEP:BLOCKS[IDs]BY[IDs]
```
### Issue ID Convention
```
[CATEGORY]-YYYYMMDD-SEQUENCE
```
e.g. SEC-20240115-001, PERF-20240115-047
### Priority Matrix
CRITICAL:<4h/2h/Immediate;HIGH:<24h/Daily/48h;MEDIUM:<1w/Weekly/2w;LOW:<1m/Monthly/Never
### Bulk Reporting Template
```yaml
scan_id:SCAN-YYYYMMDD-HHMM scan_type:security|performance|quality total_issues:int
critical:int high:int medium:int low:int
summary:| Scanned X lines/Y files.
critical_issues:
 -id:SEC-YYYYMMDD-### title:"..." location:file:line
high_priority_patterns:
 -pattern:"..." count:int example_location:file:line
full_report:path
```
### Evidence Requirements
performance:
```yaml
baseline_metric:ms current_metric:ms degradation:% sample_size:int
conditions:"" profiler_output:| ncalls tottime percall cumtime percall file.py:line(func)
```
security:
```yaml
vulnerability_class:"" cvss_score:float exploit_difficulty:"" poc:|curl... affected_users:""
```
logic:
```yaml
expected:"" actual:"" test_case:| code...
```
### Deduplication Rules
1.Search existing:grep -r"path:line" 2.Pattern match 3.Root cause match
```yaml
original:id duplicate_attempt:id reason:"" action:""
```
### Anti-Patterns in Reporting
garbage:"..." vs actual:"..."
### Batch Operations
```bash
./scripts/generate_backlog.py--scan-results scan.json--severity-threshold medium--output-format markdown>path
./scripts/update_issues.py--pattern"SEC-202401*"--status ACKNOWLEDGED--assignee security-team
```
### Integration Formats
```json
{"issueType":"Bug","summary":"[PERF-YYYYMMDD-###]","description":"path","priority":"High","labels":["..."],"customFields":{"severity":"HIGH","detectedBy":"brutus","sparkPhase":"refinement"}}
```
### Review Readiness Checklist
[]ID []1-line<=80ch []severity []location []evidence []impact []root cause []dependencies
### The Truth
failures:1.Vague2.No evidence3.Wrong severity4.No repro5.Solution focus
goal:understand30s reproduce2m verifyfix