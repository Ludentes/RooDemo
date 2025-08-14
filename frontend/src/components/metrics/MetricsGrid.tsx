import { cn } from '@/lib/utils';

export interface MetricsGridProps {
  children: React.ReactNode;
  className?: string;
}

export function MetricsGrid({ children, className }: MetricsGridProps) {
  return (
    <div className={cn('grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6', className)}>
      {children}
    </div>
  );
}