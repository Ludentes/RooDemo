# Frontend Dashboard Implementation - Component Architecture

## Overview

This document outlines the component architecture for the frontend dashboard implementation. It defines the structure of components, their relationships, and how they interact with the backend API. The dashboard will provide users with a comprehensive view of election monitoring data, including metrics, statistics, and constituency information.

## Technology Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui
- **State Management**: Zustand
- **Charts**: Recharts with shadcn/ui chart components
- **Routing**: React Router

## Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── DashboardHeader.tsx
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── MetricsSummary.tsx
│   │   │   ├── ActivityTimeline.tsx
│   │   │   ├── ConstituencyOverview.tsx
│   │   │   └── DashboardFooter.tsx
│   │   ├── metrics/
│   │   │   ├── MetricCard.tsx
│   │   │   ├── MetricsGrid.tsx
│   │   │   ├── ParticipationRateChart.tsx
│   │   │   ├── TransactionVolumeChart.tsx
│   │   │   └── HourlyActivityChart.tsx
│   │   ├── constituencies/
│   │   │   ├── ConstituencyTable.tsx
│   │   │   ├── ConstituencyFilters.tsx
│   │   │   ├── ConstituencySearch.tsx
│   │   │   └── ConstituencyCard.tsx
│   │   └── ui/
│   │       └── [shadcn/ui components]
│   ├── hooks/
│   │   ├── useMetrics.ts
│   │   ├── useConstituencies.ts
│   │   ├── useElections.ts
│   │   └── useDashboard.ts
│   ├── store/
│   │   ├── metrics.ts
│   │   ├── constituencies.ts
│   │   ├── elections.ts
│   │   ├── dashboard.ts
│   │   └── index.ts
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   ├── types/
│   │   ├── metrics.ts
│   │   ├── constituencies.ts
│   │   ├── elections.ts
│   │   └── dashboard.ts
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── ConstituencyDetail.tsx
│   │   └── ElectionOverview.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
```

## Component Hierarchy

```
App
└── AppLayout
    ├── Header
    ├── Sidebar
    └── Main Content
        ├── Dashboard
        │   ├── DashboardHeader
        │   │   ├── ElectionSelector
        │   │   └── TimeRangeSelector
        │   ├── MetricsSummary
        │   │   ├── MetricCard (multiple)
        │   │   └── MetricsGrid
        │   ├── ActivityTimeline
        │   │   ├── TimelineChart
        │   │   └── TimelineControls
        │   ├── ConstituencyOverview
        │   │   ├── ConstituencyTable
        │   │   ├── ConstituencyFilters
        │   │   └── ConstituencySearch
        │   └── DashboardFooter
        │       └── DataLastUpdated
        ├── ConstituencyDetail
        │   ├── ConstituencyHeader
        │   ├── ConstituencyMetrics
        │   ├── TransactionHistory
        │   └── HourlyStatistics
        └── ElectionOverview
            ├── ElectionHeader
            ├── ElectionMetrics
            ├── ConstituencyComparison
            └── ElectionTimeline
```

## Key Components

### Dashboard Components

#### DashboardLayout
- **Purpose**: Serves as the container for all dashboard components
- **Props**: `children`, `className`
- **State**: None
- **Dependencies**: None

#### DashboardHeader
- **Purpose**: Displays the dashboard title and provides controls for selecting elections and time ranges
- **Props**: `title`, `onElectionChange`, `onTimeRangeChange`
- **State**: `selectedElection`, `selectedTimeRange`
- **Dependencies**: `ElectionSelector`, `TimeRangeSelector`

#### MetricsSummary
- **Purpose**: Displays a grid of metric cards showing key statistics
- **Props**: `metrics`, `className`
- **State**: None
- **Dependencies**: `MetricCard`, `MetricsGrid`

#### ActivityTimeline
- **Purpose**: Displays a timeline chart of activity over time
- **Props**: `data`, `timeRange`, `className`
- **State**: `selectedTimePoint`
- **Dependencies**: `TimelineChart`, `TimelineControls`

#### ConstituencyOverview
- **Purpose**: Displays a table of constituencies with key metrics
- **Props**: `constituencies`, `onConstituencySelect`, `className`
- **State**: `filters`, `searchQuery`, `sortColumn`, `sortDirection`
- **Dependencies**: `ConstituencyTable`, `ConstituencyFilters`, `ConstituencySearch`

### Metrics Components

#### MetricCard
- **Purpose**: Displays a single metric with label, value, and trend indicator
- **Props**: `label`, `value`, `trend`, `trendLabel`, `icon`, `className`
- **State**: None
- **Dependencies**: shadcn/ui `Card`, `CardHeader`, `CardContent`, `CardFooter`

#### MetricsGrid
- **Purpose**: Arranges metric cards in a responsive grid
- **Props**: `children`, `className`
- **State**: None
- **Dependencies**: None

#### ParticipationRateChart
- **Purpose**: Displays a chart showing participation rates over time
- **Props**: `data`, `className`
- **State**: None
- **Dependencies**: Recharts, shadcn/ui chart components

#### TransactionVolumeChart
- **Purpose**: Displays a chart showing transaction volumes over time
- **Props**: `data`, `className`
- **State**: None
- **Dependencies**: Recharts, shadcn/ui chart components

#### HourlyActivityChart
- **Purpose**: Displays a chart showing activity by hour of day
- **Props**: `data`, `className`
- **State**: None
- **Dependencies**: Recharts, shadcn/ui chart components

### Constituency Components

#### ConstituencyTable
- **Purpose**: Displays a table of constituencies with key metrics
- **Props**: `constituencies`, `onConstituencySelect`, `sortColumn`, `sortDirection`, `onSort`, `className`
- **State**: None
- **Dependencies**: shadcn/ui `Table` components

#### ConstituencyFilters
- **Purpose**: Provides filters for the constituency table
- **Props**: `filters`, `onFilterChange`, `className`
- **State**: None
- **Dependencies**: shadcn/ui `Select`, `Checkbox` components

#### ConstituencySearch
- **Purpose**: Provides search functionality for the constituency table
- **Props**: `searchQuery`, `onSearchChange`, `className`
- **State**: None
- **Dependencies**: shadcn/ui `Input` component

#### ConstituencyCard
- **Purpose**: Displays a card with key information about a constituency
- **Props**: `constituency`, `className`
- **State**: None
- **Dependencies**: shadcn/ui `Card` components

## Chart Components

We'll use Recharts with shadcn/ui chart components for visualizations. The key chart components include:

### ChartContainer
- **Purpose**: Provides a container for charts with consistent styling
- **Usage**:
```tsx
<ChartContainer config={chartConfig} className="h-[200px] w-full">
  <BarChart data={chartData}>
    {/* Chart components */}
  </BarChart>
</ChartContainer>
```

### ChartTooltip
- **Purpose**: Provides tooltips for chart data points
- **Usage**:
```tsx
<ChartTooltip content={<ChartTooltipContent />} />
```

### ChartLegend
- **Purpose**: Provides a legend for chart data series
- **Usage**:
```tsx
<ChartLegend content={<ChartLegendContent />} />
```

## Chart Configuration

We'll define chart configurations using the `ChartConfig` type from shadcn/ui:

```tsx
import { type ChartConfig } from "@/components/ui/chart"

const chartConfig = {
  transactions: {
    label: "Transactions",
    color: "var(--chart-1)"
  },
  bulletins: {
    label: "Bulletins Issued",
    color: "var(--chart-2)"
  },
  votes: {
    label: "Votes Cast",
    color: "var(--chart-3)"
  }
} satisfies ChartConfig
```

## CSS Variables for Chart Colors

We'll define CSS variables for chart colors in our global CSS:

```css
@layer base {
  :root {
    --chart-1: oklch(0.646 0.222 41.116);
    --chart-2: oklch(0.6 0.118 184.704);
    --chart-3: oklch(0.398 0.07 227.392);
    --chart-4: oklch(0.828 0.189 84.429);
    --chart-5: oklch(0.769 0.188 70.08);
  }

  .dark {
    --chart-1: oklch(0.488 0.243 264.376);
    --chart-2: oklch(0.696 0.17 162.48);
    --chart-3: oklch(0.769 0.188 70.08);
    --chart-4: oklch(0.627 0.265 303.9);
    --chart-5: oklch(0.645 0.246 16.439);
  }
}
```

## State Management

We'll use Zustand for state management with the following stores:

### metricsStore
- **Purpose**: Manages metrics data and loading states
- **State**:
  - `metrics`: Object containing metrics data
  - `isLoading`: Boolean indicating if metrics are loading
  - `error`: Error object if metrics fetch fails
- **Actions**:
  - `fetchMetrics`: Fetches metrics data from the API
  - `setMetrics`: Sets metrics data in the store
  - `setLoading`: Sets loading state
  - `setError`: Sets error state

### constituenciesStore
- **Purpose**: Manages constituencies data and loading states
- **State**:
  - `constituencies`: Array of constituency objects
  - `isLoading`: Boolean indicating if constituencies are loading
  - `error`: Error object if constituencies fetch fails
  - `filters`: Object containing active filters
  - `searchQuery`: String containing search query
  - `sortColumn`: String indicating column to sort by
  - `sortDirection`: String indicating sort direction
- **Actions**:
  - `fetchConstituencies`: Fetches constituencies data from the API
  - `setConstituencies`: Sets constituencies data in the store
  - `setLoading`: Sets loading state
  - `setError`: Sets error state
  - `setFilters`: Sets filter state
  - `setSearchQuery`: Sets search query
  - `setSortColumn`: Sets sort column
  - `setSortDirection`: Sets sort direction

### electionsStore
- **Purpose**: Manages elections data and loading states
- **State**:
  - `elections`: Array of election objects
  - `selectedElection`: Object containing selected election
  - `isLoading`: Boolean indicating if elections are loading
  - `error`: Error object if elections fetch fails
- **Actions**:
  - `fetchElections`: Fetches elections data from the API
  - `setElections`: Sets elections data in the store
  - `selectElection`: Sets selected election
  - `setLoading`: Sets loading state
  - `setError`: Sets error state

### dashboardStore
- **Purpose**: Manages dashboard-specific state
- **State**:
  - `timeRange`: Object containing selected time range
  - `refreshInterval`: Number indicating refresh interval in seconds
  - `lastUpdated`: Date object indicating when data was last updated
- **Actions**:
  - `setTimeRange`: Sets time range
  - `setRefreshInterval`: Sets refresh interval
  - `setLastUpdated`: Sets last updated timestamp
  - `refreshData`: Triggers refresh of all dashboard data

## API Integration

We'll create a centralized API client in `lib/api.ts` with the following structure:

```typescript
// lib/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const metricsApi = {
  getDashboardMetrics: (electionId: string, timeRange: string) => 
    api.get(`/api/metrics/dashboard?election_id=${electionId}&time_range=${timeRange}`),
  
  getHourlyStats: (electionId: string, constituencyId?: string) => 
    api.get(`/api/metrics/hourly?election_id=${electionId}${constituencyId ? `&constituency_id=${constituencyId}` : ''}`),
  
  getParticipationRates: (electionId: string, constituencyId?: string) => 
    api.get(`/api/metrics/participation?election_id=${electionId}${constituencyId ? `&constituency_id=${constituencyId}` : ''}`),
};

export const constituenciesApi = {
  getConstituencies: (electionId: string, filters?: Record<string, any>) => 
    api.get(`/api/constituencies?election_id=${electionId}`, { params: filters }),
  
  getConstituencyById: (constituencyId: string) => 
    api.get(`/api/constituencies/${constituencyId}`),
};

export const electionsApi = {
  getElections: () => 
    api.get('/api/elections'),
  
  getElectionById: (electionId: string) => 
    api.get(`/api/elections/${electionId}`),
};

export default api;
```

## Data Flow

1. User loads the dashboard page
2. `Dashboard` component mounts and initializes
3. `electionsStore.fetchElections()` is called to load available elections
4. Once elections are loaded, the first election is selected by default
5. `dashboardStore.setTimeRange()` is called with a default time range
6. Based on the selected election and time range:
   - `metricsStore.fetchMetrics()` is called to load metrics data
   - `constituenciesStore.fetchConstituencies()` is called to load constituencies data
7. As data is loaded, components update to display the data
8. User interactions (changing elections, time ranges, filters, etc.) trigger appropriate store actions
9. Store actions update state and may trigger new API calls
10. Components react to state changes and update accordingly

## Responsive Design

The dashboard will be fully responsive with different layouts for:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

We'll use Tailwind CSS's responsive utilities to implement these layouts:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Metric cards */}
</div>
```

## Accessibility

All components will be built with accessibility in mind:
- Proper semantic HTML
- ARIA attributes where necessary
- Keyboard navigation
- Screen reader support
- Sufficient color contrast

For charts, we'll use the `accessibilityLayer` prop provided by Recharts:

```tsx
<LineChart accessibilityLayer data={chartData}>
  {/* Chart components */}
</LineChart>
```

## Performance Considerations

- Use of React.memo for pure components
- Virtualization for long lists (react-window)
- Debounced search inputs
- Optimistic UI updates
- Caching of API responses
- Lazy loading of components
- Code splitting for routes

## Next Steps

1. Set up the basic dashboard layout
2. Implement the API client
3. Create Zustand stores
4. Implement core dashboard components
5. Add chart components
6. Implement filtering and sorting
7. Add responsive behavior
8. Implement error handling and loading states