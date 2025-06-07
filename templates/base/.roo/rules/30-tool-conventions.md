## Tool Usage Conventions

### Tool Priority Order
1. **apply_diff** - Default for ALL code modifications
2. **write_to_file** - New files only
3. **insert_content** - Documentation sections  
4. **search_and_replace** - Last resort for simple text

### Required Parameters

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

**Failures**: Incomplete diffs, whitespace mismatch, nested markers, non-existent files

#### write_to_file
```xml
<write_to_file>
  <path>REQUIRED: new/file/path.py</path>
  <content>REQUIRED: Complete file content</content>
  <line_count>REQUIRED: Integer matching actual lines</line_count>
</write_to_file>
```

**Failures**: Missing/wrong line_count, overwriting files, empty content

#### insert_content
```xml
<insert_content>
  <path>REQUIRED: existing/file.md</path>
  <operations>
    [{"start_line": REQUIRED_INTEGER, "content": "REQUIRED_STRING"}]
  </operations>
</insert_content>
```

**Failures**: Invalid JSON, start_line beyond file length, missing fields, non-existent file

#### search_and_replace
```xml
<search_and_replace>
  <path>REQUIRED: file/path.py</path>
  <operations>
    [{"search": "REQUIRED_TEXT", "replace": "REQUIRED_TEXT", "use_regex": false}]
  </operations>
</search_and_replace>
```

**Failures**: Empty search, malformed regex, text not found

### File Operation Sequences

#### Modifying Existing Files
1. read_file - Verify content
2. apply_diff - Make changes
3. read_file - Verify changes

#### Creating New Files
1. list_files - Verify file doesn't exist
2. write_to_file - Create content
3. read_file - Verify creation

#### Adding to Documentation
1. read_file - Get structure
2. insert_content - Add at line
3. read_file - Verify insertion

### Error Prevention Checklist
- File exists? (read_file first)
- Exact text match? (copy-paste)
- All parameters included?
- JSON valid?
- Line counts accurate?
- Diff markers balanced?

### Performance Impact
| Tool | Speed | Risk | Use When |
|------|-------|------|----------|
| apply_diff | Fast | Medium | Precise edits |
| write_to_file | Fast | High | File new |
| insert_content | Medium | Low | Known location |
| search_and_replace | Slow | High | Simple text |

### Line Count Validation
- line_count > 300: Blocked
- line_count approaching 300: Warning
- line_count mismatch: Re-count