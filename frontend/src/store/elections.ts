import { create } from 'zustand';

interface Election {
  id: string;
  name: string;
  date: string;
  status: 'upcoming' | 'active' | 'completed';
  constituencies: string[];
}

interface Constituency {
  id: string;
  name: string;
  region: string;
  electionId: string;
}

interface Transaction {
  id: string;
  constituencyId: string;
  electionId: string;
  timestamp: string;
  data: Record<string, any>;
}

interface ElectionsState {
  elections: Election[];
  constituencies: Constituency[];
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
  
  // Elections actions
  fetchElections: () => Promise<void>;
  addElection: (election: Omit<Election, 'id'>) => Promise<void>;
  updateElection: (id: string, data: Partial<Election>) => Promise<void>;
  deleteElection: (id: string) => Promise<void>;
  
  // Constituencies actions
  fetchConstituencies: (electionId?: string) => Promise<void>;
  addConstituency: (constituency: Omit<Constituency, 'id'>) => Promise<void>;
  updateConstituency: (id: string, data: Partial<Constituency>) => Promise<void>;
  deleteConstituency: (id: string) => Promise<void>;
  
  // Transactions actions
  fetchTransactions: (filters?: { electionId?: string; constituencyId?: string }) => Promise<void>;
}

// Mock API functions (to be replaced with actual API calls)
const mockFetchElections = async (): Promise<Election[]> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  return [
    {
      id: '1',
      name: 'Presidential Election 2025',
      date: '2025-11-04',
      status: 'upcoming',
      constituencies: ['1', '2', '3']
    },
    {
      id: '2',
      name: 'Local Elections 2025',
      date: '2025-05-15',
      status: 'upcoming',
      constituencies: ['4', '5']
    }
  ];
};

export const useElectionsStore = create<ElectionsState>()((set, get) => ({
  elections: [],
  constituencies: [],
  transactions: [],
  loading: false,
  error: null,
  
  // Elections actions
  fetchElections: async () => {
    set({ loading: true, error: null });
    try {
      const elections = await mockFetchElections();
      set({ elections, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  addElection: async (election) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      const newElection = {
        ...election,
        id: Math.random().toString(36).substring(2, 9)
      };
      set(state => ({ 
        elections: [...state.elections, newElection],
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  updateElection: async (id, data) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      set(state => ({
        elections: state.elections.map(election => 
          election.id === id ? { ...election, ...data } : election
        ),
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  deleteElection: async (id) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      set(state => ({
        elections: state.elections.filter(election => election.id !== id),
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  // Constituencies actions
  fetchConstituencies: async (electionId) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      // Mock data
      const constituencies = [
        { id: '1', name: 'District 1', region: 'North', electionId: '1' },
        { id: '2', name: 'District 2', region: 'South', electionId: '1' },
        { id: '3', name: 'District 3', region: 'East', electionId: '1' },
        { id: '4', name: 'District 4', region: 'West', electionId: '2' },
        { id: '5', name: 'District 5', region: 'Central', electionId: '2' },
      ];
      
      const filtered = electionId 
        ? constituencies.filter(c => c.electionId === electionId)
        : constituencies;
        
      set({ constituencies: filtered, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  addConstituency: async (constituency) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      const newConstituency = {
        ...constituency,
        id: Math.random().toString(36).substring(2, 9)
      };
      set(state => ({ 
        constituencies: [...state.constituencies, newConstituency],
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  updateConstituency: async (id, data) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      set(state => ({
        constituencies: state.constituencies.map(constituency => 
          constituency.id === id ? { ...constituency, ...data } : constituency
        ),
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  deleteConstituency: async (id) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      set(state => ({
        constituencies: state.constituencies.filter(constituency => constituency.id !== id),
        loading: false
      }));
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  
  // Transactions actions
  fetchTransactions: async (filters) => {
    set({ loading: true, error: null });
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      // Mock empty data for now
      set({ transactions: [], loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  }
}));