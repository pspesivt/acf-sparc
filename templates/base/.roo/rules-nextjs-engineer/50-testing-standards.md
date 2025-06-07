## Next.js Testing Standards

Untested code = production crashes.

### Testing Stack
| Type | Tool | Why |
|------|------|-----|
| Unit/Component | Jest+RTL | DOM testing, not implementation |
| API Routes | Jest+Supertest | HTTP mocking |
| E2E | Playwright | Cross-browser, robust |
| Mocking | MSW | Intercept requests properly |

### Coverage Requirements
| Type | Min | Reality |
|------|-----|---------|
| Utils | 100% | No excuse |
| Hooks | 95% | State logic critical |
| Components | 90% | UI breaks visibly |
| API/Actions | 85% | Backend failures hurt |

### Jest Config
```js
// jest.config.js
const nextJest = require('next/jest');
const createJestConfig = nextJest({dir:'./'});
module.exports = createJestConfig({
  setupFilesAfterEnv:['<rootDir>/jest.setup.js'],
  testEnvironment:'jest-environment-jsdom',
  moduleNameMapper:{'^@/(.*)$':'<rootDir>/src/$1'},
  coverageThreshold:{
    global:{statements:80,branches:80,functions:80,lines:80}
  }
});

// jest.setup.js
import '@testing-library/jest-dom';
jest.mock('next/navigation',()=>({
  useRouter:()=>({push:jest.fn()}),
  usePathname:()=>'',
}));
```

### Component Testing
```tsx
// Basic pattern
describe('Button',()=>{
  it('handles clicks',()=>{
    const onClick=jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });
  it('applies variants',()=>{
    render(<Button variant="destructive">Delete</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-red-500');
  });
});

// Form testing
describe('LoginForm',()=>{
  it('validates required fields',async()=>{
    render(<LoginForm/>);
    fireEvent.click(screen.getByRole('button'));
    await waitFor(()=>{
      expect(screen.getByText(/email required/i)).toBeInTheDocument();
    });
  });
  it('submits valid data',async()=>{
    render(<LoginForm/>);
    await userEvent.type(screen.getByLabelText(/email/i),'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i),'password123');
    fireEvent.click(screen.getByRole('button'));
    await waitFor(()=>{
      expect(signIn).toHaveBeenCalledWith('credentials',{
        email:'test@example.com',
        password:'password123'
      });
    });
  });
});
```

### Hook Testing
```tsx
describe('useDebounce',()=>{
  beforeEach(()=>jest.useFakeTimers());
  afterEach(()=>jest.useRealTimers());
  it('debounces value changes',()=>{
    const {result,rerender}=renderHook(
      ({value})=>useDebounce(value,500),
      {initialProps:{value:'initial'}}
    );
    expect(result.current).toBe('initial');
    rerender({value:'changed'});
    expect(result.current).toBe('initial');
    act(()=>jest.advanceTimersByTime(500));
    expect(result.current).toBe('changed');
  });
});
```

### API Route Testing
```tsx
describe('POST /api/users',()=>{
  it('requires auth',async()=>{
    (auth).mockResolvedValue(null);
    const req=new NextRequest('http://localhost/api/users',{
      method:'POST',
      body:JSON.stringify({name:'Test'})
    });
    const res=await POST(req);
    expect(res.status).toBe(401);
  });
  it('validates input',async()=>{
    (auth).mockResolvedValue({user:{role:'ADMIN'}});
    const req=new NextRequest('http://localhost/api/users',{
      method:'POST',
      body:JSON.stringify({name:'',email:'invalid'})
    });
    const res=await POST(req);
    expect(res.status).toBe(400);
  });
  it('creates user',async()=>{
    (auth).mockResolvedValue({user:{role:'ADMIN'}});
    (db.user.create).mockResolvedValue({id:'1',name:'Test'});
    const req=new NextRequest('http://localhost/api/users',{
      method:'POST',
      body:JSON.stringify({name:'Test',email:'test@example.com'})
    });
    const res=await POST(req);
    expect(res.status).toBe(201);
  });
});
```

### Server Action Testing
```tsx
describe('submitContact',()=>{
  it('validates fields',async()=>{
    const formData=new FormData();
    const result=await submitContact({},formData);
    expect(result.errors?.name).toBeDefined();
    expect(db.contact.create).not.toHaveBeenCalled();
  });
  it('handles success',async()=>{
    const formData=new FormData();
    formData.append('name','Test');
    formData.append('email','test@example.com');
    formData.append('message','Long enough message here');
    const result=await submitContact({},formData);
    expect(result.success).toBe(true);
    expect(revalidatePath).toHaveBeenCalledWith('/contact');
  });
});
```

### E2E with Playwright
```ts
// playwright.config.ts
export default defineConfig({
  testDir:'./src/__tests__',
  use:{
    baseURL:'http://localhost:3000',
    screenshot:'only-on-failure'
  },
  projects:[
    {name:'chromium',use:devices['Desktop Chrome']},
    {name:'mobile',use:devices['iPhone 12']}
  ]
});

// auth.spec.ts
test('login flow',async({page})=>{
  await page.goto('/auth/login');
  await page.fill('[name="email"]','test@example.com');
  await page.fill('[name="password"]','password123');
  await page.click('[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
});
```

### Testing Patterns
```tsx
// Mock External APIs
const server=setupServer(
  rest.get('/api/data',(req,res,ctx)=>
    res(ctx.json({items:[]}))
  )
);
beforeAll(()=>server.listen());
afterEach(()=>server.resetHandlers());

// Test States
expect(screen.getByText('Loading...')).toBeInTheDocument();

server.use(rest.get('/api/data',(req,res,ctx)=>
  res(ctx.status(500))
));
await waitFor(()=>{
  expect(screen.getByText('Error')).toBeInTheDocument();
});

await waitFor(()=>{
  expect(screen.getByText('Data loaded')).toBeInTheDocument();
});

// Auth Context
const AuthWrapper=({children,user=null})=>(
  <SessionProvider session={user?{user}:null}>
    {children}
  </SessionProvider>
);

render(
  <AuthWrapper user={{id:'1',role:'ADMIN'}}>
    <ProtectedComponent/>
  </AuthWrapper>
);
```

### Common Failures
1. No error cases (only happy path)
2. Implementation testing (internals, not behavior)
3. Snapshot abuse (brittle, meaningless)
4. Missing async handling (race conditions)
5. Console.log debugging (use proper assertions)

Actual Testing:
```tsx
// NOT: expect(component.state.isOpen).toBe(true)
// YES: expect(screen.getByRole('dialog')).toBeVisible()

// NOT: expect(mockFn).toHaveBeenCalledTimes(1)
// YES: expect(screen.getByText('Success')).toBeInTheDocument()

// NOT: expect(wrapper).toMatchSnapshot()
// YES: expect(screen.getByText('$99.99')).toBeInTheDocument()
```

### Reality
Most "tested" code:
- 90% happy path
- 10% random snapshots
- 0% error handling
- 0% edge cases

Real testing catches:
- State bugs before users see them
- API failures before 500 errors
- Race conditions before data corruption
- Auth gaps before breaches

Every untested edge case = production incident. Every skipped test = 3am page.

Test properly or debug forever.