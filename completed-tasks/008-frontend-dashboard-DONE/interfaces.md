# Frontend Dashboard Implementation - Interfaces

## Overview

This document defines the interfaces between the frontend dashboard components and the backend API. It includes TypeScript interfaces for data structures and API endpoint specifications.

## Data Interfaces

### Metrics Interfaces

```typescript
// types/metrics.ts

export interface Metric {
  id: string;
  label: string;
  value: number;
  trend: number; // Percentage change
  trendLabel: string;
  icon?: string;
}

export interface HourlyStat {
  timestamp: string;
  constituency_id: string;
  election_id: string;
  bulletins_issued: number;
  votes_cast: number;
  transaction_count: number;
  participation_rate: number;
  anomaly_count: number;
}

export interface ParticipationRate {
  timestamp: string;
  constituency_id: string;
  election_id: string;
  participation_rate: number;
  registered_voters: number;
  votes_cast: number;
}

export interface TransactionVolume {
  timestamp: string;
  constituency_id: string;
  election_id: string;
  transaction_count: number;
  bulletins_issued: number;
  votes_cast: number;
}

export interface HourlyActivity {
  hour: number;
  transaction_count: number;
  bulletins_issued: number;
  votes_cast: number;
}

export interface DashboardMetrics {
  summary: {
    total_transactions: Metric;
    total_bulletins: Metric;
    total_votes: Metric;
    participation_rate: Metric;
    active_constituencies: Metric;
    anomalies_detected: Metric;
  };
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}

export interface TimeRange {
  start: string;
  end: string;
  label: string;
}

export interface MetricsFilter {
  election_id: string;
  constituency_id?: string;
  time_range: TimeRange;
}
```

### Constituency Interfaces

```typescript
// types/constituencies.ts

export interface Constituency {
  id: string;
  name: string;
  code: string;
  region_id: string;
  region_name: string;
  election_id: string;
  registered_voters: number;
  bulletins_issued: number;
  votes_cast: number;
  transaction_count: number;
  participation_rate: number;
  anomaly_count: number;
  last_activity: string;
}

export interface ConstituencyDetail extends Constituency {
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}

export interface ConstituencyFilter {
  election_id: string;
  region_id?: string;
  search?: string;
  min_participation_rate?: number;
  max_participation_rate?: number;
  has_anomalies?: boolean;
  sort_by?: string;
  sort_direction?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
}
```

### Election Interfaces

```typescript
// types/elections.ts

export interface Election {
  id: string;
  name: string;
  date: string;
  status: 'upcoming' | 'active' | 'completed';
  constituency_count: number;
  registered_voters: number;
  bulletins_issued: number;
  votes_cast: number;
  transaction_count: number;
  participation_rate: number;
  anomaly_count: number;
}

export interface ElectionDetail extends Election {
  constituencies: Constituency[];
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}
```

### Dashboard Interfaces

```typescript
// types/dashboard.ts

export interface DashboardState {
  selectedElection: Election | null;
  timeRange: TimeRange;
  refreshInterval: number;
  lastUpdated: string;
}

export interface DashboardFilter {
  election_id: string;
  time_range: TimeRange;
}
```

## API Endpoints

### Metrics API

#### Get Dashboard Metrics

- **Endpoint**: `GET /api/metrics/dashboard`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `time_range` (optional): Time range in format `start_date,end_date`
  - `constituency_id` (optional): ID of the constituency
- **Response**: `DashboardMetrics`

#### Get Hourly Stats

- **Endpoint**: `GET /api/metrics/hourly`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `constituency_id` (optional): ID of the constituency
  - `start_date` (optional): Start date in ISO format
  - `end_date` (optional): End date in ISO format
- **Response**: `HourlyStat[]`

#### Get Participation Rates

- **Endpoint**: `GET /api/metrics/participation`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `constituency_id` (optional): ID of the constituency
  - `start_date` (optional): Start date in ISO format
  - `end_date` (optional): End date in ISO format
- **Response**: `ParticipationRate[]`

#### Get Transaction Volumes

- **Endpoint**: `GET /api/metrics/transactions`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `constituency_id` (optional): ID of the constituency
  - `start_date` (optional): Start date in ISO format
  - `end_date` (optional): End date in ISO format
- **Response**: `TransactionVolume[]`

#### Get Hourly Activity

- **Endpoint**: `GET /api/metrics/hourly-activity`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `constituency_id` (optional): ID of the constituency
  - `date` (optional): Date in ISO format
- **Response**: `HourlyActivity[]`

### Constituencies API

#### Get Constituencies

- **Endpoint**: `GET /api/constituencies`
- **Query Parameters**:
  - `election_id` (required): ID of the election
  - `region_id` (optional): ID of the region
  - `search` (optional): Search query
  - `min_participation_rate` (optional): Minimum participation rate
  - `max_participation_rate` (optional): Maximum participation rate
  - `has_anomalies` (optional): Filter for constituencies with anomalies
  - `sort_by` (optional): Field to sort by
  - `sort_direction` (optional): Sort direction (`asc` or `desc`)
  - `page` (optional): Page number
  - `page_size` (optional): Page size
- **Response**: 
  ```typescript
  {
    constituencies: Constituency[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
  ```

#### Get Constituency by ID

- **Endpoint**: `GET /api/constituencies/:id`
- **Path Parameters**:
  - `id`: ID of the constituency
- **Response**: `ConstituencyDetail`

### Elections API

#### Get Elections

- **Endpoint**: `GET /api/elections`
- **Query Parameters**:
  - `status` (optional): Filter by status (`upcoming`, `active`, `completed`)
- **Response**: `Election[]`

#### Get Election by ID

- **Endpoint**: `GET /api/elections/:id`
- **Path Parameters**:
  - `id`: ID of the election
- **Response**: `ElectionDetail`

## Component Props Interfaces

### Dashboard Components

```typescript
// components/dashboard/DashboardHeader.tsx

export interface DashboardHeaderProps {
  title: string;
  elections: Election[];
  selectedElection: Election | null;
  timeRange: TimeRange;
  onElectionChange: (election: Election) => void;
  onTimeRangeChange: (timeRange: TimeRange) => void;
  className?: string;
}

// components/dashboard/MetricsSummary.tsx

export interface MetricsSummaryProps {
  metrics: {
    total_transactions: Metric;
    total_bulletins: Metric;
    total_votes: Metric;
    participation_rate: Metric;
    active_constituencies: Metric;
    anomalies_detected: Metric;
  };
  isLoading: boolean;
  className?: string;
}

// components/dashboard/ActivityTimeline.tsx

export interface ActivityTimelineProps {
  data: TransactionVolume[];
  timeRange: TimeRange;
  isLoading: boolean;
  onTimePointSelect?: (timestamp: string) => void;
  className?: string;
}

// components/dashboard/ConstituencyOverview.tsx

export interface ConstituencyOverviewProps {
  constituencies: Constituency[];
  isLoading: boolean;
  filters: ConstituencyFilter;
  onFilterChange: (filters: ConstituencyFilter) => void;
  onConstituencySelect: (constituency: Constituency) => void;
  className?: string;
}
```

### Metrics Components

```typescript
// components/metrics/MetricCard.tsx

export interface MetricCardProps {
  metric: Metric;
  isLoading?: boolean;
  className?: string;
}

// components/metrics/MetricsGrid.tsx

export interface MetricsGridProps {
  children: React.ReactNode;
  className?: string;
}

// components/metrics/ParticipationRateChart.tsx

export interface ParticipationRateChartProps {
  data: ParticipationRate[];
  isLoading?: boolean;
  className?: string;
}

// components/metrics/TransactionVolumeChart.tsx

export interface TransactionVolumeChartProps {
  data: TransactionVolume[];
  isLoading?: boolean;
  className?: string;
}

// components/metrics/HourlyActivityChart.tsx

export interface HourlyActivityChartProps {
  data: HourlyActivity[];
  isLoading?: boolean;
  className?: string;
}
```

### Constituency Components

```typescript
// components/constituencies/ConstituencyTable.tsx

export interface ConstituencyTableProps {
  constituencies: Constituency[];
  isLoading: boolean;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  onSort: (column: string) => void;
  onConstituencySelect: (constituency: Constituency) => void;
  className?: string;
}

// components/constituencies/ConstituencyFilters.tsx

export interface ConstituencyFiltersProps {
  filters: ConstituencyFilter;
  onFilterChange: (filters: ConstituencyFilter) => void;
  className?: string;
}

// components/constituencies/ConstituencySearch.tsx

export interface ConstituencySearchProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
  className?: string;
}

// components/constituencies/ConstituencyCard.tsx

export interface ConstituencyCardProps {
  constituency: Constituency;
  isLoading?: boolean;
  className?: string;
}
```

## Hook Interfaces

```typescript
// hooks/useMetrics.ts

export interface UseMetricsOptions {
  election_id: string;
  constituency_id?: string;
  time_range: TimeRange;
  refresh_interval?: number;
}

export interface UseMetricsResult {
  metrics: DashboardMetrics | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

// hooks/useConstituencies.ts

export interface UseConstituenciesOptions {
  election_id: string;
  filters?: ConstituencyFilter;
  refresh_interval?: number;
}

export interface UseConstituenciesResult {
  constituencies: Constituency[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  setFilters: (filters: ConstituencyFilter) => void;
}

// hooks/useElections.ts

export interface UseElectionsOptions {
  status?: 'upcoming' | 'active' | 'completed';
  refresh_interval?: number;
}

export interface UseElectionsResult {
  elections: Election[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

// hooks/useDashboard.ts

export interface UseDashboardOptions {
  initial_election_id?: string;
  initial_time_range?: TimeRange;
  refresh_interval?: number;
}

export interface UseDashboardResult {
  state: DashboardState;
  metrics: DashboardMetrics | null;
  constituencies: Constituency[];
  isLoading: boolean;
  error: Error | null;
  setElection: (election: Election) => void;
  setTimeRange: (timeRange: TimeRange) => void;
  setRefreshInterval: (interval: number) => void;
  refresh: () => Promise<void>;
}
```

## Store Interfaces

```typescript
// store/metrics.ts

export interface MetricsState {
  metrics: DashboardMetrics | null;
  isLoading: boolean;
  error: Error | null;
  lastUpdated: string | null;
}

export interface MetricsActions {
  fetchMetrics: (options: UseMetricsOptions) => Promise<void>;
  setMetrics: (metrics: DashboardMetrics) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: Error | null) => void;
  reset: () => void;
}

// store/constituencies.ts

export interface ConstituenciesState {
  constituencies: Constituency[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  filters: ConstituencyFilter;
  isLoading: boolean;
  error: Error | null;
  lastUpdated: string | null;
}

export interface ConstituenciesActions {
  fetchConstituencies: (options: UseConstituenciesOptions) => Promise<void>;
  setConstituencies: (data: { constituencies: Constituency[]; total: number; page: number; pageSize: number; totalPages: number }) => void;
  setFilters: (filters: ConstituencyFilter) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: Error | null) => void;
  reset: () => void;
}

// store/elections.ts

export interface ElectionsState {
  elections: Election[];
  selectedElection: Election | null;
  isLoading: boolean;
  error: Error | null;
  lastUpdated: string | null;
}

export interface ElectionsActions {
  fetchElections: (options?: UseElectionsOptions) => Promise<void>;
  setElections: (elections: Election[]) => void;
  selectElection: (election: Election) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: Error | null) => void;
  reset: () => void;
}

// store/dashboard.ts

export interface DashboardState {
  timeRange: TimeRange;
  refreshInterval: number;
  lastUpdated: string | null;
}

export interface DashboardActions {
  setTimeRange: (timeRange: TimeRange) => void;
  setRefreshInterval: (interval: number) => void;
  setLastUpdated: (timestamp: string) => void;
  reset: () => void;
}
```

## Default Time Ranges

```typescript
// lib/constants.ts

export const DEFAULT_TIME_RANGES: TimeRange[] = [
  {
    label: 'Last Hour',
    start: '1 hour ago',
    end: 'now',
  },
  {
    label: 'Last 6 Hours',
    start: '6 hours ago',
    end: 'now',
  },
  {
    label: 'Last 12 Hours',
    start: '12 hours ago',
    end: 'now',
  },
  {
    label: 'Last 24 Hours',
    start: '24 hours ago',
    end: 'now',
  },
  {
    label: 'Last 7 Days',
    start: '7 days ago',
    end: 'now',
  },
  {
    label: 'Last 30 Days',
    start: '30 days ago',
    end: 'now',
  },
];

export const DEFAULT_TIME_RANGE = DEFAULT_TIME_RANGES[3]; // Last 24 Hours
```

## Chart Configurations

```typescript
// lib/constants.ts

import { type ChartConfig } from "@/components/ui/chart";

export const TRANSACTION_CHART_CONFIG: ChartConfig = {
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
};

export const PARTICIPATION_CHART_CONFIG: ChartConfig = {
  participation_rate: {
    label: "Participation Rate",
    color: "var(--chart-4)"
  }
};

export const HOURLY_ACTIVITY_CHART_CONFIG: ChartConfig = {
  transaction_count: {
    label: "Transactions",
    color: "var(--chart-1)"
  },
  bulletins_issued: {
    label: "Bulletins Issued",
    color: "var(--chart-2)"
  },
  votes_cast: {
    label: "Votes Cast",
    color: "var(--chart-3)"
  }
};
```

## Mock Data Interfaces

For development and testing purposes, we'll define interfaces for mock data:

```typescript
// lib/mock-data.ts

export interface MockDataOptions {
  election_count?: number;
  constituency_count?: number;
  hourly_stats_count?: number;
  start_date?: string;
  end_date?: string;
}

export interface MockData {
  elections: Election[];
  constituencies: Constituency[];
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}