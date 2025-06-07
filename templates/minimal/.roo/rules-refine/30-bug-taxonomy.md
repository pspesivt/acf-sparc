BugClassificationSystem:
 PrimaryClassificationHierarchy:
  BUG:
   LOGIC_ERRORS:[Incorrect Computation,Wrong Conditional,State Corruption,Race Condition]
   INTEGRATION_FAILURES:[API Contract Violation,Data Format Mismatch,Protocol Error,Timeout Handling]
   RESOURCE_ISSUES:[Memory Leak,Handle Leak,Connection Pool Exhaustion,Unbounded Growth]
   SECURITY_VULNERABILITIES:[Injection,Authentication Bypass,Authorization Failure,Data Exposure]
   RELIABILITY_DEFECTS:[Crash,Hang,Data Loss,Corruption]
 SeverityClassification:
  CRITICAL:{criteria:[Data loss,Security breach,Service failure,Financial computation errors],examples:["Payment processor charges wrong amounts","Authentication bypass allows any password","Database corruption on concurrent writes"],sla:4h}
  HIGH:{criteria:[Feature broken,Perf degraded>10x,Exploitable vulnerability,Data accuracy compromised],examples:["Search returns empty for valid queries","API timeout after 30 seconds","XSS in user comments"],sla:24h}
  MEDIUM:{criteria:[Partial break,Perf degraded2-10x,Workaround available,Noncritical data issues],examples:["Pagination skips records","Slow query on large datasets","Error messages expose stack traces"],sla:1w}
  LOW:{criteria:[Cosmetic,Minor perf,Edge case only,Doc mismatch],examples:["Tooltip shows wrong format","Unnecessary database call","Typo in error message"],sla:convenient}
 BugPatterns:
  LogicErrors:
   Off-by-one:{loc:[loops,array access,pagination],causes:[bounds confusion,index base error,forgot len-1],example:"for i in range(len(items)+1):  # BOOM on items[i]"}
   NullHandling:{loc:[API responses,DB queries,optional configs],causes:[missing null check,assume present,null vs empty],example:"user.profile.settings.theme  # profile might be None"}
  StateCorruption:
   ConcurrentModification:{loc:[shared state,cache updates,session data],causes:[missing locks,nonatomic RMW,stale overwrite],example:"balance=get();#another thread;set(balance-amt)"}
  ResourceLeaks:
   ConnectionLeak:{loc:[database,HTTP clients,file handles],causes:[no finally/close,exception skip,cycle refs],example:"conn=db.connect();res=conn.query();#exc;conn.close()"}
 DetectionPatterns:
  StaticAnalysis:
   python:"#complexity bombs def f(...):#500lines;Cyclo73"
   missingErrorHandling:"data=external_api.fetch();no try"
   typeConfusion:"sum(item.price) if price str"
  RuntimeIndicators:
   memory_leak:{sym:"RSS+100MB/h",pattern:"objs not freed",detection:"import tracemalloc"}
   race_condition:{sym:"intermittent test failures",pattern:"timing",detection:"thread sanitizer"}
   performance_cliff:{sym:"fast until 1000 items",pattern:"n²",detection:"profile inc N"}
 ClassificationDecisionTree:"if dataCorrupted→CRITICAL;else if featureBroken→HIGH;elif noWorkaround→MEDIUM;else→LOW"
 BugRelationshipMapping:
  root:LOGIC-20240115-001,causes:[INTEG-20240115-023,PERF-20240115-045]
  symptom_cluster:"Login failures",bugs:[SEC-20240115-002,LOGIC-20240115-007,RES-20240115-001]
 FalsePositivePatterns:
  -{pattern:"Slow on my machine",reason:"Local environment issue"}
  -{pattern:"Works differently than I expected",reason:"Requirement misunderstanding"}
  -{pattern:"Could be optimized",reason:"Enhancement, not bug"}
  -{pattern:"Old library version",reason:"Technical debt if works"}
 ReproductionRequirements:
  MinimalReproduction:|
   """
   def test_reproduction():
       order=Order()
       order.add_item(price=100,quantity=2)
       order.add_discount(percent=10)
       order.add_discount(amount=15)
       assert order.total==165  # FAILS actual=150
   """
 ImpactScoring:|
  def calculate_bug_priority(bug):
      s={"CRITICAL":1000,"HIGH":100,"MEDIUM":10,"LOW":1}[bug.severity]
      p=s*bug.affected_users/total_users*bug.occurrences_per_day
      return{"priority_score":p,"fix_order":"IMMEDIATE" if p>100 else "QUEUED"}
 Reality:{ratios:{logic:40,integration:30,resource:20,security:10},note:"Most critical bugs are medium;most bugs are feature requests"}

.roo/rules-refine/performance-metrics.md:
 CoreMetrics:
  latency:{def:"req→resp",percentiles:[p50,p95,p99,p99.9],breakdown:[RTT,queue,proc,IO,serialization]}
  throughput:{def:"ops/time",metrics:[rps,txps,Bps],constraints:[saturation_point,bottleneck_resource]}
  resource_utilization:{def:"%capacity",targets:{cpu:"<70/90",memory:"<80",disk_io:"<60",network:"<50"}}
 MeasurementPoints:
  ApplicationLevel:
   wrong:"print(f'Time: {end-start}')"
   right:"Histogram('http_request_duration_seconds',['method','endpoint','status']).time(handle_request)"
  DatabaseLevel:|
   EXPLAIN(ANALYZE,BUFFERS) SELECT u.*,o.* FROM users u JOIN orders o ON u.id=o.user_id WHERE u.created_at>'2024-01-01';
   --ExecTime,PlanTime,BufferHits,BufferMisses,RowsFiltered
  SystemLevel:
   cpu:"perf record -F 99 -p $(pgrep python) -- sleep 30; perf report"
   memory:"tracemalloc+memory_profiler;valgrind --tool=massif"
   io:"iotop -o -P -a; iostat -x 1"
   network:"ss -i; tcpdump -i eth0 -w capture.pcap"
 MetricCollectionPatterns:
  pull:{pros:[service_discovery,no_loss],cons:[need_endpoint,poll_interval]}
  push:{pros:[fire_and_forget,fw-friendly],cons:[metric_loss,no_standard]}
 SamplingStrategies:|
  def should_sample(req):
      if req.status>=400:return True
      if random()<.1:return True
      if req.duration>1:return True
      return False
 LoadTestingProfiles:
  steady_state:{duration:3600,users:1000,ramp_up:300,scenario:[{endpoint:/api/users,GET,weight:70},{endpoint:/api/orders,POST,weight:30}]}
  stress_test:{stages:[{dur:300,users:100},{dur:600,users:1000},{dur:600,users:5000},{dur:300,users:100}],success:{err_rate:"<1%",p95:"<500ms"}}
  spike_test:{baseline:100,spike:10000,duration:60,recovery:"<120s"}
 AnalysisPatterns:
  LatencyBreakdown:|
   @trace_execution
   def api_endpoint(req):
       with trace_span("validation"):...
       with trace_span("database"):...
       with trace_span("business_logic"):...
       with trace_span("serialization"):...
  ThroughputAnalysis:"util=arrival_rate/(concurrency/latency);if util>0.8:SATURATED"
 BottleneckIdentification:
  CPU:{symptoms:[cpu_100,low_io_wait,linear_scaling],profiling:[flame_graphs,high_user_cpu],solutions:[optimize_algo,parallel,cache]}
  IO:{symptoms:[high_io_wait,low_cpu,device_sat],profiling:[strace,high_sys_cpu],solutions:[async_io,batching,indexing,pooling]}
  Memory:{symptoms:[high_mem,swap,GC_pressure],profiling:[heap_dumps,alloc_profiler],solutions:[object_pool,streaming,mem_efficient_DS]}
 PerformanceBudgets:
  page_load:{total:3000,breakdown:[dns:50,tcp:100,tls:150,server:200,download:500,parsing:200,render:800,js:1000]}
  api_endpoint:{total:200,breakdown:[parse:5,authn:10,authz:5,logic:50,db:100,serialization:10,network:20]}
 AlertingThresholds:
  -{name:"High Latency",cond:"p95>500ms for5m",sev:warning}
  -{name:"Very High Latency",cond:"p95>1000ms for2m",sev:critical}
  -{name:"Error Rate",cond:"5xx>1% for3m",sev:critical}
  -{name:"Saturation",cond:"cpu>90% for10m",sev:warning}
 CommonMeasurementFailures:
  vanity_metrics:[TotalRequests,avg_latency,uptime]
  real_metrics:[rps@p99<200ms,error_rate_by_type,TTFB]
  bad_instrumentation:"measure measurement"
  good_instrumentation:"time=op;record(time)"
 TheTruth:[Measure everything,Find actual bottleneck,Fix biggest,Measure again]