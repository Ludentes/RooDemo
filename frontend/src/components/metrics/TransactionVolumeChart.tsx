import type { TransactionVolume } from '@/types/metrics';
import { 
  Bar, 
  BarChart, 
  CartesianGrid, 
  XAxis, 
  YAxis, 
  ResponsiveContainer,
  Tooltip,
  Legend
} from 'recharts';
import { 
  Card,
  CardContent,
  CardHeader,
  CardTitle
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';
import { format, parseISO } from 'date-fns';

export interface TransactionVolumeChartProps {
  data: TransactionVolume[];
  isLoading?: boolean;
  className?: string;
  title?: string;
}

export function TransactionVolumeChart({ 
  data, 
  isLoading = false, 
  className,
  title = "Transaction Volume" 
}: TransactionVolumeChartProps) {
  if (isLoading) {
    return (
      <Card className={cn('overflow-hidden', className)}>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-[300px] w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Card className={cn('overflow-hidden', className)}>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-[300px] w-full items-center justify-center text-muted-foreground">
            No data available
          </div>
        </CardContent>
      </Card>
    );
  }

  const formattedData = data.map(item => ({
    ...item,
    timestamp: format(parseISO(item.timestamp), 'HH:mm'),
  }));

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={formattedData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis 
                dataKey="timestamp" 
                tickLine={false} 
                axisLine={false}
                tickMargin={10}
              />
              <YAxis 
                tickLine={false} 
                axisLine={false}
                tickMargin={10}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'var(--background)', 
                  borderColor: 'var(--border)',
                  borderRadius: '0.5rem',
                  boxShadow: 'var(--shadow)'
                }}
                itemStyle={{ color: 'var(--foreground)' }}
                labelStyle={{ color: 'var(--foreground)' }}
              />
              <Legend />
              <Bar 
                dataKey="transaction_count" 
                fill="var(--chart-1)" 
                radius={[4, 4, 0, 0]} 
                name="Transactions"
              />
              <Bar 
                dataKey="bulletins_issued" 
                fill="var(--chart-2)" 
                radius={[4, 4, 0, 0]} 
                name="Bulletins Issued"
              />
              <Bar 
                dataKey="votes_cast" 
                fill="var(--chart-3)" 
                radius={[4, 4, 0, 0]} 
                name="Votes Cast"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}