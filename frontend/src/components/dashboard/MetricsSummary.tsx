import type { Metric } from '@/types/metrics';
import { MetricCard } from '@/components/metrics/MetricCard';
import { MetricsGrid } from '@/components/metrics/MetricsGrid';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

export interface MetricsSummaryProps {
  metrics?: {
    total_transactions: Metric;
    total_bulletins: Metric;
    total_votes: Metric;
    participation_rate: Metric;
    active_constituencies: Metric;
    anomalies_detected: Metric;
  };
  isLoading: boolean;
  className?: string;
}

export function MetricsSummary({ metrics, isLoading, className }: MetricsSummaryProps) {
  if (isLoading) {
    return (
      <div className={cn('space-y-4', className)}>
        <h2 className="text-xl font-semibold">Summary</h2>
        <MetricsGrid>
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-[120px] w-full" />
          ))}
        </MetricsGrid>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className={cn('space-y-4', className)}>
        <h2 className="text-xl font-semibold">Summary</h2>
        <div className="rounded-md border p-8 text-center">
          <p className="text-muted-foreground">No metrics available</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('space-y-4', className)}>
      <h2 className="text-xl font-semibold">Summary</h2>
      <MetricsGrid>
        <MetricCard metric={metrics.total_transactions} />
        <MetricCard metric={metrics.total_bulletins} />
        <MetricCard metric={metrics.total_votes} />
        <MetricCard metric={metrics.participation_rate} />
        <MetricCard metric={metrics.active_constituencies} />
        <MetricCard metric={metrics.anomalies_detected} />
      </MetricsGrid>
    </div>
  );
}