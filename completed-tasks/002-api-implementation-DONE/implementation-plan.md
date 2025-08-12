# Task 2: Basic API Endpoints - Implementation Plan

## Implementation Sequence

This plan outlines the step-by-step approach to implementing the basic API endpoints for the Election Monitoring System.

### Phase 1: Setup and Foundation (Estimated time: 1 hour)

1. **Create API Router Structure**
   - Set up router modules for each endpoint category
   - Configure main FastAPI application with routers
   - Implement basic middleware (CORS, error handling)

2. **Create Service Layer Structure**
   - Set up service modules corresponding to routers
   - Implement dependency injection for services
   - Create base service class with common functionality

3. **Set Up Error Handling Framework**
   - Create custom exception classes
   - Implement exception handlers
   - Set up error response formatting

### Phase 2: Core Endpoint Implementation (Estimated time: 3 hours)

4. **Implement Health Check Endpoint**
   - Create health service with system checks
   - Implement health check router
   - Add basic system information collection

5. **Implement Constituency Endpoints**
   - Create constituency service
   - Implement list endpoint with pagination and filtering
   - Implement detail endpoint with comprehensive data

6. **Implement Election Endpoints**
   - Create election service
   - Implement list endpoint with filtering
   - Implement detail endpoint
   - Implement upcoming elections endpoint

7. **Implement Dashboard Summary Endpoint**
   - Create dashboard service
   - Implement data aggregation logic
   - Create summary endpoint with all required metrics

### Phase 3: Documentation and Testing (Estimated time: 2 hours)

8. **Enhance API Documentation**
   - Add detailed descriptions to all endpoints
   - Include request/response examples
   - Configure Swagger UI with additional information

9. **Implement Unit Tests**
   - Create test fixtures for API testing
   - Implement tests for each endpoint
   - Test error scenarios and edge cases

10. **Perform Integration Testing**
    - Test API endpoints with test database
    - Verify correct data flow through all layers
    - Validate response formats and status codes

## Detailed Implementation Steps

### 1. Create API Router Structure

```python
# Create router modules
# app/api/routes/health.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/health", tags=["health"])

# app/api/routes/constituencies.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/constituencies", tags=["constituencies"])

# app/api/routes/elections.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/elections", tags=["elections"])

# app/api/routes/dashboard.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Configure main app with routers
# app/api/__init__.py
from fastapi import APIRouter
from app.api.routes import health, constituencies, elections, dashboard

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(constituencies.router)
api_router.include_router(elections.router)
api_router.include_router(dashboard.router)

# Update main.py to include API router
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router

app = FastAPI(title="Election Monitoring API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
```

### 2. Create Service Layer Structure

```python
# app/services/base.py
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import BaseCRUD
from app.models.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=BaseCRUD)

class BaseService(Generic[ModelType, CRUDType]):
    def __init__(self, crud_class: Type[CRUDType], db: AsyncSession):
        self.crud = crud_class(db)
        self.db = db

# app/services/constituency.py
from app.services.base import BaseService
from app.models.constituency import Constituency
from app.crud.constituency import ConstituencyCRUD

class ConstituencyService(BaseService[Constituency, ConstituencyCRUD]):
    def __init__(self, db: AsyncSession):
        super().__init__(ConstituencyCRUD, db)
    
    # Add constituency-specific service methods

# Similar service classes for Election, Dashboard, Health
```

### 3. Set Up Error Handling Framework

```python
# app/api/errors/exceptions.py
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

# app/api/errors/handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.api.errors.exceptions import NotFoundError, ValidationError, DatabaseError

async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.detail}}
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.detail}}
    )

async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": exc.detail}}
    )

# Register handlers in main.py
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(DatabaseError, database_exception_handler)
```

### 4. Implement Health Check Endpoint

```python
# app/services/health.py
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

# app/api/routes/health.py
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

### 5. Implement Constituency Endpoints

```python
# app/api/routes/constituencies.py
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.services.constituency import ConstituencyService
from app.api.dependencies import get_constituency_service
from app.models.schemas.constituency import ConstituencyResponse, ConstituencyList
from app.api.errors.exceptions import NotFoundError

router = APIRouter(prefix="/constituencies", tags=["constituencies"])

@router.get("", response_model=ConstituencyList)
async def list_constituencies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    election_id: Optional[int] = None,
    status: Optional[str] = None,
    service: ConstituencyService = Depends(get_constituency_service)
):
    """
    List constituencies with pagination and optional filtering.
    
    Parameters:
        page: Page number (1-indexed)
        page_size: Number of items per page
        election_id: Filter by election ID
        status: Filter by constituency status
        
    Returns:
        ConstituencyList: Paginated list of constituencies with metadata
    """
    constituencies, total = await service.get_constituencies(
        page=page,
        page_size=page_size,
        election_id=election_id,
        status=status
    )
    
    return {
        "metadata": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size
        },
        "data": constituencies
    }

@router.get("/{constituency_id}", response_model=ConstituencyResponse)
async def get_constituency(
    constituency_id: int,
    service: ConstituencyService = Depends(get_constituency_service)
):
    """
    Get detailed information about a specific constituency.
    
    Parameters:
        constituency_id: The ID of the constituency
        
    Returns:
        ConstituencyResponse: Detailed constituency information
        
    Raises:
        404: Constituency not found
    """
    constituency = await service.get_constituency(constituency_id)
    if not constituency:
        raise NotFoundError(f"Constituency with ID {constituency_id} not found")
    return constituency
```

### 6. Implement Election Endpoints

```python
# app/api/routes/elections.py
# Similar pattern to constituency endpoints, with election-specific functionality
```

### 7. Implement Dashboard Summary Endpoint

```python
# app/services/dashboard.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.election import ElectionCRUD
from app.crud.constituency import ConstituencyCRUD
from app.crud.transaction import TransactionCRUD

class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.election_crud = ElectionCRUD(db)
        self.constituency_crud = ConstituencyCRUD(db)
        self.transaction_crud = TransactionCRUD(db)
    
    async def get_summary(self):
        # Get essential counts from core entities
        active_elections = await self.election_crud.count(status="active")
        total_constituencies = await self.constituency_crud.count()
        active_constituencies = await self.constituency_crud.count(status="active")
        recent_transactions = await self.transaction_crud.count_recent(hours=24)
        
        # Return simplified dashboard data
        return {
            "active_elections": active_elections,
            "total_constituencies": total_constituencies,
            "active_constituencies": active_constituencies,
            "recent_transactions": recent_transactions
        }
        
        # Note: Additional metrics can be added as needed in future iterations:
        # - Alert counts by priority
        # - File processing status counts

# app/api/routes/dashboard.py
from fastapi import APIRouter, Depends
from app.services.dashboard import DashboardService
from app.api.dependencies import get_dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
async def get_dashboard_summary(
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get summary statistics for the dashboard.
    
    Returns:
        dict: Dashboard summary statistics
    """
    return await service.get_summary()
```

### 8. Enhance API Documentation

```python
# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Election Monitoring API",
    description="API for the Election Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Election Monitoring API",
        version="1.0.0",
        description="API for monitoring election data and detecting anomalies",
        routes=app.routes,
    )
    
    # Add custom documentation
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    
    # Add security schemes for future use
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### 9. Implement Unit Tests

```python
# tests/api/test_health.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_connection" in data
    assert data["status"] in ["healthy", "unhealthy"]

# tests/api/test_constituencies.py
# Similar pattern for testing constituency endpoints

# tests/api/test_elections.py
# Similar pattern for testing election endpoints

# tests/api/test_dashboard.py
# Similar pattern for testing dashboard endpoints
```

## Dependencies and Requirements

- FastAPI
- SQLAlchemy (already set up)
- Pydantic (already set up)
- psutil (for health check metrics)
- pytest and pytest-asyncio (for testing)

## File Structure

See the accompanying file-structure.md document for the complete file organization.

## Testing Strategy

1. **Unit Tests**:
   - Test each endpoint in isolation
   - Mock service layer dependencies
   - Test success and error scenarios
   - Verify response formats and status codes

2. **Integration Tests**:
   - Test API with test database
   - Verify data flow through all layers
   - Test pagination and filtering
   - Verify error handling

3. **Test Coverage**:
   - Aim for 80% code coverage minimum
   - Focus on critical paths and error handling

## Deployment Considerations

- API will be deployed as part of the backend service
- CORS configuration will need to be updated for production
- Health check endpoint will be used for monitoring

## Completion Criteria

The implementation will be considered complete when:

1. All endpoints are implemented according to the specifications
2. All tests pass with the required coverage
3. API documentation is complete and accurate
4. CORS is properly configured
5. Error handling is consistent across all endpoints
6. Code follows project style guidelines