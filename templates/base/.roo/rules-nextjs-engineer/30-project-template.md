## Next.js Project Structure

### Root Structure
```
project/
├── .github/workflows/        # CI/CD
├── .husky/                   # Git hooks
├── public/                   # Static assets
├── src/                      # All code here
│   ├── app/                  # App Router
│   ├── components/           # React components
│   ├── lib/                  # Utils & logic
│   └── types/                # TypeScript types
├── .env.example              # Document secrets
├── .eslintrc.js              # Linting rules
├── .gitignore                # No node_modules
├── next.config.js            # Next.js config
├── package.json              # Dependencies
├── pnpm-lock.yaml           
├── tailwind.config.ts        # Tailwind config
└── tsconfig.json             # TypeScript config
```

### App Directory
```
src/app/
├── (auth)/                   # Public routes
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/              # Protected routes
│   ├── dashboard/page.tsx
│   └── settings/page.tsx
├── api/                      # API routes
│   └── users/route.ts
├── error.tsx                 # Error boundary
├── layout.tsx                # Root layout
├── not-found.tsx             # 404 page
└── page.tsx                  # Homepage
```

### Components Organization
```
src/components/
├── ui/                       # Primitives
├── forms/                    # Form components
├── layout/                   # Header, footer, sidebar
└── [feature]/                # Feature-specific components
```

### Lib Structure
```
src/lib/
├── api/                      # API client & endpoints
├── auth/                     # Auth utilities
├── db/                       # Database client
├── hooks/                    # Custom React hooks
├── utils/                    # Helpers
└── validations/              # Zod schemas
```

### Critical Configs
**tsconfig.json**:
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "paths": {"@/*": ["./src/*"]}
  }
}
```

**next.config.js**:
```js
module.exports = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    typedRoutes: true,
    serverActions: { bodySizeLimit: '2mb' }
  }
}
```

**tailwind.config.ts**:
```ts
export default {
  content: ['./src/**/*.{ts,tsx}'],
  theme: { extend: {} },
  plugins: []
}
```

### Naming Rules
| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | use+camelCase | `useAuth.ts` |
| Utils | camelCase | `formatDate.ts` |
| Constants | UPPER_SNAKE | `API_URL` |
| Routes | kebab-case | `user-settings` |

### Import Order
```tsx
// 1. React/Next
import { useState } from 'react';
import Link from 'next/link';

// 2. External
import { z } from 'zod';

// 3. Internal absolute
import { Button } from '@/components/ui';
import { api } from '@/lib/api';

// 4. Types
import type { User } from '@/types';

// 5. Relative
import { helper } from './utils';
```

### Component Template
```tsx
interface Props {
  title: string;
  onSubmit: () => void;
}

const MAX_LENGTH = 100;

export function Component({ title, onSubmit }: Props) {
  const [state, setState] = useState('');
  
  return (
    <div>
      {/* implementation */}
    </div>
  );
}

function truncate(text: string): string {
  return text.slice(0, MAX_LENGTH);
}
```

### Barrel Exports
```ts
// components/ui/index.ts
export * from './button';
export * from './input';
export * from './card';

// Usage
import { Button, Input, Card } from '@/components/ui';
```

Benefits: Predictability, Scalability, Performance, Maintainability