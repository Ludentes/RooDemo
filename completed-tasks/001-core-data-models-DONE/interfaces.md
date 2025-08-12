# Task 1: Core Data Models - Interfaces and Contracts

This document defines the interfaces, contracts, and APIs for the Core Data Models implementation of the Election Monitoring System.

## 1. SQLAlchemy Model Interfaces

### 1.1 Base Model Interface

All models should inherit from the `Base` class and implement the following interface:

```python
class Base:
    """Base class for all SQLAlchemy models."""
    # SQLAlchemy declarative base
    # Will be used for all model classes
```

### 1.2 TimestampMixin Interface

```python
class TimestampMixin:
    """Mixin to add created_at timestamp to models."""
    
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
```

### 1.3 UUIDMixin Interface

```python
class UUIDMixin:
    """Mixin to add UUID primary key to models."""
    
    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
```

### 1.4 Election Model Interface

```python
class Election(Base, UUIDMixin, TimestampMixin):
    """Election model representing an election event."""
    
    __tablename__ = "elections"
    
    name: str = Column(String, nullable=False)
    start_date: datetime = Column(DateTime, nullable=False)
    end_date: datetime = Column(DateTime, nullable=False)
    status: str = Column(String, default="active")  # active, completed, upcoming
    total_constituencies: int = Column(Integer, default=0)
    
    # Relationships
    constituencies: List["Constituency"] = relationship("Constituency", back_populates="election")
```

### 1.5 Constituency Model Interface

```python
class Constituency(Base, TimestampMixin):
    """Constituency model representing a voting district."""
    
    __tablename__ = "constituencies"
    
    id: str = Column(String, primary_key=True)  # Smart contract address
    election_id: str = Column(String, ForeignKey("elections.id"), nullable=False)
    name: str = Column(String, nullable=False)
    region: str = Column(String, nullable=False)
    type: str = Column(String, nullable=False)  # urban, rural, suburban
    registered_voters: int = Column(Integer, default=0)
    status: str = Column(String, default="active")  # active, offline, completed
    last_update_time: datetime = Column(DateTime, default=datetime.utcnow)
    
    # Calculated fields
    bulletins_issued: int = Column(Integer, default=0)
    votes_cast: int = Column(Integer, default=0)
    participation_rate: float = Column(Float, default=0.0)
    anomaly_score: float = Column(Float, default=0.0)
    
    # Relationships
    election: Election = relationship("Election", back_populates="constituencies")
    transactions: List["Transaction"] = relationship("Transaction", back_populates="constituency")
    alerts: List["Alert"] = relationship("Alert", back_populates="constituency")
    hourly_stats: List["HourlyStats"] = relationship("HourlyStats", back_populates="constituency")
```

### 1.6 Transaction Model Interface

```python
class Transaction(Base, UUIDMixin, TimestampMixin):
    """Transaction model representing a blockchain transaction."""
    
    __tablename__ = "transactions"
    
    constituency_id: str = Column(String, ForeignKey("constituencies.id"), nullable=False)
    block_height: int = Column(Integer, nullable=False)
    timestamp: datetime = Column(DateTime, nullable=False)
    type: str = Column(String, nullable=False)  # blindSigIssue, vote
    raw_data: Dict = Column(JSON)
    operation_data: Dict = Column(JSON)
    
    # Relationships
    constituency: Constituency = relationship("Constituency", back_populates="transactions")
```

### 1.7 Alert Model Interface

```python
class Alert(Base, UUIDMixin, TimestampMixin):
    """Alert model representing a detected anomaly."""
    
    __tablename__ = "alerts"
    
    constituency_id: str = Column(String, ForeignKey("constituencies.id"), nullable=False)
    type: str = Column(String, nullable=False)  # votes_exceed_bulletins, unusual_spike, etc.
    severity: str = Column(String, nullable=False)  # critical, warning, info
    status: str = Column(String, default="active")  # active, investigating, resolved, snoozed
    
    title: str = Column(String, nullable=False)
    description: str = Column(Text)
    details: Dict = Column(JSON)
    notes: List[str] = Column(JSON, default=list)
    
    detected_at: datetime = Column(DateTime, nullable=False)
    resolved_at: Optional[datetime] = Column(DateTime)
    assigned_to: Optional[str] = Column(String)
    
    # Relationships
    constituency: Constituency = relationship("Constituency", back_populates="alerts")
```

### 1.8 HourlyStats Model Interface

```python
class HourlyStats(Base, UUIDMixin, TimestampMixin):
    """HourlyStats model representing hourly aggregated statistics."""
    
    __tablename__ = "hourly_stats"
    
    constituency_id: str = Column(String, ForeignKey("constituencies.id"), nullable=False)
    hour: datetime = Column(DateTime, nullable=False)
    
    bulletins_issued: int = Column(Integer, default=0)
    votes_cast: int = Column(Integer, default=0)
    transaction_count: int = Column(Integer, default=0)
    bulletin_velocity: float = Column(Float, default=0.0)
    vote_velocity: float = Column(Float, default=0.0)
    
    # Relationships
    constituency: Constituency = relationship("Constituency", back_populates="hourly_stats")
```

### 1.9 FileProcessingJob Model Interface

```python
class FileProcessingJob(Base, UUIDMixin):
    """FileProcessingJob model tracking CSV file processing."""
    
    __tablename__ = "file_processing_jobs"
    
    filename: str = Column(String, nullable=False)
    status: str = Column(String, default="processing")  # processing, completed, failed
    details: Optional[str] = Column(Text)
    transactions_processed: int = Column(Integer, default=0)
    started_at: datetime = Column(DateTime, default=datetime.utcnow)
    completed_at: Optional[datetime] = Column(DateTime)
```

## 2. Pydantic Schema Interfaces

### 2.1 Base Schema Interfaces

```python
class BaseSchema(BaseModel):
    """Base schema for all Pydantic models."""
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
```

### 2.2 Election Schema Interfaces

```python
class ElectionBase(BaseSchema):
    """Base schema for Election model."""
    
    name: str
    start_date: datetime
    end_date: datetime
    status: str
    total_constituencies: int = 0

class ElectionCreate(ElectionBase):
    """Schema for creating an Election."""
    pass

class ElectionUpdate(BaseSchema):
    """Schema for updating an Election."""
    
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    total_constituencies: Optional[int] = None

class ElectionResponse(ElectionBase):
    """Schema for Election response."""
    
    id: str
    created_at: datetime
```

### 2.3 Constituency Schema Interfaces

```python
class ConstituencyBase(BaseSchema):
    """Base schema for Constituency model."""
    
    election_id: str
    name: str
    region: str
    type: str
    registered_voters: int = 0
    status: str = "active"

class ConstituencyCreate(ConstituencyBase):
    """Schema for creating a Constituency."""
    
    id: str  # Smart contract address

class ConstituencyUpdate(BaseSchema):
    """Schema for updating a Constituency."""
    
    name: Optional[str] = None
    region: Optional[str] = None
    type: Optional[str] = None
    registered_voters: Optional[int] = None
    status: Optional[str] = None
    bulletins_issued: Optional[int] = None
    votes_cast: Optional[int] = None
    participation_rate: Optional[float] = None
    anomaly_score: Optional[float] = None

class ConstituencyResponse(ConstituencyBase):
    """Schema for Constituency response."""
    
    id: str
    created_at: datetime
    last_update_time: datetime
    bulletins_issued: int
    votes_cast: int
    participation_rate: float
    anomaly_score: float
```

### 2.4 Transaction Schema Interfaces

```python
class TransactionBase(BaseSchema):
    """Base schema for Transaction model."""
    
    constituency_id: str
    block_height: int
    timestamp: datetime
    type: str
    raw_data: Dict
    operation_data: Optional[Dict] = None

class TransactionCreate(TransactionBase):
    """Schema for creating a Transaction."""
    pass

class TransactionResponse(TransactionBase):
    """Schema for Transaction response."""
    
    id: str
    created_at: datetime
```

### 2.5 Alert Schema Interfaces

```python
class AlertBase(BaseSchema):
    """Base schema for Alert model."""
    
    constituency_id: str
    type: str
    severity: str
    status: str = "active"
    title: str
    description: Optional[str] = None
    details: Optional[Dict] = None
    notes: List[str] = []
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None

class AlertCreate(AlertBase):
    """Schema for creating an Alert."""
    pass

class AlertUpdate(BaseSchema):
    """Schema for updating an Alert."""
    
    status: Optional[str] = None
    notes: Optional[List[str]] = None
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None

class AlertResponse(AlertBase):
    """Schema for Alert response."""
    
    id: str
    created_at: datetime
```

### 2.6 HourlyStats Schema Interfaces

```python
class HourlyStatsBase(BaseSchema):
    """Base schema for HourlyStats model."""
    
    constituency_id: str
    hour: datetime
    bulletins_issued: int = 0
    votes_cast: int = 0
    transaction_count: int = 0
    bulletin_velocity: float = 0.0
    vote_velocity: float = 0.0

class HourlyStatsCreate(HourlyStatsBase):
    """Schema for creating HourlyStats."""
    pass

class HourlyStatsResponse(HourlyStatsBase):
    """Schema for HourlyStats response."""
    
    id: str
    created_at: datetime
```

### 2.7 FileProcessingJob Schema Interfaces

```python
class FileProcessingJobBase(BaseSchema):
    """Base schema for FileProcessingJob model."""
    
    filename: str
    status: str = "processing"
    details: Optional[str] = None
    transactions_processed: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None

class FileProcessingJobCreate(FileProcessingJobBase):
    """Schema for creating a FileProcessingJob."""
    pass

class FileProcessingJobUpdate(BaseSchema):
    """Schema for updating a FileProcessingJob."""
    
    status: Optional[str] = None
    details: Optional[str] = None
    transactions_processed: Optional[int] = None
    completed_at: Optional[datetime] = None

class FileProcessingJobResponse(FileProcessingJobBase):
    """Schema for FileProcessingJob response."""
    
    id: str
```

## 3. Database Access (CRUD) Interfaces

### 3.1 Base CRUD Interface

```python
class BaseCRUD[T]:
    """Base CRUD operations for all models."""
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    def create(self, obj_in: Any) -> T:
        """Create a new record."""
        pass
    
    def get(self, id: Any) -> Optional[T]:
        """Get a record by ID."""
        pass
    
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[T]:
        """Get multiple records with pagination."""
        pass
    
    def update(self, *, db_obj: T, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> T:
        """Update a record."""
        pass
    
    def delete(self, *, id: Any) -> T:
        """Delete a record."""
        pass
```

### 3.2 Election CRUD Interface

```python
class ElectionCRUD(BaseCRUD[Election]):
    """CRUD operations for Election model."""
    
    def get_by_name(self, *, name: str) -> Optional[Election]:
        """Get an election by name."""
        pass
    
    def get_active_elections(self) -> List[Election]:
        """Get all active elections."""
        pass
    
    def get_by_date_range(self, *, start_date: datetime, end_date: datetime) -> List[Election]:
        """Get elections within a date range."""
        pass
```

### 3.3 Constituency CRUD Interface

```python
class ConstituencyCRUD(BaseCRUD[Constituency]):
    """CRUD operations for Constituency model."""
    
    def get_by_election(self, *, election_id: str) -> List[Constituency]:
        """Get constituencies by election ID."""
        pass
    
    def get_by_region(self, *, region: str) -> List[Constituency]:
        """Get constituencies by region."""
        pass
    
    def get_by_status(self, *, status: str) -> List[Constituency]:
        """Get constituencies by status."""
        pass
    
    def get_by_type(self, *, type: str) -> List[Constituency]:
        """Get constituencies by type."""
        pass
    
    def update_metrics(self, *, id: str, bulletins: int, votes: int) -> Constituency:
        """Update constituency metrics."""
        pass
```

### 3.4 Transaction CRUD Interface

```python
class TransactionCRUD(BaseCRUD[Transaction]):
    """CRUD operations for Transaction model."""
    
    def get_by_constituency(self, *, constituency_id: str) -> List[Transaction]:
        """Get transactions by constituency ID."""
        pass
    
    def get_by_type(self, *, type: str) -> List[Transaction]:
        """Get transactions by type."""
        pass
    
    def get_by_time_range(self, *, start_time: datetime, end_time: datetime) -> List[Transaction]:
        """Get transactions within a time range."""
        pass
    
    def get_by_block_height(self, *, block_height: int) -> List[Transaction]:
        """Get transactions by block height."""
        pass
```

### 3.5 Alert CRUD Interface

```python
class AlertCRUD(BaseCRUD[Alert]):
    """CRUD operations for Alert model."""
    
    def get_by_constituency(self, *, constituency_id: str) -> List[Alert]:
        """Get alerts by constituency ID."""
        pass
    
    def get_by_severity(self, *, severity: str) -> List[Alert]:
        """Get alerts by severity."""
        pass
    
    def get_by_status(self, *, status: str) -> List[Alert]:
        """Get alerts by status."""
        pass
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        pass
    
    def add_note(self, *, id: str, note: str) -> Alert:
        """Add a note to an alert."""
        pass
```

### 3.6 HourlyStats CRUD Interface

```python
class HourlyStatsCRUD(BaseCRUD[HourlyStats]):
    """CRUD operations for HourlyStats model."""
    
    def get_by_constituency(self, *, constituency_id: str) -> List[HourlyStats]:
        """Get hourly stats by constituency ID."""
        pass
    
    def get_by_hour_range(self, *, start_hour: datetime, end_hour: datetime) -> List[HourlyStats]:
        """Get hourly stats within a time range."""
        pass
    
    def get_latest_for_constituency(self, *, constituency_id: str) -> Optional[HourlyStats]:
        """Get the latest hourly stats for a constituency."""
        pass
```

### 3.7 FileProcessingJob CRUD Interface

```python
class FileProcessingJobCRUD(BaseCRUD[FileProcessingJob]):
    """CRUD operations for FileProcessingJob model."""
    
    def get_by_status(self, *, status: str) -> List[FileProcessingJob]:
        """Get file processing jobs by status."""
        pass
    
    def get_by_filename(self, *, filename: str) -> Optional[FileProcessingJob]:
        """Get a file processing job by filename."""
        pass
    
    def update_status(self, *, id: str, status: str, details: Optional[str] = None) -> FileProcessingJob:
        """Update the status of a file processing job."""
        pass
    
    def increment_processed_count(self, *, id: str, count: int = 1) -> FileProcessingJob:
        """Increment the processed transaction count of a file processing job."""
        pass
    
    def mark_completed(self, *, id: str) -> FileProcessingJob:
        """Mark a file processing job as completed."""
        pass
```

## 4. Database Connection Interface

```python
def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 5. Alembic Migration Interface

```python
# env.py configuration
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    pass

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    pass
```

## 6. Validation Interfaces

### 6.1 Election Validators

```python
@validator("status")
def validate_status(cls, v: str) -> str:
    """Validate election status."""
    allowed_statuses = ["active", "completed", "upcoming"]
    if v not in allowed_statuses:
        raise ValueError(f"Status must be one of {allowed_statuses}")
    return v

@validator("end_date")
def validate_end_date(cls, v: datetime, values: Dict[str, Any]) -> datetime:
    """Validate that end_date is after start_date."""
    if "start_date" in values and v <= values["start_date"]:
        raise ValueError("End date must be after start date")
    return v
```

### 6.2 Constituency Validators

```python
@validator("type")
def validate_type(cls, v: str) -> str:
    """Validate constituency type."""
    allowed_types = ["urban", "rural", "suburban"]
    if v not in allowed_types:
        raise ValueError(f"Type must be one of {allowed_types}")
    return v

@validator("status")
def validate_status(cls, v: str) -> str:
    """Validate constituency status."""
    allowed_statuses = ["active", "offline", "completed"]
    if v not in allowed_statuses:
        raise ValueError(f"Status must be one of {allowed_statuses}")
    return v
```

### 6.3 Transaction Validators

```python
@validator("type")
def validate_type(cls, v: str) -> str:
    """Validate transaction type."""
    allowed_types = ["blindSigIssue", "vote"]
    if v not in allowed_types:
        raise ValueError(f"Type must be one of {allowed_types}")
    return v
```

### 6.4 Alert Validators

```python
@validator("severity")
def validate_severity(cls, v: str) -> str:
    """Validate alert severity."""
    allowed_severities = ["critical", "warning", "info"]
    if v not in allowed_severities:
        raise ValueError(f"Severity must be one of {allowed_severities}")
    return v

@validator("status")
def validate_status(cls, v: str) -> str:
    """Validate alert status."""
    allowed_statuses = ["active", "investigating", "resolved", "snoozed"]
    if v not in allowed_statuses:
        raise ValueError(f"Status must be one of {allowed_statuses}")
    return v
```

## 7. Contract Enforcement

The interfaces defined in this document serve as contracts between different components of the system. These contracts must be adhered to during implementation to ensure proper integration and functionality.

### 7.1 Contract Enforcement Rules

1. **Type Safety**: All interfaces must maintain type safety through proper type annotations.
2. **Validation**: All input data must be validated according to the defined validators.
3. **Error Handling**: All operations must handle errors appropriately and provide meaningful error messages.
4. **Documentation**: All interfaces must be properly documented with docstrings.
5. **Testing**: All interfaces must have corresponding unit tests to verify their functionality.

### 7.2 Interface Evolution

As the system evolves, interfaces may need to be updated. The following rules apply to interface evolution:

1. **Backward Compatibility**: Changes to interfaces should maintain backward compatibility when possible.
2. **Versioning**: Major changes to interfaces should be versioned.
3. **Deprecation**: Deprecated interfaces should be marked as such and provide migration paths.
4. **Documentation**: All changes to interfaces must be documented.

## 8. Conclusion

The interfaces defined in this document provide a comprehensive contract for the implementation of the Core Data Models component of the Election Monitoring System. By adhering to these interfaces, the implementation will be consistent, maintainable, and extensible.