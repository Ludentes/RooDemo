import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from '@/pages/Dashboard';
import ConstituencyDetail from '@/pages/ConstituencyDetail';
import ElectionOverview from '@/pages/ElectionOverview';
import { AppLayout } from '@/components/layout/AppLayout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/constituencies/:id" element={<ConstituencyDetail />} />
        <Route path="/elections/:id" element={<ElectionOverview />} />
      </Routes>
    </Router>
  );
}

export default App;
