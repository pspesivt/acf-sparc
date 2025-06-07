## Incident Reporting Protocol
## Incident Report Format
template:id=INC-[YYYY][MM][DD]-[HHMM]-[MODE];fields={Mode,Phase,Task,Timestamp,Failure(line),Context(max3),RootCause,RecoveryPath(list),Handoff:{Status,Blocker,Next}}
filename:docs/retro/INC-YYYYMMDD-HHMM-MODE.md
## Triggers
immediate={tool_exec_fail_after_retry,file_not_found,handoff_rejection,constraint_violation,scope_boundary_hit,memory_context_load_fail,api_integration_timeout}
exclude={normal_validation_rejections,expected_bouncebacks,planned_handoffs,successful_retries}
## Severity Levels
CRITICAL={Cannot load project memory,Core deliverable missing,Circular dependency detected}
HIGH={Required tool unavailable,Integration API down,File corruption detected}
MEDIUM={Retry succeeded after 3 attempts,Fallback path used,Performance degradation}
## Required Sections
minimal={Mode,Phase,Task,Timestamp,Failure,RootCause,Handoff.Status}
extended(if severity∈{HIGH,CRITICAL})={Context(max3),RecoveryAttempts,DependenciesAffected}
## Examples
good:id=INC-20240115-1430-python-engineer;Mode=python-engineer;Phase=refinement;Task=Implement user authentication;Timestamp=2024-01-15T14:30:00Z;Failure=apply_diff failed: SEARCH text not found in auth.py;RootCause=File structure changed since architecture phase;RecoveryPath=[1.Read current file structure,2.Update implementation approach,3.Retry with correct paths];Handoff={Status=blocked,Blocker=Outdated file references,Next=Re-read architecture docs}
## Aggregation
weekly:docs/retro/WEEK-YYYY-MM.md;fields={Total,Critical,High,Medium,Patterns,Actions}
## Auto-Generation
python:def handle_failure(error,context)->incident{id=f"INC-{timestamp}-{mode}",mode=current_mode,phase=current_phase,task=current_task,failure=str(error)[:80],root_cause=analyze_error(error),recovery=determine_recovery_path(error)};write_incident_report(incident);create_blocked_handoff(incident["root_cause"])
## Reality
repeat_causes={no_documentation,no_root_cause_analysis,no_recovery_plan,no_pattern_detection,no_learning}