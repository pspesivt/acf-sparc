## Next.js Security Checklist

Your app is a breach waiting to happen. Fix these before hackers do.

### Auth & Authorization

| Vulnerability | Fix It | Test It |
|--------------|--------|---------|
| **Broken Auth** | Auth.js + middleware on ALL routes. No client-side auth decisions. | Hit private routes directly. Test expired tokens. |
| **Role Bypass** | Server-side role checks only. Never trust JWT claims. | Try accessing admin routes as user. |
| **Session Hijack** | HttpOnly + Secure + SameSite cookies. Rotate session IDs. | Check cookie flags. Test fixation attacks. |

### Injection & Validation

| Vulnerability | Fix It | Test It |
|--------------|--------|---------|
| **XSS** | CSP headers. DOMPurify for user content. No `dangerouslySetInnerHTML`. | Run OWASP ZAP. Test XSS payloads. |
| **CSRF** | SameSite=Strict. Custom headers. Origin verification. | POST from external domain. |
| **SQL Injection** | Parameterized queries only. Prisma/ORM. Zod validation. | SQLMap scan. Test payloads. |

### API Security

| Vulnerability | Fix It | Test It |
|--------------|--------|---------|
| **No Rate Limits** | Upstash/Redis limits. Retry-after headers. | Hammer endpoints. Check bypass methods. |
| **API Keys Exposed** | Server-side only. Proxy external APIs. Never `NEXT_PUBLIC_` secrets. | Search bundle for keys. |
| **IDOR** | UUIDs not sequential IDs. Verify ownership in queries. | Try accessing other users' data. |
| **Mass Assignment** | Explicit field selection. Zod schemas. Never pass raw input. | Send extra fields. Check updates. |

### Client Security

| Vulnerability | Fix It | Test It |
|--------------|--------|---------|
| **Data in localStorage** | Memory-only for sensitive data. Never store tokens/PII. | Check browser storage. |
| **Bad Dependencies** | Weekly `pnpm audit`. Snyk in CI. Update aggressively. | Check outdated packages. |
| **Client-Only Validation** | Duplicate ALL validation server-side. Never trust browser. | Bypass UI with Postman. |

### Config & Headers

| Vulnerability | Fix It | Test It |
|--------------|--------|---------|
| **Missing Headers** | X-Frame-Options, CSP, HSTS. Use middleware. | securityheaders.com scan. |
| **Exposed Env Vars** | `NEXT_PUBLIC_` sparingly. Server-side secrets only. | grep bundle for secrets. |
| **Debug Info Leak** | Custom error pages. Sanitize logs. No stack traces. | Trigger errors. Check responses. |

### Secure Implementation

**API Route Pattern**:
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

**Middleware Security**:
```tsx
export default auth((req) => {
  const response = NextResponse.next();
  
  // Force HTTPS
  if (process.env.NODE_ENV === 'production' && req.nextUrl.protocol === 'http:') {
    return NextResponse.redirect(`https://${req.nextUrl.host}${req.nextUrl.pathname}`);
  }
  
  // Security headers (non-negotiable)
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Content-Security-Policy', 
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
  );
  
  return response;
});
```

**Form Security**:
```tsx
const schema = z.object({
  content: z.string().min(1).max(1000)
});

export function SecureForm() {
  const onSubmit = async (data: z.infer<typeof schema>) => {
    const sanitized = DOMPurify.sanitize(data.content);
    
    await fetch('/api/submit', {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }, // CSRF protection
      body: JSON.stringify({ content: sanitized })
    });
  };
}
```

### Security Tools

**Required**:
- Zod (validation)
- Auth.js (authentication)  
- DOMPurify (sanitization)
- pnpm audit (dependencies)

**Testing**:
```bash
# Dependencies
pnpm audit --production

# Secrets
npx @secretlint/secretlint

# Headers
curl -I https://yourapp.com | grep -E "X-Frame|CSP|Strict-Transport"

# Full scan
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://yourapp.com
```

### Pre-Deploy Checklist

1. **Auth protected?** Every private route, API endpoint, server action
2. **Input validated?** Zod schemas on ALL user input
3. **Headers set?** CSP, X-Frame-Options, HSTS minimum
4. **Secrets hidden?** No API keys in bundles
5. **Dependencies clean?** Zero high/critical vulnerabilities

### The Reality

Most Next.js apps:
- Store auth state client-side (trivial bypass)
- Expose API routes without rate limits (DoS waiting)
- Trust user input (injection paradise)
- Skip security headers (XSS playground)
- Leak env vars in bundles (API keys for everyone)

**Every shortcut becomes an exploit.**

Auth checks client-side? Bypassed in DevTools. No rate limits? Script kiddies crash your API. Trust user input? Enjoy your SQL injection.

Security isn't optional. It's table stakes. Miss one item above and you're not a developer, you're a liability.
