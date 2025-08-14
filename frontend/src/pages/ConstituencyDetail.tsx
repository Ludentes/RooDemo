import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/dashboard/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { TransactionVolumeChart } from '@/components/metrics/TransactionVolumeChart';
import { ParticipationRateChart } from '@/components/metrics/ParticipationRateChart';
import { HourlyActivityChart } from '@/components/metrics/HourlyActivityChart';
import { useDashboardStore } from '@/store/dashboard';
import { constituenciesApi } from '@/lib/api';
import type { ConstituencyDetail } from '@/types/constituencies';

export default function ConstituencyDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [constituency, setConstituency] = useState<ConstituencyDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  const { selectedElection } = useDashboardStore();
  
  useEffect(() => {
    const fetchConstituencyDetail = async () => {
      if (!id) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await constituenciesApi.getConstituencyById(id);
        setConstituency(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch constituency details'));
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchConstituencyDetail();
  }, [id]);
  
  const handleBack = () => {
    navigate(-1);
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
          <Skeleton className="h-[300px] w-full" />
        </div>
      </DashboardLayout>
    );
  }
  
  if (error || !constituency) {
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
              {error ? error.message : 'Constituency not found'}
            </p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }
  
  return (
    <DashboardLayout>
      <div className="flex items-center space-x-2 mb-6">
        <Button variant="outline" onClick={handleBack}>
          Back
        </Button>
        <h1 className="text-2xl font-bold">{constituency.name}</h1>
        <span className="text-muted-foreground">({constituency.code})</span>
      </div>
      
      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Region</h3>
                <p className="text-lg font-medium">{constituency.region_name}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Registered Voters</h3>
                <p className="text-lg font-medium">{constituency.registered_voters.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Participation Rate</h3>
                <p className="text-lg font-medium">{constituency.participation_rate.toFixed(1)}%</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Bulletins Issued</h3>
                <p className="text-lg font-medium">{constituency.bulletins_issued.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Votes Cast</h3>
                <p className="text-lg font-medium">{constituency.votes_cast.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-muted-foreground">Anomalies</h3>
                <p className={`text-lg font-medium ${constituency.anomaly_count > 0 ? 'text-red-500' : 'text-green-500'}`}>
                  {constituency.anomaly_count}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <TransactionVolumeChart 
            data={constituency.transaction_volumes} 
            title="Transaction Volume" 
          />
          <ParticipationRateChart 
            data={constituency.participation_rates} 
            title="Participation Rate" 
          />
        </div>
        
        <HourlyActivityChart 
          data={constituency.hourly_activity} 
          title="Hourly Activity" 
        />
      </div>
    </DashboardLayout>
  );
}