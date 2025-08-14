import type { ConstituencyFilter } from '@/types/constituencies';
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
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { cn } from '@/lib/utils';
import { useState, useEffect } from 'react';

export interface ConstituencyFiltersProps {
  filters: ConstituencyFilter;
  onFilterChange: (filters: ConstituencyFilter) => void;
  regions?: { id: string; name: string }[];
  className?: string;
}

export function ConstituencyFilters({
  filters,
  onFilterChange,
  regions = [],
  className,
}: ConstituencyFiltersProps) {
  const [participationRange, setParticipationRange] = useState<[number, number]>([
    filters.min_participation_rate || 0,
    filters.max_participation_rate || 100,
  ]);

  // Update participation range when filters change
  useEffect(() => {
    setParticipationRange([
      filters.min_participation_rate || 0,
      filters.max_participation_rate || 100,
    ]);
  }, [filters.min_participation_rate, filters.max_participation_rate]);

  const handleRegionChange = (value: string) => {
    onFilterChange({
      ...filters,
      region_id: value === 'all' ? undefined : value,
    });
  };

  const handleSortChange = (value: string) => {
    const [sortBy, sortDirection] = value.split('-');
    onFilterChange({
      ...filters,
      sort_by: sortBy,
      sort_direction: sortDirection as 'asc' | 'desc',
    });
  };

  const handleAnomaliesChange = (checked: boolean) => {
    onFilterChange({
      ...filters,
      has_anomalies: checked || undefined,
    });
  };

  const handleParticipationRangeChange = (value: [number, number]) => {
    setParticipationRange(value);
  };

  const handleParticipationRangeCommit = () => {
    onFilterChange({
      ...filters,
      min_participation_rate: participationRange[0],
      max_participation_rate: participationRange[1],
    });
  };

  // Determine current sort value for select
  const currentSortValue = filters.sort_by && filters.sort_direction
    ? `${filters.sort_by}-${filters.sort_direction}`
    : 'name-asc';

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardContent className="p-4 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="space-y-2">
          <Label htmlFor="region-filter">Region</Label>
          <Select
            value={filters.region_id || 'all'}
            onValueChange={handleRegionChange}
          >
            <SelectTrigger id="region-filter">
              <SelectValue placeholder="All Regions" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Regions</SelectItem>
              {regions.map((region) => (
                <SelectItem key={region.id} value={region.id}>
                  {region.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="sort-filter">Sort By</Label>
          <Select
            value={currentSortValue}
            onValueChange={handleSortChange}
          >
            <SelectTrigger id="sort-filter">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="name-asc">Name (A-Z)</SelectItem>
              <SelectItem value="name-desc">Name (Z-A)</SelectItem>
              <SelectItem value="participation_rate-desc">Participation (High-Low)</SelectItem>
              <SelectItem value="participation_rate-asc">Participation (Low-High)</SelectItem>
              <SelectItem value="transaction_count-desc">Transactions (High-Low)</SelectItem>
              <SelectItem value="transaction_count-asc">Transactions (Low-High)</SelectItem>
              <SelectItem value="anomaly_count-desc">Anomalies (High-Low)</SelectItem>
              <SelectItem value="anomaly_count-asc">Anomalies (Low-High)</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2 lg:col-span-2">
          <div className="flex justify-between">
            <Label htmlFor="participation-range">Participation Rate</Label>
            <span className="text-sm text-muted-foreground">
              {participationRange[0]}% - {participationRange[1]}%
            </span>
          </div>
          <Slider
            id="participation-range"
            min={0}
            max={100}
            step={1}
            value={participationRange}
            onValueChange={handleParticipationRangeChange}
            onValueCommit={handleParticipationRangeCommit}
            className="py-4"
          />
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="anomalies-filter"
            checked={!!filters.has_anomalies}
            onCheckedChange={handleAnomaliesChange}
          />
          <Label htmlFor="anomalies-filter" className="cursor-pointer">
            Show only constituencies with anomalies
          </Label>
        </div>
      </CardContent>
    </Card>
  );
}