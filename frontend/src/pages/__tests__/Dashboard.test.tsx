import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../Dashboard';
import { useDashboardStore } from '@/store/dashboard';
import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock the dashboard store
vi.mock('@/store/dashboard', () => ({
  useDashboardStore: vi.fn(),
  DEFAULT_TIME_RANGE: {
    label: 'Last 24 Hours',
    start: '24 hours ago',
    end: 'now',
  },
}));

// Mock the react-router-dom hooks
vi.mock('react-router-dom', () => ({
  ...vi.importActual('react-router-dom'),
  useNavigate: () => vi.fn(),
}));

describe('Dashboard', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();
    
    // Setup default mock implementation
    (useDashboardStore as any).mockReturnValue({
      selectedElection: {
        id: 'election-1',
        name: 'Test Election',
        date: '2025-01-01',
        status: 'active',
      },
      timeRange: {
        label: 'Last 24 Hours',
        start: '24 hours ago',
        end: 'now',
      },
      refreshInterval: 30,
      lastUpdated: '2025-01-01T12:00:00Z',
      metrics: {
        summary: {
          total_transactions: {
            id: 'total-transactions',
            label: 'Total Transactions',
            value: 1000,
            trend: 5,
            trendLabel: 'vs. previous period',
          },
          total_bulletins: {
            id: 'total-bulletins',
            label: 'Total Bulletins',
            value: 800,
            trend: 3,
            trendLabel: 'vs. previous period',
          },
          total_votes: {
            id: 'total-votes',
            label: 'Total Votes',
            value: 750,
            trend: 2,
            trendLabel: 'vs. previous period',
          },
          participation_rate: {
            id: 'participation-rate',
            label: 'Participation Rate',
            value: 75,
            trend: 1,
            trendLabel: 'vs. previous period',
          },
          active_constituencies: {
            id: 'active-constituencies',
            label: 'Active Constituencies',
            value: 10,
            trend: 0,
            trendLabel: 'vs. previous period',
          },
          anomalies_detected: {
            id: 'anomalies-detected',
            label: 'Anomalies Detected',
            value: 5,
            trend: -2,
            trendLabel: 'vs. previous period',
          },
        },
        transaction_volumes: [],
        participation_rates: [],
        hourly_activity: [],
      },
      constituencies: [],
      elections: [
        {
          id: 'election-1',
          name: 'Test Election',
          date: '2025-01-01',
          status: 'active',
        },
      ],
      isLoadingMetrics: false,
      isLoadingConstituencies: false,
      isLoadingElections: false,
      setSelectedElection: vi.fn(),
      setTimeRange: vi.fn(),
      fetchMetrics: vi.fn(),
      fetchConstituencies: vi.fn(),
      fetchElections: vi.fn(),
      fetchAllData: vi.fn(),
    });
  });

  it('renders the dashboard header with correct title', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check if the element exists in the document
    const titleElement = screen.getByText('Election Monitoring Dashboard');
    expect(titleElement).toBeDefined();
  });

  it('renders metrics summary when data is available', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check if elements exist in the document
    const summaryElement = screen.getByText('Summary');
    const transactionsElement = screen.getByText('Total Transactions');
    const valueElement = screen.getByText('1,000');
    
    expect(summaryElement).toBeDefined();
    expect(transactionsElement).toBeDefined();
    expect(valueElement).toBeDefined();
  });

  it('fetches data on mount', () => {
    const mockFetchAllData = vi.fn();
    (useDashboardStore as any).mockReturnValue({
      ...useDashboardStore(),
      fetchAllData: mockFetchAllData,
    });
    
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check if the function was called
    expect(mockFetchAllData.mock.calls.length).toBe(1);
  });
});