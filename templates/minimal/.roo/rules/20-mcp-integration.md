MCP Integration Requirements
services:[
{name:OpenMemory,
 purpose:Persistent context across sessions,
 ops:[
  "<use_mcp_tool><server_name>openmemory</server_name><tool_name>search_memory</tool_name><arguments>{\"query\":\"*\"}</arguments></use_mcp_tool>",
  "<use_mcp_tool><server_name>openmemory</server_name><tool_name>add_memories</tool_name><arguments>{\"text\":\"[category]: [decision with rationale]\"}</arguments></use_mcp_tool>"
 ],
 categories:[PROJECT_CONVENTION,TECHNICAL_DECISION,USER_PREFERENCE,ERROR_RESOLUTION,CONSTRAINT],
 enforcement:[no_memory_load,no_decision_save]
},
{name:Context7,
 purpose:Official documentation,
 when:[implement,debug,architecture],
 ops:[
  "<use_mcp_tool><server_name>github.com/upstash/context7-mcp</server_name><tool_name>resolve-library-id</tool_name><arguments>{\"libraryName\":\"fastapi\"}</arguments></use_mcp_tool>",
  "<use_mcp_tool><server_name>github.com/upstash/context7-mcp</server_name><tool_name>get-library-docs</tool_name><arguments>{\"context7CompatibleLibraryID\":\"/python/fastapi\",\"topic\":\"dependency injection\",\"tokens\":10000}</arguments></use_mcp_tool>"
 ],
 violations:[implement_without_doc->rejected,assume_API->blocked]
},
{name:Perplexity,
 purpose:Current best practices,
 triggers:[error>=2,tech_evaluation,security_vuln,perf_optimization,deprecation],
 ops:[
  "<use_mcp_tool><server_name>perplexity-mcp</server_name><tool_name>search</tool_name><arguments>{\"query\":\"FastAPI dependency injection vs Flask 2025\",\"detail_level\":\"detailed\"}</arguments></use_mcp_tool>",
  "<use_mcp_tool><server_name>perplexity-mcp</server_name><tool_name>get_documentation</tool_name><arguments>{\"query\":\"SQLAlchemy DetachedInstanceError async session\",\"context\":\"FastAPI background tasks\"}</arguments></use_mcp_tool>",
  "<use_mcp_tool><server_name>perplexity-mcp</server_name><tool_name>check_deprecated_code</tool_name><arguments>{\"code\":\"from sqlalchemy.ext.declarative import declarative_base\",\"technology\":\"SQLAlchemy 2.0\"}</arguments></use_mcp_tool>"
 ]
}
]
integration_points:{
 orchestrator:{memory:load_all+save_handoffs,context7:-,perplexity:patterns},
 spec:{memory:load_constraints+save_requirements,context7:-,perplexity:standards},
 design:{memory:load_decisions+save_arch,context7:pattern_docs,perplexity:best_practices},
 python_engineer:{memory:load_conventions+save_impl,context7:API_docs_required,perplexity:error_res},
 refine:{memory:load_quality,context7:-,perplexity:security+perf},
 deploy:{memory:load_history,context7:tool_docs,perplexity:latest}
}
execution_flow:[
 1:load_memories,
 2:decision->{unknown_lib->Context7,best_approach->Perplexity},save_memory,
 3:error->{attempt1->Context7,attempt2->logs,attempt3->Perplexity}
]
compliance_tracking:{mcp_usage:{memory_loaded:timestamp,memories_added:count,context7_queries:count,perplexity_searches:count,violations:[]}}
violations_consequences:[
 start_without_memory->invalid_session,
 no_context7->code_rejected,
 guess_fixes->must_research,
 no_memory_saves->repeat_work,
 skip_deprecation->technical_debt
]
non_negotiable_rules:[
 memory_not_optional,
 doc_over_assumptions,
 research_over_guess,
 save_decisions_immediately,
 strict_categories
]