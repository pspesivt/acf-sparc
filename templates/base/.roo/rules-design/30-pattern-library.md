## Approved Design Patterns

### Architectural Patterns

#### Layered Architecture
Separation of concerns without distributed complexity.
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

Rules:
- Dependencies point downward only
- Domain layer knows nothing about infrastructure
- Each layer testable in isolation
```
Use: CRUD apps, clear business logic, team <10
Don't: Need horizontal scaling, true microservices

#### Hexagonal (Ports & Adapters)
For external integration complexity.
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

Ports: Interfaces defined by core
Adapters: Implementations of ports
```
Use: Multiple external systems, swappable implementations, high test coverage
Don't: Simple CRUD, few integrations, performance critical

### Component Patterns

#### Repository Pattern
Data access abstraction.
```
I:UserRepository
find(id:ID)→User|null
findByEmail(email:string)→User|null
save(user:User)→User
delete(id:ID)→bool
//T:impl_memory,mock_easy,swap_db
```
Never: Let business logic touch database directly

#### Service Layer
Business logic coordination.
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

#### Factory Pattern
Complex object creation.
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

### Integration Patterns

#### Adapter Pattern
For external APIs.
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

#### Circuit Breaker
For external service failures.
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

### Data Patterns

#### Unit of Work
Transaction boundaries.
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

#### DTO Pattern
API exposure control.
```
// Internal domain model
ENTITY User:
    id: UUID
    email: string
    hashedPassword: string
    failedAttempts: integer
    lastLoginIP: string

// What API consumers see
DTO UserResponse:
    id: string
    email: string

MAPPER UserMapper:
    toDTO(user: User) → UserResponse:
        RETURN {
            id: user.id.toString(),
            email: user.email
        }
```

### Anti-Patterns
- God Object: Split 5000-line service classes
- Anemic Domain Model: Add behavior to getter/setter objects
- Spaghetti Integration: Use adapters
- Premature Optimization: Measure before caching
- Framework Coupling: Use hexagonal for business logic

### Pattern Selection Matrix
| Need | Pattern | Complexity |
|------|---------|------------|
| Separate concerns | Layered | Low |
| Swap implementations | Hexagonal | Medium |
| Abstract data access | Repository | Low |
| Complex creation | Factory | Low |
| External API | Adapter | Low |
| Failure handling | Circuit Breaker | Medium |
| Transactions | Unit of Work | High |

### Reality Check
Don't need: Microservices for startups, Event sourcing for blogs, CQRS for CRUD, Blockchain
Need: Clean interfaces, Testable components, Clear boundaries, Boring patterns
Pick simplest pattern that solves actual problem.