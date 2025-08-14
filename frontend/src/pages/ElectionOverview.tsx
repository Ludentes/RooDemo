import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/dashboard/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { TransactionVolumeChart } from '@/components/metrics/TransactionVolumeChart';
import { ParticipationRateChart } from '@/components/metrics/ParticipationRateChart';
import { ConstituencyTable } from '@/components/constituencies/ConstituencyTable';
import { ConstituencyCard } from '@/components/constituencies/ConstituencyCard';
import { electionsApi } from '@/lib/api';
import type { ElectionDetail } from '@/types/elections';
import type { Constituency } from '@/types/constituencies';

export default function ElectionOverviewPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [election, setElection] = useState<ElectionDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [sortColumn, setSortColumn] = useState<string>('name');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  
  useEffect(() => {
    const fetchElectionDetail = async () => {
      if (!id) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await electionsApi.getElectionById(id);
        setElection(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch election details'));
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchElectionDetail();
  }, [id]);
  
  const handleBack = () => {
    navigate(-1);
  };
  
  const handleSort = (column: string) => {
    const newDirection = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
    setSortColumn(column);
    setSortDirection(newDirection);
  };
  
  const handleConstituencySelect = (constituency: Constituency) => {
    navigate(`/constituencies/${constituency.id}`);
  };
  
  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center space-x-2 mb-6">
          <Button variant="outline" onClick={handleBack}>
            Back
          </Button>
          <Skeleton className="h-8 w-64" />
        </div>
        
        <div className="grid gap-6">
          <Skeleton className="h-[200px] w-full" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Skeleton className="h-[300px] w-full" />
            <Skeleton className="h-[300px] w-full" />
          </div>
          <Skeleton className="h-[400px] w-full" />
        </div>
      </DashboardLayout>
    );
  }
  
  if (error || !election) {
    return (
      <DashboardLayout>
        <div className="flex items-center space-x-2 mb-6">
          <Button variant="outline" onClick={handleBack}>
            Back
          </Button>
          <h1 className="text-2xl font-bold">Error</h1>
        </div>
        
        <Card>
          <CardContent className="p-6">
            <p className="text-red-500">
              {error ? error.message : 'Election not found'}
            </p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }
  
  // Format date
  const electionDate = new Date(election.date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  
  // Get status badge color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'upcoming':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <DashboardLayout>
      <div className="flex items-center space-x-2 mb-6">
        <Button variant="outline" onClick={handleBack}>
          Back
        </Button>
        <h1 className="text-2xl font-bold">{election.name}</h1>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(election.status)}`}>
          {election.status.charAt(0).toUpperCase() + election.status.slice(1)}
        </span>
      </div>
      
      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Date</h3>
                <p className="text-lg font-medium">{electionDate}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Constituencies</h3>
                <p className="text-lg font-medium">{election.constituency_count.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Registered Voters</h3>
                <p className="text-lg font-medium">{election.registered_voters.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Participation Rate</h3>
                <p className="text-lg font-medium">{election.participation_rate.toFixed(1)}%</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Bulletins Issued</h3>
                <p className="text-lg font-medium">{election.bulletins_issued.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Votes Cast</h3>
                <p className="text-lg font-medium">{election.votes_cast.toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <TransactionVolumeChart 
            data={election.transaction_volumes} 
            title="Transaction Volume" 
          />
          <ParticipationRateChart 
            data={election.participation_rates} 
            title="Participation Rate" 
          />
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle>Constituencies</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <ConstituencyTable
              constituencies={election.constituencies}
              isLoading={false}
              sortColumn={sortColumn}
              sortDirection={sortDirection}
              onSort={handleSort}
              onConstituencySelect={handleConstituencySelect}
            />
          </CardContent>
        </Card>
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Top Constituencies by Participation</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {election.constituencies
              .sort((a, b) => b.participation_rate - a.participation_rate)
              .slice(0, 3)
              .map(constituency => (
                <ConstituencyCard
                  key={constituency.id}
                  constituency={constituency}
                  onClick={() => handleConstituencySelect(constituency)}
                />
              ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}