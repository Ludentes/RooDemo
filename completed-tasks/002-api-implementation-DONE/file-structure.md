# Task 2: Basic API Endpoints - File Structure

This document outlines the file structure for implementing the basic API endpoints. It builds upon the existing project structure and adds new files for the API layer.

## New Directory Structure

```
backend/
├── app/
│   ├── api/                      # New API layer
│   │   ├── __init__.py           # API router configuration
│   │   ├── dependencies.py       # Dependency injection functions
│   │   ├── routes/               # Route modules
│   │   │   ├── __init__.py
│   │   │   ├── health.py         # Health check endpoints
│   │   │   ├── constituencies.py # Constituency endpoints
│   │   │   ├── elections.py      # Election endpoints
│   │   │   └── dashboard.py      # Dashboard endpoints
│   │   └── errors/               # Error handling
│   │       ├── __init__.py
│   │       ├── exceptions.py     # Custom exception classes
│   │       └── handlers.py       # Exception handlers
│   │
│   ├── services/                 # New service layer
│   │   ├── __init__.py
│   │   ├── base.py               # Base service class
│   │   ├── health.py             # Health check service
│   │   ├── constituency.py       # Constituency service
│   │   ├── election.py           # Election service
│   │   └── dashboard.py          # Dashboard service
│   │
│   ├── models/                   # Existing models from Task 1
│   │   └── ...
│   │
│   ├── crud/                     # Existing CRUD from Task 1
│   │   └── ...
│   │
│   └── main.py                   # Updated with API configuration
│
└── tests/
    ├── api/                      # New API tests
    │   ├── __init__.py
    │   ├── conftest.py           # Test fixtures for API
    │   ├── test_health.py        # Health endpoint tests
    │   ├── test_constituencies.py # Constituency endpoint tests
    │   ├── test_elections.py     # Election endpoint tests
    │   └── test_dashboard.py     # Dashboard endpoint tests
    │
    ├── services/                 # New service tests
    │   ├── __init__.py
    │   ├── test_health.py        # Health service tests
    │   ├── test_constituency.py  # Constituency service tests
    │   ├── test_election.py      # Election service tests
    │   └── test_dashboard.py     # Dashboard service tests
    │
    └── ...                       # Existing test directories
```

## File Details

### API Layer

#### `app/api/__init__.py`
```python
from fastapi import APIRouter
from app.api.routes import health, constituencies, elections, dashboard

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(constituencies.router)
api_router.include_router(elections.router)
api_router.include_router(dashboard.router)
```

#### `app/api/dependencies.py`
```python
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db
from app.services.health import HealthService
from app.services.constituency import ConstituencyService
from app.services.election import ElectionService
from app.services.dashboard import DashboardService

async def get_health_service() -> HealthService:
    return HealthService()

async def get_constituency_service(db: AsyncSession = Depends(get_db)) -> ConstituencyService:
    return ConstituencyService(db)

async def get_election_service(db: AsyncSession = Depends(get_db)) -> ElectionService:
    return ElectionService(db)

async def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    return DashboardService(db)
```

#### `app/api/routes/health.py`
```python
from fastapi import APIRouter, Depends
from app.services.health import HealthService
from app.api.dependencies import get_health_service

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", summary="Check API health")
async def health_check(health_service: HealthService = Depends(get_health_service)):
    """
    Check the health of the API and its dependencies.
    
    Returns:
        dict: Health status information including database connection status
    """
    return await health_service.check_health()
```

#### `app/api/errors/exceptions.py`
```python
from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationError(HTTPException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
```

### Service Layer

#### `app/services/base.py`
```python
from typing import Generic, TypeVar, Type, Optional, List, Tuple, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import BaseCRUD
from app.models.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=BaseCRUD)

class BaseService(Generic[ModelType, CRUDType]):
    def __init__(self, crud_class: Type[CRUDType], db: AsyncSession):
        self.crud = crud_class(db)
        self.db = db
        
    async def get(self, id: Any) -> Optional[ModelType]:
        return await self.crud.get(id)
        
    async def get_multi(
        self, 
        page: int = 1, 
        page_size: int = 10, 
        **filters
    ) -> Tuple[List[ModelType], int]:
        skip = (page - 1) * page_size
        return await self.crud.get_multi(skip=skip, limit=page_size, **filters)
```

#### `app/services/health.py`
```python
import time
from app.models.database import engine

class HealthService:
    async def check_health(self):
        start_time = time.time()
        db_status = "ok"
        
        try:
            # Test database connection
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
        except Exception:
            db_status = "error"
            
        return {
            "status": "healthy" if db_status == "ok" else "unhealthy",
            "database_connection": db_status,
            "response_time": f"{(time.time() - start_time) * 1000:.2f}ms"
        }
```

### Main Application

#### `app/main.py` (Updated)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.api.errors.handlers import register_exception_handlers

app = FastAPI(
    title="Election Monitoring API",
    description="API for the Election Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router)

# Register exception handlers
register_exception_handlers(app)
```

### Test Files

#### `tests/api/conftest.py`
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.database import Base, get_db

# Create test database engine
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine, 
    class_=AsyncSession
)

@pytest.fixture
async def db():
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(db):
    # Override dependency
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
```

#### `tests/api/test_health.py`
```python
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_connection" in data
    assert data["status"] in ["healthy", "unhealthy"]
```

## Implementation Notes

1. **Dependency Injection**:
   - All services are injected via FastAPI's dependency injection system
   - Database sessions are managed through dependencies

2. **Error Handling**:
   - Custom exceptions extend FastAPI's HTTPException
   - Exception handlers provide consistent error responses

3. **Testing**:
   - Tests use in-memory SQLite database
   - Dependency overrides isolate tests from production database

4. **Documentation**:
   - All endpoints include docstrings for OpenAPI documentation
   - Response models are defined using Pydantic schemas

5. **CORS**:
   - CORS is configured to allow all origins in development
   - Should be restricted to specific origins in production