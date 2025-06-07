## Approved Design Patterns
### Architectural Patterns
#### Layered Architecture
desc:separation of concerns w/o distributed complexity
```
┌─────────────────────┐
│ Presentation Layer  │ ← UI logic only
├─────────────────────┤
│ Application Layer   │ ← Use cases, orchestration
├─────────────────────┤
│   Domain Layer      │ ← Business rules, entities
├─────────────────────┤
│ Infrastructure      │ ← Database, external APIs
└─────────────────────┘
```
rules:dependencies↓only;domain↛infrastructure;layers testable in isolation
UseWhen:CRUD;clear business logic;team<10
DontUseWhen:need horizontal scaling;true microservices

#### Hexagonal (Ports & Adapters)
desc:external integrations dominate complexity
```
         ┌─────────┐
         │   UI    │
         └────┬────┘
              │
    ┌─────────▼─────────┐
    │                   │
────► Core Business     ◄────
    │ Logic (Hexagon)   │
────►                   ◄────
    └───────────────────┘
              │
         ┌────▼────┐
         │Database │
         └─────────┘
```
Ports:interfaces defined by core;Adapters:implement ports
UseWhen:multiple external systems;swap implementations;high test coverage
DontUseWhen:simple CRUD;few integrations;performance critical

### Component Patterns
#### Repository Pattern
desc:abstraction over data access
```
I:UserRepository
find(id:ID)→User|null
findByEmail(email:string)→User|null
save(user:User)→User
delete(id:ID)→bool
//T:impl_memory,mock_easy,swap_db
```
never:business logic touch database directly

#### Service Layer
```
SERVICE OrderService:
    DEPENDS ON:
        - OrderRepository
        - PaymentService
        - NotificationService
    
    placeOrder(items, paymentMethod):
        //T:orchestrates_operations
        order = Order.create(items)
        payment = PaymentService.charge(paymentMethod, order.total)
        IF payment.failed:
            RETURN Error("Payment failed")
        
        OrderRepository.save(order)
        NotificationService.sendConfirmation(order)
        RETURN order
```
desc:coordinate business logic w/o fat controllers

#### Factory Pattern
```
FACTORY UserFactory:
    createCustomer(data) → Customer:
        //T:default_values
        //T:validation_during_creation
        user = Customer()
        user.role = "CUSTOMER"
        user.credits = 0
        user.email = validateEmail(data.email)
        RETURN user
    
    createAdmin(data) → Admin:
        //T:admin_rules
        user = Admin()
        user.role = "ADMIN"
        user.permissions = ALL_PERMISSIONS
        RETURN user
```
desc:complex object creation without constructor overload

### Integration Patterns
#### Adapter Pattern
```
INTERFACE PaymentProcessor:
    charge(amount, token) → Result

ADAPTER StripeAdapter IMPLEMENTS PaymentProcessor:
    charge(amount, token):
        //T:transform_domain_to_api
        response = stripe.charges.create({
            amount: amount * 100,  // They want cents
            currency: "usd",
            source: token
        })
        
        IF response.status == "succeeded":
            RETURN Success(response.id)
        ELSE:
            RETURN Failure(response.error.message)
```
desc:wrap external API idiosyncrasies

#### Circuit Breaker
```
COMPONENT CircuitBreaker:
    state: CLOSED | OPEN | HALF_OPEN
    failureCount: 0
    lastFailureTime: null
    
    call(operation):
        IF state == OPEN:
            IF currentTime - lastFailureTime > timeout:
                state = HALF_OPEN
            ELSE:
                RETURN Error("Circuit open")
        
        TRY:
            result = operation()
            IF state == HALF_OPEN:
                state = CLOSED
                failureCount = 0
            RETURN result
        CATCH:
            failureCount++
            lastFailureTime = currentTime
            IF failureCount >= threshold:
                state = OPEN
            THROW
```
desc:handle external service failures

### Data Patterns
#### Unit of Work
```
COMPONENT UnitOfWork:
    repositories: Map<Type, Repository>
    changes: List<Change>
    
    registerNew(entity):
        changes.add(Insert(entity))
    
    registerDirty(entity):
        changes.add(Update(entity))
    
    registerDeleted(entity):
        changes.add(Delete(entity))
    
    commit():
        //T:all_or_nothing
        BEGIN TRANSACTION
        FOR change IN changes:
            change.execute()
        COMMIT TRANSACTION
        changes.clear()
```
desc:manage transaction boundaries

#### DTO Pattern
```
ENTITY User:
    id: UUID
    email: string
    hashedPassword: string
    failedAttempts: integer
    lastLoginIP: string

DTO UserResponse:
    id: string
    email: string
    // No password hash
    // No security details

MAPPER UserMapper:
    toDTO(user: User) → UserResponse:
        RETURN {
            id: user.id.toString(),
            email: user.email
        }
```
desc:expose safe data slices

### Anti-Patterns to Avoid
GodObject;AnemicDomainModel;SpaghettiIntegration;PrematureOptimization;FrameworkCoupling

### Pattern Selection Matrix
SeparateConcerns:Layered:Low;SwapImplementations:Hexagonal:Medium;AbstractDataAccess:Repository:Low;ComplexCreation:Factory:Low;ExternalAPI:Adapter:Low;FailureHandling:CircuitBreaker:Medium;Transactions:UnitOfWork:High

### The Reality Check
DontNeed:Microservices;EventSourcing;CQRS;Blockchain
DoNeed:CleanInterfaces;TestableComponents;ClearBoundaries;BoringPatterns