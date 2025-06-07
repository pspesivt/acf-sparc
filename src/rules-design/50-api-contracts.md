## API Contract Standards

### 0. Absolute Mandate
Every service boundary requires a formal, versioned API contract. No exceptions. No implementation begins until contracts are STABLE.

### 1. Standard: OpenAPI 3.1
All API contracts MUST use OpenAPI 3.1 specification in YAML format.

### 2. File Structure
```
docs/architecture/api-contracts/
├── _index.md                    # Contract registry and status
├── v1.0.0/                      # Version directory
│   ├── auth-api.yaml            # Authentication service contract
│   ├── user-api.yaml            # User management contract
│   ├── order-api.yaml           # Order processing contract
│   └── README.md                # Version changelog
├── v1.1.0/                      # Next version
│   └── ...
└── contract-status.md           # DRAFT/STABLE status tracking
```

### 3. Version Lifecycle

| Status | Meaning | Implementation Allowed |
|--------|---------|------------------------|
| DRAFT | Contract under development | NO |
| STABLE | Contract frozen for version | YES |
| DEPRECATED | Marked for removal | Existing only |

### 4. Contract Requirements

**Mandatory Elements**:
```yaml
openapi: 3.1.0
info:
  title: Service Name API
  version: 1.0.0
  description: Clear service purpose
  contact:
    name: API Support
    email: api@example.com
servers:
  - url: https://api.example.com/v1
    description: Production
paths:
  /endpoint:
    post:
      operationId: uniqueOperationId
      summary: Brief description
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RequestModel'
      responses:
        '200':
          description: Success response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseModel'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'
components:
  schemas:
    # ALL request/response schemas defined here
  responses:
    # Standard error responses
  securitySchemes:
    # Auth mechanisms
```

### 5. Schema Standards

**Strict Typing Required**:
```yaml
components:
  schemas:
    UserCreateRequest:
      type: object
      required:
        - email
        - password
        - firstName
        - lastName
      properties:
        email:
          type: string
          format: email
          maxLength: 255
          description: User's email address
        password:
          type: string
          format: password
          minLength: 8
          maxLength: 128
          description: User's password
        firstName:
          type: string
          minLength: 1
          maxLength: 50
        lastName:
          type: string
          minLength: 1
          maxLength: 50
      additionalProperties: false  # No extra fields allowed
```

### 6. Error Standards

**Consistent Error Format**:
```yaml
components:
  schemas:
    ErrorResponse:
      type: object
      required:
        - error
        - message
        - timestamp
        - traceId
      properties:
        error:
          type: string
          enum:
            - VALIDATION_ERROR
            - AUTHENTICATION_ERROR
            - AUTHORIZATION_ERROR
            - NOT_FOUND
            - CONFLICT
            - INTERNAL_ERROR
        message:
          type: string
          description: Human-readable error message
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
        timestamp:
          type: string
          format: date-time
        traceId:
          type: string
          format: uuid
```

### 7. Versioning Rules

**Breaking Changes = New Version**:
- Removing endpoints
- Removing required fields
- Changing field types
- Changing response codes
- Modifying authentication

**Non-Breaking (Minor Version)**:
- Adding optional fields
- Adding new endpoints
- Adding new optional query params
- Expanding enums (carefully)

### 8. Security Requirements

**Every Endpoint Must Declare**:
```yaml
security:
  - bearerAuth: []
  - apiKey: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

### 9. Documentation Standards

**Every Element Needs Description**:
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      description: |
        Retrieves detailed user information by user ID.
        Requires authentication and appropriate permissions.
      parameters:
        - name: id
          in: path
          required: true
          description: Unique user identifier
          schema:
            type: string
            format: uuid
            example: "123e4567-e89b-12d3-a456-426614174000"
```

### 10. Implementation Sync

**Python Engineer**: Uses contract to generate Pydantic models
```bash
# Auto-generated from OpenAPI contract
openapi-generator generate -i auth-api.yaml -g python-fastapi
```

**NextJS Engineer**: Uses contract to generate TypeScript types
```bash
# Auto-generated from OpenAPI contract
openapi-generator generate -i auth-api.yaml -g typescript-axios
```

### 11. Contract Testing

**Contract Tests Required**:
- Request validation against schema
- Response validation against schema
- Error format compliance
- Status code accuracy

### 12. Change Protocol

1. Create new version directory
2. Copy existing contracts
3. Make modifications
4. Update status to DRAFT
5. Review and test
6. Mark as STABLE
7. Update implementations

### 13. Common Failures

**Schema Too Loose**:
```yaml
# WRONG
properties:
  data:
    type: object  # What's in it???

# RIGHT
properties:
  data:
    $ref: '#/components/schemas/UserData'
```

**Missing Error Cases**:
```yaml
# WRONG
responses:
  '200':
    description: Success

# RIGHT
responses:
  '200':
    description: Success
  '400':
    $ref: '#/components/responses/BadRequest'
  '401':
    $ref: '#/components/responses/Unauthorized'
  '403':
    $ref: '#/components/responses/Forbidden'
  '404':
    $ref: '#/components/responses/NotFound'
  '500':
    $ref: '#/components/responses/InternalError'
```

**No Examples**:
```yaml
# Add examples everywhere
schema:
  type: string
  format: email
  example: "user@example.com"
```

### 14. Enforcement

- No Refinement phase begins without STABLE contracts
- Contract changes require version bump
- All implementations MUST pass contract tests
- Contract violations = build failure

### 15. Contract Lifecycle & Sign-off

A contract is promoted from `DRAFT` to `STABLE` via a formal, asynchronous review brokered by the `orchestrator`.

**Review Protocol**:
1.  The `design` mode generates the `DRAFT` contract (e.g., `v1.0.0/auth-api.yaml`) and a corresponding `CONTRACT-REVIEW-AUTH-V1.yaml` task in `docs/backlog/`.
2.  The `orchestrator` reads this task and identifies the contract's producer and consumer specialists from the task description.
3.  The `orchestrator` delegates review sub-tasks to each specialist. The deliverable is not code, but written feedback.
4.  Each specialist provides feedback by **appending** to a shared review file: `docs/architecture/api-contracts/v1.0.0/auth-api-review.md`.
5.  The feedback format is non-negotiable: `[MODE_NAME]: [APPROVAL|REJECTION] - [Concise Rationale]`.
6.  After a specialist provides feedback, it marks its sub-task complete.
7.  Upon completion of all review sub-tasks, the `orchestrator` is triggered. It reads the review file to determine consensus.
    *   **If all specialists log `APPROVAL`**: The `orchestrator` updates the main `docs/architecture/api-contracts/contract-status.md` file, changing the contract version's status to `STABLE`.
    *   **If any specialist logs `REJECTION`**: The `orchestrator` creates a new task for the `design` mode, providing the compiled feedback and requiring a revised contract version. The DRAFT contract remains blocked.

The contract is the law. Break it and watch your services fail to communicate.