# Election Monitoring System - API Contracts

## Base URL
`http://localhost:8000`

## Authentication
Authentication will be implemented in future versions. The current MVP does not include authentication.

## Response Format
All API responses follow a standard format:

```json
{
  "data": {},      // Response data (varies by endpoint)
  "meta": {        // Metadata about the response (optional)
    "total": 0,    // Total count for paginated responses
    "page": 1,     // Current page
    "limit": 20    // Items per page
  },
  "error": null    // Error details if applicable
}
```

## Error Handling
Errors follow a standard format:

```json
{
  "data": null,
  "meta": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}  // Additional error details if available
  }
}
```

## Common Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## API Endpoints

### Elections Endpoints

#### List Elections
```
GET /api/elections
```

**Description**: Retrieves a paginated list of elections with optional filtering.

**Query Parameters**:
- `page` (integer, optional, default=1): Page number (1-indexed)
- `page_size` (integer, optional, default=10): Number of items per page
- `status` (string, optional): Filter by status (active, completed, upcoming, scheduled)

**Response**: List of `Election` objects

```json
{
  "data": [
    {
      "id": "2d838dbd-0af9-409e-a304-639220b37174",
      "name": "2025 Presidential Election",
      "country": "United States",
      "description": "2025 United States Presidential Election",
      "status": "active",
      "type": "presidential",
      "timezone": "America/New_York",
      "start_date": "2025-08-10T17:06:40.299970",
      "end_date": "2025-08-13T17:06:40.299988",
      "constituency_count": 50,
      "created_at": "2025-08-12T17:06:40.307124",
      "updated_at": "2025-08-12T17:06:40.307127"
    },
    {
      "id": "8d061be4-0444-43d1-bb33-a61a2945c093",
      "name": "2026 Midterm Elections",
      "country": "United States",
      "description": "2026 United States Midterm Elections",
      "status": "upcoming",
      "type": "parliamentary",
      "timezone": "America/New_York",
      "start_date": "2026-02-08T17:06:40.307546",
      "end_date": "2026-02-09T17:06:40.307559",
      "constituency_count": 10,
      "created_at": "2025-08-12T17:06:40.307758",
      "updated_at": "2025-08-12T17:06:40.307759"
    }
  ],
  "total": 3,
  "page": 1,
  "limit": 10
}
```

#### Get Election Details
```
GET /api/elections/{election_id}
```

**Description**: Retrieves detailed information about a specific election.

**Path Parameters**:
- `election_id` (string, required): Unique identifier of the election

**Response**: `Election` object with detailed information

```json
{
  "id": "2d838dbd-0af9-409e-a304-639220b37174",
  "name": "2025 Presidential Election",
  "country": "United States",
  "description": "2025 United States Presidential Election",
  "status": "active",
  "type": "presidential",
  "timezone": "America/New_York",
  "start_date": "2025-08-10T17:06:40.299970",
  "end_date": "2025-08-13T17:06:40.299988",
  "registered_voters": 1500000,
  "constituencies": [
    {
      "id": "0x00000000",
      "name": "District 1",
      "registered_voters": 15655,
      "status": "active"
    },
    {
      "id": "0x00000001",
      "name": "District 2",
      "registered_voters": 41010,
      "status": "active"
    }
  ],
  "statistics": {
    "participation_rate": 0.68,
    "bulletins_issued": 340000,
    "votes_cast": 338000,
    "invalid_votes": 2000
  },
  "created_at": "2025-08-12T17:06:40.307124",
  "updated_at": "2025-08-12T17:06:40.307127"
}
```

#### Get Upcoming Elections
```
GET /api/elections/upcoming
```

**Description**: Retrieves a paginated list of upcoming elections (status is 'upcoming' or 'scheduled').

**Query Parameters**:
- `page` (integer, optional, default=1): Page number (1-indexed)
- `page_size` (integer, optional, default=10): Number of items per page

**Response**: List of `Election` objects

```json
{
  "data": [
    {
      "id": "8d061be4-0444-43d1-bb33-a61a2945c093",
      "name": "2026 Midterm Elections",
      "country": "United States",
      "description": "2026 United States Midterm Elections",
      "status": "upcoming",
      "type": "parliamentary",
      "timezone": "America/New_York",
      "start_date": "2026-02-08T17:06:40.307546",
      "end_date": "2026-02-09T17:06:40.307559",
      "constituency_count": 10,
      "created_at": "2025-08-12T17:06:40.307758",
      "updated_at": "2025-08-12T17:06:40.307759"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

### Constituencies Endpoints

#### List Constituencies
```
GET /api/constituencies
```

**Description**: Retrieves a paginated list of constituencies with optional filtering.

**Query Parameters**:
- `page` (integer, optional, default=1): Page number (1-indexed)
- `page_size` (integer, optional, default=10): Number of items per page
- `election_id` (string, optional): Filter by election ID
- `status` (string, optional): Filter by status (active, offline, completed, inactive)

**Response**: List of `Constituency` objects

```json
{
  "data": [
    {
      "id": "0x00000000",
      "name": "District 1",
      "election_id": "2d838dbd-0af9-409e-a304-639220b37174",
      "election_name": "2025 Presidential Election",
      "region": "Central",
      "type": "urban",
      "registered_voters": 15655,
      "status": "active",
      "last_update_time": "2025-08-12T17:06:40.308836",
      "bulletins_issued": 12500,
      "votes_cast": 10200,
      "participation_rate": 0.65,
      "anomaly_score": 0.12,
      "created_at": "2025-08-12T17:06:40.308836",
      "updated_at": "2025-08-12T17:06:40.309780"
    },
    {
      "id": "0x00000001",
      "name": "District 2",
      "election_id": "2d838dbd-0af9-409e-a304-639220b37174",
      "election_name": "2025 Presidential Election",
      "region": "East",
      "type": "rural",
      "registered_voters": 41010,
      "status": "active",
      "last_update_time": "2025-08-12T17:06:40.309881",
      "bulletins_issued": 35000,
      "votes_cast": 32000,
      "participation_rate": 0.78,
      "anomaly_score": 0.05,
      "created_at": "2025-08-12T17:06:40.309881",
      "updated_at": "2025-08-12T17:06:40.309882"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}
```

#### Get Constituency Details
```
GET /api/constituencies/{constituency_id}
```

**Description**: Retrieves detailed information about a specific constituency.

**Path Parameters**:
- `constituency_id` (string, required): Unique identifier of the constituency

**Response**: `Constituency` object with detailed information

```json
{
  "id": "0x00000000",
  "name": "District 1",
  "election_id": "2d838dbd-0af9-409e-a304-639220b37174",
  "election_name": "2025 Presidential Election",
  "region": "Central",
  "type": "urban",
  "registered_voters": 15655,
  "status": "active",
  "last_update_time": "2025-08-12T17:06:40.308836",
  "bulletins_issued": 12500,
  "votes_cast": 10200,
  "participation_rate": 0.65,
  "anomaly_score": 0.12,
  "statistics": {
    "participation_rate": 0.65,
    "bulletins_issued": 12500,
    "votes_cast": 10200,
    "invalid_votes": 50
  },
  "created_at": "2025-08-12T17:06:40.308836",
  "updated_at": "2025-08-12T17:06:40.309780"
}
```

### Dashboard Endpoints

#### Get Dashboard Summary
```
GET /api/dashboard/summary
```

**Description**: Retrieves a summary of key metrics for the election monitoring system.

**Query Parameters**:
- `election_id` (string, optional): Filter metrics for a specific election
- `days` (integer, optional, default=7): Number of days to include in recent activity metrics

**Response**: Dashboard summary object with key metrics

```json
{
  "active_elections": 1,
  "upcoming_elections": 1,
  "total_constituencies": 50,
  "active_constituencies": 50,
  "recent_transactions": 150,
  "recent_anomalies": 3,
  "system_health": {
    "status": "healthy",
    "database": "connected",
    "api": "operational",
    "last_check": "2025-08-12T17:06:40.309882"
  },
  "participation_summary": {
    "average_participation": 0.72,
    "highest_participation": {
      "constituency_id": "0x00000001",
      "constituency_name": "District 2",
      "rate": 0.78
    },
    "lowest_participation": {
      "constituency_id": "0x00000000",
      "constituency_name": "District 1",
      "rate": 0.65
    }
  }
}
```

### Health Endpoint

#### Get Health Status
```
GET /api/health
```

**Description**: Checks the health status of the API and its dependencies.

**Response**: Health status object

```json
{
  "status": "healthy",
  "timestamp": "2025-08-12T17:06:40.309882",
  "version": "1.0.0",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "api": {
    "status": "operational",
    "uptime": "2d 3h 45m"
  }
}
```

## Error Responses

All API endpoints follow a consistent error response format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error context"
    }
  }
}
```

### Common Error Codes

- `NOT_FOUND`: The requested resource was not found
- `VALIDATION_ERROR`: The request contains invalid data
- `DATABASE_ERROR`: An error occurred while accessing the database
- `INTERNAL_ERROR`: An unexpected internal error occurred
- `UNAUTHORIZED`: Authentication is required or failed
- `FORBIDDEN`: The authenticated user does not have permission to access the resource

#### Get Dashboard Summary
```
GET /api/dashboard
```

**Description**: Retrieves overall dashboard metrics and summary statistics.

**Response**: `DashboardSummary`

```json
{
  "totalConstituencies": 247,
  "activeConstituencies": 240,
  "offlineConstituencies": 7,
  "totalBulletins": 125000,
  "totalVotes": 98500,
  "participationRate": 0.788,
  "lastUpdate": "2025-08-12T08:45:30Z",
  "criticalAlerts": 3,
  "warningAlerts": 12
}
```

#### Get Real-time Activity
```
GET /api/dashboard/activity
```

**Description**: Retrieves real-time voting activity metrics.

**Response**: `RealTimeActivity`

```json
{
  "votesPerHour": 1250,
  "bulletinsPerHour": 1500,
  "activityTimeline": [
    {
      "hour": "2025-08-12T07:00:00Z",
      "votes": 1100,
      "bulletins": 1300
    },
    {
      "hour": "2025-08-12T08:00:00Z",
      "votes": 1250,
      "bulletins": 1500
    }
  ]
}
```

#### WebSocket Connection
```
WS /api/dashboard/ws
```

**Description**: Establishes a WebSocket connection for real-time updates.

**Events**:

- `dashboard_update`: New dashboard summary data
- `activity_update`: New activity data
- `alert_created`: New alert notification
- `constituency_status_change`: Constituency status change

**Example Message**:
```json
{
  "type": "dashboard_update",
  "data": {
    "totalConstituencies": 247,
    "activeConstituencies": 240,
    "offlineConstituencies": 7,
    "totalBulletins": 125100,
    "totalVotes": 98600,
    "participationRate": 0.788,
    "lastUpdate": "2025-08-12T08:46:30Z",
    "criticalAlerts": 3,
    "warningAlerts": 12
  }
}
```

### Constituency Endpoints

#### List Constituencies
```
GET /api/constituencies
```

**Description**: Retrieves a paginated list of constituencies with filtering options.

**Query Parameters**:
- `region` (string, optional): Filter by region
- `status` (string, optional): Filter by status (active, offline, completed)
- `limit` (integer, optional, default=20): Number of items per page
- `offset` (integer, optional, default=0): Pagination offset

**Response**: List of `ConstituencyOverview`

```json
{
  "data": [
    {
      "id": "0x1234567890abcdef",
      "name": "Central District",
      "region": "Northern",
      "type": "urban",
      "bulletinsIssued": 5000,
      "votesCast": 4200,
      "participationRate": 0.84,
      "status": "active",
      "lastActivity": "2025-08-12T08:40:12Z",
      "anomalyScore": 0.12,
      "hasAlerts": false
    },
    {
      "id": "0xabcdef1234567890",
      "name": "Western Heights",
      "region": "Western",
      "type": "suburban",
      "bulletinsIssued": 3500,
      "votesCast": 2800,
      "participationRate": 0.8,
      "status": "active",
      "lastActivity": "2025-08-12T08:42:18Z",
      "anomalyScore": 0.05,
      "hasAlerts": false
    }
  ],
  "meta": {
    "total": 247,
    "page": 1,
    "limit": 20
  }
}
```

#### Get Constituency Detail
```
GET /api/constituencies/{constituency_id}
```

**Description**: Retrieves detailed information about a specific constituency.

**Path Parameters**:
- `constituency_id` (string, required): Unique identifier of the constituency

**Response**: `ConstituencyDetail`

```json
{
  "id": "0x1234567890abcdef",
  "name": "Central District",
  "region": "Northern",
  "type": "urban",
  "registeredVoters": 6000,
  "bulletinsIssued": 5000,
  "votesCast": 4200,
  "participationRate": 0.84,
  "status": "active",
  "lastActivity": "2025-08-12T08:40:12Z",
  "anomalyScore": 0.12,
  "hourlyStats": [
    {
      "hour": "2025-08-12T07:00:00Z",
      "bulletinsIssued": 500,
      "votesCast": 420,
      "transactionCount": 920,
      "bulletinVelocity": 500,
      "voteVelocity": 420
    },
    {
      "hour": "2025-08-12T08:00:00Z",
      "bulletinsIssued": 550,
      "votesCast": 480,
      "transactionCount": 1030,
      "bulletinVelocity": 550,
      "voteVelocity": 480
    }
  ],
  "recentTransactions": [
    {
      "id": "tx123456",
      "constituencyId": "0x1234567890abcdef",
      "type": "vote",
      "timestamp": "2025-08-12T08:40:12Z",
      "blockHeight": 12345678,
      "details": {}
    }
  ],
  "alerts": [],
  "comparativeMetrics": {
    "vsRegionalAverage": 1.05,
    "vsHistorical": 0.98,
    "vsSimilarType": 1.02
  }
}
```

#### Get Constituency Transactions
```
GET /api/constituencies/{constituency_id}/transactions
```

**Description**: Retrieves transaction history for a specific constituency.

**Path Parameters**:
- `constituency_id` (string, required): Unique identifier of the constituency

**Query Parameters**:
- `limit` (integer, optional, default=20): Number of items per page
- `offset` (integer, optional, default=0): Pagination offset
- `hours` (integer, optional): Filter transactions from the last N hours

**Response**: List of `Transaction`

```json
{
  "data": [
    {
      "id": "tx123456",
      "constituencyId": "0x1234567890abcdef",
      "type": "vote",
      "timestamp": "2025-08-12T08:40:12Z",
      "blockHeight": 12345678,
      "details": {
        "voterHash": "0xabcd1234",
        "ballotHash": "0x5678efgh"
      }
    },
    {
      "id": "tx123455",
      "constituencyId": "0x1234567890abcdef",
      "type": "blindSigIssue",
      "timestamp": "2025-08-12T08:39:45Z",
      "blockHeight": 12345677,
      "details": {
        "voterHash": "0xabcd1234",
        "bulletinId": "blt5678"
      }
    }
  ],
  "meta": {
    "total": 9250,
    "page": 1,
    "limit": 20
  }
}
```

#### Get Constituency Statistics
```
GET /api/constituencies/{constituency_id}/stats
```

**Description**: Retrieves hourly statistics for a specific constituency.

**Path Parameters**:
- `constituency_id` (string, required): Unique identifier of the constituency

**Query Parameters**:
- `hours` (integer, optional, default=24): Number of hours to include

**Response**: List of `HourlyStats`

```json
{
  "data": [
    {
      "hour": "2025-08-12T07:00:00Z",
      "bulletinsIssued": 500,
      "votesCast": 420,
      "transactionCount": 920,
      "bulletinVelocity": 500,
      "voteVelocity": 420
    },
    {
      "hour": "2025-08-12T08:00:00Z",
      "bulletinsIssued": 550,
      "votesCast": 480,
      "transactionCount": 1030,
      "bulletinVelocity": 550,
      "voteVelocity": 480
    }
  ],
  "meta": {
    "total": 24,
    "hours": 24
  }
}
```

### Alert Endpoints

#### List Alerts
```
GET /api/alerts
```

**Description**: Retrieves a paginated list of alerts with filtering options.

**Query Parameters**:
- `severity` (string, optional): Filter by severity (critical, warning, info)
- `status` (string, optional): Filter by status (active, investigating, resolved, snoozed)
- `limit` (integer, optional, default=20): Number of items per page
- `offset` (integer, optional, default=0): Pagination offset

**Response**: List of `Alert`

```json
{
  "data": [
    {
      "id": "alt123456",
      "constituencyId": "0x1234567890abcdef",
      "constituencyName": "Central District",
      "type": "votes_exceed_bulletins",
      "severity": "critical",
      "status": "active",
      "title": "Votes exceed bulletins issued",
      "description": "The number of votes cast (4300) exceeds the number of bulletins issued (4200)",
      "details": {
        "voteCount": 4300,
        "bulletinCount": 4200,
        "difference": 100
      },
      "createdAt": "2025-08-12T08:45:00Z",
      "detectedAt": "2025-08-12T08:44:30Z",
      "resolvedAt": null,
      "notes": []
    },
    {
      "id": "alt123455",
      "constituencyId": "0xabcdef1234567890",
      "constituencyName": "Western Heights",
      "type": "unusual_spike",
      "severity": "warning",
      "status": "investigating",
      "title": "Unusual voting velocity spike",
      "description": "Voting velocity increased by 300% in the last hour",
      "details": {
        "previousHourVelocity": 100,
        "currentHourVelocity": 400,
        "percentageIncrease": 300
      },
      "createdAt": "2025-08-12T08:30:00Z",
      "detectedAt": "2025-08-12T08:29:45Z",
      "resolvedAt": null,
      "notes": [
        "Investigating potential causes"
      ]
    }
  ],
  "meta": {
    "total": 15,
    "page": 1,
    "limit": 20
  }
}
```

#### Get Alert Detail
```
GET /api/alerts/{alert_id}
```

**Description**: Retrieves detailed information about a specific alert.

**Path Parameters**:
- `alert_id` (string, required): Unique identifier of the alert

**Response**: `Alert`

```json
{
  "id": "alt123456",
  "constituencyId": "0x1234567890abcdef",
  "constituencyName": "Central District",
  "type": "votes_exceed_bulletins",
  "severity": "critical",
  "status": "active",
  "title": "Votes exceed bulletins issued",
  "description": "The number of votes cast (4300) exceeds the number of bulletins issued (4200)",
  "details": {
    "voteCount": 4300,
    "bulletinCount": 4200,
    "difference": 100
  },
  "createdAt": "2025-08-12T08:45:00Z",
  "detectedAt": "2025-08-12T08:44:30Z",
  "resolvedAt": null,
  "notes": []
}
```

#### Update Alert Status
```
PUT /api/alerts/{alert_id}/status
```

**Description**: Updates the status of a specific alert.

**Path Parameters**:
- `alert_id` (string, required): Unique identifier of the alert

**Request Body**:
```json
{
  "status": "investigating",
  "notes": "Assigned to field team for investigation"
}
```

**Response**: Updated `Alert`

```json
{
  "id": "alt123456",
  "constituencyId": "0x1234567890abcdef",
  "constituencyName": "Central District",
  "type": "votes_exceed_bulletins",
  "severity": "critical",
  "status": "investigating",
  "title": "Votes exceed bulletins issued",
  "description": "The number of votes cast (4300) exceeds the number of bulletins issued (4200)",
  "details": {
    "voteCount": 4300,
    "bulletinCount": 4200,
    "difference": 100
  },
  "createdAt": "2025-08-12T08:45:00Z",
  "detectedAt": "2025-08-12T08:44:30Z",
  "resolvedAt": null,
  "notes": [
    "Assigned to field team for investigation"
  ]
}
```

#### Add Alert Note
```
POST /api/alerts/{alert_id}/notes
```

**Description**: Adds a note to a specific alert.

**Path Parameters**:
- `alert_id` (string, required): Unique identifier of the alert

**Request Body**:
```json
{
  "note": "Field team reports technical issue with bulletin counting"
}
```

**Response**: Updated `Alert`

```json
{
  "id": "alt123456",
  "constituencyId": "0x1234567890abcdef",
  "constituencyName": "Central District",
  "type": "votes_exceed_bulletins",
  "severity": "critical",
  "status": "investigating",
  "title": "Votes exceed bulletins issued",
  "description": "The number of votes cast (4300) exceeds the number of bulletins issued (4200)",
  "details": {
    "voteCount": 4300,
    "bulletinCount": 4200,
    "difference": 100
  },
  "createdAt": "2025-08-12T08:45:00Z",
  "detectedAt": "2025-08-12T08:44:30Z",
  "resolvedAt": null,
  "notes": [
    "Assigned to field team for investigation",
    "Field team reports technical issue with bulletin counting"
  ]
}
```

### File Processing Endpoints

#### Upload CSV File
```
POST /api/files/upload
```

**Description**: Uploads a CSV file for processing.

**Request**: `multipart/form-data` with CSV file

**Response**: Processing result with statistics

```json
{
  "filename": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv",
  "transactions_processed": 250,
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "date": "2024-09-06",
  "time_range": "0800-0900",
  "region_id": "90",
  "region_name": "Пермский край",
  "election_name": "Выборы депутатов Думы Красновишерского городского округа",
  "constituency_name": "Округ №1_3"
}
```

#### Process Directory
```
POST /api/files/process-directory
```

**Description**: Processes all CSV files in a directory.

**Request Body**:
```json
{
  "directory_path": "/path/to/data"
}
```

**Response**: Processing result with statistics

```json
{
  "files_processed": 10,
  "transactions_processed": 2500,
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "region_id": "90",
  "region_name": "Пермский край",
  "election_name": "Выборы депутатов Думы Красновишерского городского округа",
  "constituency_name": "Округ №1_3"
}
```

#### Watch Directory
```
POST /api/files/watch-directory
```

**Description**: Starts watching a directory for new files.

**Request Body**:
```json
{
  "directory_path": "/path/to/data",
  "recursive": true,
  "patterns": ["*.csv"]
}
```

**Response**: Success message

```json
{
  "message": "Started watching directory: /path/to/data",
  "recursive": true,
  "patterns": ["*.csv"]
}
```

#### Stop Watching
```
POST /api/files/stop-watching
```

**Description**: Stops watching a directory or all directories.

**Request Body**:
```json
{
  "directory_path": "/path/to/data"  // Optional, if not provided, stops all watchers
}
```

**Response**: Success message

```json
{
  "message": "Stopped watching directory: /path/to/data"
}
```

or

```json
{
  "message": "Stopped watching all directories"
}
```

#### Get Watching Directories
```
GET /api/files/watching-directories
```

**Description**: Gets a list of directories being watched.

**Response**: List of directories

```json
{
  "directories": ["/path/to/data1", "/path/to/data2"],
  "count": 2
}
```

#### Get Transaction Statistics
```
GET /api/files/statistics/{constituency_id}
```

**Description**: Gets transaction statistics for a constituency.

**Path Parameters**:
- `constituency_id` (string, required): Unique identifier of the constituency

**Response**: Transaction statistics

```json
{
  "total_transactions": 2500,
  "bulletins_issued": 1200,
  "votes_cast": 1000,
  "participation_rate": 0.83
}
```

### Health Endpoint

#### Check API Health
```
GET /api/health
```

**Description**: Checks the health status of the API and database connection.

**Response**: Health status information

```json
{
  "status": "healthy",
  "database_connection": "ok",
  "response_time": "0.66ms"
}
```

## Data Models

### Dashboard Models

#### DashboardSummary
```typescript
interface DashboardSummary {
  totalConstituencies: number;
  activeConstituencies: number;
  offlineConstituencies: number;
  totalBulletins: number;
  totalVotes: number;
  participationRate: number;
  lastUpdate: string; // ISO datetime
  criticalAlerts: number;
  warningAlerts: number;
}
```

#### RealTimeActivity
```typescript
interface RealTimeActivity {
  votesPerHour: number;
  bulletinsPerHour: number;
  activityTimeline: ActivityPoint[];
}

interface ActivityPoint {
  hour: string; // ISO datetime
  votes: number;
  bulletins: number;
}
```

### Constituency Models

#### ConstituencyOverview
```typescript
interface ConstituencyOverview {
  id: string;
  name: string;
  region: string;
  type: string; // urban, rural, suburban
  bulletinsIssued: number;
  votesCast: number;
  participationRate: number;
  status: string; // active, offline, completed
  lastActivity: string; // ISO datetime
  anomalyScore: number;
  hasAlerts: boolean;
}
```

#### ConstituencyDetail
```typescript
interface ConstituencyDetail {
  id: string;
  name: string;
  region: string;
  type: string;
  registeredVoters: number;
  bulletinsIssued: number;
  votesCast: number;
  participationRate: number;
  status: string;
  lastActivity: string; // ISO datetime
  anomalyScore: number;
  hourlyStats: HourlyStats[];
  recentTransactions: Transaction[];
  alerts: Alert[];
  comparativeMetrics: ComparativeMetrics;
}

interface ComparativeMetrics {
  vsRegionalAverage: number;
  vsHistorical: number;
  vsSimilarType: number;
}
```

### Transaction Model

```typescript
interface Transaction {
  id: string;
  constituencyId: string;
  type: string; // blindSigIssue, vote
  timestamp: string; // ISO datetime
  blockHeight: number;
  details: Record<string, any>;
}
```

### Alert Model

```typescript
interface Alert {
  id: string;
  constituencyId: string;
  constituencyName: string;
  type: string;
  severity: string; // critical, warning, info
  status: string; // active, investigating, resolved, snoozed
  title: string;
  description: string;
  details: Record<string, any>;
  createdAt: string; // ISO datetime
  detectedAt: string; // ISO datetime
  resolvedAt: string | null; // ISO datetime
  notes: string[];
}
```

### Statistics Model

```typescript
interface HourlyStats {
  hour: string; // ISO datetime
  bulletinsIssued: number;
  votesCast: number;
  transactionCount: number;
  bulletinVelocity: number;
  voteVelocity: number;
}