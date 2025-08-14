import type { Constituency } from '@/types/constituencies';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

export interface ConstituencyTableProps {
  constituencies: Constituency[];
  isLoading: boolean;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  onSort: (column: string) => void;
  onConstituencySelect: (constituency: Constituency) => void;
  className?: string;
}

export function ConstituencyTable({
  constituencies,
  isLoading,
  sortColumn,
  sortDirection,
  onSort,
  onConstituencySelect,
  className,
}: ConstituencyTableProps) {
  const handleSort = (column: string) => {
    onSort(column);
  };

  const getSortIcon = (column: string) => {
    if (sortColumn !== column) return null;
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  const renderSortableHeader = (column: string, label: string) => (
    <div
      className="flex cursor-pointer items-center space-x-1"
      onClick={() => handleSort(column)}
    >
      <span>{label}</span>
      <span className="text-xs">{getSortIcon(column)}</span>
    </div>
  );

  if (isLoading) {
    return (
      <div className={className}>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{renderSortableHeader('name', 'Name')}</TableHead>
              <TableHead>{renderSortableHeader('region_name', 'Region')}</TableHead>
              <TableHead className="text-right">{renderSortableHeader('registered_voters', 'Registered Voters')}</TableHead>
              <TableHead className="text-right">{renderSortableHeader('participation_rate', 'Participation')}</TableHead>
              <TableHead className="text-right">{renderSortableHeader('transaction_count', 'Transactions')}</TableHead>
              <TableHead className="text-right">{renderSortableHeader('anomaly_count', 'Anomalies')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {Array.from({ length: 5 }).map((_, i) => (
              <TableRow key={i}>
                <TableCell><Skeleton className="h-4 w-[120px]" /></TableCell>
                <TableCell><Skeleton className="h-4 w-[80px]" /></TableCell>
                <TableCell className="text-right"><Skeleton className="h-4 w-[60px] ml-auto" /></TableCell>
                <TableCell className="text-right"><Skeleton className="h-4 w-[40px] ml-auto" /></TableCell>
                <TableCell className="text-right"><Skeleton className="h-4 w-[60px] ml-auto" /></TableCell>
                <TableCell className="text-right"><Skeleton className="h-4 w-[30px] ml-auto" /></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    );
  }

  if (!constituencies || constituencies.length === 0) {
    return (
      <div className={cn('rounded-md border p-8 text-center', className)}>
        <p className="text-muted-foreground">No constituencies found</p>
      </div>
    );
  }

  return (
    <div className={className}>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{renderSortableHeader('name', 'Name')}</TableHead>
            <TableHead>{renderSortableHeader('region_name', 'Region')}</TableHead>
            <TableHead className="text-right">{renderSortableHeader('registered_voters', 'Registered Voters')}</TableHead>
            <TableHead className="text-right">{renderSortableHeader('participation_rate', 'Participation')}</TableHead>
            <TableHead className="text-right">{renderSortableHeader('transaction_count', 'Transactions')}</TableHead>
            <TableHead className="text-right">{renderSortableHeader('anomaly_count', 'Anomalies')}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {constituencies.map((constituency) => (
            <TableRow 
              key={constituency.id}
              className="cursor-pointer hover:bg-muted/50"
              onClick={() => onConstituencySelect(constituency)}
            >
              <TableCell className="font-medium">{constituency.name}</TableCell>
              <TableCell>{constituency.region_name}</TableCell>
              <TableCell className="text-right">{constituency.registered_voters.toLocaleString()}</TableCell>
              <TableCell className="text-right">
                <span className={cn(
                  constituency.participation_rate > 70 ? 'text-green-500' : 
                  constituency.participation_rate < 30 ? 'text-red-500' : 
                  'text-yellow-500'
                )}>
                  {constituency.participation_rate.toFixed(1)}%
                </span>
              </TableCell>
              <TableCell className="text-right">{constituency.transaction_count.toLocaleString()}</TableCell>
              <TableCell className="text-right">
                {constituency.anomaly_count > 0 ? (
                  <span className="text-red-500">{constituency.anomaly_count}</span>
                ) : (
                  <span className="text-green-500">0</span>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}