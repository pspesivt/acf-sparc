## Next.js Code Patterns

Your code hydrates wrong. Fix it.

**Database Interaction**: This mode consumes a pre-configured, auto-generated Prisma Client. All data access logic must be implemented through this client. Any task requiring a change to the database schema (e.g., adding a table or column) must be rejected and returned to the Orchestrator.

### Server vs Client

**Server Component**:
```tsx
// app/users/[id]/page.tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const user = await db.user.findUnique({ where: { id: params.id } });
  return user ? { title: `${user.name}'s Profile` } : { title: 'Not Found' };
}

export default async function UserPage({ params }: Props) {
  const user = await db.user.findUnique({
    where: { id: params.id },
    include: { posts: { take: 5, orderBy: { createdAt: 'desc' } } }
  });
  
  if (!user) notFound();
  return <UserProfile user={user} />;
}
```

**Client Component**:
```tsx
'use client';
export function ThemeSwitcher() {
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();
  
  useEffect(() => setMounted(true), []); // Avoid hydration mismatch
  if (!mounted) return null;
  
  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}
```

### Data Fetching

**Parallel**:
```tsx
export default async function Dashboard() {
  const [users, posts, stats] = await Promise.all([
    db.user.findMany(),
    db.post.findMany(),
    fetchStats()
  ]);
  
  return (
    <>
      <UserList users={users} />
      <RecentPosts posts={posts} />
      <Stats data={stats} />
    </>
  );
}
```

**Streaming**:
```tsx
export default function DashboardPage() {
  return (
    <>
      <h1>Dashboard</h1>
      <QuickStats /> {/* Renders immediately */}
      <Suspense fallback={<Loading />}>
        <SlowChart /> {/* Streams when ready */}
      </Suspense>
    </>
  );
}
```

**Revalidation**:
```tsx
// Time-based (ISR)
const products = await fetch('https://api.example/products', {
  next: { revalidate: 3600 } // 1hr cache
});

// On-demand
export async function POST(request: NextRequest) {
  const { path, tag, secret } = await request.json();
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  path ? revalidatePath(path) : revalidateTag(tag);
  return NextResponse.json({ revalidated: true });
}
```

### Forms

**Server Actions**:
```tsx
'use server';

const ContactSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  message: z.string().min(10)
});

export async function submitContact(prevState: State, formData: FormData) {
  const result = ContactSchema.safeParse(Object.fromEntries(formData));
  
  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }
  
  await db.contact.create({ data: result.data });
  revalidatePath('/contact');
  return { success: true };
}

// Client component
'use client';
export function ContactForm() {
  const [state, formAction] = useFormState(submitContact, {});
  
  return (
    <form action={formAction}>
      <input name="name" />
      {state.errors?.name && <p className="text-red-500">{state.errors.name[0]}</p>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### API Routes

```tsx
// app/api/users/route.ts
const UserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email()
});

export async function GET(request: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = 10;
  
  const [users, total] = await Promise.all([
    db.user.findMany({ skip: (page - 1) * limit, take: limit }),
    db.user.count()
  ]);
  
  return NextResponse.json({ users, total, page });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const result = UserSchema.safeParse(body);
  
  if (!result.success) {
    return NextResponse.json({ error: result.error.flatten() }, { status: 400 });
  }
  
  const user = await db.user.create({ data: result.data });
  return NextResponse.json(user, { status: 201 });
}
```

### Error Handling

```tsx
// app/error.tsx
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => console.error(error), [error]);
  
  return (
    <div className="flex flex-col items-center p-8">
      <h2 className="text-xl font-bold text-red-600">Something broke</h2>
      <button onClick={reset} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">
        Try again
      </button>
    </div>
  );
}

// app/not-found.tsx
export default function NotFound() {
  return (
    <div className="text-center p-8">
      <h2 className="text-2xl font-bold">404</h2>
      <Link href="/" className="text-blue-600 hover:underline">Go home</Link>
    </div>
  );
}
```

### Auth (NextAuth)

```tsx
// auth.ts
export const { auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'jwt' },
  callbacks: {
    async session({ token, session }) {
      if (session.user) {
        session.user.id = token.sub!;
        session.user.role = token.role as UserRole;
      }
      return session;
    },
    async jwt({ token }) {
      if (!token.sub) return token;
      const user = await getUserById(token.sub);
      if (user) token.role = user.role;
      return token;
    }
  }
});

// middleware.ts
export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isAdminRoute = req.nextUrl.pathname.startsWith('/admin');
  
  if (isAdminRoute && (!isLoggedIn || req.auth?.user?.role !== 'ADMIN')) {
    return Response.redirect(new URL('/auth/login', req.nextUrl));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```

### Optimization

**Images**:
```tsx
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  sizes="(max-width: 768px) 100vw, 50vw"
  className="object-cover"
/>
```

**Code Splitting**:
```tsx
const HeavyChart = dynamic(() => import('@/components/chart'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### Anti-Patterns

**1. Client Everything**:
```tsx
// WRONG: Client component for static data
'use client';
export default function BlogList() {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    fetch('/api/posts').then(r => r.json()).then(setPosts);
  }, []);
  return <>{posts.map(p => <Post key={p.id} {...p} />)}</>;
}

// RIGHT: Server component
export default async function BlogList() {
  const posts = await db.post.findMany();
  return <>{posts.map(p => <Post key={p.id} {...p} />)}</>;
}
```

**2. No Metadata**:
```tsx
// WRONG: SEO disaster
export default function Page() {
  return <div>Content</div>;
}

// RIGHT: Searchable
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: { title: 'Page Title', images: ['/og.jpg'] }
};
```

**3. API Calls in RSC**:
```tsx
// WRONG: HTTP to self
const data = await fetch('http://localhost:3000/api/data');

// RIGHT: Direct DB access
const data = await db.data.findMany();
```

**4. Loose Types**:
```tsx
// WRONG: Runtime errors
export default function User({ user }) {
  return <h1>{user.name}</h1>;
}

// RIGHT: Compile-time safety
interface UserProps {
  user: { id: string; name: string; role: 'ADMIN' | 'USER' };
}
export default function User({ user }: UserProps) {
  return <h1>{user.name}</h1>;
}
```

### The Reality

Next.js isn't React with SSR bolted on. It's a full-stack framework with opinions. Fighting them creates debt.

**Server Components default** = smaller bundles  
**TypeScript strict** = fewer runtime errors  
**App Router only** = modern patterns  
**Proper boundaries** = no hydration errors  

The framework provides guardrails. Stay within them or suffer the consequences.

When you make everything client-side, ship unnecessary JavaScript. When you skip types, choose runtime crashes. When you ignore metadata, become invisible to search engines.

Every shortcut becomes technical debt. Every pattern violation becomes a production issue.

Code properly or use Create React App.
