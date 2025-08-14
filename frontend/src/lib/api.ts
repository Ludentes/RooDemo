import axios from 'axios';
import type { 
  MetricsFilter, 
  DashboardMetrics, 
  HourlyStat, 
  ParticipationRate, 
  TransactionVolume, 
  HourlyActivity 
} from '@/types/metrics';
import type { 
  Constituency, 
  ConstituencyDetail, 
  ConstituencyFilter 
} from '@/types/constituencies';
import type { 
  Election, 
  ElectionDetail 
} from '@/types/elections';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper function to build query parameters
const buildQueryParams = (params: Record<string, any>): string => {
  const queryParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (key === 'time_range' && typeof value === 'object') {
        queryParams.append('start_date', value.start);
        queryParams.append('end_date', value.end);
      } else {
        queryParams.append(key, String(value));
      }
    }
  });
  
  return queryParams.toString();
};

export const metricsApi = {
  getDashboardMetrics: async (options: MetricsFilter): Promise<DashboardMetrics> => {
    const response = await api.get(`/api/metrics/dashboard?${buildQueryParams(options)}`);
    return response.data;
  },
  
  getHourlyStats: async (options: MetricsFilter): Promise<HourlyStat[]> => {
    const response = await api.get(`/api/metrics/hourly?${buildQueryParams(options)}`);
    return response.data;
  },
  
  getParticipationRates: async (options: MetricsFilter): Promise<ParticipationRate[]> => {
    const response = await api.get(`/api/metrics/participation?${buildQueryParams(options)}`);
    return response.data;
  },
  
  getTransactionVolumes: async (options: MetricsFilter): Promise<TransactionVolume[]> => {
    const response = await api.get(`/api/metrics/transactions?${buildQueryParams(options)}`);
    return response.data;
  },
  
  getHourlyActivity: async (options: MetricsFilter): Promise<HourlyActivity[]> => {
    const response = await api.get(`/api/metrics/hourly-activity?${buildQueryParams(options)}`);
    return response.data;
  },
};

export const constituenciesApi = {
  getConstituencies: async (options: ConstituencyFilter): Promise<{
    constituencies: Constituency[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }> => {
    const response = await api.get(`/api/constituencies?${buildQueryParams(options)}`);
    return response.data;
  },
  
  getConstituencyById: async (id: string): Promise<ConstituencyDetail> => {
    const response = await api.get(`/api/constituencies/${id}`);
    return response.data;
  },
};

export const electionsApi = {
  getElections: async (status?: 'upcoming' | 'active' | 'completed'): Promise<Election[]> => {
    const params = status ? `?status=${status}` : '';
    const response = await api.get(`/api/elections${params}`);
    return response.data;
  },
  
  getElectionById: async (id: string): Promise<ElectionDetail> => {
    const response = await api.get(`/api/elections/${id}`);
    return response.data;
  },
};

export default api;