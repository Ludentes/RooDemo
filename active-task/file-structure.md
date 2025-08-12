# Frontend Directory Structure

This document outlines the directory structure for the Election Monitoring System frontend. The structure follows a feature-based organization with clear separation of concerns.

## Root Structure

```
frontend/
├── .eslintrc.js           # ESLint configuration
├── .gitignore             # Git ignore file
├── .prettierrc            # Prettier configuration
├── components.json        # shadcn/ui configuration
├── index.html             # HTML entry point
├── package.json           # NPM package configuration
├── postcss.config.ts      # PostCSS configuration
├── README.md              # Project documentation
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
├── tsconfig.node.json     # TypeScript configuration for Node.js
└── vite.config.ts         # Vite configuration
```

## Source Directory Structure

```
frontend/src/
├── assets/                # Static assets
│   ├── fonts/             # Font files
│   └── images/            # Image files
├── components/            # Reusable UI components
│   ├── ui/                # shadcn/ui components
│   ├── layout/            # Layout components
│   └── common/            # Common components
├── features/              # Feature-specific components and logic
│   ├── dashboard/         # Dashboard feature
│   ├── constituencies/    # Constituencies feature
│   ├── alerts/            # Alerts feature
│   └── transactions/      # Transactions feature
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions and helpers
├── services/              # API and other services
│   ├── api/               # API client and services
│   └── websocket/         # WebSocket service
├── store/                 # State management (Zustand)
├── types/                 # TypeScript type definitions
├── App.tsx                # Main App component
├── index.css              # Global CSS
├── main.tsx               # Application entry point
├── routes.tsx             # Route definitions
└── vite-env.d.ts          # Vite environment type definitions
```

## Detailed Structure

### Components Directory

```
frontend/src/components/
├── ui/                    # shadcn/ui components
│   ├── alert-dialog.tsx
│   ├── avatar.tsx
│   ├── button.tsx
│   ├── card.tsx
│   ├── checkbox.tsx
│   ├── dialog.tsx
│   ├── dropdown-menu.tsx
│   ├── input.tsx
│   ├── label.tsx
│   ├── popover.tsx
│   ├── progress.tsx
│   ├── scroll-area.tsx
│   ├── select.tsx
│   ├── separator.tsx
│   ├── sheet.tsx
│   ├── skeleton.tsx
│   ├── spinner.tsx
│   ├── table.tsx
│   ├── tabs.tsx
│   ├── toast.tsx
│   ├── toaster.tsx
│   ├── tooltip.tsx
│   └── use-toast.ts
├── layout/                # Layout components
│   ├── AppLayout.tsx      # Main application layout
│   ├── Header.tsx         # Application header
│   ├── Sidebar.tsx        # Application sidebar
│   └── Footer.tsx         # Application footer
└── common/                # Common components
    ├── AlertBadge.tsx     # Alert badge component
    ├── Card.tsx           # Card component
    ├── Chart.tsx          # Chart component
    ├── DataTable.tsx      # Data table component
    ├── EmptyState.tsx     # Empty state component
    ├── ErrorBoundary.tsx  # Error boundary component
    ├── ErrorDisplay.tsx   # Error display component
    ├── LoadingSpinner.tsx # Loading spinner component
    ├── NotFound.tsx       # Not found component
    ├── Pagination.tsx     # Pagination component
    ├── StatusBadge.tsx    # Status badge component
    └── TimeAgo.tsx        # Time ago component
```

### Features Directory

```
frontend/src/features/
├── dashboard/             # Dashboard feature
│   ├── components/        # Dashboard-specific components
│   │   ├── ActivityTimeline.tsx
│   │   ├── DashboardSummaryCard.tsx
│   │   ├── ElectionStatusCard.tsx
│   │   ├── ParticipationChart.tsx
│   │   └── RecentAlerts.tsx
│   ├── hooks/             # Dashboard-specific hooks
│   │   └── useDashboard.ts
│   └── Dashboard.tsx      # Main dashboard component
├── constituencies/        # Constituencies feature
│   ├── components/        # Constituency-specific components
│   │   ├── ConstituencyCard.tsx
│   │   ├── ConstituencyFilter.tsx
│   │   ├── ConstituencyMap.tsx
│   │   ├── ConstituencyStats.tsx
│   │   ├── HourlyStatsChart.tsx
│   │   └── TransactionList.tsx
│   ├── hooks/             # Constituency-specific hooks
│   │   └── useConstituency.ts
│   ├── ConstituencyDetail.tsx # Constituency detail component
│   └── ConstituencyList.tsx   # Constituency list component
├── alerts/                # Alerts feature
│   ├── components/        # Alert-specific components
│   │   ├── AlertDetail.tsx
│   │   ├── AlertFilter.tsx
│   │   └── AlertList.tsx
│   ├── hooks/             # Alert-specific hooks
│   │   └── useAlerts.ts
│   ├── AlertDetail.tsx    # Alert detail component
│   └── AlertList.tsx      # Alert list component
└── transactions/          # Transactions feature
    ├── components/        # Transaction-specific components
    │   ├── TransactionDetail.tsx
    │   ├── TransactionFilter.tsx
    │   └── TransactionList.tsx
    ├── hooks/             # Transaction-specific hooks
    │   └── useTransactions.ts
    ├── TransactionDetail.tsx # Transaction detail component
    └── TransactionList.tsx   # Transaction list component
```

### Hooks Directory

```
frontend/src/hooks/
├── useApi.ts              # Hook for API calls
├── useDebounce.ts         # Hook for debouncing values
├── useLocalStorage.ts     # Hook for local storage
├── useMediaQuery.ts       # Hook for media queries
├── useNotification.ts     # Hook for notifications
├── usePagination.ts       # Hook for pagination
├── useSorting.ts          # Hook for sorting
├── useTheme.ts            # Hook for theme management
└── useWebSocket.ts        # Hook for WebSocket connections
```

### Services Directory

```
frontend/src/services/
├── api/                   # API services
│   ├── client.ts          # API client
│   ├── index.ts           # API service exports
│   ├── alertsApi.ts       # Alerts API service
│   ├── constituenciesApi.ts # Constituencies API service
│   ├── dashboardApi.ts    # Dashboard API service
│   ├── electionsApi.ts    # Elections API service
│   ├── filesApi.ts        # Files API service
│   └── transactionsApi.ts # Transactions API service
└── websocket/             # WebSocket services
    ├── client.ts          # WebSocket client
    └── index.ts           # WebSocket service exports
```

### Store Directory

```
frontend/src/store/
├── index.ts               # Store exports
├── uiStore.ts             # UI state store
├── electionStore.ts       # Election state store
├── constituencyStore.ts   # Constituency state store
├── alertStore.ts          # Alert state store
└── transactionStore.ts    # Transaction state store
```

### Types Directory

```
frontend/src/types/
├── index.ts               # Type exports
├── api.ts                 # API-related types
├── alert.ts               # Alert-related types
├── constituency.ts        # Constituency-related types
├── election.ts            # Election-related types
├── transaction.ts         # Transaction-related types
└── ui.ts                  # UI-related types
```

### Lib Directory

```
frontend/src/lib/
├── utils.ts               # General utility functions
├── date.ts                # Date utility functions
├── format.ts              # Formatting utility functions
├── validation.ts          # Validation utility functions
└── storage.ts             # Storage utility functions
```

## File Naming Conventions

1. **Component Files**: PascalCase (e.g., `Button.tsx`, `DataTable.tsx`)
2. **Hook Files**: camelCase with 'use' prefix (e.g., `useTheme.ts`, `useApi.ts`)
3. **Utility Files**: camelCase (e.g., `utils.ts`, `format.ts`)
4. **Store Files**: camelCase (e.g., `uiStore.ts`, `electionStore.ts`)
5. **Type Files**: camelCase (e.g., `api.ts`, `election.ts`)
6. **Configuration Files**: kebab-case (e.g., `tailwind.config.js`, `tsconfig.json`)

## Import Conventions

1. **Absolute Imports**: Use absolute imports with path aliases for better readability and maintainability.

```typescript
// Good
import { Button } from '@/components/ui/button';
import { useTheme } from '@/hooks/useTheme';

// Avoid
import { Button } from '../../components/ui/button';
import { useTheme } from '../../hooks/useTheme';
```

2. **Import Order**: Group imports in the following order:
   - React and React-related imports
   - Third-party library imports
   - Internal absolute imports
   - Internal relative imports
   - CSS/SCSS imports

```typescript
// React and React-related imports
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Third-party library imports
import { format } from 'date-fns';
import { BarChart, Bar } from 'recharts';

// Internal absolute imports
import { Button } from '@/components/ui/button';
import { useTheme } from '@/hooks/useTheme';

// Internal relative imports
import { AlertBadge } from '../common/AlertBadge';

// CSS/SCSS imports
import './styles.css';
```

## Component Organization

Each component should follow a consistent organization:

1. **Imports**: Following the import conventions above
2. **Types/Interfaces**: Component props and other related types
3. **Constants**: Component-specific constants
4. **Component**: The main component function
5. **Helper Functions**: Component-specific helper functions
6. **Export**: Default or named export

```typescript
// Imports
import React from 'react';
import { format } from 'date-fns';
import { Card } from '@/components/ui/card';

// Types/Interfaces
interface TimeAgoProps {
  date: string;
  format?: 'short' | 'long';
}

// Constants
const FORMAT_OPTIONS = {
  short: { addSuffix: true },
  long: { addSuffix: true, includeSeconds: true },
};

// Component
export const TimeAgo = ({ date, format = 'short' }: TimeAgoProps) => {
  const formattedDate = formatDate(date, format);
  
  return <span title={new Date(date).toLocaleString()}>{formattedDate}</span>;
};

// Helper Functions
function formatDate(date: string, format: 'short' | 'long'): string {
  return format(new Date(date), FORMAT_OPTIONS[format]);
}

// Export
export default TimeAgo;
```

## Conclusion

This directory structure provides a clear organization for the Election Monitoring System frontend, with a focus on maintainability, scalability, and separation of concerns. The feature-based organization allows for easy navigation and understanding of the codebase, while the consistent naming conventions and import patterns ensure a consistent development experience.