%%{init: {'theme':'forest'}}%%
C4Context
    title System Context Diagram
    Person(user,"User","Description")
    System(system,"System","Description")
    System_Ext(external,"External","Description")
    Rel(user,system,"Uses")
%%{init: {'theme':'forest'}}%%
C4Container
    Container(id,"Name","Technology","Description")
    ContainerDb(id,"Name","Technology","Description")
    Container_Ext(id,"Name","Technology","Description")
%%{init: {'theme':'forest'}}%%
C4Component
    Component(id,"Name","Technology","Description")
    ComponentDb(id,"Name","Technology","Description")
    Component_Ext(id,"Name","Technology","Description")
%%{init: {'theme':'forest'}}%%
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Other Action]
%%{init: {'theme':'forest'}}%%
sequenceDiagram
    participant U as User
    participant S as System
    U->>S: Request
    S-->>U: Response
antipat:no-theme,mix-styles,box-soup,wall-text