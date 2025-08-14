/**
 * This file provides utility functions to test the mock API
 * It can be imported and used in the browser console to verify that the mock API is working correctly
 */

import { metricsApi, constituenciesApi, electionsApi } from './api';

// Function to test the mock API
export async function testMockApi() {
  console.log('Testing mock API...');
  
  try {
    // Test elections API
    console.log('Testing elections API...');
    const elections = await electionsApi.getElections();
    console.log('Elections:', elections);
    
    if (elections.length === 0) {
      console.error('No elections found. Mock API may not be working correctly.');
      return;
    }
    
    // Test constituencies API
    console.log('Testing constituencies API...');
    const constituenciesResponse = await constituenciesApi.getConstituencies({
      election_id: elections[0].id,
    });
    console.log('Constituencies:', constituenciesResponse);
    
    if (constituenciesResponse.constituencies.length === 0) {
      console.error('No constituencies found. Mock API may not be working correctly.');
      return;
    }
    
    // Test metrics API
    console.log('Testing metrics API...');
    const metrics = await metricsApi.getDashboardMetrics({
      election_id: elections[0].id,
      time_range: {
        start: '24 hours ago',
        end: 'now',
        label: 'Last 24 Hours',
      },
    });
    console.log('Metrics:', metrics);
    
    if (!metrics || !metrics.summary) {
      console.error('No metrics found. Mock API may not be working correctly.');
      return;
    }
    
    console.log('Mock API is working correctly!');
  } catch (error) {
    console.error('Error testing mock API:', error);
  }
}

// Make the test function available globally for easy access in the browser console
if (import.meta.env.DEV) {
  (window as any).testMockApi = testMockApi;
}

export default testMockApi;