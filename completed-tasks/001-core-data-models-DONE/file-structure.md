# Task 1: Core Data Models - File Structure

This document outlines the file organization plan for the Core Data Models implementation of the Election Monitoring System.

## Project Root Structure

```
election-monitoring/
├── backend/                # Backend application
│   ├── app/                # Application code
│   ├── alembic/            # Database migrations
│   ├── tests/              # Unit tests
│   ├── data/               # Data files
│   └── requirements.txt    # Dependencies
└── frontend/               # Frontend application (not part of this task)
```

## Backend Application Structure

```
backend/
├── app/
│   ├── __init__.py         # Application initialization
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Configuration settings
│   ├── dependencies.py     # Dependency injection
│   │
│   ├── models/             # SQLAlchemy models
│   │   ├── __init__.py     # Exports all models
│   │   ├── database.py     # Base class and database connection
│   │   ├── election.py     # Election model
│   │   ├── constituency.py # Constituency model
│   │   ├── transaction.py  # Transaction model
│   │   ├── alert.py        # Alert model
│   │   ├── hourly_stats.py # HourlyStats model
│   │   └── file_processing.py # FileProcessingJob model
│   │
│   ├── models/schemas/     # Pydantic schemas
│   │   ├── __init__.py     # Exports all schemas
│   │   ├── base.py         # Base schemas and common validators
│   │   ├── election.py     # Election schemas
│   │   ├── constituency.py # Constituency schemas
│   │   ├── transaction.py  # Transaction schemas
│   │   ├── alert.py        # Alert schemas
│   │   ├── hourly_stats.py # HourlyStats schemas
│   │   └── file_processing.py # FileProcessingJob schemas
│   │
│   ├── crud/               # Database access functions
│   │   ├── __init__.py     # Exports all CRUD modules
│   │   ├── base.py         # Base CRUD operations
│   │   ├── election.py     # Election CRUD
│   │   ├── constituency.py # Constituency CRUD
│   │   ├── transaction.py  # Transaction CRUD
│   │   ├── alert.py        # Alert CRUD
│   │   ├── hourly_stats.py # HourlyStats CRUD
│   │   └── file_processing.py # FileProcessingJob CRUD
│   │
│   ├── api/                # API endpoints (not part of this task)
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes/
│   │
│   ├── core/               # Core functionality (not part of this task)
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── config.py
│   │
│   └── utils/              # Utility functions (not part of this task)
│       ├── __init__.py
│       └── validators.py
│
├── alembic/                # Database migrations
│   ├── versions/           # Migration scripts
│   │   └── xxxx_initial_migration.py # Initial migration
│   ├── env.py              # Alembic environment
│   ├── script.py.mako      # Migration script template
│   └── alembic.ini         # Alembic configuration
│
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── conftest.py         # Test configuration and fixtures
│   │
│   ├── test_models/        # Tests for SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── test_election.py
│   │   ├── test_constituency.py
│   │   ├── test_transaction.py
│   │   ├── test_alert.py
│   │   ├── test_hourly_stats.py
│   │   └── test_file_processing.py
│   │
│   ├── test_schemas/       # Tests for Pydantic schemas
│   │   ├── __init__.py
│   │   ├── test_election_schema.py
│   │   ├── test_constituency_schema.py
│   │   ├── test_transaction_schema.py
│   │   ├── test_alert_schema.py
│   │   ├── test_hourly_stats_schema.py
│   │   └── test_file_processing_schema.py
│   │
│   └── test_crud/          # Tests for CRUD operations
│       ├── __init__.py
│       ├── test_election_crud.py
│       ├── test_constituency_crud.py
│       ├── test_transaction_crud.py
│       ├── test_alert_crud.py
│       ├── test_hourly_stats_crud.py
│       └── test_file_processing_crud.py
│
├── data/                   # Data files
│   ├── input/              # Input files for processing
│   ├── processed/          # Processed files
│   └── backups/            # Backup files
│
└── requirements.txt        # Dependencies
```

## File Descriptions

### Models

#### `models/database.py`

This file contains the base SQLAlchemy setup, including:
- Base class for all models
- Database connection configuration
- Session management
- Common model mixins (timestamps, UUID generation)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Database URL
DATABASE_URL = "sqlite:///./election_monitoring.db"

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

# Common mixins
class TimestampMixin:
    """Mixin to add created_at timestamp to models."""
    created_at = Column(DateTime, default=datetime.utcnow)

class UUIDMixin:
    """Mixin to add UUID primary key to models."""
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### `models/election.py`

This file contains the Election model:

```python
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, UUIDMixin, TimestampMixin

class Election(Base, UUIDMixin, TimestampMixin):
    """Election model representing an election event."""
    
    __tablename__ = "elections"
    
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")  # active, completed, upcoming
    total_constituencies = Column(Integer, default=0)
    
    # Relationships
    constituencies = relationship("Constituency", back_populates="election")
```

Similar structure for other model files.

### Schemas

#### `models/schemas/base.py`

This file contains the base Pydantic schemas:

```python
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema for all Pydantic models."""
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
```

#### `models/schemas/election.py`

This file contains the Election schemas:

```python
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema

class ElectionBase(BaseSchema):
    """Base schema for Election model."""
    
    name: str
    start_date: datetime
    end_date: datetime
    status: str
    total_constituencies: int = 0
    
    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["active", "completed", "upcoming"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v
    
    @validator("end_date")
    def validate_end_date(cls, v, values):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("End date must be after start date")
        return v

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

Similar structure for other schema files.

### CRUD

#### `crud/base.py`

This file contains the base CRUD operations:

```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD operations for all models."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize with model class."""
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """Update a record."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: Any) -> ModelType:
        """Delete a record."""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

#### `crud/election.py`

This file contains the Election CRUD operations:

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .base import BaseCRUD
from app.models.election import Election
from app.models.schemas.election import ElectionCreate, ElectionUpdate

class ElectionCRUD(BaseCRUD[Election, ElectionCreate, ElectionUpdate]):
    """CRUD operations for Election model."""
    
    def __init__(self):
        super().__init__(Election)
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Election]:
        """Get an election by name."""
        return db.query(Election).filter(Election.name == name).first()
    
    def get_active_elections(self, db: Session) -> List[Election]:
        """Get all active elections."""
        return db.query(Election).filter(Election.status == "active").all()
    
    def get_by_date_range(self, db: Session, *, start_date: datetime, end_date: datetime) -> List[Election]:
        """Get elections within a date range."""
        return db.query(Election).filter(
            Election.start_date >= start_date,
            Election.end_date <= end_date
        ).all()
```

Similar structure for other CRUD files.

### Alembic

#### `alembic/env.py`

This file configures the Alembic environment:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import models
from app.models.database import Base
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.models.hourly_stats import HourlyStats
from app.models.file_processing import FileProcessingJob

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

# Other values from the config, defined by the needs of env.py
config.set_main_option("sqlalchemy.url", "sqlite:///./election_monitoring.db")

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Tests

#### `tests/conftest.py`

This file contains test fixtures:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.database import Base
from app.dependencies import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

#### `tests/test_models/test_election.py`

This file contains tests for the Election model:

```python
import pytest
from datetime import datetime, timedelta

from app.models.election import Election

def test_create_election(db):
    """Test creating an election."""
    election = Election(
        name="Test Election",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        status="active"
    )
    db.add(election)
    db.commit()
    db.refresh(election)
    
    assert election.id is not None
    assert election.name == "Test Election"
    assert election.status == "active"
    assert election.total_constituencies == 0
```

Similar structure for other test files.

## File Organization Principles

1. **Separation of Concerns**: Each file has a single responsibility.
2. **Modularity**: Related functionality is grouped together.
3. **Consistency**: Similar files follow the same structure and naming conventions.
4. **Discoverability**: Files are organized in a logical hierarchy.
5. **Testability**: Each component has corresponding test files.

## Implementation Guidelines

1. **File Creation Order**:
   - Start with base files (database.py, base.py)
   - Implement model files
   - Implement schema files
   - Implement CRUD files
   - Set up Alembic
   - Create tests

2. **Import Organization**:
   - Standard library imports first
   - Third-party imports second
   - Local application imports third
   - Separate import groups with a blank line

3. **Code Style**:
   - Follow PEP 8 guidelines
   - Use consistent indentation (4 spaces)
   - Use descriptive variable and function names
   - Add docstrings to all classes and functions

4. **File Naming**:
   - Use lowercase with underscores for file names
   - Use singular nouns for model files
   - Use plural nouns for collection endpoints

## Conclusion

This file structure provides a clear organization for the Core Data Models implementation. It follows best practices for FastAPI and SQLAlchemy applications, ensuring maintainability, testability, and extensibility.