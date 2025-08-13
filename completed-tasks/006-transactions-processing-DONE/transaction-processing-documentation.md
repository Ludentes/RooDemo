# Transaction Processing System Documentation

## Overview

The Transaction Processing System is a core component of the Election Monitoring System that handles blockchain transaction data. It provides functionality for validating, processing, storing, and querying transaction data from various sources, including file uploads, API submissions, and batch processing.

## Key Components

### 1. Transaction Model

The Transaction model represents blockchain transaction data in the system. It includes the following key fields:

- `id`: Unique identifier for the transaction
- `constituency_id`: ID of the constituency this transaction belongs to
- `block_height`: Blockchain block height
- `timestamp`: Transaction timestamp
- `type`: Transaction type (blindSigIssue, vote)
- `raw_data`: Raw transaction data
- `operation_data`: Processed operation data
- `status`: Transaction status (pending, processed, failed)
- `anomaly_detected`: Whether an anomaly was detected
- `anomaly_reason`: Reason for the anomaly
- `source`: Source of the transaction (file_upload, api, batch)
- `file_id`: ID of the file that contained this transaction

### 2. Transaction Schemas

The Transaction schemas define the data structures used for creating, updating, and retrieving transaction data. The key schemas include:

- `TransactionBase`: Base schema with common fields
- `TransactionCreate`: Schema for creating a new transaction
- `TransactionUpdate`: Schema for updating an existing transaction
- `TransactionResponse`: Schema for returning a transaction in API responses
- `TransactionList`: Schema for returning a list of transactions
- `TransactionStats`: Schema for transaction statistics
- `TransactionQueryParams`: Schema for transaction query parameters
- `TransactionBatchRequest`: Schema for batch transaction requests
- `TransactionBatchResponse`: Schema for batch transaction responses

### 3. Transaction CRUD Operations

The Transaction CRUD operations provide basic database operations for transactions:

- `create`: Create a new transaction
- `get`: Get a transaction by ID
- `update`: Update a transaction
- `remove`: Delete a transaction
- `get_by_constituency`: Get transactions for a constituency
- `get_transactions_with_filters`: Get transactions with filtering and pagination
- `create_batch`: Create multiple transactions in a batch

### 4. Transaction Validator

The Transaction Validator provides validation for transaction data:

- `validate_transaction`: Validate a single transaction
- `validate_transaction_batch`: Validate a batch of transactions
- `check_duplicate`: Check if a transaction already exists

### 5. Transaction Service

The Transaction Service provides high-level operations for transactions:

- `save_transactions`: Save transactions to the database
- `update_constituency_metrics`: Update constituency metrics based on transactions
- `get_transaction_statistics`: Get transaction statistics for a constituency
- `get_transaction`: Get a transaction by ID
- `create_transaction`: Create a new transaction
- `update_transaction`: Update a transaction
- `delete_transaction`: Delete a transaction
- `get_transactions`: Get transactions with filtering and pagination
- `process_transaction_batch`: Process a batch of transactions

### 6. Transaction Batch Processor

The Transaction Batch Processor provides functionality for processing transactions in batches:

- `process_batch`: Process a batch of transactions
- `split_into_batches`: Split transactions into batches
- `process_large_batch`: Process a large batch of transactions
- `process_batch_async`: Process a batch of transactions asynchronously
- `process_large_batch_async`: Process a large batch of transactions asynchronously
- `process_batch_request`: Process a batch request

### 7. Transaction Query Service

The Transaction Query Service provides advanced query capabilities for transaction data:

- `build_query`: Build a query for transactions
- `execute_query`: Execute a query with pagination
- `get_transaction_counts_by_hour`: Get transaction counts by hour
- `get_transaction_counts_by_day`: Get transaction counts by day
- `get_transaction_counts_by_type`: Get transaction counts by type
- `get_transaction_counts_by_status`: Get transaction counts by status
- `get_transaction_counts_by_source`: Get transaction counts by source
- `get_transaction_rate`: Get transaction rate (transactions per hour)
- `get_anomaly_statistics`: Get statistics about anomalies
- `get_transaction_statistics`: Get comprehensive transaction statistics
- `search_transactions`: Search for transactions

### 8. Transaction API

The Transaction API provides RESTful endpoints for transaction operations:

- `GET /transactions`: List transactions with filtering and pagination
- `GET /transactions/{transaction_id}`: Get a specific transaction
- `POST /transactions`: Create a new transaction
- `PUT /transactions/{transaction_id}`: Update a transaction
- `DELETE /transactions/{transaction_id}`: Delete a transaction
- `POST /transactions/batch`: Process a batch of transactions
- `GET /transactions/statistics`: Get transaction statistics
- `GET /transactions/search`: Search for transactions

## Integration Points

### 1. File Processing Integration

The Transaction Processing System integrates with the File Processing System to process transaction data from files:

- File upload endpoint uses the Transaction Batch Processor to process transactions from uploaded files
- Directory processing endpoint uses the Transaction Batch Processor to process transactions from all files in a directory
- File watcher service uses the Transaction Batch Processor to process transactions from new files

### 2. Dashboard Integration

The Transaction Processing System integrates with the Dashboard to provide transaction statistics:

- Dashboard summary endpoint includes transaction statistics
- Detailed dashboard summary endpoint includes comprehensive transaction statistics
- Transaction statistics endpoint provides transaction-specific statistics

## Usage Examples

### 1. Creating a Transaction

```python
from app.models.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService

# Create transaction data
transaction_data = TransactionCreate(
    constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
    block_height=104,
    timestamp=datetime.utcnow(),
    type="blindSigIssue",
    raw_data={"key": "operation", "stringValue": "blindSigIssue"},
    operation_data={"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
    status="processed",
    source="api"
)

# Create transaction
transaction_service = TransactionService(db)
transaction = transaction_service.create_transaction(transaction_data)
```

### 2. Processing a Batch of Transactions

```python
from app.models.schemas.transaction import TransactionCreate, TransactionBatchRequest
from app.services.transaction_batch_processor import TransactionBatchProcessor

# Create batch request
batch_request = TransactionBatchRequest(
    transactions=[
        TransactionCreate(...),
        TransactionCreate(...),
        ...
    ]
)

# Process batch
batch_processor = TransactionBatchProcessor(db)
result = batch_processor.process_batch_request(batch_request)
```

### 3. Querying Transactions

```python
from app.services.transaction_query_service import TransactionQueryService

# Create query service
query_service = TransactionQueryService(db)

# Get transaction statistics
stats = query_service.get_transaction_statistics()

# Search for transactions
transactions, total = query_service.search_transactions("blindSigIssue")
```

## Error Handling

The Transaction Processing System includes custom exceptions for error handling:

- `TransactionValidationError`: Raised when transaction validation fails
- `TransactionCreateError`: Raised when transaction creation fails
- `TransactionUpdateError`: Raised when transaction update fails
- `TransactionDeleteError`: Raised when transaction deletion fails
- `BatchProcessingError`: Raised when batch processing fails
- `TransactionSaveError`: Raised when saving transactions fails
- `MetricsUpdateError`: Raised when updating constituency metrics fails

## Testing

The Transaction Processing System includes comprehensive tests:

- Unit tests for all components
- API tests for all endpoints
- End-to-end tests for the complete system

## Future Enhancements

Potential future enhancements for the Transaction Processing System:

1. **Real-time Processing**: Implement real-time processing of transactions using WebSockets or Server-Sent Events
2. **Advanced Anomaly Detection**: Enhance anomaly detection with machine learning algorithms
3. **Transaction Replay**: Add functionality to replay transactions for debugging and analysis
4. **Transaction Versioning**: Implement versioning for transactions to track changes
5. **Transaction Approval Workflow**: Add approval workflow for transactions that require manual review