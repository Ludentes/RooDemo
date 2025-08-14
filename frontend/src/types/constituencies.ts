import type { HourlyStat, ParticipationRate, TransactionVolume, HourlyActivity } from './metrics';

export interface Constituency {
  id: string;
  name: string;
  code: string;
  region_id: string;
  region_name: string;
  election_id: string;
  registered_voters: number;
  bulletins_issued: number;
  votes_cast: number;
  transaction_count: number;
  participation_rate: number;
  anomaly_count: number;
  last_activity: string;
}

export interface ConstituencyDetail extends Constituency {
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}

export interface ConstituencyFilter {
  election_id: string;
  region_id?: string;
  search?: string;
  min_participation_rate?: number;
  max_participation_rate?: number;
  has_anomalies?: boolean;
  sort_by?: string;
  sort_direction?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
}