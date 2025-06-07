## TDD Anchor Standards

### What TDD Anchors Actually Do
mark decision points as contracts  
//T:[behavior] //→test;skip=bug

### Anchor Placement Rules
anchors@branch(if/else),loop boundary,error condition,state change,external call,business rule

FN processPayment(amount):
 //T:neg_reject
 IF amount<=0:RET Err("Invalid amount")
 //T:>10k_needs_approval
 IF amount>10000:
  //T:approval_logged
  requireApproval(amount)
 //T:track_attempts //T:retry_3_times //T:handle_timeout
 attempts=0
 WHILE attempts<3:
  result=chargeCard(amount)
  IF result.success:
   //T:log_transaction_id
   RET Success(result.transactionId)
  attempts++
  //T:exponential_backoff
  WAIT(2^attempts s)
 //T:mark_pending_after_failures
 RET Pending("Manual review required")

### Boundary Condition Anchors
FN paginate(items,pageSize,pageNumber):
 //T:empty_list_empty_result //T:zero_page_size_error //T:neg_page_error //T:beyond_last_page_empty //T:exact_division_fill_page //T:remainder_partial_fill
 IF pageSize<=0:THROW Err("Page size must be positive")
 startIndex=pageSize*(pageNumber-1)
 //T:start_beyond_array_empty
 IF startIndex>=items.length:RET []
 endIndex=startIndex+pageSize
 //T:clip_end_to_array_length
 RET items[startIndex:endIndex]

### State Machine Anchors
STATE MACHINE OrderStatus:
 //T:new_orders_pending
 INITIAL=PENDING
 TRANSITIONS:
  PENDING→CONFIRMED:
   //T:requires_valid_payment
   REQUIRES paymentVerified
   //T:requires_inventory
   REQUIRES inventoryReserved
   //T:sends_confirmation_email
   TRIGGERS sendConfirmationEmail
  CONFIRMED→SHIPPED:
   //T:requires_tracking
   REQUIRES trackingNumber
   //T:validates_address
   VALIDATES shippingAddress
  ANY→CANCELLED:
   //T:refund_if_paid
   IF paymentExists:TRIGGERS initiateRefund
   //T:release_inventory
   TRIGGERS releaseInventory
   //T:block_shipped_cancel
   BLOCKS IF status==SHIPPED

### Integration Point Anchors
FN fetchUserProfile(userId):
 //T:valid_id_returns_profile //T:nonexistent_returns_null //T:malformed_id_validation_error
 TRY:
  //T:timeout_5sec //T:500_triggers_retry //T:404_returns_null //T:429_respects_retry_after
  response=httpClient.get("/users/"+userId,timeout:5)
  IF response.status==404:RET null
  IF response.status!=200:THROW Err("Unexpected status:"+response.status)
  //T:missing_fields_error //T:extra_fields_ignored
  RET parseUser(response.body)
 CATCH NetworkError:
  //T:cache_prevents_stampede
  RET cachedValue||null

### Performance Anchors
FN searchProducts(query,filters):
 //T:empty_query_returns_empty_10ms //T:single_word_query_100ms //T:complex_query_filters_500ms //T:1000plus_items_pagination
 IF query.isEmpty:RET []
 normalizedQuery=normalize(query) //T:query_normalized
 tokens=removeStopWords(tokenize(normalizedQuery)) //T:stopwords_removed
 IF tokens.length>10:tokens=tokens[0:10] //T:max_10_tokens
 results=index.search(tokens,filters)
 //T:ranked_by_relevance //T:sponsored_clearly_marked
 RET rankResults(results)

### Security Anchors
FN updateProfile(userId,updates):
 //T:owner_only_update //T:admin_update_any //T:sensitive_reauth //T:mass_assignment_protection
 IF currentUser.id!=userId&&!currentUser.isAdmin:THROW ForbiddenError()
 //T:email_change_verification
 IF updates.email!=null:
  requireRecentAuth();sendVerificationEmail(updates.email);updates.emailPending=updates.email;DELETE updates.email
 //T:whitelist_fields
 allowedFields=["name","bio","avatar"]
 sanitizedUpdates=pick(updates,allowedFields)
 //T:strip_html //T:validate_image_urls
 FOR field IN sanitizedUpdates:
  sanitizedUpdates[field]=sanitize(field,sanitizedUpdates[field])
 RET updateUser(userId,sanitizedUpdates)

### Common Anchor Failures
// TEST:Works←meaningless // TEST:Returns user if email matches←testable  
// TEST:Valid input processed←missing negative  
// TEST:Should be fast|Good user experience←untestable  
// TEST:Uses Redis cache←impl detail // TEST:Caches miss populates from database←behavior

### The Anchor Density Rule
AnchorDensity:SimpleGetters=1-2,BusinessLogic=5-10,Integration=10-15,StateMachine=15-20

### Reality Check
UncaughtEdges:NullPointer,Timeout/threadPoolExhaustion,SQLInjection,DataCorruption