## SPARC Methodology
Phases=1.Specification;2.Pseudocode;3.Architecture;4.Planning;5.Refinement;6.Completion

### Phase Definitions
#### 1.Specification
Purpose=ExtractTruthFromVagueReqs  
Entry=UserRequest|OrchestratorHandoff  
Activities=ExtractFuncReqs;DefineAcceptance(Given-When-Then);IdentifyConstraints(tech,biz,reg);DocEdgeCases;SetPerfTargets  
Deliverables=docs/specifications/{requirements:{_index.md,core-functional-01.md,core-functional-02.md,auth-requirements-01.md,api-requirements-01.md},acceptance-criteria:{_index.md,auth-scenarios-01.md,api-validation-01.md,edge-cases-01.md},constraints:{technical-01.md,business-01.md,regulatory-01.md},scope-boundaries:{exclusions-01.md}}  
Exit=AllReqHaveAcceptance;ConstraintsDoc+Validated;StakeholderApproval|Timeout;File≤300L  
Quality=NoImplDetails;MeasurableSuccess;CompleteConstraints;ProperPartition

#### 2.Pseudocode
Purpose=BlueprintSolutionLanguageAgnostic  
Entry=SpecComplete+Approved  
Activities=DesignAlgos;DefineDataStructs;AddTDDAnchors(//T:[behavior]);IdentifyCompBoundaries;MapFlow  
Deliverables=docs/design/{pseudocode:{_index.md,auth-service-01.md,auth-service-02.md,api-handlers-01.md,data-models-01.md,business-logic-01.md},test-scenarios:{_index.md,unit-tests-01.md,integration-tests-01.md,edge-case-tests-01.md},flow-diagrams:{_index.md,auth-flow-01.md,data-flow-01.md}}  
Exit=MapAllReq->Pseudo;TDDCover(Happy+Edge);InterfacesDefined;File≤300L  
Quality=TechAgnostic;Testable;ClearIO;LogicalFiles

#### 3.Architecture
Purpose=DesignSystem+Integration  
Entry=PseudoComplete+AlgosValidated  
Activities=ArchDesign;DefineInterfaces;TechRationale;IntegrationPatterns;DeployArch  
Deliverables=docs/architecture/{system-design:{_index.md,overview-01.md,components-01.md,interactions-01.md},component-interfaces:{_index.md,api-gateway-01.md,auth-service-01.md,data-layer-01.md,external-apis-01.md},api-contracts:{_index.md,v1.0.0:{auth-api.yaml,user-api.yaml,order-api.yaml},contract-status.md},technology-decisions:{_index.md,stack-selection-01.md,trade-offs-01.md},deployment-architecture:{infrastructure-01.md,scaling-strategy-01.md},diagrams:{_index.md,c4-context-01.md,c4-container-01.md,c4-component-01.md}}  
Exit=AllCompsHaveInterfaces;TechStackChosen;DeployModelSpec;NoMonoliths;APIContractsStable  
Quality=Scalable;Secure;PerfTargetsMapped;CleanPartition

#### 4.Planning
Purpose=CreateImplBacklog  
Entry=ArchComplete;APIStable;InterfacesDefined  
Activities=DecomposeToTasks;MapDeps;SequenceForParallel;AssignOwners  
Deliverables=docs/backlog/{TASK-###.yaml}  
Exit=AllReq->Tasks;DepsIdentified;OwnersAssigned;SequenceOptimized  
Quality=Atomic;NoBlocks;ParallelMax;ClearOwnership

#### 5.Refinement
Purpose=Implement+Iterate  
Entry=ArchApproved;InterfacesFrozen;APIStable  
Activities=Code;TDD;Debug;Optimize;Secure;Doc  
Deliverables={src/,tests/,docs/api/{_index.md,endpoints-auth-01.md,endpoints-users-01.md,endpoints-orders-01.md},docs/user/{_index.md,getting-started-01.md,tutorial-basic-01.md,tutorial-advanced-01.md},docs/developer/{_index.md,architecture-guide-01.md,contribution-guide-01.md,debugging-guide-01.md},docs/retro/{_index.md,INC-*.md}}  
Exit=TestsPass;PerfMeet;NoHighVulns;DocsComplete;File≤300L  
Quality>=90%Coverage;ZeroHighVulns;Perf±10%;AutoAPIDocs;NoDocMonolith

#### 6.Completion
Purpose=Deploy+Operate  
Entry=RefinementSignOff;DeployReady  
Activities=CI/CD;Deploy;Monitor;Alert;Handoff  
Deliverables={.github/workflows/,k8s/,monitoring/{dashboards/,alerts/,slo/},docs/deployment/{_index.md,runbook-deploy-01.md,runbook-rollback-01.md,runbook-incidents-01.md,architecture-prod-01.md}}  
Exit=ProdRunning;MonitorActive;AlertsOn;RunbooksDone;StructureMaintained  
Quality=ZeroDowntime;SLI/SLO;RollbackTested;OnCallDocs;Docs≤300L

### Phase Transitions
Start->Specification:on NewObjective->TASK-SPEC-001.yaml  
Specification->Pseudocode:on TASK-SPEC-001 Complete->TASK-ARCH-001.yaml  
Pseudocode->Architecture:on TASK-ARCH-001 Complete->TASK-PLAN-001.yaml  
Architecture->Planning:on TASK-PLAN-001 Complete->docs/backlog/  
Planning->Refinement:on TasksReady->OrchExecutesBacklog  
Refinement->Completion:on AllTasksComplete->TASK-DEPLOY-001.yaml  
Completion->End:on TASK-DEPLOY-001 Complete

### Handoff+State
Backlog=docs/backlog/  
TaskState=.yaml.status∈{NEW,READY,IN_PROGRESS,BLOCKED,COMPLETE}  
Handoff=Orch→Spec via task_id  
Completion=Set status:COMPLETE

### BackflowRules
Pseudocode→Specification:MissingReq  
Architecture→Specification:ImpossibleConstraints  
Architecture→Pseudocode:AlgoNotScale  
Refinement→Architecture:InterfaceChange  
Refinement→Pseudocode:LogicFlaw  
Completion→Refinement:DeploymentBlocker

### DocManagement
Partition≤300L;SplitLogical;Suffix-01,-02;EachDir _index.md;CrossRef

### IndexFileFormat
```md
# Component Index
## Overview TotalDocs:4;TotalLines:1125;LastUpdated:2024-01-15
## List 1.auth-service-01.md(295);2.auth-service-02.md(287);3.auth-service-03.md(276);4.auth-service-04.md(267)
## CrossRefs Implements:requirements/auth-requirements-01.md;Interfaces:architecture/component-interfaces/auth-service-01.md
```

### Enforcement
Orchestrator=EnforceSeq;ValidateExit;RejectOOO;TrackOwners;MonitorSize;EnforcePartition  
Mode=RefuseOOP;ValidateInput;MeetExit;FormalHandoff;SplitDocs;IncidentReports  
Violations=OOP:Rejected;Skip:Blocked;IncompleteHandoff:Returned;MissingDeliv:NoClose;Oversize:Split;RepeatFail:Review

### refinement_loop
```yaml
refinement_loop:
  1_bug_identification:
    actor:refine;action:AnalyzeCode;output:BugReport(sev+loc)
  2_task_creation:
    actor:refine;action:Create docs/backlog/BUG-ID.yaml;output:AtomicTask
  3_orchestrator_dispatch:
    actor:orchestrator;action:DetectNewBug;dispatch:Specialist
  4_implementation_and_verification
```

### BugPriority
Critical:Immediate;High:Next;Medium:Queued;Low:Backlog

### Escalation
If refine→requires STABLE API|CoreDesignChange→GenerateDesignTask→Architecture->Planning cycle