## TDD Anchor Standards

Your test anchors are useless. Here's why and how to fix them.

### What TDD Anchors Actually Do

They mark decision points in pseudocode where behavior changes. Not decoration. Not suggestions. Contracts.

```
//T:[behavior]
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
FN processPayment(amount):
    //T:neg_reject
    IF amount<=0:RETURN Error("Invalid amount")
    
    //T:>10k_needs_approval
    IF amount>10000:
        //T:approval_logged
        requireApproval(amount)
    
    //T:track_attempts
    //T:retry_3_times
    //T:handle_timeout
    attempts = 0
    WHILE attempts < 3:
        result = chargeCard(amount)
        IF result.success:
            //T:log_transaction_id
            RETURN Success(result.transactionId)
        attempts++
        //T:exponential_backoff
        WAIT(2^attempts seconds)
    
    //T:mark_pending_after_failures
    RETURN Pending("Manual review required")
```

### Boundary Condition Anchors

The edges where your code dies:

```
FN paginate(items, pageSize, pageNumber):
    //T:empty_list_empty_result
    //T:zero_page_size_error
    //T:neg_page_error
    //T:beyond_last_page_empty
    //T:exact_division_fill_page
    //T:remainder_partial_fill
    
    IF pageSize <= 0:
        THROW Error("Page size must be positive")
    
    startIndex = pageSize * (pageNumber - 1)
    
    //T:start_beyond_array_empty
    IF startIndex >= items.length:
        RETURN []
    
    endIndex = startIndex + pageSize
    //T:clip_end_to_array_length
    RETURN items[startIndex:endIndex]
```

### State Machine Anchors

Every transition needs proof:

```
STATE MACHINE OrderStatus:
    //T:new_orders_pending
    INITIAL = PENDING
    
    TRANSITIONS:
        PENDING → CONFIRMED:
            //T:requires_valid_payment
            REQUIRES paymentVerified
            //T:requires_inventory
            REQUIRES inventoryReserved
            //T:sends_confirmation_email
            TRIGGERS sendConfirmationEmail
        
        CONFIRMED → SHIPPED:
            //T:requires_tracking
            REQUIRES trackingNumber
            //T:validates_address
            VALIDATES shippingAddress
        
        ANY → CANCELLED:
            //T:refund_if_paid
            IF paymentExists:
                TRIGGERS initiateRefund
            //T:release_inventory
            TRIGGERS releaseInventory
            //T:block_shipped_cancel
            BLOCKS IF status == SHIPPED
```

### Integration Point Anchors

External systems will fail. Plan for it:

```
FUNCTION fetchUserProfile(userId):
    //T:valid_id_returns_profile
    //T:nonexistent_returns_null
    //T:malformed_id_validation_error
    
    TRY:
        //T:timeout_5sec
        //T:500_triggers_retry
        //T:404_returns_null
        //T:429_respects_retry_after
        response = httpClient.get("/users/" + userId, timeout: 5)
        
        IF response.status == 404:
            RETURN null
            
        IF response.status != 200:
            THROW Error("Unexpected status: " + response.status)
            
        //T:missing_fields_error
        //T:extra_fields_ignored
        RETURN parseUser(response.body)
        
    CATCH NetworkError:
        //T:cache_prevents_stampede
        RETURN cachedValue OR null
```

### Performance Anchors

Numbers matter:

```
FUNCTION searchProducts(query, filters):
    //T:empty_query_returns_empty_10ms
    //T:single_word_query_100ms
    //T:complex_query_filters_500ms
    //T:1000plus_items_pagination
    
    IF query.isEmpty:
        RETURN []
    
    //T:query_normalized
    normalizedQuery = normalize(query)
    
    //T:stopwords_removed
    tokens = removeStopWords(tokenize(normalizedQuery))
    
    //T:max_10_tokens
    IF tokens.length > 10:
        tokens = tokens[0:10]
    
    results = index.search(tokens, filters)
    
    //T:ranked_by_relevance
    //T:sponsored_clearly_marked
    RETURN rankResults(results)
```

### Security Anchors

Every input is hostile:

```
FUNCTION updateProfile(userId, updates):
    //T:owner_only_update
    //T:admin_update_any
    //T:sensitive_reauth
    //T:mass_assignment_protection
    
    IF currentUser.id != userId AND !currentUser.isAdmin:
        THROW ForbiddenError()
    
    //T:email_change_verification
    IF updates.email != null:
        requireRecentAuth()
        sendVerificationEmail(updates.email)
        updates.emailPending = updates.email
        DELETE updates.email
    
    //T:whitelist_fields
    allowedFields = ["name", "bio", "avatar"]
    sanitizedUpdates = pick(updates, allowedFields)
    
    //T:strip_html
    //T:validate_image_urls
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
