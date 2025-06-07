## API Contract Standards
### 0. Absolute Mandate
services.boundaries:require(versioned API_contract);implAllowed if status==STABLE
### 1. Standard: OpenAPI 3.1
contracts:OpenAPI3.1+YAML
### 2. File Structure
```text
docs/architecture/api-contracts/
├── _index.md
├── v1.0.0/
│   ├── auth-api.yaml
│   ├── user-api.yaml
│   ├── order-api.yaml
│   └── README.md
├── v1.1.0/
└── contract-status.md
```
### 3. Version Lifecycle
statuses:
  DRAFT:impl=false
  STABLE:impl=true
  DEPRECATED:existingOnly
### 4. Contract Requirements
```yaml
openapi:3.1.0
info:
  title:Service Name API
  version:1.0.0
  description:Clear service purpose
  contact:{name:API Support,email:api@example.com}
servers:
  - url:https://api.example.com/v1,description:Production
paths:
  /endpoint:
    post:
      operationId:uniqueOperationId
      summary:Brief description
      requestBody:
        required:true
        content:
          application/json:
            schema:{$ref:'#/components/schemas/RequestModel'}
      responses:
        '200':{description:Success response,content:{application/json:{schema:{$ref:'#/components/schemas/ResponseModel'}}}}
        '400':{$ref:'#/components/responses/BadRequest'}
        '401':{$ref:'#/components/responses/Unauthorized'}
        '500':{$ref:'#/components/responses/InternalError'}
components:
  schemas:{}
  responses:{}
  securitySchemes:{}
```
### 5. Schema Standards
```yaml
components:
  schemas:
    UserCreateRequest:
      type:object
      required:[email,password,firstName,lastName]
      properties:
        email:{type:string,format:email,maxLength:255,description:"User's email address"}
        password:{type:string,format:password,minLength:8,maxLength:128,description:"User's password"}
        firstName:{type:string,minLength:1,maxLength:50}
        lastName:{type:string,minLength:1,maxLength:50}
      additionalProperties:false
```
### 6. Error Standards
```yaml
components:
  schemas:
    ErrorResponse:
      type:object
      required:[error,message,timestamp,traceId]
      properties:
        error:{type:string,enum:[VALIDATION_ERROR,AUTHENTICATION_ERROR,AUTHORIZATION_ERROR,NOT_FOUND,CONFLICT,INTERNAL_ERROR]}
        message:{type:string,description:"Human-readable error message"}
        details:{type:array,items:{type:object,properties:{field:{type:string},message:{type:string}}}}
        timestamp:{type:string,format:date-time}
        traceId:{type:string,format:uuid}
```
### 7. Versioning Rules
breakingChanges:[remove_endpoints,remove_required_fields,change_field_types,change_response_codes,modify_auth]→new_version  
nonBreaking:[add_optional_fields,new_endpoints,new_optional_query_params,expand_enums]→minor_version
### 8. Security Requirements
```yaml
security:
  - bearerAuth:[]
  - apiKey:[]
components:
  securitySchemes:
    bearerAuth:{type:http,scheme:bearer,bearerFormat:JWT}
    apiKey:{type:apiKey,in:header,name:X-API-Key}
```
### 9. Documentation Standards
```yaml
paths:
  /users/{id}:
    get:
      summary:Get user by ID
      description:|"Retrieves detailed user information by user ID.\nRequires authentication and appropriate permissions."
      parameters:
        - name:id,in:path,required:true,description:"Unique user identifier",schema:{type:string,format:uuid,example:"123e4567-e89b-12d3-a456-426614174000"}
```
### 10. Implementation Sync
- openapi-generator generate -i auth-api.yaml -g python-fastapi
- openapi-generator generate -i auth-api.yaml -g typescript-axios
### 11. Contract Testing
tests:[request_validation,response_validation,error_format_compliance,status_code_accuracy]
### 12. Change Protocol
steps:[1:create_new_version_dir,2:copy_contracts,3:modify,4:set_status=DRAFT,5:review_and_test,6:mark_STABLE,7:update_impl]
### 13. Common Failures
```yaml
# WRONG
properties:
  data:
    type:object
# RIGHT
properties:
  data:
    $ref:'#/components/schemas/UserData'
```
```yaml
# WRONG
responses:
  '200':description:Success
# RIGHT
responses:
  '200':description:Success
  '400':{$ref:'#/components/responses/BadRequest'}
  '401':{$ref:'#/components/responses/Unauthorized'}
  '403':{$ref:'#/components/responses/Forbidden'}
  '404':{$ref:'#/components/responses/NotFound'}
  '500':{$ref:'#/components/responses/InternalError'}
```
```yaml
schema:{type:string,format:email,example:"user@example.com"}
```
### 14. Enforcement
- no_refinement_without_STABLE
- contract_change→version_bump
- impl_must_pass_contract_tests
- violation→build_failure
### 15. Contract Lifecycle & Sign-off
review_protocol:
  - design:generate_DRAFT+create_task(CONTRACT-REVIEW-*.yaml)
  - orchestrator:assign_specialists,delegate_review
  - specialist:append_to_review_file(docs/.../auth-api-review.md) format="[MODE]:[APPROVAL|REJECTION]-Rationale";mark_subtask_complete
  - orchestrator:if(all_APPROVAL)->update(contract-status.md,status=STABLE) else->create_design_task(with_feedback),DRAFT_blocked