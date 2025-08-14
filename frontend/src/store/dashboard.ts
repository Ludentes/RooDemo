import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  DashboardState,
  DashboardFilter
} from '@/types/dashboard';
import type {
  TimeRange,
  DashboardMetrics
} from '@/types/metrics';
import type {
  Constituency,
  ConstituencyFilter
} from '@/types/constituencies';
import type {
  Election
} from '@/types/elections';
import { metricsApi, constituenciesApi, electionsApi } from '@/lib/api';

const DEFAULT_TIME_RANGES: TimeRange[] = [
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

interface DashboardStore extends DashboardState {
  // Dashboard metrics
  metrics: DashboardMetrics | null;
  constituencies: Constituency[];
  elections: Election[];
  
  // Filters
  constituencyFilters: ConstituencyFilter;
  
  // Loading states
  isLoadingMetrics: boolean;
  isLoadingConstituencies: boolean;
  isLoadingElections: boolean;
  
  // Error states
  metricsError: Error | null;
  constituenciesError: Error | null;
  electionsError: Error | null;
  
  // Actions
  setSelectedElection: (election: Election | null) => void;
  setTimeRange: (timeRange: TimeRange) => void;
  setRefreshInterval: (interval: number) => void;
  setLastUpdated: (timestamp: string) => void;
  setConstituencyFilters: (filters: ConstituencyFilter) => void;
  
  // Data fetching
  fetchMetrics: () => Promise<void>;
  fetchConstituencies: () => Promise<void>;
  fetchElections: () => Promise<void>;
  fetchAllData: () => Promise<void>;
  
  // Reset
  reset: () => void;
}

export const useDashboardStore = create<DashboardStore>()(
  persist(
    (set, get) => ({
      // Dashboard state
      selectedElection: null,
      timeRange: DEFAULT_TIME_RANGE,
      refreshInterval: 30, // 30 seconds
      lastUpdated: new Date().toISOString(),
      
      // Data
      metrics: null,
      constituencies: [],
      elections: [],
      
      // Filters
      constituencyFilters: {
        election_id: '',
        sort_by: 'name',
        sort_direction: 'asc',
      },
      
      // Loading states
      isLoadingMetrics: false,
      isLoadingConstituencies: false,
      isLoadingElections: false,
      
      // Error states
      metricsError: null,
      constituenciesError: null,
      electionsError: null,
      
      // Actions
      setSelectedElection: (election) => {
        set({ selectedElection: election });
        if (election) {
          set(state => ({
            constituencyFilters: {
              ...state.constituencyFilters,
              election_id: election.id
            }
          }));
          
          // Fetch new data for the selected election
          setTimeout(() => {
            get().fetchMetrics();
            get().fetchConstituencies();
          }, 0);
        }
      },
      setTimeRange: (timeRange) => {
        set({ timeRange });
        // Fetch new metrics with updated time range
        get().fetchMetrics();
      },
      setRefreshInterval: (interval) => set({ refreshInterval: interval }),
      setLastUpdated: (timestamp) => set({ lastUpdated: timestamp }),
      setConstituencyFilters: (filters) => {
        set({ constituencyFilters: filters });
        // Fetch new data with updated filters
        get().fetchConstituencies();
      },
      
      // Data fetching
      fetchMetrics: async () => {
        const { selectedElection, timeRange } = get();
        
        if (!selectedElection) {
          return;
        }
        
        set({ isLoadingMetrics: true, metricsError: null });
        
        try {
          const metrics = await metricsApi.getDashboardMetrics({
            election_id: selectedElection.id,
            time_range: timeRange,
          });
          
          set({ 
            metrics, 
            isLoadingMetrics: false,
            lastUpdated: new Date().toISOString(),
          });
        } catch (error) {
          set({ 
            isLoadingMetrics: false, 
            metricsError: error instanceof Error ? error : new Error('Unknown error'),
          });
        }
      },
      
      fetchConstituencies: async () => {
        const { selectedElection, constituencyFilters } = get();
        
        if (!selectedElection) {
          return;
        }
        
        set({ isLoadingConstituencies: true, constituenciesError: null });
        
        try {
          const response = await constituenciesApi.getConstituencies({
            ...constituencyFilters,
            election_id: selectedElection.id,
          });
          
          set({
            constituencies: response.constituencies,
            isLoadingConstituencies: false,
          });
        } catch (error) {
          set({
            isLoadingConstituencies: false,
            constituenciesError: error instanceof Error ? error : new Error('Unknown error'),
          });
        }
      },
      
      fetchElections: async () => {
        set({ isLoadingElections: true, electionsError: null });
        
        try {
          const elections = await electionsApi.getElections();
          
          set({ 
            elections, 
            isLoadingElections: false,
            // Select the first active election if none is selected
            selectedElection: get().selectedElection || 
              elections.find(e => e.status === 'active') || 
              (elections.length > 0 ? elections[0] : null),
          });
        } catch (error) {
          set({ 
            isLoadingElections: false, 
            electionsError: error instanceof Error ? error : new Error('Unknown error'),
          });
        }
      },
      
      fetchAllData: async () => {
        await get().fetchElections();
        
        if (get().selectedElection) {
          await Promise.all([
            get().fetchMetrics(),
            get().fetchConstituencies(),
          ]);
        }
      },
      
      reset: () => set({
        metrics: null,
        constituencies: [],
        isLoadingMetrics: false,
        isLoadingConstituencies: false,
        metricsError: null,
        constituenciesError: null,
        constituencyFilters: {
          election_id: '',
          sort_by: 'name',
          sort_direction: 'asc',
        },
      }),
    }),
    {
      name: 'dashboard-storage',
    }
  )
);

// Export time ranges
export { DEFAULT_TIME_RANGES };