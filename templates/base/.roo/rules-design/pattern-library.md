## Approved Design Patterns

Stop reinventing wheels. Use these patterns or justify why not.

### Architectural Patterns

#### Layered Architecture
When you need separation of concerns without distributed system complexity.

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

**Use When**: Most CRUD applications, clear business logic, team under 10 people

**Don't Use When**: Need horizontal scaling per component, true microservices required

#### Hexagonal (Ports & Adapters)
When external integrations dominate your complexity.

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

**Use When**: Multiple external systems, need to swap implementations, high test coverage required

**Don't Use When**: Simple CRUD, few integrations, performance critical

### Component Patterns

#### Repository Pattern
Abstraction over data access. Always.

```
INTERFACE UserRepository:
    find(id: ID) → User | null
    findByEmail(email: string) → User | null
    save(user: User) → User
    delete(id: ID) → boolean

// TEST: Implementation can be in-memory
// TEST: Easy to mock for unit tests
// TEST: Swap databases without touching business logic
```

**Never**: Let business logic touch database directly

#### Service Layer
Business logic coordination without fat controllers.

```
SERVICE OrderService:
    DEPENDS ON:
        - OrderRepository
        - PaymentService
        - NotificationService
    
    placeOrder(items, paymentMethod):
        // TEST: Orchestrates multiple operations
        order = Order.create(items)
        payment = PaymentService.charge(paymentMethod, order.total)
        IF payment.failed:
            RETURN Error("Payment failed")
        
        OrderRepository.save(order)
        NotificationService.sendConfirmation(order)
        RETURN order
```

#### Factory Pattern
Complex object creation without constructor hell.

```
FACTORY UserFactory:
    createCustomer(data) → Customer:
        // TEST: Default values applied
        // TEST: Validation during creation
        user = Customer()
        user.role = "CUSTOMER"
        user.credits = 0
        user.email = validateEmail(data.email)
        RETURN user
    
    createAdmin(data) → Admin:
        // TEST: Different rules for admin
        user = Admin()
        user.role = "ADMIN"
        user.permissions = ALL_PERMISSIONS
        RETURN user
```

### Integration Patterns

#### Adapter Pattern
When external APIs suck (they always do).

```
INTERFACE PaymentProcessor:
    charge(amount, token) → Result

ADAPTER StripeAdapter IMPLEMENTS PaymentProcessor:
    charge(amount, token):
        // TEST: Transforms our domain to their API
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
When external services inevitably fail.

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
Transaction boundaries that don't leak.

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
        // TEST: All or nothing
        BEGIN TRANSACTION
        FOR change IN changes:
            change.execute()
        COMMIT TRANSACTION
        changes.clear()
```

#### DTO Pattern
Stop exposing your guts.

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
    // No password hash
    // No security details

MAPPER UserMapper:
    toDTO(user: User) → UserResponse:
        RETURN {
            id: user.id.toString(),
            email: user.email
        }
```

### Anti-Patterns to Avoid

**God Object**: That 5000-line service class? Split it.

**Anemic Domain Model**: Objects with only getters/setters? Add behavior.

**Spaghetti Integration**: Direct API calls everywhere? Use adapters.

**Premature Optimization**: Caching before measuring? Stop.

**Framework Coupling**: Business logic importing web framework? Hexagon time.

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

### The Reality Check

You don't need:
- Microservices for your startup
- Event sourcing for your blog
- CQRS for your CRUD app
- Blockchain for anything

You do need:
- Clean interfaces
- Testable components
- Clear boundaries
- Boring patterns that work

Pick the simplest pattern that solves your actual problem. Not the one that impresses at conferences.
