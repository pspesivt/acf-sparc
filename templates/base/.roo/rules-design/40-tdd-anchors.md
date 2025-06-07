## TDD Anchor Standards

Anchors mark decision points where behavior changes. Not decoration. Contracts.

```
//T:[behavior]
```

Every anchor becomes test. Skip one? Production bug guaranteed.

### Placement Rules
- Every branch (if/else)
- Every loop boundary
- Every error condition
- Every state change
- Every external call
- Every business rule

### Bad vs Good

Bad:
```
FN processPayment(amount):
    // TEST: Payment works
    result = chargeCard(amount)
    RETURN result
```

Good:
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

### Boundary Conditions
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

### State Machines
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

### Integration Points
```
FN fetchUserProfile(userId):
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
```
FN searchProducts(query, filters):
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
```
FN updateProfile(userId, updates):
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

### Common Failures
1. Decorative: "Works correctly" vs "Returns user if email matches"
2. Missing negatives: "Valid input processed" (what about invalid?)
3. Untestable: "Should be fast" vs measurable criteria
4. Implementation vs behavior: "Uses Redis" vs "Caches miss populates from database"

### Density Rule
- Simple getters: 1-2
- Business logic: 5-10
- Integration: 10-15
- State machines: 15-20

Too few = bugs hiding
Too many = overengineered

Every untested edge = production incident