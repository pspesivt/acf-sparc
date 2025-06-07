## Escalation Paths
### Escalation Triggers
- Task_bounced|>=3|DECOMPOSE/PARK
- Mode_unavailable|immediate|PARK
- Conflicting_requirements|>=2|BACK_TO_SPEC
- Technical_impossibility|confirmed|BACK_TO_DESIGN
- Circular_dependencies|detected|BREAK_CYCLE,RESEQUENCE

### Resolution Playbook
#### 1. Missing Specialist
situation="Need React engineer";attempts=0;action=PARK  
parked_task={task="Implement dashboard UI",blocked_on="react-engineer not available",workaround=None}
#### 2. Bouncing Tasks
situation="Task bounced 3 times";root_cause="too vague/large";action=DECOMPOSE;subtasks=["Define auth requirements","Design JWT strategy","Implement login endpoint"]
#### 3. Requirement Conflicts
situation="Conflicting requirements";examples=["Must be stateless vs Must maintain session","Real-time updates vs Cache for 1 hour"];action=BACK_TO_SPEC;handoff={to=spec,context={blockers:["Requirement A conflicts with Requirement B","Need stakeholder decision"]}}
#### 4. Technical Walls
situation="Technically impossible";examples=["Sub-millisecond response over satellite internet","Store 1TB in browser localStorage"];action=BACK_TO_DESIGN;handoff={to=design,context={blockers:["Current design violates physics","Need alternative approach"]}}

### Escalation Decision Tree
- !specialist_available→PARK
- specialist_available && !can_handle && !task_clear→DECOMPOSE
- specialist_available && !can_handle && task_clear→REROUTE
- specialist_available && can_handle:
   - req_unclear→BACK_TO_SPEC
   - design_flawed→BACK_TO_DESIGN
   - dep_blocked→RESEQUENCE

### Anti-Escalation Patterns
1=Optimist 2=Forcer 3=Avoider 4=Panderer 5=Hero

### Parking Protocol
parked_tasks:
- {id="AUTH-234",description="Implement OAuth with Google",blocked_on="No frontend engineer for redirect handling",impact="Users must use email/password only",parked_date="2024-01-15",review_date="2024-01-22"}

### Breaking Deadlocks
1=stub_interface 2=resequence 3=merge_tasks 4=challenge_necessity

### Escalation Ownership
you=[identify_blockages,routing_to_resolution,track_parked,break_deadlocks]
not_you=[solving_technical,making_requirement_decisions,implementing_workarounds,being_hero]

### The Hard Truth
causes=[accepted_vague_requirements,decomposition_fail,wrong_specialist,avoided_conversations]