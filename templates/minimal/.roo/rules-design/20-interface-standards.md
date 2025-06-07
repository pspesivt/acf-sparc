Interface Definition Standards
Interface Anatomy:I:ComponentName;P:[problem];M:[operations];IN:[types,constraints];OUT:[success|failure];SE:[logs,events,state];INV:[constants]

Method Specification
I:UserRepository:
 findById(userId:UUID)->User|null;PRE:valid_UUID;OK:User(all_fields);FAIL:null;SE:log(query_time);PERF:cache<10ms,DB<100ms)
 findByEmail(email:string)->User|null;PRE:email_RFC5322;OK:User;FAIL:null;SE:none;NOTE:case_insensitive
 create(userData:CreateUserInput)->User|ValidationError;PRE:required_fields;OK:User(with_generated_ID);FAIL:ValidationError(field_errors);SE:publish(UserCreated);CON:email_unique

Input/Output Contracts
TYPE CreateUserInput:{email:string[REQUIRED,RFC5322,max255,lowercase];password:string[REQUIRED,min12,upper+lower+digit+symbol,max128];name:string?[max100,unicode,trim]}
TYPE User:{id:UUID[gen,immutable];email:string[unique,immutable];name:string|null[mutable];createdAt:ISO8601DateTime[UTC,immutable];status:enum[PENDING,ACTIVE,SUSPENDED,DELETED,state_machine]}

Error Specification
PaymentProcessor.chargeCard(amount:Money,cardToken:string)->ChargeResult;Success:[CHARGED,PENDING];Failure:INSUFFICIENT_FUNDS{code:insufficient_funds,retryable:false},CARD_EXPIRED{code:card_expired,retryable:false},NETWORK_ERROR{code:network_error,retryable:true,retryAfter:30},RATE_LIMITED{code:rate_limited,retryable:true,retryAfter:60},INVALID_TOKEN{code:invalid_token,retryable:false}

Async Interface Patterns
ReportGenerator.startReport(params)->{jobId:UUID,estimatedTime:s}(sync);getStatus(jobId)->JobStatus[QUEUED{pos},PROCESSING{progress},COMPLETED{url},FAILED{error},EXPIRED];getResult(jobId)->ReportData|null[24h,paginated]

Event Contracts
Event:OrderPlaced v1 Schema:{orderId:UUID,customerId:UUID,items:[{productId:UUID,quantity:int,price:Money}],total:Money,timestamp:ISO8601DateTime};Guarantees:[at-least-once,customer-partition-order,7d retention];Consumers:[idempotent,out-of-order,tolerate-versions]

Interface Versioning
UserAPI:v1(URL:/v1/,deprecated:2024-03-01,sunset:2024-09-01)->UserV1;v2(URL:/v2/,current)->UserV2{+phoneNumber,-legacyId,name:{firstName,lastName}};Migration:{adapter,dep-warning:headers,guide}

Performance Contracts
SearchService.search(query:string,filters:FilterSet)->SearchResults;Perf:[p50<100ms,p99<500ms,throughput>=1000/s,availability>=99.9%,error<0.1%];Degradation:[>1000/s:backpressure,>10k:paginate,complex:timeout30s]

Integration Testing Boundaries
EmailService.Testing:{mockMode=config,testAddr:*@test.example.com->bypass,sandbox:realSMTP-noDelivery,webhook:POST endpoint};Tests:[validEmail,invalidEmail->error,rateLimiting,templateSub,attachments<size]

Common Interface Failures
1:UserRepository.findById(userId:UUID)->User|null;PRE:valid_UUID;OK:User;FAIL:null;SE:log;PERF:cache<10ms,DB<100ms
3:process(data,{timeout?:number,retries?:number})
4:init enforced in constructor

Contract Checklist:[params:type+constraints,returns,errors,perf,sideEffects,versioning,testing]