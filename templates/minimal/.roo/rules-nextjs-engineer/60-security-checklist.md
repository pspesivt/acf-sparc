## Next.js Security Checklist

### Auth & Authorization
Broken Auth|Auth.js+middleware ALL routes,no client-side auth|hit private routes,expired tokens  
Role Bypass|server-side role checks only,never trust JWT claims|access admin routes as user  
Session Hijack|HttpOnly+Secure+SameSite cookies,rotate session IDs|check cookie flags,fixation attacks  

### Injection & Validation
XSS|CSP headers,DOMPurify,no dangerouslySetInnerHTML|OWASP ZAP,XSS payloads  
CSRF|SameSite=Strict,custom headers,origin verification|POST external domain  
SQL Injection|parameterized queries,Prisma/ORM,Zod validation|SQLMap,injection payloads  

### API Security
No Rate Limits|Upstash/Redis rate limits,retry-after headers|hammer endpoints,check bypass methods  
API Keys Exposed|server-side only,proxy external APIs,no NEXT_PUBLIC_ secrets|grep bundle  
IDOR|UUIDs not sequential,verify ownership in queries|access other users' data  
Mass Assignment|explicit field selection,Zod schemas,no raw input|send extra fields,check updates  

### Client Security
Data in localStorage|memory-only for sensitive data,no tokens/PII|check browser storage  
Bad Dependencies|weekly pnpm audit,Snyk in CI,update aggressively|check outdated packages  
Client-Only Validation|duplicate ALL validation server-side|bypass UI via Postman  

### Config & Headers
Missing Headers|X-Frame-Options,CSP,HSTS via middleware|securityheaders.com scan  
Exposed Env Vars|server-side secrets only,limit NEXT_PUBLIC_|grep bundle  
Debug Info Leak|custom error pages,sanitize logs,no stack traces|trigger errors,check responses  

### Secure Implementation
```tsx
export async function GET(request: Request, { params }: { params: { id: string } }) {
  // 1. Auth always first
  const session = await auth();
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });
  // 2. Validate input
  if (!/^[0-9a-f]{24}$/i.test(params.id)) {
    return Response.json({ error: 'Invalid ID' }, { status: 400 });
  }
  // 3. Check ownership
  const resource = await db.resource.findUnique({ where: { id: params.id } });
  if (resource?.ownerId !== session.user.id && session.user.role !== 'ADMIN') {
    return Response.json({ error: 'Forbidden' }, { status: 403 });
  }
  // 4. Return minimal data
  return Response.json({ id: resource.id, name: resource.name });
}
```
```tsx
export default auth((req) => {
  const response = NextResponse.next();
  if (process.env.NODE_ENV === 'production' && req.nextUrl.protocol === 'http:') {
    return NextResponse.redirect(`https://${req.nextUrl.host}${req.nextUrl.pathname}`);
  }
  response.headers.set('X-Frame-Options','DENY');
  response.headers.set('X-Content-Type-Options','nosniff');
  response.headers.set('Referrer-Policy','strict-origin-when-cross-origin');
  response.headers.set('Content-Security-Policy',"default-src 'self';script-src 'self';style-src 'self' 'unsafe-inline';");
  return response;
});
```
```tsx
const schema = z.object({content:z.string().min(1).max(1000)});
export function SecureForm(){
  const onSubmit=async(data:z.infer<typeof schema>)=>{
    const sanitized=DOMPurify.sanitize(data.content);
    await fetch('/api/submit',{method:'POST',headers:{'X-Requested-With':'XMLHttpRequest'},body:JSON.stringify({content:sanitized})});
  };
}
```

### Security Tools
Required: Zod, Auth.js, DOMPurify, pnpm audit  
Testing:
pnpm audit --production  
npx @secretlint/secretlint  
curl -I https://yourapp.com|grep -E "X-Frame|CSP|Strict-Transport"  
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://yourapp.com  

### Pre-Deploy Checklist
Auth protected? every private route/API/server action  
Input validated? Zod schemas on all user input  
Headers set? CSP, X-Frame-Options, HSTS  
Secrets hidden? no API keys in bundles  
Dependencies clean? zero high/critical vulnerabilities