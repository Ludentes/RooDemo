# Transaction API Documentation

## Overview

The Transaction API provides RESTful endpoints for managing blockchain transaction data in the Election Monitoring System. It allows for creating, retrieving, updating, and deleting transactions, as well as batch processing, statistics, and search functionality.

## Base URL

All API endpoints are relative to the base URL:

```
/api/transactions
```

## Authentication

Authentication will be added in a future update.

## Endpoints

### List Transactions

Retrieves a paginated list of transactions with optional filtering.

**URL**: `/`

**Method**: `GET`

**Query Parameters**:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| constituency_id | string | Filter by constituency ID | None |
| transaction_type | string | Filter by transaction type | None |
| start_time | datetime | Filter by start time | None |
| end_time | datetime | Filter by end time | None |
| status | string | Filter by status | None |
| anomaly_detected | boolean | Filter by anomaly detection | None |
| source | string | Filter by source | None |
| file_id | string | Filter by file ID | None |
| page | integer | Page number | 1 |
| limit | integer | Items per page | 100 |
| sort_by | string | Field to sort by | "timestamp" |
| sort_order | string | Sort order (asc, desc) | "desc" |

**Response**:

```json
{
  "data": [
    {
      "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
      "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
      "block_height": 104,
      "timestamp": "2024-09-06T08:30:28.819Z",
      "type": "blindSigIssue",
      "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
      "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
      "status": "processed",
      "anomaly_detected": false,
      "anomaly_reason": null,
      "source": "api",
      "file_id": null,
      "created_at": "2024-09-06T08:30:28.819Z",
      "updated_at": "2024-09-06T08:30:28.819Z"
    },
    // More transactions...
  ],
  "total": 150,
  "page": 1,
  "limit": 100
}
```

### Get Transaction

Retrieves a specific transaction by ID.

**URL**: `/{transaction_id}`

**Method**: `GET`

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| transaction_id | string | ID of the transaction to retrieve |

**Response**:

```json
{
  "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "block_height": 104,
  "timestamp": "2024-09-06T08:30:28.819Z",
  "type": "blindSigIssue",
  "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
  "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
  "status": "processed",
  "anomaly_detected": false,
  "anomaly_reason": null,
  "source": "api",
  "file_id": null,
  "created_at": "2024-09-06T08:30:28.819Z",
  "updated_at": "2024-09-06T08:30:28.819Z"
}
```

**Error Responses**:

- `404 Not Found`: Transaction not found

### Create Transaction

Creates a new transaction.

**URL**: `/`

**Method**: `POST`

**Request Body**:

```json
{
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "block_height": 104,
  "timestamp": "2024-09-06T08:30:28.819Z",
  "type": "blindSigIssue",
  "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
  "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
  "status": "processed",
  "anomaly_detected": false,
  "anomaly_reason": null,
  "source": "api",
  "file_id": null
}
```

**Response**:

```json
{
  "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "block_height": 104,
  "timestamp": "2024-09-06T08:30:28.819Z",
  "type": "blindSigIssue",
  "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
  "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
  "status": "processed",
  "anomaly_detected": false,
  "anomaly_reason": null,
  "source": "api",
  "file_id": null,
  "created_at": "2024-09-06T08:30:28.819Z",
  "updated_at": "2024-09-06T08:30:28.819Z"
}
```

**Error Responses**:

- `400 Bad Request`: Validation error
- `500 Internal Server Error`: Creation error

### Update Transaction

Updates an existing transaction.

**URL**: `/{transaction_id}`

**Method**: `PUT`

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| transaction_id | string | ID of the transaction to update |

**Request Body**:

```json
{
  "status": "failed",
  "anomaly_detected": true,
  "anomaly_reason": "Invalid signature"
}
```

**Response**:

```json
{
  "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
  "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
  "block_height": 104,
  "timestamp": "2024-09-06T08:30:28.819Z",
  "type": "blindSigIssue",
  "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
  "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
  "status": "failed",
  "anomaly_detected": true,
  "anomaly_reason": "Invalid signature",
  "source": "api",
  "file_id": null,
  "created_at": "2024-09-06T08:30:28.819Z",
  "updated_at": "2024-09-06T08:35:12.456Z"
}
```

**Error Responses**:

- `404 Not Found`: Transaction not found
- `500 Internal Server Error`: Update error

### Delete Transaction

Deletes a transaction.

**URL**: `/{transaction_id}`

**Method**: `DELETE`

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| transaction_id | string | ID of the transaction to delete |

**Response**:

- `204 No Content`: Transaction deleted successfully

**Error Responses**:

- `404 Not Found`: Transaction not found
- `500 Internal Server Error`: Deletion error

### Process Batch

Processes a batch of transactions.

**URL**: `/batch`

**Method**: `POST`

**Request Body**:

```json
{
  "transactions": [
    {
      "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
      "block_height": 104,
      "timestamp": "2024-09-06T08:30:28.819Z",
      "type": "blindSigIssue",
      "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
      "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
      "status": "processed",
      "source": "batch"
    },
    // More transactions...
  ]
}
```

**Response**:

```json
{
  "success": true,
  "processed": 2,
  "failed": 0,
  "errors": []
}
```

**Error Responses**:

- `500 Internal Server Error`: Batch processing error

### Get Statistics

Retrieves transaction statistics.

**URL**: `/statistics`

**Method**: `GET`

**Response**:

```json
{
  "total_transactions": 350,
  "total_bulletins": 200,
  "total_votes": 150,
  "transactions_per_hour": 15.0,
  "bulletins_per_hour": 8.5,
  "votes_per_hour": 6.5,
  "counts_by_type": {
    "blindSigIssue": 200,
    "vote": 150
  },
  "counts_by_status": {
    "processed": 300,
    "failed": 50
  },
  "counts_by_source": {
    "file_upload": 250,
    "api": 100
  },
  "anomalies": {
    "total_transactions": 350,
    "anomaly_count": 20,
    "anomaly_percentage": 5.7,
    "anomaly_reasons": {
      "Invalid signature": 12,
      "Duplicate vote": 8
    }
  }
}
```

### Search Transactions

Searches for transactions.

**URL**: `/search`

**Method**: `GET`

**Query Parameters**:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| q | string | Search term | Required |
| page | integer | Page number | 1 |
| limit | integer | Items per page | 100 |

**Response**:

```json
{
  "data": [
    {
      "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
      "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
      "block_height": 104,
      "timestamp": "2024-09-06T08:30:28.819Z",
      "type": "blindSigIssue",
      "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
      "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
      "status": "processed",
      "anomaly_detected": false,
      "anomaly_reason": null,
      "source": "api",
      "file_id": null,
      "created_at": "2024-09-06T08:30:28.819Z",
      "updated_at": "2024-09-06T08:30:28.819Z"
    },
    // More transactions...
  ],
  "total": 5,
  "page": 1,
  "limit": 100
}
```

## Data Models

### Transaction

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string | Unique identifier for the transaction | Auto-generated |
| constituency_id | string | ID of the constituency this transaction belongs to | Yes |
| block_height | integer | Blockchain block height | Yes |
| timestamp | datetime | Transaction timestamp | Yes |
| type | string | Transaction type (blindSigIssue, vote) | Yes |
| raw_data | object | Raw transaction data | Yes |
| operation_data | object | Processed operation data | No |
| status | string | Transaction status (pending, processed, failed) | Yes |
| anomaly_detected | boolean | Whether an anomaly was detected | Yes |
| anomaly_reason | string | Reason for the anomaly | No |
| source | string | Source of the transaction (file_upload, api, batch) | No |
| file_id | string | ID of the file that contained this transaction | No |
| created_at | datetime | Creation timestamp | Auto-generated |
| updated_at | datetime | Last update timestamp | Auto-generated |

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request was successful
- `201 Created`: The resource was successfully created
- `204 No Content`: The request was successful but there is no content to return
- `400 Bad Request`: The request was invalid or cannot be served
- `404 Not Found`: The requested resource does not exist
- `500 Internal Server Error`: An error occurred on the server

Error responses include a detail message explaining the error:

```json
{
  "detail": "Transaction with ID 65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS not found"
}
```

## Rate Limiting

Rate limiting will be added in a future update.

## Versioning

API versioning will be added in a future update.