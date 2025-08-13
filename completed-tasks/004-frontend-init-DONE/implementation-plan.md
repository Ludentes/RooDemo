# Frontend Infrastructure Implementation Plan

This document outlines the step-by-step implementation plan for the Election Monitoring System frontend infrastructure. The plan is organized into phases, with each phase building upon the previous one.

## Phase 1: Project Setup and Configuration

### Step 1.1: Initialize the Frontend Project

```bash
# Create a new Vite project with React and TypeScript
pnpm create vite@latest frontend -- --template react-ts

# Navigate to the project directory
cd frontend

# Install core dependencies
pnpm install
```

### Step 1.2: Configure TypeScript

1. Update `tsconfig.json` with stricter type checking:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Step 1.3: Set Up Tailwind CSS 4

1. Install Tailwind CSS 4 and its dependencies:

```bash
pnpm install tailwindcss @tailwindcss/postcss postcss
```

2. Create a `postcss.config.ts` file:

```typescript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
}
```

3. Create a `tailwind.config.js` file:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

4. Update `src/index.css` to import Tailwind CSS:

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --radius: 0.625rem;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.637 0.237 25.331);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Step 1.4: Set Up ESLint and Prettier

1. Install ESLint and Prettier dependencies:

```bash
npm install -D eslint eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-import eslint-plugin-jsx-a11y @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier eslint-config-prettier eslint-plugin-prettier
```

2. Create `.eslintrc.js` file:

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:jsx-a11y/recommended',
    'prettier',
    'plugin:prettier/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks', '@typescript-eslint', 'import', 'jsx-a11y', 'prettier'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
    'import/resolver': {
      typescript: {},
    },
  },
};
```

3. Create `.prettierrc` file:

```json
{
  "semi": true,
  "tabWidth": 2,
  "printWidth": 100,
  "singleQuote": true,
  "trailingComma": "es5",
  "jsxSingleQuote": false,
  "bracketSpacing": true
}
```

### Step 1.5: Set Up shadcn/ui

1. Install shadcn/ui CLI:

```bash
npm install -D shadcn-ui
```

2. Create a `components.json` file:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "hooks": "@/hooks",
    "lib": "@/lib",
    "ui": "@/components/ui"
  }
}
```

3. Install shadcn/ui core dependencies:

```bash
npm install class-variance-authority clsx tailwind-merge lucide-react tw-animate-css
```

4. Create a utils file at `src/lib/utils.ts`:

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Phase 2: Project Structure Setup

### Step 2.1: Create Directory Structure

Create the following directory structure:

```
src/
├── assets/           # Static assets like images, fonts, etc.
├── components/       # Reusable UI components
│   ├── ui/           # shadcn/ui components
│   ├── layout/       # Layout components
│   └── common/       # Common components used across features
├── features/         # Feature-specific components and logic
│   ├── dashboard/    # Dashboard feature
│   ├── constituencies/ # Constituencies feature
│   └── alerts/       # Alerts feature
├── hooks/            # Custom React hooks
├── lib/              # Utility functions and helpers
├── services/         # API and other services
├── store/            # State management (Zustand)
└── types/            # TypeScript type definitions
```

### Step 2.2: Set Up Basic App Structure

1. Update `src/App.tsx`:

```tsx
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes';
import { AppLayout } from './components/layout/AppLayout';

function App() {
  return (
    <Router>
      <AppLayout>
        <AppRoutes />
      </AppLayout>
    </Router>
  );
}

export default App;
```

2. Create `src/routes.tsx`:

```tsx
import { Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { Spinner } from './components/ui/spinner';

// Lazy-loaded components
const Dashboard = lazy(() => import('./features/dashboard/Dashboard'));
const ConstituencyList = lazy(() => import('./features/constituencies/ConstituencyList'));
const ConstituencyDetail = lazy(() => import('./features/constituencies/ConstituencyDetail'));
const AlertList = lazy(() => import('./features/alerts/AlertList'));
const AlertDetail = lazy(() => import('./features/alerts/AlertDetail'));
const NotFound = lazy(() => import('./components/common/NotFound'));

const AppRoutes = () => {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-full"><Spinner /></div>}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/constituencies" element={<ConstituencyList />} />
        <Route path="/constituencies/:id" element={<ConstituencyDetail />} />
        <Route path="/alerts" element={<AlertList />} />
        <Route path="/alerts/:id" element={<AlertDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
```

## Phase 3: UI Components Setup

### Step 3.1: Install and Configure shadcn/ui Components

Install the core shadcn/ui components:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add select
npx shadcn-ui@latest add sheet
npx shadcn-ui@latest add table
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add tooltip
npx shadcn-ui@latest add spinner
npx shadcn-ui@latest add skeleton
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add popover
npx shadcn-ui@latest add pagination
npx shadcn-ui@latest add avatar
```

### Step 3.2: Create Layout Components

1. Create `src/components/layout/AppLayout.tsx`:

```tsx
import { ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface AppLayoutProps {
  children: ReactNode;
}

export const AppLayout = ({ children }: AppLayoutProps) => {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-auto p-4">{children}</main>
      </div>
    </div>
  );
};
```

2. Create `src/components/layout/Header.tsx`:

```tsx
import { Button } from '../ui/button';
import { MoonIcon, SunIcon } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';

export const Header = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b border-border h-14 px-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold">Election Monitoring System</h1>
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="icon" onClick={toggleTheme}>
          {theme === 'dark' ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
        </Button>
      </div>
    </header>
  );
};
```

3. Create `src/components/layout/Sidebar.tsx`:

```tsx
import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { cn } from '../../lib/utils';
import { Button } from '../ui/button';
import { ScrollArea } from '../ui/scroll-area';
import {
  BarChart3Icon,
  HomeIcon,
  AlertTriangleIcon,
  MapIcon,
  MenuIcon,
  XIcon,
} from 'lucide-react';

export const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div
      className={cn(
        'border-r border-border bg-card text-card-foreground h-screen transition-all duration-300',
        collapsed ? 'w-16' : 'w-64'
      )}
    >
      <div className="flex items-center justify-between h-14 px-4 border-b border-border">
        {!collapsed && <span className="font-semibold">Election Monitor</span>}
        <Button variant="ghost" size="icon" onClick={toggleSidebar}>
          {collapsed ? <MenuIcon className="h-5 w-5" /> : <XIcon className="h-5 w-5" />}
        </Button>
      </div>
      <ScrollArea className="h-[calc(100vh-3.5rem)]">
        <nav className="p-2">
          <ul className="space-y-2">
            <NavItem
              to="/"
              icon={<HomeIcon className="h-5 w-5" />}
              label="Dashboard"
              collapsed={collapsed}
            />
            <NavItem
              to="/constituencies"
              icon={<MapIcon className="h-5 w-5" />}
              label="Constituencies"
              collapsed={collapsed}
            />
            <NavItem
              to="/alerts"
              icon={<AlertTriangleIcon className="h-5 w-5" />}
              label="Alerts"
              collapsed={collapsed}
            />
            <NavItem
              to="/statistics"
              icon={<BarChart3Icon className="h-5 w-5" />}
              label="Statistics"
              collapsed={collapsed}
            />
          </ul>
        </nav>
      </ScrollArea>
    </div>
  );
};

interface NavItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
  collapsed: boolean;
}

const NavItem = ({ to, icon, label, collapsed }: NavItemProps) => {
  return (
    <li>
      <NavLink
        to={to}
        className={({ isActive }) =>
          cn(
            'flex items-center p-2 rounded-md transition-colors',
            isActive
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-secondary hover:text-secondary-foreground',
            collapsed ? 'justify-center' : 'space-x-3'
          )
        }
      >
        {icon}
        {!collapsed && <span>{label}</span>}
      </NavLink>
    </li>
  );
};
```

### Step 3.3: Create Common Components

1. Create `src/components/common/NotFound.tsx`:

```tsx
import { Button } from '../ui/button';
import { useNavigate } from 'react-router-dom';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <p className="text-xl mb-8">Page not found</p>
      <Button onClick={() => navigate('/')}>Go to Dashboard</Button>
    </div>
  );
};

export default NotFound;
```

2. Create `src/components/common/ErrorBoundary.tsx`:

```tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Button } from '../ui/button';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center h-full p-4">
          <h2 className="text-2xl font-bold mb-4">Something went wrong</h2>
          <p className="text-muted-foreground mb-6">
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
          <Button onClick={() => this.setState({ hasError: false })}>Try again</Button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

3. Create `src/components/common/LoadingSpinner.tsx`:

```tsx
import { Spinner } from '../ui/spinner';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner = ({ message = 'Loading...' }: LoadingSpinnerProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <Spinner className="h-8 w-8 mb-4" />
      <p className="text-muted-foreground">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
```

## Phase 4: State Management Setup

### Step 4.1: Install Zustand

```bash
npm install zustand immer
```

### Step 4.2: Create Store Structure

1. Create `src/store/index.ts`:

```typescript
export * from './uiStore';
export * from './electionStore';
export * from './constituencyStore';
export * from './alertStore';
```

2. Create `src/store/uiStore.ts`:

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: 'light',
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
    }),
    {
      name: 'ui-store',
    }
  )
);
```

3. Create `src/store/electionStore.ts`:

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

export interface Election {
  id: string;
  name: string;
  date: string;
  status: 'upcoming' | 'active' | 'completed';
}

interface ElectionState {
  elections: Election[];
  selectedElection: Election | null;
  loading: boolean;
  error: string | null;
  fetchElections: () => Promise<void>;
  selectElection: (id: string) => void;
}

export const useElectionStore = create<ElectionState>()(
  immer((set, get) => ({
    elections: [],
    selectedElection: null,
    loading: false,
    error: null,
    fetchElections: async () => {
      set((state) => {
        state.loading = true;
        state.error = null;
      });
      try {
        // Replace with actual API call
        const response = await fetch('/api/elections');
        const data = await response.json();
        set((state) => {
          state.elections = data;
          state.loading = false;
        });
      } catch (error) {
        set((state) => {
          state.error = error instanceof Error ? error.message : 'Failed to fetch elections';
          state.loading = false;
        });
      }
    },
    selectElection: (id) => {
      const election = get().elections.find((e) => e.id === id) || null;
      set((state) => {
        state.selectedElection = election;
      });
    },
  }))
);
```

4. Create similar store files for constituencies and alerts.

### Step 4.3: Create Custom Hooks for Store Access

1. Create `src/hooks/useTheme.ts`:

```typescript
import { useEffect } from 'react';
import { useUIStore } from '../store';

export const useTheme = () => {
  const { theme, setTheme, toggleTheme } = useUIStore();

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
  }, [theme]);

  return { theme, setTheme, toggleTheme };
};
```

## Phase 5: API Client Setup

### Step 5.1: Install Axios and React Query

```bash
npm install axios @tanstack/react-query
```

### Step 5.2: Create API Client

1. Create `src/services/api/client.ts`:

```typescript
import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Define base API configuration
const apiConfig: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
};

// Create API client instance
const apiClient: AxiosInstance = axios.create(apiConfig);

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can modify the request config here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle common errors here
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Network Error:', error.message);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

2. Create `src/services/api/index.ts`:

```typescript
import apiClient from './client';

// Elections API
export const electionsApi = {
  getAll: () => apiClient.get('/elections'),
  getById: (id: string) => apiClient.get(`/elections/${id}`),
  getUpcoming: () => apiClient.get('/elections/upcoming'),
};

// Constituencies API
export const constituenciesApi = {
  getAll: () => apiClient.get('/constituencies'),
  getById: (id: string) => apiClient.get(`/constituencies/${id}`),
};

// Alerts API
export const alertsApi = {
  getAll: () => apiClient.get('/alerts'),
  getById: (id: string) => apiClient.get(`/alerts/${id}`),
};

// Dashboard API
export const dashboardApi = {
  getSummary: () => apiClient.get('/dashboard/summary'),
};

// Files API
export const filesApi = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  processDirectory: (path: string) => apiClient.post('/files/process-directory', { path }),
  getStatistics: (constituencyId: string) => apiClient.get(`/files/statistics/${constituencyId}`),
};
```

### Step 5.3: Set Up React Query

1. Update `src/main.tsx`:

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

## Phase 6: Error Handling and Notifications

### Step 6.1: Set Up Toast Notifications

1. Create `src/components/ui/toaster.tsx` using shadcn/ui:

```bash
npx shadcn-ui@latest add toast
```

2. Create `src/hooks/useToast.ts`:

```typescript
import { useToast } from '../components/ui/use-toast';

export const useNotification = () => {
  const { toast } = useToast();

  const showSuccess = (message: string) => {
    toast({
      title: 'Success',
      description: message,
      variant: 'default',
    });
  };

  const showError = (message: string) => {
    toast({
      title: 'Error',
      description: message,
      variant: 'destructive',
    });
  };

  const showInfo = (message: string) => {
    toast({
      title