# Frontend Infrastructure Interfaces

This document defines the key interfaces and contracts for the Election Monitoring System frontend infrastructure. These interfaces establish the boundaries between different components and ensure consistent communication patterns.

## Table of Contents

1. [Data Models](#data-models)
2. [Component Props](#component-props)
3. [API Contracts](#api-contracts)
4. [Store Interfaces](#store-interfaces)
5. [Hook Interfaces](#hook-interfaces)
6. [Service Interfaces](#service-interfaces)

## Data Models

### Core Domain Models

These models represent the core domain entities in the application.

#### Election

```typescript
interface Election {
  id: string;
  name: string;
  date: string;
  status: 'upcoming' | 'active' | 'completed';
  description?: string;
  constituencies: string[]; // Array of constituency IDs
}
```

#### Constituency

```typescript
interface Constituency {
  id: string;
  name: string;
  electionId: string;
  region: string;
  voterCount: number;
  statistics: ConstituencyStatistics;
}

interface ConstituencyStatistics {
  participationRate: number;
  bulletinsIssued: number;
  votesCount: number;
  lastUpdated: string;
}
```

#### Transaction

```typescript
interface Transaction {
  id: string;
  constituencyId: string;
  blockHeight: number;
  timestamp: string;
  type: 'vote' | 'bulletin' | 'other';
  rawData: Record<string, any>;
  operationData: Record<string, any>;
}
```

#### Alert

```typescript
interface Alert {
  id: string;
  constituencyId: string;
  timestamp: string;
  type: 'anomaly' | 'warning' | 'info';
  severity: 'high' | 'medium' | 'low';
  message: string;
  status: 'new' | 'investigating' | 'resolved' | 'dismissed';
  relatedTransactions?: string[]; // Array of transaction IDs
}
```

#### HourlyStats

```typescript
interface HourlyStats {
  constituencyId: string;
  hour: string; // ISO format
  bulletinsIssued: number;
  votesCount: number;
  participationRate: number;
}
```

#### Dashboard Summary

```typescript
interface DashboardSummary {
  activeElections: number;
  totalConstituencies: number;
  activeAlerts: number;
  participationRate: number;
  recentTransactions: Transaction[];
  recentAlerts: Alert[];
  constituencyStatistics: {
    id: string;
    name: string;
    participationRate: number;
  }[];
}
```

## Component Props

### Layout Components

#### AppLayout

```typescript
interface AppLayoutProps {
  children: ReactNode;
}
```

#### Sidebar

```typescript
interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
}
```

#### Header

```typescript
interface HeaderProps {
  title?: string;
}
```

### Common Components

#### DataTable

```typescript
interface DataTableProps<T> {
  data: T[];
  columns: {
    id: string;
    header: string;
    accessorKey?: keyof T;
    accessorFn?: (row: T) => any;
    cell?: (info: { row: { original: T } }) => ReactNode;
  }[];
  pagination?: {
    pageIndex: number;
    pageSize: number;
    pageCount: number;
    onPageChange: (page: number) => void;
    onPageSizeChange: (size: number) => void;
  };
  sorting?: {
    sortBy: string;
    sortDirection: 'asc' | 'desc';
    onSortChange: (column: string, direction: 'asc' | 'desc') => void;
  };
  loading?: boolean;
  error?: string | null;
}
```

#### Card

```typescript
interface CardProps {
  title: string;
  subtitle?: string;
  icon?: ReactNode;
  value?: string | number;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  loading?: boolean;
  className?: string;
  children?: ReactNode;
}
```

#### Chart

```typescript
interface ChartProps {
  data: any[];
  type: 'bar' | 'line' | 'pie' | 'area';
  xAxis?: {
    dataKey: string;
    label?: string;
  };
  yAxis?: {
    label?: string;
  };
  series: {
    dataKey: string;
    name: string;
    color?: string;
  }[];
  height?: number | string;
  width?: number | string;
  loading?: boolean;
  error?: string | null;
}
```

#### AlertBadge

```typescript
interface AlertBadgeProps {
  type: Alert['type'];
  severity: Alert['severity'];
  size?: 'sm' | 'md' | 'lg';
}
```

#### StatusBadge

```typescript
interface StatusBadgeProps {
  status: 'success' | 'warning' | 'error' | 'info' | 'pending';
  label: string;
  size?: 'sm' | 'md' | 'lg';
}
```

#### LoadingSpinner

```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
}
```

#### ErrorDisplay

```typescript
interface ErrorDisplayProps {
  error: string | Error;
  onRetry?: () => void;
}
```

#### EmptyState

```typescript
interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

### Feature Components

#### DashboardSummaryCard

```typescript
interface DashboardSummaryCardProps {
  summary: DashboardSummary;
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
}
```

#### ConstituencyList

```typescript
interface ConstituencyListProps {
  constituencies: Constituency[];
  loading?: boolean;
  error?: string | null;
  onConstituencySelect?: (id: string) => void;
}
```

#### ConstituencyDetail

```typescript
interface ConstituencyDetailProps {
  constituency: Constituency;
  transactions: Transaction[];
  alerts: Alert[];
  hourlyStats: HourlyStats[];
  loading?: boolean;
  error?: string | null;
}
```

#### AlertList

```typescript
interface AlertListProps {
  alerts: Alert[];
  loading?: boolean;
  error?: string | null;
  onAlertSelect?: (id: string) => void;
  onStatusChange?: (id: string, status: Alert['status']) => void;
}
```

#### TransactionList

```typescript
interface TransactionListProps {
  transactions: Transaction[];
  loading?: boolean;
  error?: string | null;
  onTransactionSelect?: (id: string) => void;
}
```

## API Contracts

### Elections API

#### GET /api/elections

**Response:**
```typescript
{
  data: Election[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    pageCount: number;
  };
}
```

#### GET /api/elections/:id

**Response:**
```typescript
{
  data: Election;
}
```

#### GET /api/elections/upcoming

**Response:**
```typescript
{
  data: Election[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    pageCount: number;
  };
}
```

### Constituencies API

#### GET /api/constituencies

**Query Parameters:**
```typescript
{
  electionId?: string;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortDirection?: 'asc' | 'desc';
}
```

**Response:**
```typescript
{
  data: Constituency[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    pageCount: number;
  };
}
```

#### GET /api/constituencies/:id

**Response:**
```typescript
{
  data: Constituency;
}
```

### Alerts API

#### GET /api/alerts

**Query Parameters:**
```typescript
{
  constituencyId?: string;
  type?: Alert['type'];
  severity?: Alert['severity'];
  status?: Alert['status'];
  page?: number;
  pageSize?: number;
  sortBy?: string;
  sortDirection?: 'asc' | 'desc';
}
```

**Response:**
```typescript
{
  data: Alert[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    pageCount: number;
  };
}
```

#### GET /api/alerts/:id

**Response:**
```typescript
{
  data: Alert;
}
```

### Dashboard API

#### GET /api/dashboard/summary

**Response:**
```typescript
{
  data: DashboardSummary;
}
```

### Files API

#### POST /api/files/upload

**Request:**
```typescript
// FormData with 'file' field containing the CSV file
```

**Response:**
```typescript
{
  data: {
    filename: string;
    transactions_processed: number;
    constituency_id: string;
    date: string;
    time_range: string;
  };
}
```

#### POST /api/files/process-directory

**Request:**
```typescript
{
  path: string;
}
```

**Response:**
```typescript
{
  data: {
    files_processed: number;
    transactions_processed: number;
    constituency_id: string;
  };
}
```

#### GET /api/files/statistics/:constituency_id

**Response:**
```typescript
{
  data: {
    total_files: number;
    total_transactions: number;
    last_processed: string;
    transaction_types: {
      [key: string]: number;
    };
  };
}
```

## Store Interfaces

### UI Store

```typescript
interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
}
```

### Election Store

```typescript
interface ElectionState {
  elections: Election[];
  selectedElection: Election | null;
  loading: boolean;
  error: string | null;
  fetchElections: () => Promise<void>;
  selectElection: (id: string) => void;
}
```

### Constituency Store

```typescript
interface ConstituencyState {
  constituencies: Constituency[];
  selectedConstituency: Constituency | null;
  loading: boolean;
  error: string | null;
  fetchConstituencies: (electionId?: string) => Promise<void>;
  fetchConstituency: (id: string) => Promise<void>;
  selectConstituency: (id: string) => void;
}
```

### Alert Store

```typescript
interface AlertState {
  alerts: Alert[];
  selectedAlert: Alert | null;
  loading: boolean;
  error: string | null;
  fetchAlerts: (filters?: Partial<Alert>) => Promise<void>;
  fetchAlert: (id: string) => Promise<void>;
  selectAlert: (id: string) => void;
  updateAlertStatus: (id: string, status: Alert['status']) => Promise<void>;
}
```

### Transaction Store

```typescript
interface TransactionState {
  transactions: Transaction[];
  selectedTransaction: Transaction | null;
  loading: boolean;
  error: string | null;
  fetchTransactions: (constituencyId?: string) => Promise<void>;
  fetchTransaction: (id: string) => Promise<void>;
  selectTransaction: (id: string) => void;
}
```

## Hook Interfaces

### useTheme

```typescript
interface UseThemeResult {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
}
```

### useNotification

```typescript
interface UseNotificationResult {
  showSuccess: (message: string) => void;
  showError: (message: string) => void;
  showInfo: (message: string) => void;
  showWarning: (message: string) => void;
}
```

### useElections

```typescript
interface UseElectionsResult {
  elections: Election[];
  selectedElection: Election | null;
  loading: boolean;
  error: string | null;
  fetchElections: () => Promise<void>;
  selectElection: (id: string) => void;
}
```

### useConstituencies

```typescript
interface UseConstituenciesResult {
  constituencies: Constituency[];
  selectedConstituency: Constituency | null;
  loading: boolean;
  error: string | null;
  fetchConstituencies: (electionId?: string) => Promise<void>;
  fetchConstituency: (id: string) => Promise<void>;
  selectConstituency: (id: string) => void;
}
```

### useAlerts

```typescript
interface UseAlertsResult {
  alerts: Alert[];
  selectedAlert: Alert | null;
  loading: boolean;
  error: string | null;
  fetchAlerts: (filters?: Partial<Alert>) => Promise<void>;
  fetchAlert: (id: string) => Promise<void>;
  selectAlert: (id: string) => void;
  updateAlertStatus: (id: string, status: Alert['status']) => Promise<void>;
}
```

### useTransactions

```typescript
interface UseTransactionsResult {
  transactions: Transaction[];
  selectedTransaction: Transaction | null;
  loading: boolean;
  error: string | null;
  fetchTransactions: (constituencyId?: string) => Promise<void>;
  fetchTransaction: (id: string) => Promise<void>;
  selectTransaction: (id: string) => void;
}
```

### useDashboard

```typescript
interface UseDashboardResult {
  summary: DashboardSummary | null;
  loading: boolean;
  error: string | null;
  fetchSummary: () => Promise<void>;
}
```

## Service Interfaces

### API Client

```typescript
interface ApiClient {
  get: <T>(url: string, config?: AxiosRequestConfig) => Promise<AxiosResponse<T>>;
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) => Promise<AxiosResponse<T>>;
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) => Promise<AxiosResponse<T>>;
  delete: <T>(url: string, config?: AxiosRequestConfig) => Promise<AxiosResponse<T>>;
}
```

### Elections API Service

```typescript
interface ElectionsApiService {
  getAll: () => Promise<AxiosResponse<{ data: Election[]; meta: PaginationMeta }>>;
  getById: (id: string) => Promise<AxiosResponse<{ data: Election }>>;
  getUpcoming: () => Promise<AxiosResponse<{ data: Election[]; meta: PaginationMeta }>>;
}
```

### Constituencies API Service

```typescript
interface ConstituenciesApiService {
  getAll: (params?: {
    electionId?: string;
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortDirection?: 'asc' | 'desc';
  }) => Promise<AxiosResponse<{ data: Constituency[]; meta: PaginationMeta }>>;
  getById: (id: string) => Promise<AxiosResponse<{ data: Constituency }>>;
}
```

### Alerts API Service

```typescript
interface AlertsApiService {
  getAll: (params?: {
    constituencyId?: string;
    type?: Alert['type'];
    severity?: Alert['severity'];
    status?: Alert['status'];
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortDirection?: 'asc' | 'desc';
  }) => Promise<AxiosResponse<{ data: Alert[]; meta: PaginationMeta }>>;
  getById: (id: string) => Promise<AxiosResponse<{ data: Alert }>>;
  updateStatus: (id: string, status: Alert['status']) => Promise<AxiosResponse<{ data: Alert }>>;
}
```

### Dashboard API Service

```typescript
interface DashboardApiService {
  getSummary: () => Promise<AxiosResponse<{ data: DashboardSummary }>>;
}
```

### Files API Service

```typescript
interface FilesApiService {
  upload: (file: File) => Promise<AxiosResponse<{
    data: {
      filename: string;
      transactions_processed: number;
      constituency_id: string;
      date: string;
      time_range: string;
    };
  }>>;
  processDirectory: (path: string) => Promise<AxiosResponse<{
    data: {
      files_processed: number;
      transactions_processed: number;
      constituency_id: string;
    };
  }>>;
  getStatistics: (constituencyId: string) => Promise<AxiosResponse<{
    data: {
      total_files: number;
      total_transactions: number;
      last_processed: string;
      transaction_types: {
        [key: string]: number;
      };
    };
  }>>;
}
```

### Common Types

```typescript
interface PaginationMeta {
  total: number;
  page: number;
  pageSize: number;
  pageCount: number;
}