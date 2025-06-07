# Rollback Procedures

When you inevitably break production, here's how to unfuck it.

## Rollback Triggers

| Symptom | Threshold | Action |
|---------|-----------|--------|
| 5xx errors | > 10% for 2 min | Immediate rollback |
| Response time | p95 > 5x baseline | Immediate rollback |
| Memory usage | OOM kills detected | Immediate rollback |
| CPU usage | > 95% for 5 min | Investigate, then rollback |
| Health check | 3 consecutive fails | Automatic rollback |

## Blue-Green Rollback

Your deployment already supports instant rollback:

```bash
#!/bin/bash
# rollback.sh

# Find previous container
PREVIOUS=$(docker ps -a --format "{{.Names}}" | grep -E "^app-" | head -2 | tail -1)

if [ -z "$PREVIOUS" ]; then
  echo "No previous version found"
  exit 1
fi

# Swap nginx upstream
sed -i 's/8000/8001/g' /etc/nginx/sites-available/app
sed -i 's/8001 backup/8000 backup/g' /etc/nginx/sites-available/app
nginx -t && nginx -s reload

# Verify rollback
sleep 2
curl -f http://localhost:8000/health || exit 1

# Stop broken version
docker stop app
docker rm app

echo "Rolled back to $PREVIOUS"
```

## Image-Based Rollback

When blue-green isn't available:

```bash
#!/bin/bash
# rollback-image.sh

# Get previous image
CURRENT=$(docker inspect app --format='{{.Config.Image}}')
PREVIOUS=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep -A1 "$CURRENT" | tail -1)

if [ "$PREVIOUS" == "$CURRENT" ]; then
  echo "No previous image found"
  exit 1
fi

# Deploy previous
docker stop app || true
docker run -d --name app-rollback \
  --restart always \
  -p 127.0.0.1:8000:8000 \
  --env-file /etc/app/production.env \
  $PREVIOUS

# Verify
sleep 5
if curl -f http://localhost:8000/health; then
  docker rm app
  docker rename app-rollback app
  echo "Rolled back to $PREVIOUS"
else
  docker stop app-rollback
  docker rm app-rollback
  echo "Rollback failed!"
  exit 1
fi
```

## Database Rollbacks

The hard truth: **You can't rollback data**.

### Migration Strategy
```python
# alembic/versions/001_add_user_status.py
def upgrade():
    # SAFE: Additive only
    op.add_column('users', 
        sa.Column('status', sa.String(20), nullable=True)
    )

def downgrade():
    # DANGEROUS: Data loss
    op.drop_column('users', 'status')
```

### Safe Migrations
```python
# Two-phase deployment
# Phase 1: Add column (nullable)
def upgrade():
    op.add_column('users', 
        sa.Column('email_new', sa.String(255), nullable=True)
    )

# Phase 2: Migrate data (separate deployment)
def upgrade():
    op.execute("""
        UPDATE users 
        SET email_new = email 
        WHERE email_new IS NULL
    """)
    
# Phase 3: Switch columns (after verification)
def upgrade():
    op.drop_column('users', 'email')
    op.alter_column('users', 'email_new', new_column_name='email')
```

### Emergency DB Restore
```bash
#!/bin/bash
# restore-db.sh

BACKUP=$(ls -t /backups/postgres/*.sql.gz | head -1)

if [ -z "$BACKUP" ]; then
  echo "No backup found"
  exit 1
fi

echo "Restoring from $BACKUP"
echo "DATA WILL BE LOST SINCE $(stat -c %y $BACKUP)"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  exit 1
fi

# Stop app
docker stop app

# Restore
gunzip -c $BACKUP | docker exec -i postgres psql -U postgres dbname

# Restart
docker start app
```

## Verification

```bash
#!/bin/bash
# verify-rollback.sh

CHECKS=(
  "curl -f http://localhost:8000/health"
  "curl -f http://localhost:8000/api/v1/status"
  "docker exec app python -c 'import sys; sys.exit(0)'"
)

FAILED=0
for check in "${CHECKS[@]}"; do
  if eval $check > /dev/null 2>&1; then
    echo "✓ $check"
  else
    echo "✗ $check"
    FAILED=$((FAILED + 1))
  fi
done

if [ $FAILED -gt 0 ]; then
  echo "Rollback verification failed!"
  exit 1
fi

# Check metrics
ERROR_RATE=$(curl -s http://localhost:9090/api/v1/query?query=rate\(http_requests_total{status=~\"5..\"}\[1m\]\) | jq '.data.result[0].value[1]' | tr -d '"')

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "High error rate: $ERROR_RATE"
  exit 1
fi

echo "Rollback successful"
```

## GitHub Actions Rollback

```yaml
# .github/workflows/rollback.yml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        default: 'production'
        type: choice
        options:
          - production
          - staging

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - name: Get previous deployment
        id: previous
        uses: actions/github-script@v7
        with:
          script: |
            const deploys = await github.rest.actions.listWorkflowRuns({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'deploy.yml',
              status: 'success',
              per_page: 2
            });
            const previous = deploys.data.workflow_runs[1];
            core.setOutput('sha', previous.head_sha);
            core.setOutput('run_id', previous.id);
      
      - name: Rollback
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: deploy
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            IMAGE="ghcr.io/${{ github.repository }}:${{ steps.previous.outputs.sha }}"
            docker pull $IMAGE
            /opt/deploy/rollback.sh $IMAGE
```

## Common Failures

**Your Rollback Disasters**:
1. **No previous version**: Deleted old images to "save space"
2. **Database migrations**: Can't undo DELETE FROM users
3. **Config changes**: New version needs new env vars
4. **Shared state**: Redis has incompatible data
5. **No verification**: Rolled back to also-broken version

**Prevention**:
```yaml
# Keep last 5 deployments
docker image prune -a --filter "until=168h" --filter "label!=keep"

# Tag stable versions
docker tag app:$SHA app:stable-$(date +%Y%m%d)

# Backup before deploy
pg_dump dbname | gzip > backup-$(date +%Y%m%d-%H%M%S).sql.gz
```

## Rollback Decision Tree

```
Error detected
├─ Health check failing?
│  └─ Yes: Automatic rollback
│  └─ No: Continue monitoring
├─ User-facing errors?
│  └─ Yes: Immediate rollback
│  └─ No: Can it wait?
│     ├─ Yes: Schedule fix
│     └─ No: Rollback
└─ Data corruption?
   └─ Yes: STOP EVERYTHING
   └─ No: Standard rollback
```

## Post-Rollback

1. **Incident report** (within 24h)
   - Timeline
   - Root cause
   - Impact (users, revenue)
   - Prevention measures

2. **Fix forward**
   - Never re-deploy same broken version
   - Add tests for failure case
   - Add monitoring for failure pattern

3. **Update runbook**
   - Document new failure mode
   - Update rollback procedures
   - Share with team

## The Reality

Rollbacks fail because:
1. **No practice**: First rollback is during outage
2. **Missing pieces**: Old configs deleted
3. **Data corruption**: Can't rollback database
4. **Cascading failures**: Dependencies also need rollback
5. **Panic**: Skipping verification steps

Good rollback strategy:
- **Fast**: < 60 seconds to previous version
- **Verified**: Automated checks confirm success
- **Practiced**: Monthly rollback drills
- **Documented**: Runbook updated continuously

Your deployment isn't complete until rollback is tested.

Most teams learn this during their first major outage. Don't be most teams.
