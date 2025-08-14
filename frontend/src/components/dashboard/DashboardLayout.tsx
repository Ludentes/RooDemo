import { cn } from '@/lib/utils';

export interface DashboardLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className={cn('container mx-auto py-6 space-y-8', className)}>
      {children}
    </div>
  );
}