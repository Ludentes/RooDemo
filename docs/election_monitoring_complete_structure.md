# Election Monitoring System - MVP Complete Structure

## 0. Technology Stack and Implementation Structure

### Backend Components

| Component | Version | Description |
|-----------|---------|-------------|
| FastAPI | 0.115.13 | Web framework for building APIs |
| SQLAlchemy | 2.0.41 | SQL toolkit and Object-Relational Mapper |
| Pydantic | 2.5.0 | Data validation and settings management |
| Alembic | 1.13.0 | Database migration tool |

### Recommended File Structure for Core Data Models

```
backend/
  app/
    models/
      __init__.py       # Exports all models
      database.py       # Base class and database connection
      election.py       # Election model
      constituency.py   # Constituency model
      transaction.py    # Transaction model
      alert.py          # Alert model
      hourly_stats.py   # HourlyStats model
      file_processing.py # FileProcessingJob model
    
    models/schemas/
      __init__.py       # Exports all schemas
      base.py           # Base schemas and common validators
      election.py       # Election schemas
      constituency.py   # Constituency schemas
      transaction.py    # Transaction schemas
      alert.py          # Alert schemas
      hourly_stats.py   # HourlyStats schemas
      file_processing.py # FileProcessingJob schemas
    
    crud/
      __init__.py       # Exports all CRUD modules
      base.py           # Base CRUD operations
      election.py       # Election CRUD
      constituency.py   # Constituency CRUD
      transaction.py    # Transaction CRUD
      alert.py          # Alert CRUD
      hourly_stats.py   # HourlyStats CRUD
      file_processing.py # FileProcessingJob CRUD
```

### Implementation Approach

The core data models implementation follows a systematic approach with triple-gate control:

1. **Gate 1**: AI Self-Verification (Automated)
   - Code compiles without errors
   - Type checking passes
   - Basic validation complete

2. **Gate 2**: Mandatory Human Verification (Manual)
   - Run/execute the code manually
   - Inspect output with your own eyes
   - Review code changes line by line

3. **Gate 3**: Understanding Validation (Quiz)
   - Explain key technical decisions
   - Demonstrate understanding of edge cases
   - Show ability to modify for different requirements

This ensures high-quality implementation with proper knowledge transfer.

## 1. API Specification (FastAPI)

### Base URL: `http://localhost:8000`

### Endpoints

#### Dashboard
```python
GET /api/dashboard
Response: DashboardSummary

GET /api/dashboard/activity
Response: RealTimeActivity

GET /api/dashboard/ws
WebSocket: Real-time updates
```

#### Constituencies
```python
GET /api/constituencies
Query: ?region=string&status=string&limit=int&offset=int
Response: List[ConstituencyOverview]

GET /api/constituencies/{constituency_id}
Response: ConstituencyDetail

GET /api/constituencies/{constituency_id}/transactions
Query: ?limit=int&offset=int&hours=int
Response: List[Transaction]

GET /api/constituencies/{constituency_id}/stats
Query: ?hours=int
Response: List[HourlyStats]
```

#### Alerts
```python
GET /api/alerts
Query: ?severity=string&status=string&limit=int&offset=int
Response: List[Alert]

GET /api/alerts/{alert_id}
Response: AlertDetail

PUT /api/alerts/{alert_id}/status
Body: {"status": "investigating|resolved|snoozed", "notes": "string"}
Response: Alert

POST /api/alerts/{alert_id}/notes
Body: {"note": "string"}
Response: Alert
```

#### File Processing
```python
POST /api/files/upload
Body: multipart/form-data with CSV file
Response: {"message": "Processing started", "job_id": "string"}

GET /api/files/status/{job_id}
Response: {"status": "processing|completed|failed", "details": "string"}
```

#### Health
```python
GET /api/health
Response: {"status": "ok", "timestamp": "ISO string"}
```

### Response Models

```python
# Dashboard
DashboardSummary {
  totalConstituencies: int
  activeConstituencies: int
  offlineConstituencies: int
  totalBulletins: int
  totalVotes: int
  participationRate: float
  lastUpdate: datetime
  criticalAlerts: int
  warningAlerts: int
}

RealTimeActivity {
  votesPerHour: int
  bulletinsPerHour: int
  activityTimeline: List[ActivityPoint]
}

ActivityPoint {
  hour: datetime
  votes: int
  bulletins: int
}

# Constituencies
ConstituencyOverview {
  id: str
  name: str
  region: str
  type: str
  bulletinsIssued: int
  votesCast: int
  participationRate: float
  status: str
  lastActivity: datetime
  anomalyScore: float
  hasAlerts: bool
}

ConstituencyDetail {
  id: str
  name: str
  region: str
  type: str
  registeredVoters: int
  bulletinsIssued: int
  votesCast: int
  participationRate: float
  status: str
  lastActivity: datetime
  anomalyScore: float
  hourlyStats: List[HourlyStats]
  recentTransactions: List[Transaction]
  alerts: List[Alert]
  comparativeMetrics: ComparativeMetrics
}

ComparativeMetrics {
  vsRegionalAverage: float
  vsHistorical: float
  vsSimilarType: float
}

# Transactions
Transaction {
  id: str
  constituencyId: str
  type: str
  timestamp: datetime
  blockHeight: int
  details: dict
}

# Alerts
Alert {
  id: str
  constituencyId: str
  constituencyName: str
  type: str
  severity: str
  status: str
  title: str
  description: str
  details: dict
  createdAt: datetime
  detectedAt: datetime
  resolvedAt: datetime | null
  notes: List[str]
}

# Statistics
HourlyStats {
  hour: datetime
  bulletinsIssued: int
  votesCast: int
  transactionCount: int
  bulletinVelocity: float
  voteVelocity: float
}
```

## 2. Frontend Data Model (Zustand State Manager)

### Why Zustand?
- Simple, lightweight
- No boilerplate
- TypeScript friendly
- Perfect for MVP scope

### State Structure

```typescript
// stores/types.ts
export interface DashboardState {
  summary: DashboardSummary | null
  activity: RealTimeActivity | null
  isLoading: boolean
  lastUpdate: Date | null
  error: string | null
}

export interface ConstituencyState {
  constituencies: ConstituencyOverview[]
  selectedConstituency: ConstituencyDetail | null
  filters: {
    region?: string
    status?: string
    search?: string
  }
  pagination: {
    page: number
    limit: number
    total: number
  }
  isLoading: boolean
  error: string | null
}

export interface AlertState {
  alerts: Alert[]
  selectedAlert: Alert | null
  filters: {
    severity?: string
    status?: string
  }
  pagination: {
    page: number
    limit: number
    total: number
  }
  isLoading: boolean
  error: string | null
}

export interface AppState {
  isConnected: boolean
  websocket: WebSocket | null
  notifications: Notification[]
}

// stores/dashboardStore.ts
import { create } from 'zustand'
import { DashboardState, DashboardSummary, RealTimeActivity } from './types'
import { dashboardService } from '../services/dashboardService'

interface DashboardStore extends DashboardState {
  // Actions
  fetchDashboard: () => Promise<void>
  fetchActivity: () => Promise<void>
  setError: (error: string | null) => void
  reset: () => void
}

export const useDashboardStore = create<DashboardStore>((set, get) => ({
  // Initial state
  summary: null,
  activity: null,
  isLoading: false,
  lastUpdate: null,
  error: null,

  // Actions
  fetchDashboard: async () => {
    set({ isLoading: true, error: null })
    try {
      const summary = await dashboardService.getSummary()
      set({ summary, lastUpdate: new Date(), isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  fetchActivity: async () => {
    try {
      const activity = await dashboardService.getActivity()
      set({ activity })
    } catch (error) {
      set({ error: error.message })
    }
  },

  setError: (error) => set({ error }),
  
  reset: () => set({
    summary: null,
    activity: null,
    isLoading: false,
    lastUpdate: null,
    error: null
  })
}))

// stores/constituencyStore.ts
import { create } from 'zustand'
import { ConstituencyState } from './types'
import { constituencyService } from '../services/constituencyService'

interface ConstituencyStore extends ConstituencyState {
  // Actions
  fetchConstituencies: () => Promise<void>
  fetchConstituencyDetail: (id: string) => Promise<void>
  setFilters: (filters: Partial<ConstituencyState['filters']>) => void
  setPage: (page: number) => void
  reset: () => void
}

export const useConstituencyStore = create<ConstituencyStore>((set, get) => ({
  // Initial state
  constituencies: [],
  selectedConstituency: null,
  filters: {},
  pagination: { page: 1, limit: 20, total: 0 },
  isLoading: false,
  error: null,

  // Actions
  fetchConstituencies: async () => {
    const { filters, pagination } = get()
    set({ isLoading: true, error: null })
    try {
      const response = await constituencyService.getList({
        ...filters,
        limit: pagination.limit,
        offset: (pagination.page - 1) * pagination.limit
      })
      set({ 
        constituencies: response.data,
        pagination: { ...pagination, total: response.total },
        isLoading: false 
      })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  fetchConstituencyDetail: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const constituency = await constituencyService.getDetail(id)
      set({ selectedConstituency: constituency, isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  setFilters: (newFilters) => {
    set(state => ({ 
      filters: { ...state.filters, ...newFilters },
      pagination: { ...state.pagination, page: 1 }
    }))
    get().fetchConstituencies()
  },

  setPage: (page) => {
    set(state => ({ pagination: { ...state.pagination, page } }))
    get().fetchConstituencies()
  },

  reset: () => set({
    constituencies: [],
    selectedConstituency: null,
    filters: {},
    pagination: { page: 1, limit: 20, total: 0 },
    isLoading: false,
    error: null
  })
}))

// stores/alertStore.ts
import { create } from 'zustand'
import { AlertState } from './types'
import { alertService } from '../services/alertService'

interface AlertStore extends AlertState {
  fetchAlerts: () => Promise<void>
  updateAlertStatus: (id: string, status: string, notes?: string) => Promise<void>
  addNote: (id: string, note: string) => Promise<void>
  setFilters: (filters: Partial<AlertState['filters']>) => void
  reset: () => void
}

export const useAlertStore = create<AlertStore>((set, get) => ({
  // Initial state
  alerts: [],
  selectedAlert: null,
  filters: {},
  pagination: { page: 1, limit: 20, total: 0 },
  isLoading: false,
  error: null,

  // Actions
  fetchAlerts: async () => {
    const { filters, pagination } = get()
    set({ isLoading: true, error: null })
    try {
      const response = await alertService.getList({
        ...filters,
        limit: pagination.limit,
        offset: (pagination.page - 1) * pagination.limit
      })
      set({ 
        alerts: response.data,
        pagination: { ...pagination, total: response.total },
        isLoading: false 
      })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  updateAlertStatus: async (id: string, status: string, notes?: string) => {
    try {
      const updatedAlert = await alertService.updateStatus(id, status, notes)
      set(state => ({
        alerts: state.alerts.map(alert => 
          alert.id === id ? updatedAlert : alert
        ),
        selectedAlert: state.selectedAlert?.id === id ? updatedAlert : state.selectedAlert
      }))
    } catch (error) {
      set({ error: error.message })
    }
  },

  addNote: async (id: string, note: string) => {
    try {
      const updatedAlert = await alertService.addNote(id, note)
      set(state => ({
        alerts: state.alerts.map(alert => 
          alert.id === id ? updatedAlert : alert
        ),
        selectedAlert: state.selectedAlert?.id === id ? updatedAlert : state.selectedAlert
      }))
    } catch (error) {
      set({ error: error.message })
    }
  },

  setFilters: (newFilters) => {
    set(state => ({ 
      filters: { ...state.filters, ...newFilters },
      pagination: { ...state.pagination, page: 1 }
    }))
    get().fetchAlerts()
  },

  reset: () => set({
    alerts: [],
    selectedAlert: null,
    filters: {},
    pagination: { page: 1, limit: 20, total: 0 },
    isLoading: false,
    error: null
  })
}))

// stores/appStore.ts
import { create } from 'zustand'

interface AppStore {
  isConnected: boolean
  websocket: WebSocket | null
  notifications: Notification[]
  
  // Actions
  connectWebSocket: () => void
  disconnectWebSocket: () => void
  addNotification: (notification: Notification) => void
  removeNotification: (id: string) => void
}

export const useAppStore = create<AppStore>((set, get) => ({
  isConnected: false,
  websocket: null,
  notifications: [],

  connectWebSocket: () => {
    const ws = new WebSocket('ws://localhost:8000/api/dashboard/ws')
    
    ws.onopen = () => set({ isConnected: true })
    ws.onclose = () => set({ isConnected: false, websocket: null })
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      // Handle real-time updates
      // Update relevant stores based on message type
    }
    
    set({ websocket: ws })
  },

  disconnectWebSocket: () => {
    const { websocket } = get()
    if (websocket) {
      websocket.close()
    }
    set({ websocket: null, isConnected: false })
  },

  addNotification: (notification) => {
    set(state => ({ 
      notifications: [...state.notifications, notification] 
    }))
  },

  removeNotification: (id) => {
    set(state => ({
      notifications: state.notifications.filter(n => n.id !== id)
    }))
  }
}))
```

### Services

```typescript
// services/apiClient.ts
const API_BASE = 'http://localhost:8000/api'

class ApiClient {
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = new URL(`${API_BASE}${endpoint}`)
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) url.searchParams.append(key, value.toString())
      })
    }
    
    const response = await fetch(url.toString())
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`)
    return response.json()
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data ? JSON.stringify(data) : undefined
    })
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`)
    return response.json()
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: data ? JSON.stringify(data) : undefined
    })
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`)
    return response.json()
  }
}

export const apiClient = new ApiClient()

// services/dashboardService.ts
import { apiClient } from './apiClient'
import { DashboardSummary, RealTimeActivity } from '../stores/types'

export const dashboardService = {
  getSummary: (): Promise<DashboardSummary> => 
    apiClient.get('/dashboard'),
    
  getActivity: (): Promise<RealTimeActivity> => 
    apiClient.get('/dashboard/activity')
}

// services/constituencyService.ts
import { apiClient } from './apiClient'

export const constituencyService = {
  getList: (params?: any): Promise<{ data: ConstituencyOverview[], total: number }> =>
    apiClient.get('/constituencies', params),
    
  getDetail: (id: string): Promise<ConstituencyDetail> =>
    apiClient.get(`/constituencies/${id}`),
    
  getTransactions: (id: string, params?: any): Promise<Transaction[]> =>
    apiClient.get(`/constituencies/${id}/transactions`, params),
    
  getStats: (id: string, params?: any): Promise<HourlyStats[]> =>
    apiClient.get(`/constituencies/${id}/stats`, params)
}

// services/alertService.ts
import { apiClient } from './apiClient'

export const alertService = {
  getList: (params?: any): Promise<{ data: Alert[], total: number }> =>
    apiClient.get('/alerts', params),
    
  getDetail: (id: string): Promise<Alert> =>
    apiClient.get(`/alerts/${id}`),
    
  updateStatus: (id: string, status: string, notes?: string): Promise<Alert> =>
    apiClient.put(`/alerts/${id}/status`, { status, notes }),
    
  addNote: (id: string, note: string): Promise<Alert> =>
    apiClient.post(`/alerts/${id}/notes`, { note })
}
```

## 3. Backend Data Model (SQLAlchemy)

```python
# models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Election(Base):
    __tablename__ = "elections"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")  # active, completed, upcoming
    total_constituencies = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    constituencies = relationship("Constituency", back_populates="election")

class Constituency(Base):
    __tablename__ = "constituencies"
    
    id = Column(String, primary_key=True)  # Smart contract address
    election_id = Column(String, ForeignKey("elections.id"), nullable=False)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    type = Column(String, nullable=False)  # urban, rural, suburban
    registered_voters = Column(Integer, default=0)
    status = Column(String, default="active")  # active, offline, completed
    last_update_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Calculated fields (updated by background jobs)
    bulletins_issued = Column(Integer, default=0)
    votes_cast = Column(Integer, default=0)
    participation_rate = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0)
    
    # Relationships
    election = relationship("Election", back_populates="constituencies")
    transactions = relationship("Transaction", back_populates="constituency")
    alerts = relationship("Alert", back_populates="constituency")
    hourly_stats = relationship("HourlyStats", back_populates="constituency")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False)
    block_height = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)  # blindSigIssue, vote
    raw_data = Column(JSON)
    operation_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="transactions")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False)
    type = Column(String, nullable=False)  # votes_exceed_bulletins, unusual_spike, etc.
    severity = Column(String, nullable=False)  # critical, warning, info
    status = Column(String, default="active")  # active, investigating, resolved, snoozed
    
    title = Column(String, nullable=False)
    description = Column(Text)
    details = Column(JSON)
    notes = Column(JSON, default=list)  # List of note strings
    
    created_at = Column(DateTime, default=datetime.utcnow)
    detected_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime)
    assigned_to = Column(String)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="alerts")

class HourlyStats(Base):
    __tablename__ = "hourly_stats"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False)
    hour = Column(DateTime, nullable=False)  # Rounded to hour
    
    bulletins_issued = Column(Integer, default=0)
    votes_cast = Column(Integer, default=0)
    transaction_count = Column(Integer, default=0)
    bulletin_velocity = Column(Float, default=0.0)  # per hour
    vote_velocity = Column(Float, default=0.0)  # per hour
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="hourly_stats")

class FileProcessingJob(Base):
    __tablename__ = "file_processing_jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    status = Column(String, default="processing")  # processing, completed, failed
    details = Column(Text)
    transactions_processed = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

# Database setup
DATABASE_URL = "sqlite:///./election_monitoring.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 4. Repository Structure

```
election-monitoring/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── file_processor.py
│   │   │   ├── metrics_calculator.py
│   │   │   ├── anomaly_detector.py
│   │   │   ├── alert_manager.py
│   │   │   └── dashboard_service.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   ├── constituencies.py
│   │   │   ├── alerts.py
│   │   │   ├── files.py
│   │   │   └── health.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── background_tasks.py
│   │   │   ├── file_watcher.py
│   │   │   └── websocket_manager.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── csv_parser.py
│   │       └── validators.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_utils/
│   │
│   ├── data/
│   │   ├── input/           # CSV files dropped here
│   │   ├── processed/       # Processed files moved here
│   │   └── backups/         # File backups
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic/            # Database migrations
│       ├── versions/
│       └── alembic.ini
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          # Reusable UI components
│   │   │   ├── dashboard/   # Dashboard specific components
│   │   │   ├── constituencies/
│   │   │   ├── alerts/
│   │   │   └── layout/
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ConstituencyDetail.tsx
│   │   │   └── AlertDetail.tsx
│   │   │
│   │   ├── stores/
│   │   │   ├── types.ts
│   │   │   ├── dashboardStore.ts
│   │   │   ├── constituencyStore.ts
│   │   │   ├── alertStore.ts
│   │   │   └── appStore.ts
│   │   │
│   │   ├── services/
│   │   │   ├── apiClient.ts
│   │   │   ├── dashboardService.ts
│   │   │   ├── constituencyService.ts
│   │   │   └── alertService.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── usePolling.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── styles/
│   │   │   └── globals.css
│   │   │
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── docker-compose.yml
├── .gitignore
├── README.md
└── Makefile
```

## 5. Dependencies

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.13.0
pydantic==2.5.0
python-multipart==0.0.6
watchdog==3.0.0
pandas==2.1.4
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Frontend (package.json)
```json
{
  "name": "election-monitoring-frontend",
  "version": "0.1.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.7",
    "recharts": "^2.8.0",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^4.5.0"
  }
}
```

This structure provides:
- Clean API design with proper REST conventions
- Type-safe frontend with Zustand for state management
- Scalable backend with proper service separation
- Real-time updates via WebSocket
- File processing pipeline
- Comprehensive error handling
- Testing structure

Would you like me to create the README.md next, or dive deeper into any specific component?