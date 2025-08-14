/**
 * This file overrides the real API with mock implementations for development
 * It uses module augmentation to replace the API functions with mock implementations
 */

import * as mockApi from './mock-api';
import * as realApi from './api';

// Override the real API with mock implementations
if (import.meta.env.DEV) {
  // Metrics API
  realApi.metricsApi.getDashboardMetrics = mockApi.metricsApi.getDashboardMetrics;
  realApi.metricsApi.getHourlyStats = mockApi.metricsApi.getHourlyStats;
  realApi.metricsApi.getParticipationRates = mockApi.metricsApi.getParticipationRates;
  realApi.metricsApi.getTransactionVolumes = mockApi.metricsApi.getTransactionVolumes;
  realApi.metricsApi.getHourlyActivity = mockApi.metricsApi.getHourlyActivity;
  
  // Constituencies API
  realApi.constituenciesApi.getConstituencies = mockApi.constituenciesApi.getConstituencies;
  realApi.constituenciesApi.getConstituencyById = mockApi.constituenciesApi.getConstituencyById;
  
  // Elections API
  realApi.electionsApi.getElections = mockApi.electionsApi.getElections;
  realApi.electionsApi.getElectionById = mockApi.electionsApi.getElectionById;
  
  console.log('API overridden with mock implementations');
}

export default realApi;