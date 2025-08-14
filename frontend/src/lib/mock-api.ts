// Create and export mock data
import { mockData, getMockElection, getMockConstituency } from './mock-data';

// Log that mock data is loaded
console.log('Mock data loaded:', {
  elections: mockData.elections.length,
  constituencies: mockData.constituencies.length,
  hourly_stats: mockData.hourly_stats.length,
});
import type { MetricsFilter } from '@/types/metrics';
import type { ConstituencyFilter } from '@/types/constituencies';

// Helper function to simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock API functions that return promises with mock data
export const mockApi = {
  // Metrics API
  getDashboardMetrics: async (options: MetricsFilter) => {
    await delay(500); // Simulate network delay
    
    if (!options.election_id) {
      throw new Error('election_id is required');
    }
    
    // Find the election
    const election = mockData.elections.find(e => e.id === options.election_id);
    if (!election) {
      throw new Error(`Election with ID ${options.election_id} not found`);
    }
    
    // Create a copy of the dashboard metrics and modify it based on the election
    const metrics = { ...mockData.dashboard_metrics };
    
    // Modify metrics based on election
    const randomFactor = Math.random() * 0.5 + 0.75; // Randomize values by ±25%
    
    // Update each metric individually
    metrics.summary = {
      ...metrics.summary,
      total_transactions: {
        ...metrics.summary.total_transactions,
        value: election.transaction_count,
        trend: Math.random() > 0.5 ? 1.5 : -1.5,
      },
      total_bulletins: {
        ...metrics.summary.total_bulletins,
        value: election.bulletins_issued,
        trend: Math.random() > 0.5 ? 2.3 : -2.3,
      },
      total_votes: {
        ...metrics.summary.total_votes,
        value: election.votes_cast,
        trend: Math.random() > 0.5 ? 3.1 : -3.1,
      },
      participation_rate: {
        ...metrics.summary.participation_rate,
        value: election.participation_rate,
        trend: Math.random() > 0.5 ? 1.2 : -1.2,
      },
      active_constituencies: {
        ...metrics.summary.active_constituencies,
        value: mockData.constituencies.filter(c => c.election_id === election.id).length,
        trend: 0,
      },
      anomalies_detected: {
        ...metrics.summary.anomalies_detected,
        value: mockData.constituencies.filter(c => c.election_id === election.id)
          .reduce((sum, c) => sum + c.anomaly_count, 0),
        trend: Math.random() > 0.5 ? -2.1 : 2.1,
      },
    };
    
    return metrics;
  },
  
  getHourlyStats: async (options: MetricsFilter) => {
    await delay(300);
    
    if (!options.election_id) {
      throw new Error('election_id is required');
    }
    
    let stats = mockData.hourly_stats.filter(stat => stat.election_id === options.election_id);
    
    if (options.constituency_id) {
      stats = stats.filter(stat => stat.constituency_id === options.constituency_id);
    }
    
    return stats;
  },
  
  getParticipationRates: async (options: MetricsFilter) => {
    await delay(300);
    
    if (!options.election_id) {
      throw new Error('election_id is required');
    }
    
    let rates = mockData.participation_rates.filter(rate => rate.election_id === options.election_id);
    
    if (options.constituency_id) {
      rates = rates.filter(rate => rate.constituency_id === options.constituency_id);
    }
    
    return rates;
  },
  
  getTransactionVolumes: async (options: MetricsFilter) => {
    await delay(300);
    
    if (!options.election_id) {
      throw new Error('election_id is required');
    }
    
    // Find the election
    const election = mockData.elections.find(e => e.id === options.election_id);
    if (!election) {
      throw new Error(`Election with ID ${options.election_id} not found`);
    }
    
    // Get base volumes
    let volumes = mockData.transaction_volumes.filter(volume => volume.election_id === options.election_id);
    
    if (options.constituency_id) {
      volumes = volumes.filter(volume => volume.constituency_id === options.constituency_id);
    }
    
    // If time_range is provided, filter by time range
    if (options.time_range) {
      // For mock purposes, we'll just return a subset of the data based on the time range
      const timeRangeHours = options.time_range.label.includes('Hour')
        ? parseInt(options.time_range.label.match(/\d+/)?.[0] || '24')
        : options.time_range.label.includes('Day')
          ? parseInt(options.time_range.label.match(/\d+/)?.[0] || '1') * 24
          : 24;
      
      // Take the last N hours of data based on the time range
      volumes = volumes.slice(-timeRangeHours);
      
      // If we don't have enough data, generate more
      if (volumes.length < timeRangeHours) {
        const lastTimestamp = volumes.length > 0
          ? new Date(volumes[volumes.length - 1].timestamp)
          : new Date();
        
        for (let i = volumes.length; i < timeRangeHours; i++) {
          const timestamp = new Date(lastTimestamp);
          timestamp.setHours(timestamp.getHours() - (timeRangeHours - i));
          
          volumes.push({
            election_id: options.election_id,
            constituency_id: options.constituency_id || '',
            timestamp: timestamp.toISOString(),
            transaction_count: Math.floor(Math.random() * 1000) + 500,
            bulletins_issued: Math.floor(Math.random() * 500) + 200,
            votes_cast: Math.floor(Math.random() * 500) + 200,
          });
        }
        
        // Sort by timestamp
        volumes.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
      }
    }
    
    return volumes;
  },
  
  getHourlyActivity: async (options: MetricsFilter) => {
    await delay(300);
    return mockData.hourly_activity;
  },
  
  // Constituencies API
  getConstituencies: async (options: ConstituencyFilter) => {
    await delay(400);
    
    if (!options.election_id) {
      throw new Error('election_id is required');
    }
    
    let filteredConstituencies = mockData.constituencies.filter(
      constituency => constituency.election_id === options.election_id
    );
    
    // Apply filters
    if (options.region_id) {
      filteredConstituencies = filteredConstituencies.filter(
        constituency => constituency.region_id === options.region_id
      );
    }
    
    if (options.search) {
      const searchLower = options.search.toLowerCase();
      filteredConstituencies = filteredConstituencies.filter(
        constituency => 
          constituency.name.toLowerCase().includes(searchLower) ||
          constituency.code.toLowerCase().includes(searchLower) ||
          constituency.region_name.toLowerCase().includes(searchLower)
      );
    }
    
    if (options.min_participation_rate !== undefined) {
      filteredConstituencies = filteredConstituencies.filter(
        constituency => constituency.participation_rate >= options.min_participation_rate!
      );
    }
    
    if (options.max_participation_rate !== undefined) {
      filteredConstituencies = filteredConstituencies.filter(
        constituency => constituency.participation_rate <= options.max_participation_rate!
      );
    }
    
    if (options.has_anomalies) {
      filteredConstituencies = filteredConstituencies.filter(
        constituency => constituency.anomaly_count > 0
      );
    }
    
    // Apply sorting
    if (options.sort_by) {
      const sortDirection = options.sort_direction === 'desc' ? -1 : 1;
      filteredConstituencies.sort((a, b) => {
        const aValue = a[options.sort_by as keyof typeof a];
        const bValue = b[options.sort_by as keyof typeof b];
        
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortDirection * aValue.localeCompare(bValue);
        }
        
        if (typeof aValue === 'number' && typeof bValue === 'number') {
          return sortDirection * (aValue - bValue);
        }
        
        return 0;
      });
    }
    
    // Apply pagination
    const page = options.page || 1;
    const pageSize = options.page_size || 10;
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedConstituencies = filteredConstituencies.slice(startIndex, endIndex);
    
    return {
      constituencies: paginatedConstituencies,
      total: filteredConstituencies.length,
      page,
      page_size: pageSize,
      total_pages: Math.ceil(filteredConstituencies.length / pageSize),
    };
  },
  
  getConstituencyById: async (id: string) => {
    await delay(300);
    const constituency = getMockConstituency(id);
    
    if (!constituency) {
      throw new Error(`Constituency with ID ${id} not found`);
    }
    
    return constituency;
  },
  
  // Elections API
  getElections: async (status?: 'upcoming' | 'active' | 'completed') => {
    await delay(300);
    
    let filteredElections = mockData.elections;
    
    if (status) {
      filteredElections = filteredElections.filter(election => election.status === status);
    }
    
    return filteredElections;
  },
  
  getElectionById: async (id: string) => {
    await delay(300);
    const election = getMockElection(id);
    
    if (!election) {
      throw new Error(`Election with ID ${id} not found`);
    }
    
    return election;
  },
};

// Export the mock API functions to be used directly
export const metricsApi = {
  getDashboardMetrics: mockApi.getDashboardMetrics,
  getHourlyStats: mockApi.getHourlyStats,
  getParticipationRates: mockApi.getParticipationRates,
  getTransactionVolumes: mockApi.getTransactionVolumes,
  getHourlyActivity: mockApi.getHourlyActivity,
};

export const constituenciesApi = {
  getConstituencies: mockApi.getConstituencies,
  getConstituencyById: mockApi.getConstituencyById,
};

export const electionsApi = {
  getElections: mockApi.getElections,
  getElectionById: mockApi.getElectionById,
};

// Function to initialize mock API
export function initMockApi() {
  console.log('Mock API initialized');
  // The actual replacement happens in main.tsx by importing from mock-api instead of api
}