import type { Constituency } from '@/types/constituencies';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Skeleton } from '@/components/ui/skeleton';
import { format, parseISO } from 'date-fns';

export interface ConstituencyCardProps {
  constituency: Constituency;
  isLoading?: boolean;
  className?: string;
  onClick?: () => void;
}

export function ConstituencyCard({
  constituency,
  isLoading = false,
  className,
  onClick,
}: ConstituencyCardProps) {
  if (isLoading) {
    return (
      <Card className={cn('overflow-hidden', className)}>
        <CardHeader>
          <Skeleton className="h-5 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </CardHeader>
        <CardContent className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
        </CardContent>
        <CardFooter>
          <Skeleton className="h-4 w-1/3" />
        </CardFooter>
      </Card>
    );
  }

  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  return (
    <Card 
      className={cn(
        'overflow-hidden transition-shadow hover:shadow-md', 
        onClick && 'cursor-pointer',
        className
      )}
      onClick={handleClick}
    >
      <CardHeader>
        <CardTitle>{constituency.name}</CardTitle>
        <p className="text-sm text-muted-foreground">{constituency.region_name}</p>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex justify-between">
          <span className="text-sm text-muted-foreground">Registered Voters:</span>
          <span className="font-medium">{constituency.registered_voters.toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-muted-foreground">Participation Rate:</span>
          <span 
            className={cn(
              'font-medium',
              constituency.participation_rate > 70 ? 'text-green-500' : 
              constituency.participation_rate < 30 ? 'text-red-500' : 
              'text-yellow-500'
            )}
          >
            {constituency.participation_rate.toFixed(1)}%
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-muted-foreground">Transactions:</span>
          <span className="font-medium">{constituency.transaction_count.toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-muted-foreground">Anomalies:</span>
          <span 
            className={cn(
              'font-medium',
              constituency.anomaly_count > 0 ? 'text-red-500' : 'text-green-500'
            )}
          >
            {constituency.anomaly_count}
          </span>
        </div>
      </CardContent>
      <CardFooter>
        <p className="text-xs text-muted-foreground">
          Last activity: {format(parseISO(constituency.last_activity), 'MMM d, yyyy HH:mm')}
        </p>
      </CardFooter>
    </Card>
  );
}