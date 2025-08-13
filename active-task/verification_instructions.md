# Transaction Processing System - Verification Instructions

This document provides instructions for verifying the Transaction Processing System implementation.

## Prerequisites

1. Python 3.8+
2. FastAPI
3. SQLAlchemy
4. Access to the Election Monitoring System codebase

## Setup

1. Install the required dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Apply database migrations:
   ```bash
   cd backend
   python run_migrations.py
   ```

3. Start the FastAPI application:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## Verification Tests

### 1. Transaction Validator

#### Test 1.1: Validator Initialization

1. Run the following command to test the Transaction Validator initialization:
   ```bash
   cd backend
   python -c "from app.services.transaction_validator import TransactionValidator; validator = TransactionValidator(); print('Transaction Validator initialized successfully')"
   ```

2. Verify that the output shows "Transaction Validator initialized successfully" without any errors.

#### Test 1.2: Transaction Validation

1. Run the following command to test transaction validation:
   ```bash
   cd backend
   python -c "from app.services.transaction_validator import TransactionValidator; from app.models.schemas.transaction import TransactionCreate; from datetime import datetime; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; validator = TransactionValidator(); db = SessionLocal(); transaction = TransactionCreate(constituency_id='AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM', block_height=104, timestamp=datetime.utcnow(), type='blindSigIssue', raw_data={'key': 'operation', 'stringValue': 'blindSigIssue'}, operation_data={'key': 'BLINDSIG_TEST'}, status='processed', source='api'); errors = validator.validate_transaction(db, transaction); print(f'Validation errors: {errors}')"
   ```

2. Verify that the output shows an empty list of validation errors or specific errors if the constituency doesn't exist.

### 2. Transaction Batch Processor

#### Test 2.1: Batch Processor Initialization

1. Run the following command to test the Transaction Batch Processor initialization:
   ```bash
   cd backend
   python -c "from app.services.transaction_batch_processor import TransactionBatchProcessor; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); processor = TransactionBatchProcessor(db); print('Transaction Batch Processor initialized successfully')"
   ```

2. Verify that the output shows "Transaction Batch Processor initialized successfully" without any errors.

#### Test 2.2: Batch Processing

1. Run the following command to test batch processing:
   ```bash
   cd backend
   python -c "from app.services.transaction_batch_processor import TransactionBatchProcessor; from app.models.schemas.transaction import TransactionCreate, TransactionBatchRequest; from datetime import datetime; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); processor = TransactionBatchProcessor(db); transaction1 = TransactionCreate(constituency_id='AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM', block_height=104, timestamp=datetime.utcnow(), type='blindSigIssue', raw_data={'key': 'operation', 'stringValue': 'blindSigIssue'}, operation_data={'key': 'BLINDSIG_TEST1'}, status='processed', source='batch'); transaction2 = TransactionCreate(constituency_id='AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM', block_height=105, timestamp=datetime.utcnow(), type='blindSigIssue', raw_data={'key': 'operation', 'stringValue': 'blindSigIssue'}, operation_data={'key': 'BLINDSIG_TEST2'}, status='processed', source='batch'); batch_request = TransactionBatchRequest(transactions=[transaction1, transaction2]); try: result = processor.process_batch_request(batch_request); print(f'Batch processing result: {result}'); except Exception as e: print(f'Error: {e}')"
   ```

2. Verify that the output shows a successful batch processing result or specific errors if the constituencies don't exist.

### 3. Transaction Query Service

#### Test 3.1: Query Service Initialization

1. Run the following command to test the Transaction Query Service initialization:
   ```bash
   cd backend
   python -c "from app.services.transaction_query_service import TransactionQueryService; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); query_service = TransactionQueryService(db); print('Transaction Query Service initialized successfully')"
   ```

2. Verify that the output shows "Transaction Query Service initialized successfully" without any errors.

#### Test 3.2: Transaction Statistics

1. Run the following command to test transaction statistics:
   ```bash
   cd backend
   python -c "from app.services.transaction_query_service import TransactionQueryService; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); query_service = TransactionQueryService(db); stats = query_service.get_transaction_statistics(); print(f'Transaction statistics: {stats}')"
   ```

2. Verify that the output shows transaction statistics without any errors.

### 4. Transaction API

#### Test 4.1: List Transactions

1. Use the Swagger UI at http://localhost:8000/docs to test the list transactions endpoint.
2. Navigate to the `/api/transactions` GET endpoint.
3. Execute the request without any parameters.
4. Verify that the response contains a list of transactions with pagination information.

#### Test 4.2: Create Transaction

1. Use the Swagger UI at http://localhost:8000/docs to test the create transaction endpoint.
2. Navigate to the `/api/transactions` POST endpoint.
3. Enter the following JSON in the request body:
   ```json
   {
     "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
     "block_height": 104,
     "timestamp": "2024-09-06T08:30:28.819Z",
     "type": "blindSigIssue",
     "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
     "operation_data": {"key": "BLINDSIG_TEST_API"},
     "status": "processed",
     "source": "api"
   }
   ```
4. Execute the request.
5. Verify that the response contains the created transaction with an ID.

#### Test 4.3: Batch Processing

1. Use the Swagger UI at http://localhost:8000/docs to test the batch processing endpoint.
2. Navigate to the `/api/transactions/batch` POST endpoint.
3. Enter the following JSON in the request body:
   ```json
   {
     "transactions": [
       {
         "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
         "block_height": 104,
         "timestamp": "2024-09-06T08:30:28.819Z",
         "type": "blindSigIssue",
         "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
         "operation_data": {"key": "BLINDSIG_BATCH_1"},
         "status": "processed",
         "source": "batch"
       },
       {
         "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
         "block_height": 105,
         "timestamp": "2024-09-06T08:35:12.456Z",
         "type": "blindSigIssue",
         "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
         "operation_data": {"key": "BLINDSIG_BATCH_2"},
         "status": "processed",
         "source": "batch"
       }
     ]
   }
   ```
4. Execute the request.
5. Verify that the response indicates successful batch processing.

#### Test 4.4: Transaction Statistics

1. Use the Swagger UI at http://localhost:8000/docs to test the transaction statistics endpoint.
2. Navigate to the `/api/transactions/statistics` GET endpoint.
3. Execute the request.
4. Verify that the response contains transaction statistics.

### 5. File Processing Integration

#### Test 5.1: File Upload with Transaction Batch Processing

1. Use the Swagger UI at http://localhost:8000/docs to test the file upload endpoint.
2. Navigate to the `/api/files/upload` POST endpoint.
3. Upload a sample CSV file containing transaction data.
4. Verify that the response indicates successful processing and includes the number of transactions processed.

#### Test 5.2: Directory Processing with Transaction Batch Processing

1. Use the Swagger UI at http://localhost:8000/docs to test the directory processing endpoint.
2. Navigate to the `/api/files/process-directory` POST endpoint.
3. Enter the path to a directory containing CSV files with transaction data.
4. Verify that the response indicates successful processing and includes the number of transactions processed.

### 6. Dashboard Integration

#### Test 6.1: Dashboard Summary with Transaction Statistics

1. Use the Swagger UI at http://localhost:8000/docs to test the dashboard summary endpoint.
2. Navigate to the `/api/dashboard/summary` GET endpoint.
3. Execute the request.
4. Verify that the response includes transaction statistics.

#### Test 6.2: Detailed Dashboard Summary

1. Use the Swagger UI at http://localhost:8000/docs to test the detailed dashboard summary endpoint.
2. Navigate to the `/api/dashboard/detailed-summary` GET endpoint.
3. Execute the request.
4. Verify that the response includes detailed transaction statistics.

#### Test 6.3: Transaction Statistics from Dashboard

1. Use the Swagger UI at http://localhost:8000/docs to test the transaction statistics endpoint.
2. Navigate to the `/api/dashboard/transaction-stats` GET endpoint.
3. Execute the request.
4. Verify that the response includes transaction statistics.

## Verification Checklist

- [ ] Transaction Validator initializes without errors
- [ ] Transaction validation works correctly
- [ ] Transaction Batch Processor initializes without errors
- [ ] Batch processing works correctly
- [ ] Transaction Query Service initializes without errors
- [ ] Transaction statistics are generated correctly
- [ ] Transaction API endpoints work correctly
- [ ] File Processing integration works correctly
- [ ] Dashboard integration works correctly
- [ ] No circular import errors occur during testing

## Troubleshooting

### Issue 1: Circular Import Errors

If you encounter circular import errors, check the following files for potential circular dependencies:

1. `backend/app/services/__init__.py`
2. `backend/app/services/transaction_service.py`
3. `backend/app/services/transaction_validator.py`
4. `backend/app/services/transaction_batch_processor.py`
5. `backend/app/services/transaction_query_service.py`
6. `backend/app/api/dependencies.py`
7. `backend/app/api/routes/transactions.py`
8. `backend/app/api/routes/files.py`
9. `backend/app/services/file_watcher_service.py`
10. `backend/app/services/dashboard.py`

Common solutions for circular import issues:

1. Move imports inside functions or methods instead of at the module level.
2. Create a separate module for shared functionality.
3. Use dependency injection instead of direct imports.
4. Restructure the code to avoid circular dependencies.

### Issue 2: Database Errors

If you encounter database errors, try the following:

1. Delete the database file: `rm backend/election_monitoring.db`
2. Run the migrations again: `cd backend && python run_migrations.py`
3. Seed the database: `cd backend && python scripts/seed_db.py`

### Issue 3: API Endpoint Errors

If you encounter API endpoint errors, try the following:

1. Check that the FastAPI application is running.
2. Check that the request parameters are correct.
3. Check the logs for error messages.
4. Restart the application.