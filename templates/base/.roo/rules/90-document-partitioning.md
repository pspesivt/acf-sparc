## Document Partitioning Protocol

Max Lines: 300 (hard limit)

### Splitting Algorithm
1. Stop at 300 lines
2. Split at last semantic boundary:
   - MD: Level 1/2 header
   - Code: function/class start
   - YAML: top-level key
3. Split before boundary
4. Create new file with increment suffix
5. Add cross-references
6. Update _index.md

### Naming
```
docs/{phase}/{type}/{component}-{subcomponent}-{sequence}.md
```

### Required Splits
- Specifications: by feature/module
- Design: by component
- Architecture: by layer/service

### Cross-Reference Index
Each split needs _index.md with links to all parts

### Split Triggers
- 250 lines: Plan splits
- 280 lines: Warning
- 300 lines: STOP, split required

### Mode Responsibilities
- Generating: Monitor count, split at boundaries, create index
- Consuming: Check index, load all docs, maintain context

### Anti-Patterns
- No monolithic files
- Use proper boundaries
- Include cross-references
- Split at logical points

### Rationale
Large docs fail: context windows choke, modes timeout, navigation issues, git diff problems, blocks parallel work