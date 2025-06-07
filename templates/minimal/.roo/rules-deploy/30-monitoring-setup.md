Stack:[Prometheus,Grafana,Alertmanager,NodeExporter,Loki]
Prometheus:
  cfg:
    global:{scrape_interval:15s,evaluation_interval:15s}
    alerting:{alertmanagers:[{static_configs:[{targets:[localhost:9093]}]}]}
    rule_files:[alerts.yml]
    scrape_configs:[
      {job_name:app,static_configs:[{targets:[localhost:8000]}],metrics_path:/metrics,scrape_timeout:5s},
      {job_name:node,static_configs:[{targets:[localhost:9100]}]},
      {job_name:postgres,static_configs:[{targets:[localhost:9187]}]}
    ]
  alerts:
    groups:[
      {name:critical,interval:30s,rules:[
        {alert:ServiceDown,expr:up==0,for:1m,labels:{severity:page},annotations:{summary:"{{ $labels.job }} down"}},
        {alert:HighErrorRate,expr:rate(http_requests_total{status=~\"5..\"}[2m])>0.05,for:2m,labels:{severity:page},annotations:{summary:\"5xx errors>5%\"}},
        {alert:HighLatency,expr:histogram_quantile(0.95,rate(http_request_duration_seconds_bucket[5m]))>1,for:5m,labels:{severity:warning},annotations:{summary:\"p95 latency>1s\"}},
        {alert:DiskFull,expr:node_filesystem_avail_bytes{mountpoint:\"/\"}/node_filesystem_size_bytes<0.1,for:5m,labels:{severity:page},annotations:{summary:\"Disk<10% free\"}},
        {alert:OOMKill,expr:increase(node_vmstat_oom_kill[5m])>0,labels:{severity:page},annotations:{summary:\"OOM killer triggered\"}}
      ]}
    ]
AppMetrics:
  FastAPI:middleware+endpoint
  Business:{counters:[user_signups_total,payment_failures_total],histograms:[order_value_dollars]}
Grafana:
  dashboard:{title:Service Health,panels:[
    {title:Request Rate,expr:rate(http_requests_total[5m])},
    {title:Error Rate,expr:rate(http_requests_total{status=~'5..'}[5m])/rate(http_requests_total[5m])},
    {title:p95 Latency,expr:histogram_quantile(0.95,rate(http_request_duration_seconds_bucket[5m]))},
    {title:Active Connections,expr:http_requests_active}
  ]}
Alertmanager:
  cfg:
    global:{resolve_timeout:5m}
    route:{group_by:[alertname,severity],group_wait:10s,group_interval:10s,repeat_interval:1h,receiver:default,routes:[{match:{severity:page},receiver:pagerduty}]}
    receivers:[
      {name:default,slack_configs:[{api_url:$SLACK_WEBHOOK,channel:\#alerts}]},
      {name:pagerduty,pagerduty_configs:[{service_key:$PAGERDUTY_KEY}]}
    ]
DockerCompose:
  services:{
    prometheus:{image:prom/prometheus:latest,volumes:[./prometheus.yml:/etc/prometheus/prometheus.yml,./alerts.yml:/etc/prometheus/alerts.yml,prometheus_data:/prometheus],command:[--config.file=/etc/prometheus/prometheus.yml,--storage.tsdb.retention.time=30d],ports:[9090:9090]},
    grafana:{image:grafana/grafana:latest,volumes:[grafana_data:/var/lib/grafana],environment:[GF_SECURITY_ADMIN_PASSWORD=changeme,GF_INSTALL_PLUGINS=redis-datasource],ports:[3000:3000]},
    alertmanager:{image:prom/alertmanager:latest,volumes:[./alertmanager.yml:/etc/alertmanager/alertmanager.yml],ports:[9093:9093]},
    node_exporter:{image:prom/node-exporter:latest,network_mode:host,pid:host,volumes:[/proc:/host/proc:ro,/sys:/host/sys:ro,/:/rootfs:ro]}
  }
  volumes:[prometheus_data,grafana_data]
QuickSetup:"docker-compose -f monitoring/docker-compose.yml up -d;until curl -s http://localhost:3000/api/health;do sleep 1;done;curl -XPOST http://admin:changeme@localhost:3000/api/datasources -HContent-Type:application/json -d{\"name\":\"Prometheus\",\"type\":\"prometheus\",\"url\":\"http://prometheus:9090\",\"access\":\"proxy\",\"isDefault\":true};curl -XPOST http://admin:changeme@localhost:3000/api/dashboards/db -HContent-Type:application/json -d @dashboard.json"
SLOs:{availability:{target:99.9%,query:avg_over_time(up[30d])},latency:{target:95%<200ms,query:histogram_quantile(0.95,rate(http_request_duration_seconds_bucket[30d]))<0.2},error_rate:{target:<0.1%,query:rate(http_requests_total{status=~\"5..\"}[30d])/rate(http_requests_total[30d])<0.001}}
DebugQueries:[topk(5,rate(process_cpu_seconds_total[5m])),rate(process_resident_memory_bytes[1h]),histogram_quantile(0.99,rate(http_request_duration_seconds_bucket{endpoint=\"/api/search\"}[5m])),sum by(endpoint,status)(rate(http_requests_total{status=~\"5..\"}[5m]))]