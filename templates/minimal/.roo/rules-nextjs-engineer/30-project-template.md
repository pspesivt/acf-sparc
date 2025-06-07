## Next.js Project Structure
### Root Structure
project/
├── .github/workflows/
├── .husky/
├── public/
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── types/
├── .env.example
├── .eslintrc.js
├── .gitignore
├── next.config.js
├── package.json
├── pnpm-lock.yaml
├── tailwind.config.ts
└── tsconfig.json

### App Directory
src/app/
├── (auth)/
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/
│   ├── dashboard/page.tsx
│   └── settings/page.tsx
├── api/
│   └── users/route.ts
├── error.tsx
├── layout.tsx
├── not-found.tsx
└── page.tsx

### Components Organization
src/components/
├── ui/
├── forms/
├── layout/
└── [feature]/

### Lib Structure
src/lib/
├── api/
├── auth/
├── db/
├── hooks/
├── utils/
└── validations/

### Critical Configs
tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "paths": {"@/*": ["./src/*"]}
  }
}
next.config.js
module.exports = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    typedRoutes: true,
    serverActions: { bodySizeLimit: '2mb' }
  }
}
tailwind.config.ts
export default {
  content: ['./src/**/*.{ts,tsx}'],
  theme: { extend: { /* custom theme */ } },
  plugins: []
}

### Naming Rules
Components:PascalCase(UserCard.tsx);Hooks:use+camelCase(useAuth.ts);Utils:camelCase(formatDate.ts);Constants:UPPER_SNAKE(API_URL);Routes:kebab-case(user-settings)

### Import Order
1.React/Next:import { useState } from 'react';import Link from 'next/link'
2.External:import { z } from 'zod'
3.Internal:import { Button } from '@/components/ui';import { api } from '@/lib/api'
4.Types:import type { User } from '@/types'
5.Relative:import { helper } from './utils'

### Component Template
// imports
interface Props {
  title: string;
  onSubmit: () => void;
}

// constants
const MAX_LENGTH = 100;

// component
export function Component({ title, onSubmit }: Props) {
  const [state, setState] = useState('');
  
  return (
    <div>
      {/* implementation */}
    </div>
  );
}

// helpers (if any)
function truncate(text: string): string {
  return text.slice(0, MAX_LENGTH);
}

### Barrel Exports
components/ui/index.ts
export * from './button';
export * from './input';
export * from './card';
// Usage
import { Button, Input, Card } from '@/components/ui';

### The Reality
Most Next.js projects: scattered files, inconsistent naming, circular dependencies, no clear boundaries; This structure enforces: 1.Predictability 2.Scalability 3.Performance 4.Maintainability