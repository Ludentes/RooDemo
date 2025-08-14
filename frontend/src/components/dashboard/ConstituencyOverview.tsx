import type { Constituency } from '@/types/constituencies';
import type { ConstituencyFilter } from '@/types/constituencies';
import { ConstituencyTable } from '@/components/constituencies/ConstituencyTable';
import { ConstituencyFilters } from '@/components/constituencies/ConstituencyFilters';
import { ConstituencySearch } from '@/components/constituencies/ConstituencySearch';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { useState } from 'react';

export interface ConstituencyOverviewProps {
  constituencies: Constituency[];
  isLoading: boolean;
  filters: ConstituencyFilter;
  onFilterChange: (filters: ConstituencyFilter) => void;
  onConstituencySelect: (constituency: Constituency) => void;
  className?: string;
}

export function ConstituencyOverview({
  constituencies,
  isLoading,
  filters,
  onFilterChange,
  onConstituencySelect,
  className,
}: ConstituencyOverviewProps) {
  const [sortColumn, setSortColumn] = useState<string>(filters.sort_by || 'name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>(
    filters.sort_direction || 'asc'
  );

  const handleSort = (column: string) => {
    const newDirection = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
    setSortColumn(column);
    setSortDirection(newDirection);
    onFilterChange({
      ...filters,
      sort_by: column,
      sort_direction: newDirection,
    });
  };

  const handleSearchChange = (query: string) => {
    onFilterChange({
      ...filters,
      search: query || undefined,
    });
  };

  // Extract unique regions from constituencies for the filter dropdown
  const regions = constituencies
    .reduce<{ id: string; name: string }[]>((acc, constituency) => {
      if (!acc.some(r => r.id === constituency.region_id)) {
        acc.push({
          id: constituency.region_id,
          name: constituency.region_name,
        });
      }
      return acc;
    }, [])
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className={cn('space-y-4', className)}>
      <h2 className="text-xl font-semibold">Constituencies</h2>
      
      <div className="grid gap-4 md:grid-cols-4">
        <div className="md:col-span-3">
          <ConstituencySearch
            searchQuery={filters.search || ''}
            onSearchChange={handleSearchChange}
          />
        </div>
        <div className="md:col-span-1">
          <Card>
            <CardHeader className="py-2">
              <CardTitle className="text-sm">Total: {constituencies.length}</CardTitle>
            </CardHeader>
          </Card>
        </div>
      </div>
      
      <ConstituencyFilters
        filters={filters}
        onFilterChange={onFilterChange}
        regions={regions}
      />
      
      <Card>
        <CardContent className="p-0">
          <ConstituencyTable
            constituencies={constituencies}
            isLoading={isLoading}
            sortColumn={sortColumn}
            sortDirection={sortDirection}
            onSort={handleSort}
            onConstituencySelect={onConstituencySelect}
          />
        </CardContent>
      </Card>
    </div>
  );
}