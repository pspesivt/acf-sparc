## Tool Usage Conventions

Wrong tool usage kills productivity. Here's the hierarchy. Follow it.

### Tool Priority Order

1. **apply_diff** - Default for ALL code modifications
2. **write_to_file** - New files only
3. **insert_content** - Documentation sections  
4. **search_and_replace** - Last resort for simple text

Using the wrong tool? Your work gets rejected. No exceptions.

### Required Parameters

Missing parameters = failed execution. Stop wasting time.

#### apply_diff
```xml
<apply_diff>
  <path>REQUIRED: exact/file/path.py</path>
  <diff>
    <<<<<<< SEARCH
    REQUIRED: Exact text to find (whitespace matters)
    =======
    REQUIRED: Complete replacement text
    >>>>>>> REPLACE
  </diff>
</apply_diff>
```

**Common Failures**:
- Incomplete diff blocks
- Whitespace mismatch in SEARCH
- Nested diff markers
- Attempting on non-existent files

#### write_to_file
```xml
<write_to_file>
  <path>REQUIRED: new/file/path.py</path>
  <content>REQUIRED: Complete file content</content>
  <line_count>REQUIRED: Integer matching actual lines</line_count>
</write_to_file>
```

**Common Failures**:
- Missing line_count
- Wrong line_count
- Overwriting existing files
- Empty content

#### insert_content
```xml
<insert_content>
  <path>REQUIRED: existing/file.md</path>
  <operations>
    [{"start_line": REQUIRED_INTEGER, "content": "REQUIRED_STRING"}]
  </operations>
</insert_content>
```

**Common Failures**:
- Invalid JSON in operations
- start_line beyond file length
- Missing required fields
- Non-existent file

#### search_and_replace
```xml
<search_and_replace>
  <path>REQUIRED: file/path.py</path>
  <operations>
    [{"search": "REQUIRED_TEXT", "replace": "REQUIRED_TEXT", "use_regex": false}]
  </operations>
</search_and_replace>
```

**Common Failures**:
- Empty search parameter
- Malformed regex when use_regex: true
- Text not found in file

### File Operation Sequences

Do these in order or fail:

#### Modifying Existing Files
1. **read_file** - Verify content exists
2. **apply_diff** - Make targeted changes
3. **read_file** - Verify changes applied

Skip step 1? Your diff fails on mismatch.
Skip step 3? You ship broken code.

#### Creating New Files
1. **list_files** - Verify file doesn't exist
2. **write_to_file** - Create with complete content
3. **read_file** - Verify creation succeeded

Overwrite existing file? Data loss. Your fault.

#### Adding to Documentation
1. **read_file** - Get current structure
2. **insert_content** - Add at specific line
3. **read_file** - Verify insertion

Wrong line number? Content lands in wrong place.

### Error Prevention Checklist

Before EVERY tool call:

- [ ] File exists? (read_file first)
- [ ] Exact text match? (copy-paste from read_file)
- [ ] All parameters included? (check schema)
- [ ] JSON valid? (operations arrays)
- [ ] Line counts accurate? (count newlines)
- [ ] Diff markers balanced? (SEARCH/REPLACE pairs)

### Tool Anti-Patterns

**DON'T**:
```xml
<!-- WRONG: Attempting blind diff -->
<apply_diff>
  <path>src/main.py</path>
  <diff>
    <<<<<<< SEARCH
    def process():  <!-- Guessing at content -->
    =======
    def process_data():
    >>>>>>> REPLACE
  </diff>
</apply_diff>
```

**DO**:
```xml
<!-- RIGHT: Verify first -->
<read_file>
  <path>src/main.py</path>
</read_file>
<!-- Then exact match from output -->
<apply_diff>
  <path>src/main.py</path>
  <diff>
    <<<<<<< SEARCH
    def process():  <!-- Copied exactly from read_file -->
    =======
    def process_data():
    >>>>>>> REPLACE
  </diff>
</apply_diff>
```

### Performance Impact

| Tool | Speed | Risk | Use When |
|------|-------|------|----------|
| apply_diff | Fast | Medium | Precise edits needed |
| write_to_file | Fast | High | File guaranteed new |
| insert_content | Medium | Low | Adding to known location |
| search_and_replace | Slow | High | Simple text, multiple occurrences |

### Enforcement

**Violations and Consequences**:
- Use search_and_replace for code: **Rejected, redo with apply_diff**
- Skip read_file verification: **Diff failures, wasted time**
- Wrong parameter types: **Immediate failure, no recovery**
- Overwrite without checking: **Data loss, your responsibility**

**Orchestrator Tracks**:
```yaml
tool_usage:
  apply_diff_count: 0
  write_to_file_count: 0
  failed_attempts: 0
  wrong_tool_selections: 0
```

High failure rate? You're not reading documentation.
Wrong tool selections? You're not following conventions.

### The Reality

Tools are simple. Parameters are documented. Yet most failures come from:
1. Laziness - not reading file first
2. Assumptions - guessing at content
3. Rushing - skipping verification

This isn't complex. Read first. Match exactly. Verify after. 

Professionals don't guess. Amateurs debug tool failures for hours.

Choose wisely.
