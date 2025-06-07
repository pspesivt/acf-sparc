## API Contract Standards

### 0. Absolute Mandate
Every service boundary requires formal, versioned API contract. No implementation until contracts STABLE.

### 1. Standard: OpenAPI 3.1
All API contracts MUST use OpenAPI 3.1 in YAML.

### 2. File Structure
```
docs/architecture/api-contracts/
├── _index.md                    # Registry and status
├── v1.0.0/                      # Version directory
│   ├── auth-api.yaml            # Auth service contract
│   ├── user-api.yaml            # User management
│   ├── order-api.yaml           # Order processing
│   └── README.md                # Version changelog
├── v1.1.0/                      # Next version
│   └── ...
└── contract-status.md           # Status tracking
```

### 3. Version Lifecycle
| Status | Meaning | Implementation Allowed |
|--------|---------|------------------------|
| DRAFT | Under development | NO |
| STABLE | Frozen for version | YES |
| DEPRECATED | For removal | Existing only |

### 4. Contract Requirements
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
  schemas: # ALL schemas defined here
  responses: # Standard error responses
  securitySchemes: # Auth mechanisms
```

### 5. Schema Standards
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
        firstName:
          type: string
          minLength: 1
          maxLength: 50
        lastName:
          type: string
          minLength: 1
          maxLength: 50
      additionalProperties: false
```

### 6. Error Standards
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
Breaking Changes = New Version:
- Removing endpoints
- Removing required fields
- Changing field types
- Changing response codes
- Modifying authentication

Non-Breaking (Minor Version):
- Adding optional fields
- Adding new endpoints
- Adding optional query params
- Expanding enums (carefully)

### 8. Security Requirements
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
Python: `openapi-generator generate -i auth-api.yaml -g python-fastapi`
NextJS: `openapi-generator generate -i auth-api.yaml -g typescript-axios`

### 11. Contract Testing
Required:
- Request validation
- Response validation
- Error format compliance
- Status code accuracy

### 12. Change Protocol
1. Create new version dir
2. Copy existing contracts
3. Make modifications
4. Update status to DRAFT
5. Review and test
6. Mark as STABLE
7. Update implementations

### 13. Common Failures
Schema Too Loose:
```yaml
# WRONG
properties:
  data:
    type: object

# RIGHT
properties:
  data:
    $ref: '#/components/schemas/UserData'
```

Missing Error Cases:
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

No Examples:
```yaml
schema:
  type: string
  format: email
  example: "user@example.com"
```

### 14. Enforcement
- No Refinement without STABLE contracts
- Contract changes require version bump
- All implementations MUST pass contract tests
- Contract violations = build failure

### 15. Contract Lifecycle & Sign-off
DRAFT→STABLE via formal review:
1. `design` creates DRAFT contract + REVIEW task
2. `orchestrator` identifies reviewers
3. Specialists provide feedback in review file
4. Format: `[MODE_NAME]: [APPROVAL|REJECTION] - [Rationale]`
5. When complete, `orchestrator` checks consensus
   - All APPROVAL: Update status to STABLE
   - Any REJECTION: Create revision task, DRAFT blocked

Contract is law. Break it = service communication failure.