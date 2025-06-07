Next.js State Management
State Categories:
- ServerState|Server|DB|Users,content|Prisma,Drizzle
- RequestState|Server|Req|Form data,auth|ServerActions
- UIState|Client|Session|Theme,modals|Zustand,Context
- ComponentState|Client|Comp|Forms,toggles|useState
- URLState|Both|Bookmark|Filters,pages|searchParams
- Cache|Both|Config|API responses|TanStackQuery

CoreRules:1.Server-first;2.Min.Client;3.Single source;4.Derive don't store;5.Hydration safe

Server State
```tsx
export default async function UsersPage(){const users=await db.user.findMany();const active=users.filter(u=>u.isActive);return<UserList users={active}/>}
const users=await fetch('/api/users');
return<UserList users={users}/>;
const safe=users.map(({id,name})=>({id,name}));
```

Client State
```tsx
'use client';export function Counter(){const[count,set]=useState(0);return<button onClick={()=>set(c=>c+1)}>{count}</button>}
const[full,set]=useState('');useEffect(()=>set(`${first} ${last}`),[first,last]);
const full=`${first} ${last}`;
```

Global Client State
```tsx
import{create}from'zustand';export const useThemeStore=create(set=>({theme:'light',toggle:()=>set(s=>({theme:s.theme==='light'?'dark':'light'}))}));
export function ThemeProvider({children}){const[m,set]=useState(false);const{theme}=useThemeStore();useEffect(()=>set(true),[]);if(!m)return null;return<div data-theme={theme}>{children}</div>;}
```

Form State
```tsx
'use client';import{useForm}from'react-hook-form';import{zodResolver}from'@hookform/resolvers/zod';const schema=z.object({name:z.string().min(2),email:z.string().email()});export function ContactForm(){const{register,handleSubmit,formState:{errors}}=useForm({resolver:zodResolver(schema)});return<form onSubmit={handleSubmit(async d=>await submitContactForm(d))}><input{...register('name')}/>{errors.name&&<p>{errors.name.message}</p>}<button type="submit">Send</button></form>;}
```

Server Actions
```tsx
'use server';export async function createTodo(formData:FormData){const r=TodoSchema.safeParse({title:formData.get('title')});if(!r.success)return{error:r.error.flatten()};await db.todo.create({data:r.data});revalidatePath('/todos');return{success:true}}
<form action={createTodo}><input name="title"/><button type="submit">Add</button></form>
```

URL State
```tsx
'use client';export function Filters(){const sp=useSearchParams(),r=useRouter(),p=usePathname();const upd=(k,v)=>{const q=new URLSearchParams(sp);q.set(k,v);r.push(`${p}?${q}`)};return<select onChange={e=>upd('sort',e.target.value)}><option value="newest">Newest</option><option value="price">Price</option></select>}
```

Context vs Zustand
Context
```tsx
const ModalContext=createContext(null);export function ModalProvider({children}){const[open,set]=useState(false);return<ModalContext.Provider value={{isOpen:open,toggle:()=>set(v=>!v)}}>{children}</ModalContext.Provider>}
```
Zustand
```tsx
export const useCartStore=create(persist(set=>({items:[],add:item=>set(s=>({items:[...s.items,item]}))}),{name:'cart',skipHydration:true}));
```

Query State
```tsx
'use client';export function Products({category}){const{data,error,isLoading}=useQuery({queryKey:['products',category],queryFn:()=>getProducts(category)});if(isLoading)return<Skeleton/>;if(error)return<Error/>;return<ProductGrid products={data}/>}
```

Antipatterns:
1.ClientFetchingServerData→ServerComponent
2.MonolithicStore→focused stores
3.StoringServerStateClientSide→ServerComponent or useQuery

DecisionTree:1.Server-rendered?ServerComp;2.Shared?Zustand;3.Tree?Context;4.URL?searchParams;5.Form?ReactHookForm;6.Simple?useState

Reality:
- server data stays server
- UI minimal
- URL for nav
- forms use proper libs