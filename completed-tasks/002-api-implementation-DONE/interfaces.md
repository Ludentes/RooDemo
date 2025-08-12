# Task 2: Basic API Endpoints - Interfaces

This document defines the interfaces for the API endpoints and services to be implemented in this task.

## API Contracts

### Health Check Endpoint

#### `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "database_connection": "ok",
  "response_time": "5.23ms"
}
```

**Status Codes:**
- 200: Success
- 500: Server error

### Constituency Endpoints

#### `GET /api/constituencies`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)
- `election_id`: Filter by election ID (optional)
- `status`: Filter by constituency status (optional)

**Response:**
```json
{
  "metadata": {
    "total": 100,
    "page": 1,
    "page_size": 10,
    "pages": 10
  },
  "data": [
    {
      "id": 1,
      "name": "District 1",
      "code": "D001",
      "election_id": 1,
      "election_name": "Presidential Election 2025",
      "registered_voters": 10000,
      "status": "active",
      "created_at": "2025-08-01T12:00:00Z",
      "updated_at": "2025-08-01T12:00:00Z"
    },
    // More constituencies...
  ]
}
```

**Status Codes:**
- 200: Success
- 400: Invalid parameters
- 500: Server error

#### `GET /api/constituencies/{constituency_id}`

**Path Parameters:**
- `constituency_id`: ID of the constituency

**Response:**
```json
{
  "id": 1,
  "name": "District 1",
  "code": "D001",
  "description": "Northern district covering areas A, B, and C",
  "election_id": 1,
  "election_name": "Presidential Election 2025",
  "registered_voters": 10000,
  "status": "active",
  "location": {
    "region": "North",
    "city": "Capital City"
  },
  "statistics": {
    "participation_rate": 0.65,
    "bulletins_issued": 6500,
    "votes_cast": 6450,
    "invalid_votes": 50
  },
  "created_at": "2025-08-01T12:00:00Z",
  "updated_at": "2025-08-01T12:00:00Z"
}
```

**Status Codes:**
- 200: Success
- 404: Constituency not found
- 500: Server error

### Election Endpoints

#### `GET /api/elections`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)
- `status`: Filter by election status (optional)

**Response:**
```json
{
  "metadata": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "pages": 1
  },
  "data": [
    {
      "id": 1,
      "name": "Presidential Election 2025",
      "description": "General presidential election",
      "status": "active",
      "start_date": "2025-08-01T00:00:00Z",
      "end_date": "2025-08-01T20:00:00Z",
      "constituency_count": 50,
      "created_at": "2025-07-01T12:00:00Z",
      "updated_at": "2025-07-01T12:00:00Z"
    },
    // More elections...
  ]
}
```

**Status Codes:**
- 200: Success
- 400: Invalid parameters
- 500: Server error

#### `GET /api/elections/{election_id}`

**Path Parameters:**
- `election_id`: ID of the election

**Response:**
```json
{
  "id": 1,
  "name": "Presidential Election 2025",
  "description": "General presidential election",
  "status": "active",
  "start_date": "2025-08-01T00:00:00Z",
  "end_date": "2025-08-01T20:00:00Z",
  "registered_voters": 500000,
  "constituencies": [
    {
      "id": 1,
      "name": "District 1",
      "code": "D001",
      "registered_voters": 10000,
      "status": "active"
    },
    // More constituencies...
  ],
  "statistics": {
    "participation_rate": 0.68,
    "bulletins_issued": 340000,
    "votes_cast": 338000,
    "invalid_votes": 2000
  },
  "created_at": "2025-07-01T12:00:00Z",
  "updated_at": "2025-07-01T12:00:00Z"
}
```

**Status Codes:**
- 200: Success
- 404: Election not found
- 500: Server error

#### `GET /api/elections/upcoming`

**Response:**
```json
{
  "metadata": {
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  },
  "data": [
    {
      "id": 2,
      "name": "Local Elections 2025",
      "description": "Local council elections",
      "status": "scheduled",
      "start_date": "2025-09-15T00:00:00Z",
      "end_date": "2025-09-15T20:00:00Z",
      "constituency_count": 30,
      "created_at": "2025-07-15T12:00:00Z",
      "updated_at": "2025-07-15T12:00:00Z"
    },
    // More upcoming elections...
  ]
}
```

**Status Codes:**
- 200: Success
- 500: Server error

### Dashboard Summary Endpoint

#### `GET /api/dashboard/summary`

**Response:**
```json
{
  "active_elections": 1,
  "total_constituencies": 100,
  "active_constituencies": 80,
  "recent_transactions": 1500
}
```

**Status Codes:**
- 200: Success
- 500: Server error

## Service Interfaces

### Base Service

```python
class BaseService(Generic[ModelType, CRUDType]):
    def __init__(self, crud_class: Type[CRUDType], db: AsyncSession):
        self.crud = crud_class(db)
        self.db = db
        
    async def get(self, id: Any) -> Optional[ModelType]:
        """Get a single record by ID"""
        
    async def get_multi(
        self, 
        page: int = 1, 
        page_size: int = 10, 
        **filters
    ) -> Tuple[List[ModelType], int]:
        """Get multiple records with pagination and filtering"""
```

### Health Service

```python
class HealthService:
    async def check_health(self) -> Dict[str, Any]:
        """
        Check the health of the system
        
        Returns:
            Dict with basic health status information including:
            - API status
            - Database connection status
            - Response time
        """
```

### Constituency Service

```python
class ConstituencyService(BaseService[Constituency, ConstituencyCRUD]):
    def __init__(self, db: AsyncSession):
        super().__init__(ConstituencyCRUD, db)
    
    async def get_constituencies(
        self,
        page: int = 1,
        page_size: int = 10,
        election_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get constituencies with pagination and filtering
        
        Returns:
            Tuple of (constituencies list, total count)
        """
    
    async def get_constituency(self, constituency_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific constituency
        
        Returns:
            Constituency data with statistics or None if not found
        """
```

### Election Service

```python
class ElectionService(BaseService[Election, ElectionCRUD]):
    def __init__(self, db: AsyncSession):
        super().__init__(ElectionCRUD, db)
    
    async def get_elections(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get elections with pagination and filtering
        
        Returns:
            Tuple of (elections list, total count)
        """
    
    async def get_election(self, election_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific election
        
        Returns:
            Election data with statistics or None if not found
        """
    
    async def get_upcoming_elections(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get upcoming elections (scheduled or upcoming status)
        
        Returns:
            Tuple of (upcoming elections list, total count)
        """
```

### Dashboard Service

```python
class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.election_crud = ElectionCRUD(db)
        self.constituency_crud = ConstituencyCRUD(db)
        self.transaction_crud = TransactionCRUD(db)
    
    async def get_summary(self) -> Dict[str, Any]:
        """
        Get essential summary statistics for the dashboard
        
        Returns:
            Dict with core summary statistics:
            - Active elections count
            - Total constituencies count
            - Active constituencies count
            - Recent transactions count
        """
```

## Error Handling

### Custom Exceptions

```python
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

### Error Response Format

For this small-scale project, we'll use a simplified but effective error response format:

```json
{
  "error": {
    "message": "Human-readable error message"
  }
}
```

This provides clear error information without unnecessary complexity. If more detailed error information is needed for debugging, it can be logged server-side rather than exposed in the API response.

Common HTTP status codes used:
- `404`: Resource not found
- `400`: Invalid input data
- `500`: Server or database error

## Pagination Format

All paginated responses will follow this format:

```json
{
  "metadata": {
    "total": 100,    // Total number of items
    "page": 1,       // Current page number
    "page_size": 10, // Items per page
    "pages": 10      // Total number of pages
  },
  "data": [
    // Array of items
  ]
}
```

## Dependencies

### API Dependencies

```python
async def get_health_service() -> HealthService:
    """Dependency for health service"""

async def get_constituency_service(db: AsyncSession = Depends(get_db)) -> ConstituencyService:
    """Dependency for constituency service"""

async def get_election_service(db: AsyncSession = Depends(get_db)) -> ElectionService:
    """Dependency for election service"""

async def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    """Dependency for dashboard service"""