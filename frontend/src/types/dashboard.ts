import type { Election } from './elections';
import type { TimeRange, Metric, TransactionVolume } from './metrics';
import type { Constituency, ConstituencyFilter } from './constituencies';

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

export interface DashboardProps {
  className?: string;
}

export interface DashboardHeaderProps {
  title: string;
  elections: Election[];
  selectedElection: Election | null;
  timeRange: TimeRange;
  onElectionChange: (election: Election) => void;
  onTimeRangeChange: (timeRange: TimeRange) => void;
  className?: string;
}

export interface MetricsSummaryProps {
  metrics: {
    total_transactions: Metric;
    total_bulletins: Metric;
    total_votes: Metric;
    participation_rate: Metric;
    active_constituencies: Metric;
    anomalies_detected: Metric;
  } | null;
  isLoading: boolean;
  className?: string;
}

export interface ActivityTimelineProps {
  data: TransactionVolume[];
  timeRange: TimeRange;
  isLoading: boolean;
  onTimePointSelect?: (timestamp: string) => void;
  className?: string;
}

export interface ConstituencyOverviewProps {
  constituencies: Constituency[];
  isLoading: boolean;
  filters: ConstituencyFilter;
  onFilterChange: (filters: ConstituencyFilter) => void;
  onConstituencySelect: (constituency: Constituency) => void;
  className?: string;
}

export interface DashboardFooterProps {
  lastUpdated?: string;
  className?: string;
}