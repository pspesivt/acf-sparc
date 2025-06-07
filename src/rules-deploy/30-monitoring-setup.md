# Monitoring Setup

Stop flying blind. Here's minimal viable observability.

## Stack

- **Prometheus**: Metrics collection
- **Grafana**: Visualization  
- **Alertmanager**: Wake you up
- **Node Exporter**: System metrics
- **Loki**: Logs (optional)

## Prometheus

### Config
```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - 'alerts.yml'

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_timeout: 5s

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']
```

### Critical Alerts
```yaml
# /etc/prometheus/alerts.yml
groups:
  - name: critical
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: page
        annotations:
          summary: "{{ $labels.job }} down"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[2m]) > 0.05
        for: 2m
        labels:
          severity: page
        annotations:
          summary: "5xx errors > 5%"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p95 latency > 1s"

      - alert: DiskFull
        expr: node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes < 0.1
        for: 5m
        labels:
          severity: page
        annotations:
          summary: "Disk < 10% free"

      - alert: OOMKill
        expr: increase(node_vmstat_oom_kill[5m]) > 0
        labels:
          severity: page
        annotations:
          summary: "OOM killer triggered"
```

## Application Metrics

### FastAPI Integration
```python
# src/monitoring.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
import time

# Core metrics
request_count = Counter(
    'http_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'http_requests_active',
    'Active requests'
)

# Middleware
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    active_requests.inc()
    
    try:
        response = await call_next(request)
        return response
    finally:
        duration = time.time() - start
        active_requests.dec()
        
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

# Metrics endpoint
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Business Metrics
```python
# Track what matters
user_signups = Counter('user_signups_total', 'User registrations')
order_value = Histogram('order_value_dollars', 'Order amounts')
payment_failures = Counter('payment_failures_total', 'Failed payments', ['reason'])
```

## Grafana Dashboards

### Essential Dashboard
```json
{
  "title": "Service Health",
  "panels": [
    {
      "title": "Request Rate",
      "targets": [{
        "expr": "rate(http_requests_total[5m])"
      }]
    },
    {
      "title": "Error Rate",
      "targets": [{
        "expr": "rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])"
      }]
    },
    {
      "title": "p95 Latency",
      "targets": [{
        "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
      }]
    },
    {
      "title": "Active Connections",
      "targets": [{
        "expr": "http_requests_active"
      }]
    }
  ]
}
```

## Alertmanager

### Config
```yaml
# /etc/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'
  routes:
    - match:
        severity: page
      receiver: pagerduty
      
receivers:
  - name: 'default'
    slack_configs:
      - api_url: '$SLACK_WEBHOOK'
        channel: '#alerts'
        
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '$PAGERDUTY_KEY'
```

## Docker Compose

```yaml
# monitoring/docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=changeme
      - GF_INSTALL_PLUGINS=redis-datasource
    ports:
      - "3000:3000"

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

  node_exporter:
    image: prom/node-exporter:latest
    network_mode: host
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro

volumes:
  prometheus_data:
  grafana_data:
```

## Quick Setup

```bash
#!/bin/bash
# setup-monitoring.sh

# Start stack
docker-compose -f monitoring/docker-compose.yml up -d

# Wait for Grafana
until curl -s http://localhost:3000/api/health; do sleep 1; done

# Add Prometheus datasource
curl -X POST http://admin:changeme@localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "access": "proxy",
    "isDefault": true
  }'

# Import dashboard
curl -X POST http://admin:changeme@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboard.json
```

## SLO Tracking

```yaml
# Key metrics to track
slos:
  availability:
    target: 99.9%
    query: avg_over_time(up[30d])
    
  latency:
    target: 95% < 200ms
    query: |
      histogram_quantile(0.95,
        rate(http_request_duration_seconds_bucket[30d])
      ) < 0.2
      
  error_rate:
    target: < 0.1%
    query: |
      rate(http_requests_total{status=~"5.."}[30d]) / 
      rate(http_requests_total[30d]) < 0.001
```

## Debugging Queries

```promql
# High CPU process
topk(5, rate(process_cpu_seconds_total[5m]))

# Memory leaks
rate(process_resident_memory_bytes[1h])

# Slow queries
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{endpoint="/api/search"}[5m]))

# Error patterns
sum by (endpoint, status) (rate(http_requests_total{status=~"5.."}[5m]))
```

## The Reality

Most monitoring fails because:
1. **Too many metrics**: Collecting everything, watching nothing
2. **Alert fatigue**: Every hiccup pages someone
3. **No SLOs**: Alerting on arbitrary thresholds
4. **Dashboard porn**: Pretty graphs, zero actionability

Good monitoring:
- **Four golden signals**: Latency, Traffic, Errors, Saturation
- **Business metrics**: Revenue impacting events
- **Actionable alerts**: Only page for user-facing issues
- **Simple dashboards**: Answer "is it broken?" in 5 seconds

Complexity kills. Start simple. Add only what you'll act on.
