## Next.js State Management

Your state is chaos. Here's the fix.

### State Categories

| Type | Where | Persists | Examples | Tools |
|------|-------|----------|----------|-------|
| **Server State** | Server | Database | Users, content | Prisma, Drizzle |
| **Request State** | Server | Request | Form data, auth | Server Actions |
| **UI State** | Client | Session | Theme, modals | Zustand, Context |
| **Component State** | Client | Component | Forms, toggles | useState |
| **URL State** | Both | Bookmarks | Filters, pages | searchParams |
| **Cache** | Both | Configurable | API responses | TanStack Query |

### Core Rules

1. **Server-first**: Database queries in Server Components
2. **Minimize client**: Only UI interactions 
3. **Single source**: No duplicate state
4. **Derive don't store**: Calculate on-demand
5. **Hydration safe**: Prevent mismatches

### Server State

```tsx
// Direct queries, no hooks
export default async function UsersPage() {
  const users = await db.user.findMany();
  const activeUsers = users.filter(u => u.isActive);
  
  return <UserList users={activeUsers} />;
}

// WRONG: API call to self
const users = await fetch('/api/users');

// WRONG: Exposing DB entities
return <UserList users={users} />; // Sensitive fields exposed

// RIGHT: Transform first
const safeUsers = users.map(({id, name}) => ({id, name}));
```

### Client State

```tsx
'use client';

// Simple component state
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// WRONG: Storing derived state
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(`${first} ${last}`), [first, last]);

// RIGHT: Derive on render
const fullName = `${first} ${last}`;
```

### Global Client State

```tsx
// store/theme-store.ts
import { create } from 'zustand';

export const useThemeStore = create((set) => ({
  theme: 'light',
  toggleTheme: () => set(s => ({ 
    theme: s.theme === 'light' ? 'dark' : 'light' 
  })),
}));

// Hydration safety
export function ThemeProvider({ children }) {
  const [mounted, setMounted] = useState(false);
  const { theme } = useThemeStore();
  
  useEffect(() => setMounted(true), []);
  if (!mounted) return null; // Prevent mismatch
  
  return <div data-theme={theme}>{children}</div>;
}
```

### Form State

```tsx
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export function ContactForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });
  
  return (
    <form onSubmit={handleSubmit(async (data) => {
      await submitContactForm(data);
    })}>
      <input {...register('name')} />
      {errors.name && <p>{errors.name.message}</p>}
      <button type="submit">Send</button>
    </form>
  );
}
```

### Server Actions

```tsx
'use server';

export async function createTodo(formData: FormData) {
  const result = TodoSchema.safeParse({
    title: formData.get('title')
  });
  
  if (!result.success) {
    return { error: result.error.flatten() };
  }
  
  await db.todo.create({ data: result.data });
  revalidatePath('/todos');
  return { success: true };
}

// Usage
<form action={createTodo}>
  <input name="title" />
  <button type="submit">Add</button>
</form>
```

### URL State

```tsx
'use client';
export function Filters() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  
  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams);
    params.set(key, value);
    router.push(`${pathname}?${params}`);
  };
  
  return (
    <select onChange={e => updateFilter('sort', e.target.value)}>
      <option value="newest">Newest</option>
      <option value="price">Price</option>
    </select>
  );
}
```

### Context vs Zustand

**Context**: Component tree state only
```tsx
const ModalContext = createContext<{
  isOpen: boolean;
  toggle: () => void;
}>(null);

export function ModalProvider({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <ModalContext.Provider value={{ 
      isOpen, 
      toggle: () => setIsOpen(v => !v) 
    }}>
      {children}
    </ModalContext.Provider>
  );
}
```

**Zustand**: Global app state
```tsx
// With persistence
export const useCartStore = create(
  persist(
    (set) => ({
      items: [],
      add: (item) => set(s => ({ 
        items: [...s.items, item] 
      })),
    }),
    { 
      name: 'cart',
      skipHydration: true // Handle manually
    }
  )
);
```

### Query State

```tsx
'use client';
export function Products({ category }) {
  const { data, error, isLoading } = useQuery({
    queryKey: ['products', category],
    queryFn: () => getProducts(category),
  });
  
  if (isLoading) return <Skeleton />;
  if (error) return <Error />;
  return <ProductGrid products={data} />;
}
```

### Antipatterns

**1. Client Fetching Server Data**
```tsx
// WRONG
'use client';
useEffect(() => {
  fetch('/api/users').then(setUsers);
}, []);

// RIGHT: Server Component
export default async function Users() {
  const users = await db.user.findMany();
  return <UserList users={users} />;
}
```

**2. Monolithic Store**
```tsx
// WRONG: Everything in one store
const useStore = create({
  user: null,
  cart: [],
  theme: 'light',
  sidebar: false,
  // 50 more properties...
});

// RIGHT: Focused stores
const useUserStore = create({user: null});
const useCartStore = create({items: []});
const useUIStore = create({theme: 'light'});
```

**3. Storing Server State Client-Side**
```tsx
// WRONG: Manual sync
const [users, setUsers] = useState([]);
useEffect(() => fetchUsers().then(setUsers), []);

// RIGHT: Let framework handle it
const users = await db.user.findMany(); // Server Component
// OR
const { data } = useQuery(['users'], fetchUsers); // TanStack Query
```

### Decision Tree

1. **Server-rendered?** → Server Component fetch
2. **Global shared?** → Zustand
3. **Component tree?** → Context
4. **URL-addressable?** → searchParams
5. **Complex form?** → React Hook Form
6. **Simple UI?** → useState

### The Reality

Your state management sucks because you:
- Put server state on client (unnecessary complexity)
- Use Redux for theme toggles (overkill)
- Ignore URL state (missing shareability)
- Duplicate state everywhere (sync nightmares)
- Mix all concerns (unmaintainable mess)

**Fix**: Specialize your state. Server data stays server-side. UI state stays minimal. URLs handle navigation state. Forms use proper libraries.

Each state type has its place. Use the right tool or suffer the consequences.
