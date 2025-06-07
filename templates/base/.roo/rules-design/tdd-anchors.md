## TDD Anchor Standards

Your test anchors are useless. Here's why and how to fix them.

### What TDD Anchors Actually Do

They mark decision points in pseudocode where behavior changes. Not decoration. Not suggestions. Contracts.

```
// TEST: [Specific behavior that must be verified]
```

Every anchor becomes a test. Skip one? Bug in production. Guaranteed.

### Anchor Placement Rules

**Put anchors at**:
1. Every branch (if/else)
2. Every loop boundary
3. Every error condition
4. Every state change
5. Every external call
6. Every business rule

**Your pathetic attempts**:
```
FUNCTION processPayment(amount):
    // TEST: Payment works
    result = chargeCard(amount)
    RETURN result
```

**Actual anchors**:
```
FUNCTION processPayment(amount):
    // TEST: Negative amounts rejected immediately
    IF amount <= 0:
        RETURN Error("Invalid amount")
    
    // TEST: Amounts over $10,000 require approval
    IF amount > 10000:
        // TEST: Approval request logged
        requireApproval(amount)
    
    // TEST: Card charge attempts tracked
    // TEST: Failed charges retry 3 times
    // TEST: Network timeout handled gracefully
    attempts = 0
    WHILE attempts < 3:
        result = chargeCard(amount)
        IF result.success:
            // TEST: Successful payment logs transaction ID
            RETURN Success(result.transactionId)
        attempts++
        // TEST: Exponential backoff between retries
        WAIT(2^attempts seconds)
    
    // TEST: After 3 failures, payment marked pending
    RETURN Pending("Manual review required")
```

### Boundary Condition Anchors

The edges where your code dies:

```
FUNCTION paginate(items, pageSize, pageNumber):
    // TEST: Empty list returns empty page
    // TEST: Page size 0 throws error
    // TEST: Negative page number throws error
    // TEST: Page number beyond last page returns empty
    // TEST: Exactly divisible items fill last page
    // TEST: Remainder items partially fill last page
    
    IF pageSize <= 0:
        THROW Error("Page size must be positive")
    
    startIndex = pageSize * (pageNumber - 1)
    
    // TEST: Start index beyond array returns empty
    IF startIndex >= items.length:
        RETURN []
    
    endIndex = startIndex + pageSize
    // TEST: End index clips to array length
    RETURN items[startIndex:endIndex]
```

### State Machine Anchors

Every transition needs proof:

```
STATE MACHINE OrderStatus:
    // TEST: New orders start as PENDING
    INITIAL = PENDING
    
    TRANSITIONS:
        PENDING → CONFIRMED:
            // TEST: Only with valid payment
            REQUIRES paymentVerified
            // TEST: Inventory must be available
            REQUIRES inventoryReserved
            // TEST: Customer notified on confirmation
            TRIGGERS sendConfirmationEmail
        
        CONFIRMED → SHIPPED:
            // TEST: Tracking number required
            REQUIRES trackingNumber
            // TEST: Cannot ship to invalid address
            VALIDATES shippingAddress
        
        ANY → CANCELLED:
            // TEST: Refund initiated if payment exists
            IF paymentExists:
                TRIGGERS initiateRefund
            // TEST: Inventory released
            TRIGGERS releaseInventory
            // TEST: Cannot cancel shipped orders
            BLOCKS IF status == SHIPPED
```

### Integration Point Anchors

External systems will fail. Plan for it:

```
FUNCTION fetchUserProfile(userId):
    // TEST: Valid user ID returns complete profile
    // TEST: Non-existent user returns null, not error
    // TEST: Malformed user ID throws validation error
    
    TRY:
        // TEST: Network timeout after 5 seconds
        // TEST: 500 response triggers retry
        // TEST: 404 response returns null
        // TEST: 429 response respects retry-after header
        response = httpClient.get("/users/" + userId, timeout: 5)
        
        IF response.status == 404:
            RETURN null
            
        IF response.status != 200:
            THROW Error("Unexpected status: " + response.status)
            
        // TEST: Missing required fields throws parse error
        // TEST: Extra fields ignored gracefully
        RETURN parseUser(response.body)
        
    CATCH NetworkError:
        // TEST: Network errors cached to prevent stampede
        RETURN cachedValue OR null
```

### Performance Anchors

Numbers matter:

```
FUNCTION searchProducts(query, filters):
    // TEST: Empty query returns empty results < 10ms
    // TEST: Single word query returns results < 100ms
    // TEST: Complex query with filters < 500ms
    // TEST: Result set > 1000 items triggers pagination
    
    IF query.isEmpty:
        RETURN []
    
    // TEST: Query normalized (lowercase, trimmed)
    normalizedQuery = normalize(query)
    
    // TEST: Stop words removed for performance
    tokens = removeStopWords(tokenize(normalizedQuery))
    
    // TEST: Maximum 10 tokens processed
    IF tokens.length > 10:
        tokens = tokens[0:10]
    
    results = index.search(tokens, filters)
    
    // TEST: Results ranked by relevance
    // TEST: Sponsored results marked clearly
    RETURN rankResults(results)
```

### Security Anchors

Every input is hostile:

```
FUNCTION updateProfile(userId, updates):
    // TEST: Only owner can update their profile
    // TEST: Admin can update any profile
    // TEST: Sensitive fields require reauthentication
    // TEST: Mass assignment protection enforced
    
    IF currentUser.id != userId AND !currentUser.isAdmin:
        THROW ForbiddenError()
    
    // TEST: Email change requires verification
    IF updates.email != null:
        requireRecentAuth()
        sendVerificationEmail(updates.email)
        updates.emailPending = updates.email
        DELETE updates.email
    
    // TEST: Whitelist allowed fields
    allowedFields = ["name", "bio", "avatar"]
    sanitizedUpdates = pick(updates, allowedFields)
    
    // TEST: HTML stripped from text fields
    // TEST: Image URLs validated
    FOR field IN sanitizedUpdates:
        sanitizedUpdates[field] = sanitize(field, sanitizedUpdates[field])
    
    RETURN updateUser(userId, sanitizedUpdates)
```

### Common Anchor Failures

**1. Decorative Comments**
```
// TEST: Works correctly  ← Meaningless
// TEST: Returns user if email matches  ← Testable
```

**2. Missing Negative Cases**
```
// TEST: Valid input processed  ← What about invalid?
```

**3. Untestable Wishes**
```
// TEST: Should be fast  ← Define fast
// TEST: Good user experience  ← Unmeasurable
```

**4. Implementation Details**
```
// TEST: Uses Redis cache  ← That's how, not what
// TEST: Caches miss populates from database  ← Behavior
```

### The Anchor Density Rule

**Minimum anchors per function**:
- Simple getters: 1-2
- Business logic: 5-10
- Integration points: 10-15
- State machines: 15-20

Too few? Bugs hiding.
Too many? Overengineered.

### Reality Check

Every untested edge case becomes a production incident:
- That null check you skipped? NullPointerException
- That timeout you ignored? Thread pool exhaustion
- That validation you forgot? SQL injection
- That race condition? Data corruption

TDD anchors aren't bureaucracy. They're your defense against the inevitable chaos of production.

Write them like your pager depends on it. Because it does.
