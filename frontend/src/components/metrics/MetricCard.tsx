import type { Metric } from '@/types/metrics';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Skeleton } from '@/components/ui/skeleton';

export interface MetricCardProps {
  metric: Metric;
  isLoading?: boolean;
  className?: string;
}

export function MetricCard({ metric, isLoading = false, className }: MetricCardProps) {
  if (isLoading) {
    return (
      <Card className={cn('overflow-hidden', className)}>
        <CardHeader className="pb-2">
          <Skeleton className="h-4 w-1/2" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-10 w-3/4" />
        </CardContent>
        <CardFooter>
          <Skeleton className="h-4 w-1/3" />
        </CardFooter>
      </Card>
    );
  }

  const trendColor = metric.trend > 0 ? 'text-green-500' : metric.trend < 0 ? 'text-red-500' : 'text-gray-500';
  const trendIcon = metric.trend > 0 ? '↑' : metric.trend < 0 ? '↓' : '→';

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{metric.label}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{metric.value.toLocaleString()}</div>
      </CardContent>
      {metric.trend !== 0 && (
        <CardFooter>
          <div className={cn('flex items-center text-sm', trendColor)}>
            <span className="mr-1">{trendIcon}</span>
            <span>{Math.abs(metric.trend)}%</span>
            <span className="ml-1 text-muted-foreground">{metric.trendLabel}</span>
          </div>
        </CardFooter>
      )}
    </Card>
  );
}