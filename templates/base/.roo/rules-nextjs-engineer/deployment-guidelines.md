## Next.js Deployment Guidelines

Your app is useless if nobody can access it.

### Platform Comparison

| Platform | Best For | Key Trade-offs |
|----------|----------|----------------|
| **Vercel** | Most Next.js projects | Native support, edge functions, preview deploys. Higher cost at scale. |
| **Netlify** | Simple sites | Easy setup, form handling. Less Next.js optimized. |
| **AWS Amplify** | Enterprise AWS shops | Full AWS integration. Complex setup. |
| **Cloudflare Pages** | Global static sites | Free tier, DDoS protection. Limited server functions. |
| **Docker/K8s** | Custom infrastructure | Complete control. High maintenance overhead. |

### Pre-Deploy Checklist

**1. Performance**
```bash
npm install -g @lhci/cli && lhci autorun
```
Minimum: Performance 90+, Accessibility 95+, Best Practices 95+, SEO 95+

**2. Security**
```bash
pnpm audit --production
npx owasp-dependency-check --project "App" --scan node_modules
```
Fix: High/critical vulns, exposed env vars, missing CSP, insecure deps

**3. Environment**
```env
# .env.example (template only)
DATABASE_URL=postgresql://...
NEXTAUTH_SECRET=your-secret-here
NEXT_PUBLIC_API_URL=https://api.example.com
```
Rules: Never commit secrets, `NEXT_PUBLIC_` for client-side only, rotate regularly

**4. Bundle Analysis**
```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
```
Targets: First Load < 150KB, route-based splitting, no large polyfills

### Deployment Configs

**Vercel**
```json
{
  "buildCommand": "pnpm build",
  "installCommand": "pnpm install --frozen-lockfile",
  "regions": ["iad1", "sfo1"],
  "headers": [{
    "source": "/(.*)",
    "headers": [
      {"key": "X-Frame-Options", "value": "DENY"},
      {"key": "X-Content-Type-Options", "value": "nosniff"}
    ]
  }]
}
```

**Docker**
```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### CI/CD Pipeline

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v3
        with: {node-version: 18, cache: pnpm}
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint && pnpm test && pnpm build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-args: '--prod'
```

### Monitoring

**Error Tracking**
```tsx
// app/error.tsx
'use client';
import * as Sentry from '@sentry/nextjs';

export default function Error({ error, reset }) {
  useEffect(() => Sentry.captureException(error), [error]);
  
  return (
    <div className="flex flex-col items-center p-4">
      <h2 className="text-2xl font-bold text-red-600">Something broke!</h2>
      <button onClick={reset} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">
        Try again
      </button>
    </div>
  );
}
```

**Service Options**
- **Sentry**: Errors + replay + performance
- **Datadog**: Full APM + infrastructure
- **Vercel Analytics**: Core Web Vitals + user journeys

### Post-Deploy Verification

```js
// scripts/verify-deployment.js
const endpoints = ['/', '/api/health', '/sitemap.xml'];

async function verify() {
  for (const endpoint of endpoints) {
    try {
      const res = await fetch(`${BASE_URL}${endpoint}`);
      console.log(`✅ ${endpoint} - ${res.status}`);
    } catch (err) {
      console.error(`❌ ${endpoint} - ${err.message}`);
      process.exit(1);
    }
  }
}
```

**Manual Checks**: Auth flow, core journeys, forms, search, cross-device

### Progressive Rollout

1. **10% traffic** → monitor errors
2. **25%** → check performance
3. **50%** → verify stability
4. **100%** → full deployment

Rollback triggers: Error rate >0.5%, performance -20%, critical path broken

```bash
# Instant rollback
vercel rollback --scope=team_name
```

### Reality Check

Amateur deployment:
- Push to prod, pray it works
- Learn about failures from Twitter
- No monitoring, no rollback plan

Professional deployment:
1. **Test first** (performance, security, a11y)
2. **Monitor always** (errors, perf, behavior)
3. **Rollback ready** (immediate recovery)
4. **Automate everything** (CI/CD mandatory)
5. **Optimize continuously** (regular reviews)

Perfect code means nothing if users can't access it. Deploy with the same rigor you code.
