S:Artifact_Compression_Protocol
S:Compression_Framework compress(input)->output:pres_exact{global_headers,titles,paths,protocols,names,identifiers,values,code} pres_semantic{structure,hierarchy,logic,relationships,content} remove{formatting,redundancy,filler,fluff,verbosity,human_markup,meta_commentary} apply{merge_similar,compact_syntax,implicit_structure} effort=ultrathink constraint=lossless_technical output_format=direct_start_no_preamble forbidden{introduction,commentary,evaluation,transition_text,acknowledgment} special_rule=preserve_first_line_if_title_or_header return=compressed_content_only_no_surrounding_text
S:Scope machine_artifacts={specs,pseudocode,interfaces,architecture_docs,test_scenarios,issue_backlogs,handoff_contexts} human_artifacts={README,usr_doc,API_doc,code_comments,err_msgs,git_commits}
S:Compression_Rules structure_markers{hdr→S:,bold→,list→','} templates{G:W:T:} labels{Priority→P:,Category→C:,Status→S:} implicit{Requirements_list→flat_kv}
S:Mode_Specific_Compression modes{spec:{FR-###:Title→ID:Title,SHALL,WHEN,creds,rate_limit(x/min)} pseudocode:{FUNCTION→FN,//TEST→//T:,IF_!cond:RETURN,IS_EMPTY→!} interface:{Interface→I:,Precondition→PRE:,Success→OK:,Failure→FAIL:}}
S:Compression_Patterns KV{Severity→SEV:} Hier{>→'/'} Cond{IF cond THEN action→cond→action} Rel{Requires→R:,Blocks→B:}
S:Token_Savings Req{1247→374(70%)} Intf{892→312(65%)} Issues{3451→863(75%)}
S:Implementation handoff:from=orchestrator,to=spec,phase=spec,status=ready,deliv=docs/specs/reqs.md:spec:complete,decisions=FastAPI,PostgreSQL,blockers=auth_undefined,next=define_auth,rate_limits
S:Validation parse_det,expand_lossless,semantic_pres,tool_support
S:Enforcement checks{size/content,compliance,sem_pres};violations{verbose→reject,resubmit,track}
S:The_Reality wasted{10_specs:10000,50_handoffs:5000,100_issues:25000},impact{slows,cost↑,context↓,delays},note{machine→dense}