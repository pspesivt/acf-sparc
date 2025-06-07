## Next.js Deployment Guidelines

### Platform Comparison
Platform:Vercel|Best:Most Next.js projects|Pros:Native support,edge funcs,preview deploys|Cons:High cost;
Platform:Netlify|Best:Simple sites|Pros:Easy setup,form handling|Cons:Less Next.js optimized;
Platform:AWS Amplify|Best:Enterprise AWS shops|Pros:Full AWS integration|Cons:Complex setup;
Platform:Cloudflare Pages|Best:Global static sites|Pros:Free,DDoS protection|Cons:Limited server funcs;
Platform:Docker/K8s|Best:Custom infra|Pros:Complete control|Cons:High maintenance overhead;

### Pre-Deploy Checklist
1.Performance:`npm install -g @lhci/cli && lhci autorun`;min:Perf>=90,Access>=95,BestPract>=95,SEO>=95  
2.Security:`pnpm audit --production`,`npx owasp-dependency-check --project "App" --scan node_modules`;fix:high/crit vulns,exposed env,CSP,insecure deps  
3.Environment:.env.example→DATABASE_URL=postgresql://…,NEXTAUTH_SECRET=…,NEXT_PUBLIC_API_URL=https://api.example.com;rules:never commit secrets,NEXT_PUBLIC_=client,rotate regularly  
4.Bundle Analysis:next.config.js uses `@next/bundle-analyzer` w/ANALYZE=true;targets:firstLoad<150KB,route-split,no large polyfills  

### Deployment Configs
**Vercel**
```json
{ "buildCommand":"pnpm build","installCommand":"pnpm install --frozen-lockfile","regions":["iad1","sfo1"],"headers":[{"source":"/(.*)","headers":[{"key":"X-Frame-Options","value":"DENY"},{"key":"X-Content-Type-Options","value":"nosniff"}]}] }
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
CMD ["node","server.js"]
```

### CI/CD Pipeline
```yaml
name:CI
on:[push,pull_request]
jobs:
  test:
    runs-on:ubuntu-latest
    steps:
      - uses:actions/checkout@v3
      - uses:pnpm/action-setup@v2
      - uses:actions/setup-node@v3 with:{node-version:18,cache:pnpm}
      - run:pnpm install --frozen-lockfile
      - run:pnpm lint&&pnpm test&&pnpm build
  deploy:
    needs:test
    if:github.ref=='refs/heads/main'
    runs-on:ubuntu-latest
    steps:
      - uses:actions/checkout@v3
      - uses:amondnet/vercel-action@v25 with:{vercel-token:${{secrets.VERCEL_TOKEN}},vercel-args:'--prod'}
```

### Monitoring
**Error Tracking**
```tsx
'use client';
import * as Sentry from '@sentry/nextjs';
export default function Error({error,reset}) {
  useEffect(()=>Sentry.captureException(error),[error]);
  return(
    <div className="flex flex-col items-center p-4">
      <h2 className="text-2xl font-bold text-red-600">Something broke!</h2>
      <button onClick={reset} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Try again</button>
    </div>
  );
}
```
Services:Sentry(errors,replay,perf),Datadog(APM,infrastructure),Vercel Analytics(CWV,user journeys)

### Post-Deploy Verification
```js
const endpoints=['/','/api/health','/sitemap.xml'];
async function verify(){
 for(const e of endpoints){
  try{const r=await fetch(`${BASE_URL}${e}`);console.log(`✅ ${e} - ${r.status}`)}
  catch(err){console.error(`❌ ${e} - ${err.message}`);process.exit(1)}
 }
}
```
Manual checks:auth flow,core journeys,forms,search,cross-device

### Progressive Rollout
10%→monitor errors;25%→perf;50%→stability;100%→full  
Rollback triggers:error rate>0.5%,perf-20%,critical path broken  
```bash
vercel rollback --scope=team_name
```

### Reality Check
amateur:push to prod,pray,learn from Twitter,no monitoring,no rollback  
professional:test(perf,security,a11y),monitor(errors,perf,behavior),rollback ready,automate CI/CD,optimize continuously