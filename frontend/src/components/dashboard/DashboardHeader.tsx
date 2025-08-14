import type { Election } from '@/types/elections';
import type { TimeRange } from '@/types/metrics';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import { 
  Card,
  CardContent
} from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { DEFAULT_TIME_RANGES } from '@/store/dashboard';

export interface DashboardHeaderProps {
  title: string;
  elections: Election[];
  selectedElection: Election | null;
  timeRange: TimeRange;
  onElectionChange: (election: Election) => void;
  onTimeRangeChange: (timeRange: TimeRange) => void;
  className?: string;
}

export function DashboardHeader({
  title,
  elections,
  selectedElection,
  timeRange,
  onElectionChange,
  onTimeRangeChange,
  className,
}: DashboardHeaderProps) {
  const handleElectionChange = (value: string) => {
    const election = elections.find(e => e.id === value);
    if (election) {
      onElectionChange(election);
    }
  };

  const handleTimeRangeChange = (value: string) => {
    const range = DEFAULT_TIME_RANGES.find(r => r.label === value);
    if (range) {
      onTimeRangeChange(range);
    }
  };

  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
        <div className="mt-2 sm:mt-0">
          {/* Add refresh button or other controls here */}
        </div>
      </div>

      <Card>
        <CardContent className="p-4 grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label htmlFor="election-select" className="text-sm font-medium">
              Election
            </label>
            <Select
              value={selectedElection?.id || ''}
              onValueChange={handleElectionChange}
              disabled={elections.length === 0}
            >
              <SelectTrigger id="election-select">
                <SelectValue placeholder="Select an election" />
              </SelectTrigger>
              <SelectContent>
                {elections.map((election) => (
                  <SelectItem key={election.id} value={election.id}>
                    {election.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label htmlFor="time-range-select" className="text-sm font-medium">
              Time Range
            </label>
            <Select
              value={timeRange.label}
              onValueChange={handleTimeRangeChange}
            >
              <SelectTrigger id="time-range-select">
                <SelectValue placeholder="Select time range" />
              </SelectTrigger>
              <SelectContent>
                {DEFAULT_TIME_RANGES.map((range) => (
                  <SelectItem key={range.label} value={range.label}>
                    {range.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}