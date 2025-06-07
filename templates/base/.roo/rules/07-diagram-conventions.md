## Diagram Conventions

All diagrams use mermaid with forest theme. No exceptions.

### Required Header
```
%%{init: {'theme':'forest'}}%%
```

### C4 Architecture Levels

**Level 1 - System Context**:
```mermaid
%%{init: {'theme':'forest'}}%%
C4Context
    title System Context Diagram
    Person(user, "User", "Description")
    System(system, "System", "Description")
    System_Ext(external, "External", "Description")
    Rel(user, system, "Uses")
```

**Level 2 - Container**:
```mermaid
%%{init: {'theme':'forest'}}%%
C4Container
    Container(id, "Name", "Technology", "Description")
    ContainerDb(id, "Name", "Technology", "Description")
    Container_Ext(id, "Name", "Technology", "Description")
```

**Level 3 - Component**:
```mermaid
%%{init: {'theme':'forest'}}%%
C4Component
    Component(id, "Name", "Technology", "Description")
    ComponentDb(id, "Name", "Technology", "Description")
    Component_Ext(id, "Name", "Technology", "Description")
```

### Other Diagram Types

**Flow Diagrams**:
```mermaid
%%{init: {'theme':'forest'}}%%
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Other Action]
```

**Sequence Diagrams**:
```mermaid
%%{init: {'theme':'forest'}}%%
sequenceDiagram
    participant U as User
    participant S as System
    U->>S: Request
    S-->>U: Response
```

Any other mermaid supported diagram types.

### Anti-Patterns
- No theme specified (defaults look amateur)
- Mixing diagram styles (pick one notation)
- Box-and-arrow soup (use C4 hierarchy)
- Wall of text in boxes (concise labels only)
