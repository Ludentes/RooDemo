# Election Monitoring System - Data Model

## Technology Stack

The Election Monitoring System uses the following backend components:

| Component | Version | Description |
|-----------|---------|-------------|
| FastAPI | 0.115.0+ | Web framework for building APIs |
| SQLAlchemy | 2.0.0+ | SQL toolkit and Object-Relational Mapper |
| Pydantic | 2.5.0+ | Data validation and settings management |

## Database Overview

The Election Monitoring System uses SQLAlchemy ORM with SQLite for the MVP (upgradeable to PostgreSQL for production). The data model is designed to track election data across multiple constituencies, process transaction logs, and detect anomalies.

## Entity Relationship Diagram

```
┌─────────────┐       ┌───────────────┐       ┌─────────────┐
│  Election   │       │ Constituency  │       │ Transaction │
├─────────────┤       ├───────────────┤       ├─────────────┤
│ id          │       │ id            │       │ id          │
│ name        │       │ election_id   │◄──────┤ constituency_id
│ country     │       │ name          │       │ block_height│
│ start_date  │       │ region        │       │ timestamp   │
│ end_date    │       │ type          │       │ type        │
│ status      │◄──────┤ reg_voters    │       │ raw_data    │
│ type        │       │ status        │       │ op_data     │
│ description │       │ last_update   │       │ created_at  │
│ timezone    │       │ bulletins     │       │ updated_at  │
│ total_const.│       │ votes         │       └─────────────┘
│ created_at  │       │ participation │
│ updated_at  │       │ anomaly_score │       ┌─────────────┐
└─────────────┘       │ created_at    │       │ HourlyStats │
                      │ updated_at    │       ├─────────────┤
                      └───────────────┘       │ id          │
                              ▲               │ constituency_id
                              │               │ hour         │
                              │               │ bulletins    │
┌─────────────┐               │               │ votes        │
│   Alert     │               │               │ transactions │
├─────────────┤               │               │ bulletin_vel │
│ id          │               │               │ vote_vel     │
│ constituency_id ────────────┘               │ created_at   │
│ type        │                               │ updated_at   │
│ severity    │                               └─────────────┘
│ status      │       ┌─────────────────────┐
│ title       │       │ FileProcessingJob   │
│ description │       ├─────────────────────┤
│ details     │       │ id                  │
│ notes       │       │ filename            │
│ created_at  │       │ status              │
│ updated_at  │       │ details             │
│ detected_at │       │ transactions_proc   │
│ resolved_at │       │ started_at          │
│ assigned_to │       │ completed_at        │
└─────────────┘       └─────────────────────┘
```

## Database Models

### Election

Represents an election event that contains multiple constituencies.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, UUID |
| name | String | Name of the election |
| country | String | Country where the election is held |
| start_date | DateTime | Official start date of the election |
| end_date | DateTime | Official end date of the election |
| status | String | Status of the election (active, completed, upcoming, scheduled) |
| type | String | Type of election (presidential, parliamentary, general, local, referendum) |
| description | Text | Description of the election |
| timezone | String | Timezone of the election |
| total_constituencies | Integer | Total number of constituencies in this election |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships**:
- `constituencies`: One-to-many relationship with Constituency model

### Constituency

Represents a voting district with its own smart contract.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, smart contract address |
| election_id | String | Foreign key to Election |
| name | String | Name of the constituency |
| region | String | Geographic region |
| type | String | Type of constituency (urban, rural, suburban, district) |
| registered_voters | Integer | Number of registered voters |
| status | String | Status of the constituency (active, offline, completed, inactive) |
| last_update_time | DateTime | Last data update timestamp |
| bulletins_issued | Integer | Number of electronic bulletins issued |
| votes_cast | Integer | Number of votes cast |
| participation_rate | Float | Percentage of registered voters who voted |
| anomaly_score | Float | Calculated anomaly score (0-1) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships**:
- `election`: Many-to-one relationship with Election model
- `transactions`: One-to-many relationship with Transaction model
- `alerts`: One-to-many relationship with Alert model
- `hourly_stats`: One-to-many relationship with HourlyStats model

### Transaction

Represents a blockchain transaction from the voting system.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, UUID |
| constituency_id | String | Foreign key to Constituency |
| block_height | Integer | Blockchain block height |
| timestamp | DateTime | Transaction timestamp |
| type | String | Transaction type (vote, registration, verification, audit) |
| raw_data | JSON | Raw transaction data |
| operation_data | JSON | Processed operation data |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships**:
- `constituency`: Many-to-one relationship with Constituency model

### Alert

Represents a detected anomaly or issue requiring attention.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, UUID |
| constituency_id | String | Foreign key to Constituency |
| type | String | Alert type (votes_exceed_bulletins, unusual_spike, etc.) |
| severity | String | Alert severity (critical, warning, info) |
| status | String | Alert status (active, investigating, resolved, snoozed) |
| title | String | Short alert title |
| description | Text | Detailed alert description |
| details | JSON | Additional alert details |
| notes | JSON | List of investigation notes |
| detected_at | DateTime | When the anomaly was detected |
| resolved_at | DateTime | When the alert was resolved (nullable) |
| assigned_to | String | Person assigned to investigate (nullable) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships**:
- `constituency`: Many-to-one relationship with Constituency model

### HourlyStats

Represents hourly aggregated statistics for a constituency.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, UUID |
| constituency_id | String | Foreign key to Constituency |
| hour | DateTime | Hour timestamp (rounded to hour) |
| bulletins_issued | Integer | Number of bulletins issued in this hour |
| votes_cast | Integer | Number of votes cast in this hour |
| transaction_count | Integer | Total transactions in this hour |
| bulletin_velocity | Float | Rate of bulletin issuance per hour |
| vote_velocity | Float | Rate of vote casting per hour |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships**:
- `constituency`: Many-to-one relationship with Constituency model

### FileProcessingJob

Tracks the status of CSV file processing jobs.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key, UUID |
| filename | String | Name of the processed file |
| status | String | Job status (processing, completed, failed) |
| details | Text | Processing details or error messages |
| transactions_processed | Integer | Number of transactions processed |
| started_at | DateTime | Job start timestamp |
| completed_at | DateTime | Job completion timestamp (nullable) |

## Database Configuration

```python
# Get the absolute path to the backend directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
db_path = os.path.join(backend_dir, "election_monitoring.db")

# Database URL with absolute path
DATABASE_URL = f"sqlite:///{db_path}"

# Create engine with SQLite-specific arguments
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_tables():
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
```

## Data Flow

1. **CSV File Import**:
   - CSV files are dropped in the `data/input/` directory
   - FileWatcher detects new files and creates a FileProcessingJob
   - CSV Parser extracts transaction data
   - Transactions are stored in the Transaction table

2. **Metrics Calculation**:
   - Background job processes new transactions
   - Updates Constituency metrics (bulletins_issued, votes_cast, participation_rate)
   - Generates HourlyStats records

3. **Anomaly Detection**:
   - Background job analyzes metrics and transactions
   - Calculates anomaly scores
   - Creates Alert records for detected anomalies

4. **API Data Access**:
   - API endpoints query the database
   - Data is transformed into response models
   - WebSocket pushes real-time updates

## Database Migrations

The system uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Indexing Strategy

The following indexes are recommended for optimal performance:

1. **Transaction Indexes**:
   - `constituency_id` + `timestamp` (for time-based queries)
   - `type` + `constituency_id` (for filtering by transaction type)
   - `block_height` (for blockchain synchronization)

2. **Alert Indexes**:
   - `constituency_id` + `status` (for active alerts by constituency)
   - `severity` + `status` (for critical alerts)
   - `detected_at` (for time-based queries)

3. **HourlyStats Indexes**:
   - `constituency_id` + `hour` (for time series queries)

## Data Validation

Data validation is handled through Pydantic models in the API layer:

```python
class TransactionCreate(BaseModel):
    constituency_id: str
    block_height: int
    timestamp: datetime
    type: str
    raw_data: Dict[str, Any]
    
    @validator('type')
    def validate_transaction_type(cls, v):
        allowed_types = ['blindSigIssue', 'vote']
        if v not in allowed_types:
            raise ValueError(f'Transaction type must be one of {allowed_types}')
        return v
```

## Data Retention Policy

- Transaction data: Retained for the duration of the election plus 30 days
- Hourly statistics: Retained for 1 year
- Alerts: Retained indefinitely
- File processing jobs: Retained for 90 days

## PostgreSQL Migration Path

For production deployment, the system can be migrated to PostgreSQL:

1. Update the DATABASE_URL:
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/election_monitoring"
   ```

2. Remove SQLite-specific connection arguments:
   ```python
   engine = create_engine(DATABASE_URL)
   ```

3. Add PostgreSQL-specific indexes and optimizations:
   ```python
   # Add GIN index for JSON fields
   Index('ix_transaction_raw_data', Transaction.raw_data, postgresql_using='gin')
   ```

4. Run Alembic migrations to create the PostgreSQL schema

## Current Implementation Structure

The current implementation follows a well-organized structure that separates concerns and improves maintainability:

### SQLAlchemy Models

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
```

### Pydantic Schemas

```
backend/
  app/
    models/
      schemas/
        __init__.py       # Exports all schemas
        base.py           # Base schemas and common validators
        election.py       # Election schemas
        constituency.py   # Constituency schemas
        transaction.py    # Transaction schemas
        alert.py          # Alert schemas
        hourly_stats.py   # HourlyStats schemas
        file_processing.py # FileProcessingJob schemas
```

### Database Access Functions (CRUD)

```
backend/
  app/
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

### Service Layer

```
backend/
  app/
    services/
      __init__.py       # Exports all services
      base.py           # Base service operations
      health.py         # Health check service
      election.py       # Election service
      constituency.py   # Constituency service
      dashboard.py      # Dashboard service
```

### API Routes

```
backend/
  app/
    api/
      __init__.py       # Exports all routes
      dependencies.py   # API dependencies
      routes/
        __init__.py     # Exports all route modules
        health.py       # Health check routes
        elections.py    # Election routes
        constituencies.py # Constituency routes
        dashboard.py    # Dashboard routes
```

### Error Handling

```
backend/
  app/
    api/
      errors/
        __init__.py     # Exports all error modules
        exceptions.py   # Custom exceptions
        handlers.py     # Exception handlers
```

### Utility Scripts

```
backend/
  scripts/
    seed_db.py          # Database seeding script
    clear_db.py         # Database clearing script
    README.md           # Script documentation
```

This structure follows best practices for FastAPI and SQLAlchemy applications, providing a clean separation of concerns and making the codebase maintainable and extensible.