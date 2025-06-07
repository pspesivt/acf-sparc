## Next.js Testing Standards
### Testing Stack
Unit/Component:Jest+RTL;API Routes:Jest+Supertest;E2E:Playwright;Mocking:MSW
### Coverage Requirements
Utils:100%;Hooks:95%;Components:90%;API/Actions:85%
### Jest Config
```js
const nextJest=require('next/jest');const createJestConfig=nextJest({dir:'./'});
module.exports=createJestConfig({
 setupFilesAfterEnv:['<rootDir>/jest.setup.js'],
 testEnvironment:'jest-environment-jsdom',
 moduleNameMapper:{'^@/(.*)$':'<rootDir>/src/$1'},
 coverageThreshold:{global:{statements:80,branches:80,functions:80,lines:80}}
});
// jest.setup.js
import'@testing-library/jest-dom';
jest.mock('next/navigation',()=>({useRouter:()=>({push:jest.fn()}),usePathname:()=>''}));
```
### Component Testing
```tsx
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
describe('LoginForm',()=>{
 it('validates required fields',async()=>{
  render(<LoginForm/>);
  fireEvent.click(screen.getByRole('button'));
  await waitFor(()=>expect(screen.getByText(/email required/i)).toBeInTheDocument());
 });
 it('submits valid data',async()=>{
  render(<LoginForm/>);
  await userEvent.type(screen.getByLabelText(/email/i),'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i),'password123');
  fireEvent.click(screen.getByRole('button'));
  await waitFor(()=>expect(signIn).toHaveBeenCalledWith('credentials',{email:'test@example.com',password:'password123'}));
 });
});
```
### Hook Testing
```tsx
describe('useDebounce',()=>{
 beforeEach(()=>jest.useFakeTimers());
 afterEach(()=>jest.useRealTimers());
 it('debounces value changes',()=>{
  const{result,rerender}=renderHook(({value})=>useDebounce(value,500),{initialProps:{value:'initial'}});
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
  (auth as jest.Mock).mockResolvedValue(null);
  const req=new NextRequest('http://localhost/api/users',{method:'POST',body:JSON.stringify({name:'Test'})});
  const res=await POST(req);
  expect(res.status).toBe(401);
 });
 it('validates input',async()=>{
  (auth as jest.Mock).mockResolvedValue({user:{role:'ADMIN'}});
  const req=new NextRequest('http://localhost/api/users',{method:'POST',body:JSON.stringify({name:'',email:'invalid'})});
  const res=await POST(req);
  expect(res.status).toBe(400);
 });
 it('creates user',async()=>{
  (auth as jest.Mock).mockResolvedValue({user:{role:'ADMIN'}});
  (db.user.create as jest.Mock).mockResolvedValue({id:'1',name:'Test'});
  const req=new NextRequest('http://localhost/api/users',{method:'POST',body:JSON.stringify({name:'Test',email:'test@example.com'})});
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
  formData.append('name','Test');formData.append('email','test@example.com');formData.append('message','Long enough message here');
  const result=await submitContact({},formData);
  expect(result.success).toBe(true);
  expect(revalidatePath).toHaveBeenCalledWith('/contact');
 });
});
```
### E2E with Playwright
```ts
// playwright.config.ts
export default defineConfig({testDir:'./src/__tests__',use:{baseURL:'http://localhost:3000',screenshot:'only-on-failure'},projects:[{name:'chromium',use:devices['Desktop Chrome']},{name:'mobile',use:devices['iPhone 12']}]});
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
const server=setupServer(rest.get('/api/data',(req,res,ctx)=>res(ctx.json({items:[]}))));
beforeAll(()=>server.listen());
afterEach(()=>server.resetHandlers());
```
```tsx
// states
expect(screen.getByText('Loading...')).toBeInTheDocument();
server.use(rest.get('/api/data',(req,res,ctx)=>res(ctx.status(500))));
await waitFor(()=>expect(screen.getByText('Error')).toBeInTheDocument());
await waitFor(()=>expect(screen.getByText('Data loaded')).toBeInTheDocument());
```
```tsx
const AuthWrapper=({children,user=null})=>(
 <SessionProvider session={user?{user}:null}>{children}</SessionProvider>
);
render(<AuthWrapper user={{id:'1',role:'ADMIN'}}><ProtectedComponent/></AuthWrapper>);
```
### Common Failures
No error cases;Implementation testing;Snapshot abuse;Missing async handling;Console.log debugging
```tsx
expect(screen.getByRole('dialog')).toBeVisible();
expect(screen.getByText('$99.99')).toBeInTheDocument();
```
### The Reality
testedCode:happy:90%;snapshots:10%;error:0%;edge:0%
realTesting:catches[state bugs,API failures,race conditions,auth gaps]