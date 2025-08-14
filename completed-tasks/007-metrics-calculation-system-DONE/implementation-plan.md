# Implementation Plan: Metrics Calculation System

## 1. Overview

The Metrics Calculation System is a comprehensive solution for calculating, storing, and retrieving metrics related to election monitoring. It addresses the current inconsistencies in the HourlyStats model and CRUD operations, and implements a robust architecture for metrics calculation and caching.

### 1.1 Key Components

1. **Enhanced HourlyStats Model**: Fix inconsistencies and add missing fields
2. **Hourly Statistics Aggregation Service**: Aggregate transaction data into hourly statistics
3. **Constituency Metrics Calculator**: Calculate metrics for constituencies
4. **Participation Rate Calculation**: Calculate participation rates at different levels
5. **Automatic Metrics Update Mechanism**: Ensure metrics are updated automatically
6. **Metrics Caching System**: Improve performance through caching
7. **Metrics API Endpoints**: Expose metrics data to clients
8. **Metrics Calculation Tests**: Ensure the system works correctly

## 2. Current Issues and Gaps

### 2.1 HourlyStats Model Issues

- Missing fields:
  - `election_id`: Foreign key to the Election model
  - `participation_rate`: Float field to store the participation rate
  - `anomaly_count`: Integer field to store the count of anomalies
  - `timestamp`: DateTime field to store the exact timestamp

- Inconsistencies:
  - References to `election_id` in CRUD operations but the field doesn't exist in the model
  - References to `participation_rate` and `anomaly_count` in CRUD operations but the fields don't exist in the model
  - References to `timestamp` in CRUD operations but the field doesn't exist in the model

### 2.2 Missing Services

- No dedicated service for hourly statistics aggregation
- No constituency metrics calculator
- No participation rate calculation logic
- No automatic metrics update mechanism
- No metrics caching system

### 2.3 API Endpoints

- Limited dashboard endpoints that don't expose detailed metrics
- No specific metrics API endpoints

### 2.4 Testing

- No tests for metrics calculation

## 3. Implementation Details

### 3.1 Enhanced HourlyStats Model

#### 3.1.1 Model Changes

Update the `HourlyStats` model in `backend/app/models/hourly_stats.py` to include the missing fields:
- Add `election_id` as a foreign key to the Election model
- Add `participation_rate` to store the percentage of registered voters who cast votes
- Add `anomaly_count` to store the count of anomalies detected
- Add `timestamp` to store the exact timestamp of the stats

#### 3.1.2 Schema Changes

Update the `HourlyStatsBase` schema in `backend/app/models/schemas/hourly_stats.py` to include the missing fields:
- Add `election_id` field
- Add `participation_rate` field
- Add `anomaly_count` field
- Add `timestamp` field

Update the `HourlyStatsUpdate` schema to include the new fields as optional parameters.

#### 3.1.3 CRUD Changes

Update the `HourlyStatsCRUD` class in `backend/app/crud/hourly_stats.py` to ensure all methods correctly use the new fields.

### 3.2 Hourly Statistics Aggregation Service

Create a new service in `backend/app/services/hourly_stats_service.py` that will:
- Aggregate transaction data for a specific constituency and hour
- Calculate metrics like bulletins issued, votes cast, transaction count, etc.
- Calculate velocities (rate of bulletin issuance, rate of vote casting)
- Calculate participation rate
- Create or update hourly stats in the database

### 3.3 Constituency Metrics Calculator

Create a new service in `backend/app/services/constituency_metrics_service.py` that will:
- Calculate metrics for a constituency based on hourly stats
- Calculate total metrics (bulletins, votes, transactions, anomalies)
- Calculate participation rate and anomaly score
- Calculate hourly activity patterns
- Update the constituency model with calculated metrics
- Support metrics calculation by time period (hour, day, week, month)

### 3.4 Participation Rate Calculation

Implement participation rate calculation in both the hourly statistics aggregation service and the constituency metrics calculator using the formula:
```
Participation Rate = (Votes Cast / Registered Voters) * 100
```

### 3.5 Automatic Metrics Update Mechanism

Create a new service in `backend/app/services/metrics_update_service.py` that will:
- Provide a queue-based system for metrics updates
- Support different update triggers (new transaction, scheduled update, manual trigger)
- Process updates asynchronously
- Handle failures and retries
- Run scheduled updates for active elections

### 3.6 Metrics Caching System

Create a new service in `backend/app/services/metrics_cache_service.py` that will:
- Provide a consistent API for cache operations (get, set, delete)
- Support different cache backends (in-memory, Redis, etc.)
- Implement cache invalidation strategies
- Support time-based expiration

### 3.7 Metrics API Endpoints

Create a new router in `backend/app/api/routes/metrics.py` that will expose the following endpoints:

#### 3.7.1 Hourly Stats Endpoints

```python
@router.get("/hourly-stats/constituency/{constituency_id}")
async def get_hourly_stats_by_constituency(
    constituency_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get hourly stats for a constituency.
    """
    # Implementation details...
```

```python
@router.get("/hourly-stats/election/{election_id}")
async def get_hourly_stats_by_election(
    election_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get hourly stats for an election.
    """
    # Implementation details...
```

#### 3.7.2 Constituency Metrics Endpoints

```python
@router.get("/metrics/constituency/{constituency_id}")
async def get_constituency_metrics(
    constituency_id: str,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get metrics for a constituency.
    """
    # Implementation details...
```

```python
@router.get("/metrics/constituency/{constituency_id}/time-period")
async def get_constituency_metrics_by_time_period(
    constituency_id: str,
    period: str = "day",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get metrics for a constituency by time period.
    """
    # Implementation details...
```

#### 3.7.3 Election Metrics Endpoints

```python
@router.get("/metrics/election/{election_id}")
async def get_election_metrics(
    election_id: str,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get metrics for an election.
    """
    # Implementation details...
```

```python
@router.get("/metrics/election/{election_id}/constituencies")
async def get_election_constituency_metrics(
    election_id: str,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get metrics for all constituencies in an election.
    """
    # Implementation details...
```

#### 3.7.4 Dashboard Metrics Endpoints

```python
@router.get("/metrics/dashboard/summary")
async def get_dashboard_metrics_summary(
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get summary metrics for the dashboard.
    """
    # Implementation details...
```

```python
@router.get("/metrics/dashboard/detailed")
async def get_dashboard_metrics_detailed(
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_metrics_cache)
):
    """
    Get detailed metrics for the dashboard.
    """
    # Implementation details...
```

### 3.8 Metrics Calculation Tests

Create tests for the metrics calculation system in the following files:

#### 3.8.1 Model Tests

Create tests for the HourlyStats model in `backend/tests/test_models/test_hourly_stats.py`:
- Test model creation
- Test model relationships
- Test model methods

#### 3.8.2 CRUD Tests

Create tests for the HourlyStats CRUD operations in `backend/tests/test_crud/test_hourly_stats_crud.py`:
- Test create operation
- Test read operations
- Test update operation
- Test delete operation
- Test specialized methods

#### 3.8.3 Service Tests

Create tests for the metrics services:
- `backend/tests/services/test_hourly_stats_service.py`
- `backend/tests/services/test_constituency_metrics_service.py`
- `backend/tests/services/test_metrics_update_service.py`
- `backend/tests/services/test_metrics_cache_service.py`

#### 3.8.4 API Tests

Create tests for the metrics API endpoints in `backend/tests/api/test_metrics.py`:
- Test hourly stats endpoints
- Test constituency metrics endpoints
- Test election metrics endpoints
- Test dashboard metrics endpoints

## 4. Implementation Phases

### 4.1 Phase 1: Model and Schema Updates

1. Update the HourlyStats model with missing fields
2. Update the HourlyStats schemas
3. Update the HourlyStats CRUD operations
4. Create database migration for model changes
5. Run migration to update the database schema

### 4.2 Phase 2: Core Services Implementation

1. Implement the hourly statistics aggregation service
2. Implement the constituency metrics calculator
3. Implement the participation rate calculation
4. Implement the metrics caching system
5. Write tests for the core services

### 4.3 Phase 3: Automatic Update Mechanism

1. Implement the metrics update service
2. Implement the update queue
3. Implement the scheduled updates
4. Implement the update triggers
5. Write tests for the update mechanism

### 4.4 Phase 4: API Endpoints

1. Implement the metrics API router
2. Implement the hourly stats endpoints
3. Implement the constituency metrics endpoints
4. Implement the election metrics endpoints
5. Implement the dashboard metrics endpoints
6. Write tests for the API endpoints

### 4.5 Phase 5: Integration and Testing

1. Integrate all components
2. Write integration tests
3. Perform performance testing
4. Fix any issues found during testing
5. Document the metrics calculation system

## 5. Dependencies and Prerequisites

- SQLAlchemy for database operations
- FastAPI for API endpoints
- Pydantic for data validation
- Alembic for database migrations
- Redis (optional) for caching
- Pytest for testing

## 6. Conclusion and Handoff

This implementation plan provides a comprehensive approach to implementing a metrics calculation system for the Election Monitoring System. It addresses the current issues with the HourlyStats model and provides a clear architecture for the metrics system.

### 6.1 Handoff to Systematic Developer

The implementation should proceed in the phases outlined above, with each phase being completed and tested before moving on to the next. The Systematic Developer should:

1. Start with the model and schema updates
2. Implement the core services
3. Add the automatic update mechanism
4. Create the API endpoints
5. Integrate and test all components

### 6.2 Key Considerations

- Ensure proper error handling throughout the implementation
- Implement comprehensive logging for debugging
- Use caching to improve performance
- Write thorough tests for all components
- Document the API endpoints and services

### 6.3 Success Criteria

The implementation will be considered successful when:

1. All model inconsistencies are fixed
2. Hourly statistics are correctly aggregated
3. Constituency metrics are accurately calculated
4. Participation rates are correctly computed
5. Metrics are automatically updated
6. Metrics are properly cached
7. API endpoints return correct data
8. All tests pass

With this implementation plan, the Systematic Developer has a clear roadmap for implementing the metrics calculation system.