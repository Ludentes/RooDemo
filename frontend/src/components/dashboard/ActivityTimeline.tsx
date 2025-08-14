import type { TransactionVolume, TimeRange } from '@/types/metrics';
import { TransactionVolumeChart } from '@/components/metrics/TransactionVolumeChart';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { useState } from 'react';

export interface ActivityTimelineProps {
  data: TransactionVolume[];
  timeRange: TimeRange;
  isLoading: boolean;
  onTimePointSelect?: (timestamp: string) => void;
  className?: string;
}

export function ActivityTimeline({
  data,
  timeRange,
  isLoading,
  onTimePointSelect,
  className,
}: ActivityTimelineProps) {
  const [selectedTimestamp, setSelectedTimestamp] = useState<string | null>(null);

  const handleTimePointSelect = (timestamp: string) => {
    setSelectedTimestamp(timestamp);
    if (onTimePointSelect) {
      onTimePointSelect(timestamp);
    }
  };

  return (
    <div className={cn('space-y-4', className)}>
      <h2 className="text-xl font-semibold">Activity Timeline</h2>
      <Card>
        <CardHeader>
          <CardTitle>Transaction Volume ({timeRange.label})</CardTitle>
        </CardHeader>
        <CardContent>
          <TransactionVolumeChart 
            data={data} 
            isLoading={isLoading} 
            title="" 
          />
        </CardContent>
      </Card>
    </div>
  );
}