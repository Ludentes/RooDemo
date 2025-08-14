import type { ParticipationRate } from '@/types/metrics';
import { 
  Line, 
  LineChart, 
  CartesianGrid, 
  XAxis, 
  YAxis, 
  ResponsiveContainer,
  Tooltip,
  Legend,
  ReferenceLine
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

export interface ParticipationRateChartProps {
  data: ParticipationRate[];
  isLoading?: boolean;
  className?: string;
  title?: string;
}

export function ParticipationRateChart({ 
  data, 
  isLoading = false, 
  className,
  title = "Participation Rate" 
}: ParticipationRateChartProps) {
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
    participation_rate: Number(item.participation_rate.toFixed(2))
  }));

  // Calculate average participation rate
  const avgParticipationRate = formattedData.reduce(
    (sum, item) => sum + item.participation_rate, 
    0
  ) / formattedData.length;

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={formattedData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
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
                domain={[0, 100]}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip 
                formatter={(value) => [`${value}%`, 'Participation Rate']}
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
              <ReferenceLine 
                y={avgParticipationRate} 
                stroke="var(--muted-foreground)" 
                strokeDasharray="3 3" 
                label={{ 
                  value: `Avg: ${avgParticipationRate.toFixed(2)}%`,
                  position: 'right',
                  fill: 'var(--muted-foreground)',
                  fontSize: 12
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="participation_rate" 
                stroke="var(--chart-4)" 
                strokeWidth={2}
                dot={{ r: 3, fill: 'var(--chart-4)' }}
                activeDot={{ r: 5 }}
                name="Participation Rate"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}