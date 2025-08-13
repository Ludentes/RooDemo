# File Processing System Enhancement - Verification Instructions

This document provides instructions for verifying the file processing system enhancements.

## Prerequisites

1. Python 3.8+
2. FastAPI
3. SQLAlchemy
4. Watchdog 3.0.0+
5. Access to the sample data directory

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

### 1. Folder Structure Processing

#### Test 1.1: Metadata Extraction from Folder Structure

1. Run the following command to test metadata extraction from a sample file:
   ```bash
   cd backend
   python -c "from app.services.file_service import FileService; from pathlib import Path; service = FileService(); metadata = service.extract_metadata_from_path(Path('../data/sample-data/90 - Пермский край/Выборы депутатов Думы Красновишерского городского округа/Округ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv')); print(metadata)"
   ```

2. Verify that the output contains the following information:
   - Region ID: "90"
   - Region Name: "Пермский край"
   - Election Name: "Выборы депутатов Думы Красновишерского городского округа"
   - Constituency Name: "Округ №1_3"
   - Constituency ID: "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"

#### Test 1.2: File Processing with Enhanced Metadata

1. Run the following command to test file processing with enhanced metadata:
   ```bash
   cd backend
   python -c "from app.services.file_service import FileService; from pathlib import Path; service = FileService(); result, transactions = service.process_file(Path('../data/sample-data/90 - Пермский край/Выборы депутатов Думы Красновишерского городского округа/Округ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv')); print(result)"
   ```

2. Verify that the output contains the following information:
   - Filename: "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
   - Transactions Processed: > 0
   - Constituency ID: "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
   - Date: "2024-09-06"
   - Time Range: "0800-0900"
   - Region ID: "90"
   - Region Name: "Пермский край"
   - Election Name: "Выборы депутатов Думы Красновишерского городского округа"
   - Constituency Name: "Округ №1_3"

#### Test 1.3: Directory Processing with Enhanced Metadata

1. Run the following command to test directory processing with enhanced metadata:
   ```bash
   cd backend
   python -c "from app.services.file_service import FileService; service = FileService(); result, transactions = service.process_directory('../data/sample-data/90 - Пермский край/Выборы депутатов Думы Красновишерского городского округа/Округ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900'); print(result)"
   ```

2. Verify that the output contains the following information:
   - Files Processed: > 0
   - Transactions Processed: > 0
   - Constituency ID: "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
   - Region ID: "90"
   - Region Name: "Пермский край"
   - Election Name: "Выборы депутатов Думы Красновишерского городского округа"
   - Constituency Name: "Округ №1_3"

#### Test 1.4: API Endpoint for File Upload

1. Use the Swagger UI at http://localhost:8000/docs to test the file upload endpoint.
2. Upload a sample CSV file from the data directory.
3. Verify that the response contains the enhanced metadata.
4. Check the database to ensure that the region, election, and constituency records were created or updated.

#### Test 1.5: API Endpoint for Directory Processing

1. Use the Swagger UI at http://localhost:8000/docs to test the directory processing endpoint.
2. Enter the path to a sample directory from the data directory.
3. Verify that the response contains the enhanced metadata.
4. Check the database to ensure that the region, election, and constituency records were created or updated.

### 2. Code Refactoring

#### Test 2.1: Code Quality

1. Run the following command to check code quality:
   ```bash
   cd backend
   flake8 app/services/file_service.py app/services/transaction_service.py app/api/routes/files.py
   ```

2. Verify that there are no linting errors or warnings.

#### Test 2.2: Unit Tests

1. Run the following command to run unit tests:
   ```bash
   cd backend
   pytest tests/services/test_file_service.py tests/services/test_transaction_service.py
   ```

2. Verify that all tests pass.

### 3. File Watching

#### Test 3.1: File Watcher Service

1. Run the following command to test the file watcher service:
   ```bash
   cd backend
   python -c "from app.services.file_watcher_service import FileWatcherService; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); watcher = FileWatcherService.get_instance('../data/sample-data', db); watcher.start(); import time; time.sleep(5); watcher.stop()"
   ```

2. Verify that the watcher starts and stops without errors.

#### Test 3.2: File Creation Event

1. Start the file watcher service:
   ```bash
   cd backend
   python -c "from app.services.file_watcher_service import FileWatcherService; from sqlalchemy.orm import Session; from app.models.database import SessionLocal; db = SessionLocal(); watcher = FileWatcherService.get_instance('../data/sample-data', db); watcher.start(); print('Watcher started. Press Ctrl+C to stop.'); input()"
   ```

2. In another terminal, copy a sample CSV file to the watched directory:
   ```bash
   cp data/sample-data/90\ -\ Пермский\ край/Выборы\ депутатов\ Думы\ Красновишерского\ городского\ округа/Округ\ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv data/sample-data/90\ -\ Пермский\ край/Выборы\ депутатов\ Думы\ Красновишерского\ городского\ округа/Округ\ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/test.csv
   ```

3. Verify that the file watcher detects the new file and processes it.
4. Check the database to ensure that the transactions were saved.

#### Test 3.3: API Endpoints for File Watching

1. Use the Swagger UI at http://localhost:8000/docs to test the watch-directory endpoint.
2. Enter the path to a sample directory from the data directory.
3. Verify that the response indicates that the directory is being watched.
4. Copy a sample CSV file to the watched directory.
5. Verify that the file is processed automatically.
6. Use the Swagger UI to test the stop-watching endpoint.
7. Verify that the response indicates that the directory is no longer being watched.
8. Copy another sample CSV file to the directory.
9. Verify that the file is not processed automatically.

## Verification Checklist

- [x] Folder structure metadata extraction works correctly
- [x] File processing with enhanced metadata works correctly
- [x] Directory processing with enhanced metadata works correctly
- [x] API endpoints for file upload and directory processing work correctly
- [x] Region, election, and constituency records are created or updated correctly
- [x] Code quality meets standards
- [x] All unit tests pass
- [x] File watcher service works correctly
- [x] File creation events are detected and processed
- [x] API endpoints for file watching work correctly

## Troubleshooting

### Issue 1: Database Migration Errors

If you encounter database migration errors, try the following:
1. Delete the database file: `rm backend/election_monitoring.db`
2. Run the migrations again: `cd backend && python run_migrations.py`
3. Seed the database: `cd backend && python scripts/seed_db.py`

### Issue 2: File Watcher Errors

If you encounter file watcher errors, try the following:
1. Check that the watchdog package is installed: `pip install watchdog`
2. Check that the directory path is correct and accessible
3. Check the logs for error messages
4. Restart the application

### Issue 3: API Endpoint Errors

If you encounter API endpoint errors, try the following:
1. Check that the FastAPI application is running
2. Check that the request parameters are correct
3. Check the logs for error messages
4. Restart the application