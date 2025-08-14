import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/dashboard/DashboardLayout';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { MetricsSummary } from '@/components/dashboard/MetricsSummary';
import { ActivityTimeline } from '@/components/dashboard/ActivityTimeline';
import { ConstituencyOverview } from '@/components/dashboard/ConstituencyOverview';
import { DashboardFooter } from '@/components/dashboard/DashboardFooter';
import { useDashboardStore, DEFAULT_TIME_RANGE } from '@/store/dashboard';
import { useNavigate } from 'react-router-dom';
import type { Election } from '@/types/elections';
import type { TimeRange } from '@/types/metrics';
import type { Constituency, ConstituencyFilter } from '@/types/constituencies';

export default function Dashboard() {
  const navigate = useNavigate();
  
  const {
    selectedElection,
    timeRange,
    refreshInterval,
    lastUpdated,
    metrics,
    constituencies,
    elections,
    constituencyFilters,
    isLoadingMetrics,
    isLoadingConstituencies,
    isLoadingElections,
    setSelectedElection,
    setTimeRange,
    setConstituencyFilters,
    fetchMetrics,
    fetchConstituencies,
    fetchElections,
    fetchAllData
  } = useDashboardStore();
  
  // Set default time range if not already set
  useEffect(() => {
    if (!timeRange) {
      setTimeRange(DEFAULT_TIME_RANGE);
    }
  }, [timeRange, setTimeRange]);
  
  // Fetch all data on mount
  useEffect(() => {
    fetchAllData();
    
    // Set up polling for data refresh
    if (refreshInterval > 0) {
      const intervalId = setInterval(() => {
        fetchAllData();
      }, refreshInterval * 1000);
      
      return () => clearInterval(intervalId);
    }
  }, [fetchAllData, refreshInterval]);
  
  // No need for this effect anymore as it's handled in the store

  const handleElectionChange = (election: Election) => {
    setSelectedElection(election);
  };
  
  const handleTimeRangeChange = (newTimeRange: TimeRange) => {
    setTimeRange(newTimeRange);
  };
  
  const handleConstituencySelect = (constituency: Constituency) => {
    navigate(`/constituencies/${constituency.id}`);
  };
  
  const isLoading = isLoadingElections || isLoadingMetrics || isLoadingConstituencies;
  
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
          filters={constituencyFilters}
          onFilterChange={setConstituencyFilters}
          onConstituencySelect={handleConstituencySelect}
        />
      </div>
      
      <DashboardFooter lastUpdated={lastUpdated} />
    </DashboardLayout>
  );
}