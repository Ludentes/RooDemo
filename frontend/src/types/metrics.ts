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