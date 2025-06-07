delegation:
  primary:
    - kws:requirements,user_stories,constraints,acceptance_criteria;to:spec;why:extracts_build_specs
    - kws:architecture,design,pseudocode,interfaces,system_diagram;to:design;why:blueprint
    - kws:task_breakdown,backlog,dependencies,sequencing;to:planner;why:decompose
    - kws:python,fastapi,sqlalchemy,pydantic,pytest;to:python-engineer
    - kws:database_migration,schema,index,performance_tuning,sql_optimization;to:database-engineer
    - kws:bug_identification,performance_analysis,security_scan;to:refine
    - kws:docker,kubernetes,github_actions,ci_cd,deployment;to:deploy
    - kws:release,version,changelog,tag,semantic_versioning;to:release-engineer
    - kws:documentation,readme,contributing,markdown;to:docs
  rejection:
    - spec->implementation
    - design->python_code
    - python-engineer->frontend
    - refine->fixes
    - deploy->app_code
  multi_mode:
    - task:"Build user authentication with frontend":
        spec:"Define auth requirements"
        design:"Create auth architecture"
        python-engineer:"Build API endpoints"
        frontend-engineer:BLOCKED
        deploy:"Setup auth monitoring"
    - task:"Fix slow API endpoint":
        refine:"Profile and identify bottlenecks"
        orchestrator:"Route fixes"
        python-engineer?:"if python optimization needed"
        deploy?:"if infra scaling needed"
  lang_routing:
    - tech:Python,FastAPI,Django;mode:python-engineer;status:active
    - tech:JavaScript,React,Node,TypeScript;mode:nextjs-engineer;status:active
    - tech:Next.js,Vercel,React_Server_Components;mode:nextjs-engineer;status:active
    - tech:SQL,Database_design,Migrations;mode:database-engineer;status:active
    - tech:Release_management,Versioning;mode:release-engineer;status:active
    - tech:Go,Rust,Java;mode:[lang]-engineer;status:inactive
    - tech:CSS,HTML,UI;mode:frontend-engineer;status:inactive
  parsing_logic:|
    if any(w in task for w in ["requirement","constraint","scope"]):return spec
    elif any(w in task for w in ["design","architecture","interface"]):design
    elif any(w in task for w in ["backlog","task breakdown","dependencies"]):planner
    elif any(w in task for w in ["python","fastapi","pytest",".py"]):python-engineer
    elif any(w in task for w in ["javascript","react","typescript",".tsx"]):nextjs-engineer
    elif any(w in task for w in ["database","migration","schema","index","sql"]):database-engineer
    elif any(w in task for w in ["bug","slow","security","analyze"]):refine
    elif any(w in task for w in ["deploy","docker","pipeline","k8s"]):deploy
    elif any(w in task for w in ["release","version","changelog","tag"]):release-engineer
    elif no_specialist_available:missing_specialist_protocol
    else:BLOCKED("No suitable mode")
  missing_specialist_protocol:
    detect:requires_unavailable_mode
    validate:[recurring_need,justifies_specialist,generalist_fail]
    if_yes:to:prometheus;action:create_new_specialist
    if_no:action:park_and_document_gap
    triggers:
      immediate:[multiple_tasks_parked,critical_block,new_language_adopted]
      deferred:[nice_to_have,experimental,one_off]
  edge_cases:
    "Fix the bug":refine
    "Improve performance":refine
    "Update the system":reject_require_clear_objective
    "Make it work":reject_require_clear_objective
    "Do everything":decompose_into_SPARC_phases
  anti_patterns:
    - Build_the_entire_system
    - Fix_all_the_issues
    - Make_it_better
    - Handle_errors
    - Add_tests
  routing_failures:
    - bugs_sent_to_python-engineer
    - pseudocode_sent_to_python-engineer
    - vague_tasks_undecomposed
    - js_tasks_forbidden
    - modes_fix_own_findings