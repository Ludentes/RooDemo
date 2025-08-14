import type { 
  Election, 
  ElectionDetail 
} from '@/types/elections';
import type { 
  Constituency, 
  ConstituencyDetail 
} from '@/types/constituencies';
import type { 
  HourlyStat, 
  ParticipationRate, 
  TransactionVolume, 
  HourlyActivity,
  Metric,
  DashboardMetrics
} from '@/types/metrics';
import { subHours, addHours, format } from 'date-fns';

export interface MockDataOptions {
  election_count?: number;
  constituency_count?: number;
  hourly_stats_count?: number;
  start_date?: string;
  end_date?: string;
}

export interface MockData {
  elections: Election[];
  constituencies: Constituency[];
  hourly_stats: HourlyStat[];
  participation_rates: ParticipationRate[];
  transaction_volumes: TransactionVolume[];
  hourly_activity: HourlyActivity[];
  dashboard_metrics: DashboardMetrics;
}

export function generateMockData(options: MockDataOptions = {}): MockData {
  const {
    election_count = 3,
    constituency_count = 20,
    hourly_stats_count = 24,
    start_date = subHours(new Date(), 24).toISOString(),
    end_date = new Date().toISOString(),
  } = options;

  // Generate mock elections
  const elections: Election[] = Array.from({ length: election_count }).map((_, i) => ({
    id: `election-${i + 1}`,
    name: `Election ${i + 1}`,
    date: new Date().toISOString(),
    status: i === 0 ? 'active' : i === 1 ? 'upcoming' : 'completed',
    constituency_count,
    registered_voters: 1000000 + i * 100000,
    bulletins_issued: 600000 + i * 50000,
    votes_cast: 550000 + i * 45000,
    transaction_count: 700000 + i * 60000,
    participation_rate: 55 + i * 2,
    anomaly_count: Math.floor(Math.random() * 10),
  }));

  // Generate mock constituencies
  const constituencies: Constituency[] = [];
  for (let e = 0; e < election_count; e++) {
    for (let i = 0; i < constituency_count; i++) {
      const registered_voters = 5000 + Math.floor(Math.random() * 15000);
      const bulletins_issued = Math.floor(registered_voters * (0.4 + Math.random() * 0.4));
      const votes_cast = Math.floor(bulletins_issued * (0.9 + Math.random() * 0.1));
      
      constituencies.push({
        id: `constituency-${e + 1}-${i + 1}`,
        name: `Constituency ${e + 1}-${i + 1}`,
        code: `C${e + 1}${i + 1}`,
        region_id: `region-${Math.floor(i / 5) + 1}`,
        region_name: `Region ${Math.floor(i / 5) + 1}`,
        election_id: `election-${e + 1}`,
        registered_voters,
        bulletins_issued,
        votes_cast,
        transaction_count: bulletins_issued + votes_cast + Math.floor(Math.random() * 1000),
        participation_rate: (votes_cast / registered_voters) * 100,
        anomaly_count: Math.floor(Math.random() * 5),
        last_activity: new Date().toISOString(),
      });
    }
  }

  // Generate hourly stats
  const hourly_stats: HourlyStat[] = [];
  const participation_rates: ParticipationRate[] = [];
  const transaction_volumes: TransactionVolume[] = [];
  const hourly_activity: HourlyActivity[] = [];

  // Generate hourly data for each constituency
  for (const constituency of constituencies) {
    const start = new Date(start_date);
    const end = new Date(end_date);
    const hours = Math.floor((end.getTime() - start.getTime()) / (60 * 60 * 1000));
    
    for (let h = 0; h < Math.min(hours, hourly_stats_count); h++) {
      const timestamp = addHours(start, h).toISOString();
      const registered_voters = constituency.registered_voters;
      const bulletins_issued = Math.floor((constituency.bulletins_issued / hours) * (0.8 + Math.random() * 0.4));
      const votes_cast = Math.floor((constituency.votes_cast / hours) * (0.8 + Math.random() * 0.4));
      const transaction_count = bulletins_issued + votes_cast + Math.floor(Math.random() * 50);
      
      hourly_stats.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        bulletins_issued,
        votes_cast,
        transaction_count,
        participation_rate: (votes_cast / registered_voters) * 100,
        anomaly_count: Math.random() > 0.9 ? Math.floor(Math.random() * 3) : 0,
      });

      participation_rates.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        participation_rate: (votes_cast / registered_voters) * 100,
        registered_voters,
        votes_cast,
      });

      transaction_volumes.push({
        timestamp,
        constituency_id: constituency.id,
        election_id: constituency.election_id,
        transaction_count,
        bulletins_issued,
        votes_cast,
      });
    }
  }

  // Generate hourly activity (by hour of day)
  for (let h = 0; h < 24; h++) {
    const hour = h;
    const transaction_count = Math.floor(Math.random() * 1000);
    const bulletins_issued = Math.floor(transaction_count * 0.4);
    const votes_cast = Math.floor(transaction_count * 0.35);
    
    hourly_activity.push({
      hour,
      transaction_count,
      bulletins_issued,
      votes_cast,
    });
  }

  // Generate dashboard metrics
  const activeElection = elections.find(e => e.status === 'active') || elections[0];
  const activeElectionConstituencies = constituencies.filter(c => c.election_id === activeElection.id);
  
  const createMetric = (id: string, label: string, value: number, trend: number): Metric => ({
    id,
    label,
    value,
    trend,
    trendLabel: 'vs. previous period',
  });

  const dashboard_metrics: DashboardMetrics = {
    summary: {
      total_transactions: createMetric(
        'total-transactions',
        'Total Transactions',
        activeElection.transaction_count,
        5.2
      ),
      total_bulletins: createMetric(
        'total-bulletins',
        'Total Bulletins',
        activeElection.bulletins_issued,
        3.8
      ),
      total_votes: createMetric(
        'total-votes',
        'Total Votes',
        activeElection.votes_cast,
        2.5
      ),
      participation_rate: createMetric(
        'participation-rate',
        'Participation Rate',
        activeElection.participation_rate,
        1.2
      ),
      active_constituencies: createMetric(
        'active-constituencies',
        'Active Constituencies',
        activeElectionConstituencies.length,
        0
      ),
      anomalies_detected: createMetric(
        'anomalies-detected',
        'Anomalies Detected',
        activeElectionConstituencies.reduce((sum, c) => sum + c.anomaly_count, 0),
        -2.1
      ),
    },
    hourly_stats: hourly_stats.filter(h => h.election_id === activeElection.id),
    participation_rates: participation_rates.filter(p => p.election_id === activeElection.id),
    transaction_volumes: transaction_volumes.filter(t => t.election_id === activeElection.id),
    hourly_activity,
  };

  return {
    elections,
    constituencies,
    hourly_stats,
    participation_rates,
    transaction_volumes,
    hourly_activity,
    dashboard_metrics,
  };
}

// Create and export a singleton instance of the mock data
export const mockData = generateMockData();

// Helper functions to get mock data for specific entities
export const getMockElection = (id: string): ElectionDetail | undefined => {
  const election = mockData.elections.find(e => e.id === id);
  if (!election) return undefined;

  const electionConstituencies = mockData.constituencies.filter(c => c.election_id === id);
  const electionHourlyStats = mockData.hourly_stats.filter(h => h.election_id === id);
  const electionParticipationRates = mockData.participation_rates.filter(p => p.election_id === id);
  const electionTransactionVolumes = mockData.transaction_volumes.filter(t => t.election_id === id);

  return {
    ...election,
    constituencies: electionConstituencies,
    hourly_stats: electionHourlyStats,
    participation_rates: electionParticipationRates,
    transaction_volumes: electionTransactionVolumes,
    hourly_activity: mockData.hourly_activity,
  };
};

export const getMockConstituency = (id: string): ConstituencyDetail | undefined => {
  const constituency = mockData.constituencies.find(c => c.id === id);
  if (!constituency) return undefined;

  const constituencyHourlyStats = mockData.hourly_stats.filter(h => h.constituency_id === id);
  const constituencyParticipationRates = mockData.participation_rates.filter(p => p.constituency_id === id);
  const constituencyTransactionVolumes = mockData.transaction_volumes.filter(t => t.constituency_id === id);

  return {
    ...constituency,
    hourly_stats: constituencyHourlyStats,
    participation_rates: constituencyParticipationRates,
    transaction_volumes: constituencyTransactionVolumes,
    hourly_activity: mockData.hourly_activity,
  };
};