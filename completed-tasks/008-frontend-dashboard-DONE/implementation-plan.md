# Frontend Dashboard Implementation - Step-by-Step Plan

## Overview

This document outlines a detailed implementation plan for the frontend dashboard. It breaks down the development process into logical phases and specific tasks, providing a clear roadmap for the development team.

## Phase 1: Project Setup and Configuration (1 day)

### 1.1 Install Required Dependencies

```bash
# Install shadcn/ui components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add select
npx shadcn@latest add input
npx shadcn@latest add tabs
npx shadcn@latest add table
npx shadcn@latest add dropdown-menu
npx shadcn@latest add sheet
npx shadcn@latest add skeleton
npx shadcn@latest add chart

# Install additional dependencies
npm install recharts axios date-fns react-router-dom zustand
```

### 1.2 Configure CSS Variables for Charts

Update `src/index.css` to include chart color variables:

```css
@layer base {
  :root {
    /* Existing variables */
    
    /* Chart colors */
    --chart-1: oklch(0.646 0.222 41.116);
    --chart-2: oklch(0.6 0.118 184.704);
    --chart-3: oklch(0.398 0.07 227.392);
    --chart-4: oklch(0.828 0.189 84.429);
    --chart-5: oklch(0.769 0.188 70.08);
  }

  .dark {
    /* Existing variables */
    
    /* Chart colors */
    --chart-1: oklch(0.488 0.243 264.376);
    --chart-2: oklch(0.696 0.17 162.48);
    --chart-3: oklch(0.769 0.188 70.08);
    --chart-4: oklch(0.627 0.265 303.9);
    --chart-5: oklch(0.645 0.246 16.439);
  }
}
```

### 1.3 Set Up Project Structure

Create the directory structure as defined in the file-structure.md document:

```bash
mkdir -p src/components/{dashboard,metrics,constituencies,ui}
mkdir -p src/hooks
mkdir -p src/store
mkdir -p src/lib
mkdir -p src/types
mkdir -p src/pages
```

### 1.4 Configure Routing

Update `src/App.tsx` to include routing:

```tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ConstituencyDetail from './pages/ConstituencyDetail';
import ElectionOverview from './pages/ElectionOverview';
import AppLayout from './components/layout/AppLayout';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/constituencies/:id" element={<ConstituencyDetail />} />
          <Route path="/elections/:id" element={<ElectionOverview />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;
```

## Phase 2: Core Infrastructure (2 days)

### 2.1 Create Type Definitions

Create the TypeScript interfaces as defined in the interfaces.md document:

- `src/types/metrics.ts`
- `src/types/constituencies.ts`
- `src/types/elections.ts`
- `src/types/dashboard.ts`

### 2.2 Implement API Client

Create `src/lib/api.ts` with the API client implementation:

```typescript
import axios from 'axios';
import { MetricsFilter } from '../types/metrics';
import { ConstituencyFilter } from '../types/constituencies';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Implement API functions as defined in interfaces.md
export const metricsApi = {
  getDashboardMetrics: (options: MetricsFilter) => 
    api.get('/api/metrics/dashboard', { params: options }),
  
  getHourlyStats: (options: MetricsFilter) => 
    api.get('/api/metrics/hourly', { params: options }),
  
  // ... other metrics API functions
};

export const constituenciesApi = {
  getConstituencies: (options: ConstituencyFilter) => 
    api.get('/api/constituencies', { params: options }),
  
  getConstituencyById: (id: string) => 
    api.get(`/api/constituencies/${id}`),
};

export const electionsApi = {
  getElections: () => 
    api.get('/api/elections'),
  
  getElectionById: (id: string) => 
    api.get(`/api/elections/${id}`),
};

export default api;
```

### 2.3 Create Utility Functions

Create `src/lib/utils.ts` with utility functions:

```typescript
import { format, parseISO, subHours, subDays } from 'date-fns';
import { TimeRange } from '../types/metrics';

export function formatDate(date: string, formatString: string = 'MMM d, yyyy'): string {
  return format(parseISO(date), formatString);
}

export function formatNumber(num: number, options: Intl.NumberFormatOptions = {}): string {
  return new Intl.NumberFormat('en-US', options).format(num);
}

export function formatPercentage(num: number, decimals: number = 1): string {
  return `${num.toFixed(decimals)}%`;
}

export function getTimeRangeDate(timeRange: TimeRange): { start: Date, end: Date } {
  const end = new Date();
  let start: Date;

  if (timeRange.start.includes('hour')) {
    const hours = parseInt(timeRange.start.split(' ')[0]);
    start = subHours(end, hours);
  } else if (timeRange.start.includes('day')) {
    const days = parseInt(timeRange.start.split(' ')[0]);
    start = subDays(end, days);
  } else {
    start = parseISO(timeRange.start);
  }

  return { start, end };
}

export function cn(...classes: (string | undefined | boolean)[]): string {
  return classes.filter(Boolean).join(' ');
}
```

### 2.4 Create Constants

Create `src/lib/constants.ts` with constants:

```typescript
import { TimeRange } from '../types/metrics';
import { type ChartConfig } from "@/components/ui/chart";

export const DEFAULT_TIME_RANGES: TimeRange[] = [
  {
    label: 'Last Hour',
    start: '1 hour ago',
    end: 'now',
  },
  // ... other time ranges as defined in interfaces.md
];

export const DEFAULT_TIME_RANGE = DEFAULT_TIME_RANGES[3]; // Last 24 Hours

export const TRANSACTION_CHART_CONFIG: ChartConfig = {
  transactions: {
    label: "Transactions",
    color: "var(--chart-1)"
  },
  // ... other chart configs as defined in interfaces.md
};

// ... other chart configs
```

### 2.5 Implement Zustand Stores

Create store files:

- `src/store/metrics.ts`
- `src/store/constituencies.ts`
- `src/store/elections.ts`
- `src/store/dashboard.ts`
- `src/store/index.ts`

Example implementation for metrics store:

```typescript
import { create } from 'zustand';
import { metricsApi } from '../lib/api';
import { DashboardMetrics, MetricsFilter } from '../types/metrics';
import { MetricsState, MetricsActions } from '../types/store';

export const useMetricsStore = create<MetricsState & MetricsActions>((set) => ({
  metrics: null,
  isLoading: false,
  error: null,
  lastUpdated: null,

  fetchMetrics: async (options: MetricsFilter) => {
    set({ isLoading: true, error: null });
    try {
      const response = await metricsApi.getDashboardMetrics(options);
      set({ 
        metrics: response.data, 
        isLoading: false,
        lastUpdated: new Date().toISOString()
      });
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error : new Error('Unknown error') 
      });
    }
  },

  setMetrics: (metrics: DashboardMetrics) => set({ metrics }),
  setLoading: (isLoading: boolean) => set({ isLoading }),
  setError: (error: Error | null) => set({ error }),
  reset: () => set({ metrics: null, isLoading: false, error: null, lastUpdated: null }),
}));
```

### 2.6 Implement Custom Hooks

Create hook files:

- `src/hooks/useMetrics.ts`
- `src/hooks/useConstituencies.ts`
- `src/hooks/useElections.ts`
- `src/hooks/useDashboard.ts`

Example implementation for useMetrics hook:

```typescript
import { useEffect, useCallback } from 'react';
import { useMetricsStore } from '../store/metrics';
import { UseMetricsOptions, UseMetricsResult } from '../types/hooks';

export function useMetrics(options: UseMetricsOptions): UseMetricsResult {
  const { 
    metrics, 
    isLoading, 
    error, 
    fetchMetrics, 
    reset 
  } = useMetricsStore();

  const refetch = useCallback(() => {
    return fetchMetrics(options);
  }, [fetchMetrics, options]);

  useEffect(() => {
    refetch();

    if (options.refresh_interval) {
      const intervalId = setInterval(refetch, options.refresh_interval * 1000);
      return () => clearInterval(intervalId);
    }
  }, [refetch, options.refresh_interval]);

  useEffect(() => {
    return () => {
      reset();
    };
  }, [reset]);

  return {
    metrics,
    isLoading,
    error,
    refetch,
  };
}
```

## Phase 3: UI Components (3 days)

### 3.1 Implement Layout Components

Create layout components:

- `src/components/layout/AppLayout.tsx`
- `src/components/layout/Header.tsx`
- `src/components/layout/Sidebar.tsx`

### 3.2 Implement Dashboard Components

Create dashboard components:

- `src/components/dashboard/DashboardHeader.tsx`
- `src/components/dashboard/DashboardLayout.tsx`
- `src/components/dashboard/MetricsSummary.tsx`
- `src/components/dashboard/ActivityTimeline.tsx`
- `src/components/dashboard/ConstituencyOverview.tsx`
- `src/components/dashboard/DashboardFooter.tsx`

Example implementation for MetricsSummary:

```tsx
import { MetricsSummaryProps } from '../../types/props';
import { MetricCard } from '../metrics/MetricCard';
import { MetricsGrid } from '../metrics/MetricsGrid';
import { Skeleton } from '../ui/skeleton';
import { cn } from '../../lib/utils';

export function MetricsSummary({ metrics, isLoading, className }: MetricsSummaryProps) {
  if (isLoading) {
    return (
      <div className={cn('space-y-4', className)}>
        <h2 className="text-xl font-semibold">Summary</h2>
        <MetricsGrid>
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-[120px] w-full" />
          ))}
        </MetricsGrid>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className={cn('space-y-4', className)}>
      <h2 className="text-xl font-semibold">Summary</h2>
      <MetricsGrid>
        <MetricCard metric={metrics.total_transactions} />
        <MetricCard metric={metrics.total_bulletins} />
        <MetricCard metric={metrics.total_votes} />
        <MetricCard metric={metrics.participation_rate} />
        <MetricCard metric={metrics.active_constituencies} />
        <MetricCard metric={metrics.anomalies_detected} />
      </MetricsGrid>
    </div>
  );
}
```

### 3.3 Implement Metrics Components

Create metrics components:

- `src/components/metrics/MetricCard.tsx`
- `src/components/metrics/MetricsGrid.tsx`
- `src/components/metrics/ParticipationRateChart.tsx`
- `src/components/metrics/TransactionVolumeChart.tsx`
- `src/components/metrics/HourlyActivityChart.tsx`

Example implementation for TransactionVolumeChart:

```tsx
import { TransactionVolumeChartProps } from '../../types/props';
import { 
  Bar, 
  BarChart, 
  CartesianGrid, 
  XAxis, 
  YAxis, 
  ResponsiveContainer 
} from 'recharts';
import { 
  ChartContainer, 
  ChartTooltip, 
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent
} from '../ui/chart';
import { TRANSACTION_CHART_CONFIG } from '../../lib/constants';
import { formatDate } from '../../lib/utils';
import { Skeleton } from '../ui/skeleton';

export function TransactionVolumeChart({ data, isLoading, className }: TransactionVolumeChartProps) {
  if (isLoading) {
    return <Skeleton className="h-[300px] w-full" />;
  }

  if (!data || data.length === 0) {
    return <div className="h-[300px] w-full flex items-center justify-center">No data available</div>;
  }

  const formattedData = data.map(item => ({
    ...item,
    timestamp: formatDate(item.timestamp, 'HH:mm'),
  }));

  return (
    <ChartContainer config={TRANSACTION_CHART_CONFIG} className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={formattedData} accessibilityLayer>
          <CartesianGrid vertical={false} strokeDasharray="3 3" />
          <XAxis 
            dataKey="timestamp" 
            tickLine={false} 
            axisLine={false}
            tickMargin={10}
          />
          <YAxis 
            tickLine={false} 
            axisLine={false}
            tickMargin={10}
          />
          <ChartTooltip content={<ChartTooltipContent />} />
          <ChartLegend content={<ChartLegendContent />} />
          <Bar 
            dataKey="transaction_count" 
            fill="var(--chart-1)" 
            radius={[4, 4, 0, 0]} 
            name="Transactions"
          />
          <Bar 
            dataKey="bulletins_issued" 
            fill="var(--chart-2)" 
            radius={[4, 4, 0, 0]} 
            name="Bulletins Issued"
          />
          <Bar 
            dataKey="votes_cast" 
            fill="var(--chart-3)" 
            radius={[4, 4, 0, 0]} 
            name="Votes Cast"
          />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
```

### 3.4 Implement Constituency Components

Create constituency components:

- `src/components/constituencies/ConstituencyTable.tsx`
- `src/components/constituencies/ConstituencyFilters.tsx`
- `src/components/constituencies/ConstituencySearch.tsx`
- `src/components/constituencies/ConstituencyCard.tsx`

## Phase 4: Page Components (2 days)

### 4.1 Implement Dashboard Page

Create `src/pages/Dashboard.tsx`:

```tsx
import { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';
import { DashboardHeader } from '../components/dashboard/DashboardHeader';
import { MetricsSummary } from '../components/dashboard/MetricsSummary';
import { ActivityTimeline } from '../components/dashboard/ActivityTimeline';
import { ConstituencyOverview } from '../components/dashboard/ConstituencyOverview';
import { DashboardFooter } from '../components/dashboard/DashboardFooter';
import { useElectionsStore } from '../store/elections';
import { useDashboardStore } from '../store/dashboard';
import { useMetrics } from '../hooks/useMetrics';
import { useConstituencies } from '../hooks/useConstituencies';
import { DEFAULT_TIME_RANGE } from '../lib/constants';

export default function Dashboard() {
  const { 
    elections, 
    selectedElection, 
    isLoading: electionsLoading, 
    fetchElections, 
    selectElection 
  } = useElectionsStore();
  
  const { 
    timeRange, 
    setTimeRange, 
    refreshInterval, 
    setLastUpdated 
  } = useDashboardStore();

  // Set default time range if not already set
  useEffect(() => {
    if (!timeRange) {
      setTimeRange(DEFAULT_TIME_RANGE);
    }
  }, [timeRange, setTimeRange]);

  // Fetch elections on mount
  useEffect(() => {
    fetchElections();
  }, [fetchElections]);

  // Select first election if none selected
  useEffect(() => {
    if (!selectedElection && elections.length > 0) {
      selectElection(elections[0]);
    }
  }, [elections, selectedElection, selectElection]);

  // Fetch metrics and constituencies based on selected election and time range
  const { 
    metrics, 
    isLoading: metricsLoading 
  } = useMetrics({
    election_id: selectedElection?.id || '',
    time_range: timeRange || DEFAULT_TIME_RANGE,
    refresh_interval: refreshInterval
  });

  const { 
    constituencies, 
    isLoading: constituenciesLoading,
    filters,
    setFilters
  } = useConstituencies({
    election_id: selectedElection?.id || '',
    refresh_interval: refreshInterval
  });

  // Update last updated timestamp when data is refreshed
  useEffect(() => {
    if (metrics) {
      setLastUpdated(new Date().toISOString());
    }
  }, [metrics, setLastUpdated]);

  const handleElectionChange = (election) => {
    selectElection(election);
  };

  const handleTimeRangeChange = (newTimeRange) => {
    setTimeRange(newTimeRange);
  };

  const isLoading = electionsLoading || metricsLoading || constituenciesLoading;

  return (
    <DashboardLayout>
      <DashboardHeader
        title="Election Monitoring Dashboard"
        elections={elections}
        selectedElection={selectedElection}
        timeRange={timeRange || DEFAULT_TIME_RANGE}
        onElectionChange={handleElectionChange}
        onTimeRangeChange={handleTimeRangeChange}
      />
      
      <div className="space-y-8 py-8">
        <MetricsSummary 
          metrics={metrics?.summary} 
          isLoading={isLoading} 
        />
        
        <ActivityTimeline 
          data={metrics?.transaction_volumes || []} 
          timeRange={timeRange || DEFAULT_TIME_RANGE}
          isLoading={isLoading} 
        />
        
        <ConstituencyOverview 
          constituencies={constituencies} 
          isLoading={isLoading}
          filters={filters}
          onFilterChange={setFilters}
          onConstituencySelect={(constituency) => {
            // Navigate to constituency detail page
            window.location.href = `/constituencies/${constituency.id}`;
          }}
        />
      </div>
      
      <DashboardFooter />
    </DashboardLayout>
  );
}
```

### 4.2 Implement Constituency Detail Page

Create `src/pages/ConstituencyDetail.tsx`.

### 4.3 Implement Election Overview Page

Create `src/pages/ElectionOverview.tsx`.

## Phase 5: Integration and Testing (2 days)

### 5.1 Create Mock Data for Development

Create `src/lib/mock-data.ts` with mock data for development:

```typescript
import { MockDataOptions, MockData } from '../types/mock';
import { 
  Election, 
  Constituency, 
  HourlyStat, 
  ParticipationRate, 
  TransactionVolume, 
  HourlyActivity 
} from '../types';
import { subHours, addHours, format } from 'date-fns';

export function generateMockData(options: MockDataOptions = {}): MockData {
  const {
    election_count = 3,
    constituency_count = 20,
    hourly_stats_count = 24,
    start_date = subHours(new Date(), 24).toISOString(),
    end_date = new Date().toISOString(),
  } = options;

  // Generate mock elections
  const elections: Election[] = Array.from({ length: election_count }).map((_, i) => ({
    id: `election-${i + 1}`,
    name: `Election ${i + 1}`,
    date: new Date().toISOString(),
    status: i === 0 ? 'active' : i === 1 ? 'upcoming' : 'completed',
    constituency_count,
    registered_voters: 1000000 + i * 100000,
    bulletins_issued: 600000 + i * 50000,
    votes_cast: 550000 + i * 45000,
    transaction_count: 700000 + i * 60000,
    participation_rate: 55 + i * 2,
    anomaly_count: Math.floor(Math.random() * 10),
  }));

  // Generate mock constituencies
  const constituencies: Constituency[] = [];
  for (let e = 0; e < election_count; e++) {
    for (let i = 0; i < constituency_count; i++) {
      const registered_voters = 5000 + Math.floor(Math.random() * 15000);
      const bulletins_issued = Math.floor(registered_voters * (0.4 + Math.random() * 0.4));
      const votes_cast = Math.floor(bulletins_issued * (0.9 + Math.random() * 0.1));
      
      constituencies.push({
        id: `constituency-${e + 1}-${i + 1}`,
        name: `Constituency ${e + 1}-${i + 1}`,
        code: `C${e + 1}${i + 1}`,
        region_id: `region-${Math.floor(i / 5) + 1}`,
        region_name: `Region ${Math.floor(i / 5) + 1}`,
        election_id: `election-${e + 1}`,
        registered_voters,
        bulletins_issued,
        votes_cast,
        transaction_count: bulletins_issued + votes_cast + Math.floor(Math.random() * 1000),
        participation_rate: (votes_cast / registered_voters) * 100,
        anomaly_count: Math.floor(Math.random() * 5),
        last_activity: new Date().toISOString(),
      });
    }
  }

  // Generate hourly stats
  const hourly_stats: HourlyStat[] = [];
  const participation_rates: ParticipationRate[] = [];
  const transaction_volumes: TransactionVolume[] = [];
  const hourly_activity: HourlyActivity[] = [];

  // Generate hourly data for each constituency
  for (const constituency of constituencies) {
    const start = new Date(start_date);
    const end = new Date(end_date);
    const hours = Math.floor((end.getTime() - start.getTime()) / (60 * 60 * 1000));
    
    for (let h = 0; h < Math.min(hours, hourly_stats_count); h++) {
      const timestamp = addHours(start, h).toISOString();
      const registered_voters = constituency.registered_voters;
      const bulletins_issued = Math.floor((constituency.bulletins_issued / hours) * (0.8 + Math.random() * 0.4));
      const votes_cast = Math.floor((constituency.votes_cast / hours) * (0.8 + Math.random() * 0.4));
      const transaction_count = bulletins_issued + votes_cast + Math.floor(Math.random() * 50);
      
      hourly_stats.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        bulletins_issued,
        votes_cast,
        transaction_count,
        participation_rate: (votes_cast / registered_voters) * 100,
        anomaly_count: Math.random() > 0.9 ? Math.floor(Math.random() * 3) : 0,
      });

      participation_rates.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        participation_rate: (votes_cast / registered_voters) * 100,
        registered_voters,
        votes_cast,
      });

      transaction_volumes.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        transaction_count,
        bulletins_issued,
        votes_cast,
      });
    }

    // Generate hourly activity (by hour of day)
    for (let h = 0; h < 24; h++) {
      const hour = h;
      const transaction_count = Math.floor(Math.random() * 1000);
      const bulletins_issued = Math.floor(transaction_count * 0.4);
      const votes_cast = Math.floor(transaction_count * 0.35);
      
      hourly_activity.push({
        hour,
        transaction_count,
        bulletins_issued,
        votes_cast,
      });
    }
  }

  return {
    elections,
    constituencies,
    hourly_stats,
    participation_rates,
    transaction_volumes,
    hourly_activity,
  };
}
```

### 5.2 Implement API Mocking

Create `src/lib/mock-api.ts` to mock API responses during development:

```typescript
import { rest } from 'msw';
import { setupWorker } from 'msw/browser';
import { generateMockData } from './mock-data';

const mockData = generateMockData();

export const handlers = [
  // Metrics API
  rest.get('/api/metrics/dashboard', (req, res, ctx) => {
    const election_id = req.url.searchParams.get('election_id');
    
    if (!election_id) {
      return res(ctx.status(400), ctx.json({ error: 'election_id is required' }));
    }

    const election = mockData.elections.find(e => e.id === election_id);
    
    if (!election) {
      return res(ctx.status(404), ctx.json({ error: 'Election not found' }));
    }

    const constituency_id = req.url.searchParams.get('constituency_id');
    
    // Filter data based on constituency_id if provided
    const filteredHourlyStats = mockData.hourly_stats.filter(
      stat => stat.election_id === election_id && 
      (!constituency_id || stat.constituency_id === constituency_id)
    );
    
    const filteredParticipationRates = mockData.participation_rates.filter(
      rate => rate.election_id === election_id && 
      (!constituency_id || rate.constituency_id === constituency_id)
    );
    
    const filteredTransactionVolumes = mockData.transaction_volumes.filter(
      vol => vol.election_id === election_id && 
      (!constituency_id || vol.constituency_id === constituency_id)
    );

    // Calculate summary metrics
    const total_transactions = filteredTransactionVolumes.reduce((sum, vol) => sum + vol.transaction_count, 0);
    const total_bulletins = filteredTransactionVolumes.reduce((sum, vol) => sum + vol.bulletins_issued, 0);
    const total_votes = filteredTransactionVolumes.reduce((sum, vol) => sum + vol.votes_cast, 0);
    const participation_rate = election.participation_rate;
    const active_constituencies = mockData.constituencies.filter(c => c.election_id === election_id).length;
    const anomalies_detected = filteredHourlyStats.reduce((sum, stat) => sum + stat.anomaly_count, 0);

    return res(
      ctx.status(200),
      ctx.json({
        summary: {
          total_transactions: {
            id: 'total-transactions',
            label: 'Total Transactions',
            value: total_transactions,
            trend: 2.5,
            trendLabel: 'vs. previous period',
            icon: 'activity',
          },
          total_bulletins: {
            id: 'total-bulletins',
            label: 'Bulletins Issued',
            value: total_bulletins,
            trend: 1.8,
            trendLabel: 'vs. previous period',
            icon: 'file-text',
          },
          total_votes: {
            id: 'total-votes',
            label: 'Votes Cast',
            value: total_votes,
            trend: 3.2,
            trendLabel: 'vs. previous period',
            icon: 'check-square',
          },
          participation_rate: {
            id: 'participation-rate',
            label: 'Participation Rate',
            value: participation_rate,
            trend: 0.5,
            trendLabel: 'vs. previous period',
            icon: 'percent',
          },
          active_constituencies: {
            id: 'active-constituencies',
            label: 'Active Constituencies',
            value: active_constituencies,
            trend: 0,
            trendLabel: 'vs. previous period',
            icon: 'map-pin',
          },
          anomalies_detected: {
            id: 'anomalies-detected',
            label: 'Anomalies Detected',
            value: anomalies_detected,
            trend: -1.2,
            trendLabel: 'vs. previous period',
            icon: 'alert-triangle',
          },
        },
        hourly_stats: filteredHourlyStats,
        participation_rates: filteredParticipationRates,
        transaction_volumes: filteredTransactionVolumes,
        hourly_activity: mockData.hourly_activity,
      })
    );
  }),

  // ... other API handlers
];

export const worker = setupWorker(...handlers);
```

### 5.3 