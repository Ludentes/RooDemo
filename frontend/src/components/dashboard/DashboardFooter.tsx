import { cn } from '@/lib/utils';
import { format, parseISO } from 'date-fns';

export interface DashboardFooterProps {
  lastUpdated?: string;
  className?: string;
}

export function DashboardFooter({ lastUpdated, className }: DashboardFooterProps) {
  return (
    <div className={cn('border-t py-4 text-center text-sm text-muted-foreground', className)}>
      <div className="flex items-center justify-center space-x-1">
        <span>Data last updated:</span>
        <span className="font-medium">
          {lastUpdated
            ? format(parseISO(lastUpdated), 'MMM d, yyyy HH:mm:ss')
            : 'Never'}
        </span>
      </div>
      <div className="mt-1">
        <span>Election Monitoring System</span>
      </div>
    </div>
  );
}