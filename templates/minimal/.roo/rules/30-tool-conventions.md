## Tool Usage Conventions
Tool hierarchy enforced; wrong tool=reject.

### Tool Priority Order
1 apply_diff(default code mods),2 write_to_file(new files),3 insert_content(docs),4 search_and_replace(simple text)

### Required Parameters
Missing⇒fail

apply_diff
<apply_diff>
  <path>…</path>
  <diff>
    <<<<<<< SEARCH
    …exact text…
    =======
    …replacement…
    >>>>>>> REPLACE
  </diff>
</apply_diff>
Common failures: incomplete diff,nested markers,whitespace mismatch,target absent

write_to_file
<write_to_file>
  <path>…</path>
  <content>…</content>
  <line_count>…</line_count>
</write_to_file>
Common failures: missing/wrong line_count,overwrite,empty content

insert_content
<insert_content>
  <path>…</path>
  <operations>[{"start_line":…, "content":"…"}]
</insert_content>
Common failures: invalid JSON,start_line OOB,missing fields,file absent

search_and_replace
<search_and_replace>
  <path>…</path>
  <operations>[{"search":"…","replace":"…","use_regex":false}]
</search_and_replace>
Common failures: empty search,malformed regex,target absent

### File Operation Sequences
Modifying: read_file→apply_diff→read_file  
Creating: list_files→write_to_file→read_file  
Docs: read_file→insert_content→read_file

### Error Prevention Checklist
File exists? Exact match? All params? JSON valid? Line counts ok? Diff markers balanced?

### Tool Anti-Patterns
DON’T:
<apply_diff>…blind diff example…</apply_diff>
DO:
<read_file>…</read_file>
<apply_diff>…exact match…</apply_diff>

### Performance Impact
apply_diff: fast/med risk/precise  
write_to_file: fast/high risk/new only  
insert_content: med/low risk  
search_and_replace: slow/high risk/simple

### Enforcement
Violations⇒rejected  
orchestrator:
tool_usage:
  apply_diff_count:0
  write_to_file_count:0
  failed_attempts:0
  wrong_tool_selections:0

### Line Count Validation
write_to_file/apply_diff require line_count  
Rules: >300→block; ≈300→warn; mismatch→recount  
On limit: stop→split→new file→update index

### The Reality
Always read_file, copy exact, verify post-change; no guesses.