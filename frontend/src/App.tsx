import { useEffect } from 'react';
import { AppLayout } from '@/components/layout/AppLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useElectionsStore } from '@/store';

function App() {
  const { elections, constituencies, fetchElections, fetchConstituencies, loading } = useElectionsStore();
  
  useEffect(() => {
    fetchElections();
    fetchConstituencies();
  }, [fetchElections, fetchConstituencies]);
  
  return (
    <AppLayout>
      <div className="grid gap-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Total Elections</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">{loading ? '...' : elections.length}</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Active Elections</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">
                {loading ? '...' : elections.filter(e => e.status === 'active').length}
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Constituencies</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">{loading ? '...' : constituencies.length}</p>
            </CardContent>
          </Card>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle>Recent Elections</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-gray-500">Loading...</p>
            ) : elections.length === 0 ? (
              <p className="text-gray-500">No elections found.</p>
            ) : (
              <div className="space-y-4">
                {elections.map(election => (
                  <div key={election.id} className="rounded-lg border p-4">
                    <h3 className="font-medium">{election.name}</h3>
                    <p className="text-sm text-gray-500">Date: {election.date}</p>
                    <p className="text-sm text-gray-500">
                      Status: <span className="capitalize">{election.status}</span>
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  );
}

export default App;
