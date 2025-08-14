import type { Constituency } from './constituencies';
import type { HourlyStat, ParticipationRate, TransactionVolume, HourlyActivity } from './metrics';

export interface Election {
  id: string;
  name: string;
  date: string;
  status: 'upcoming' | 'active' | 'completed';
  constituency_count: number;
  registered_voters: number;
  bulletins_issued: number;
  votes_cast: number;
  transaction_count: number;
  participation_rate: number;
  anomaly_count: number;
}

export interface ElectionDetail extends Election {
  constituencies: Constituency[];
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
}