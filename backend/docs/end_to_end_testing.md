# End-to-End Testing for the File Processing System

This document provides a comprehensive guide on how to perform end-to-end testing for the File Processing System, which tests the complete flow from file upload API to database storage and metrics updates.

## What is End-to-End Testing?

End-to-end (E2E) testing is a methodology used to test whether the flow of an application is performing as designed from start to finish. The purpose of carrying out end-to-end tests is to identify system dependencies and to ensure that the right information is passed between various system components and systems.

For the File Processing System, end-to-end testing involves:

1. Uploading CSV files via the API
2. Verifying that transactions are extracted correctly
3. Verifying that transactions are stored in the database
4. Verifying that constituency metrics are updated correctly
5. Verifying that transaction statistics can be retrieved

## Test Environment Setup

The end-to-end tests use an in-memory SQLite database to avoid affecting the production data. This ensures that tests are isolated and can be run without any side effects on the production database. The test environment is set up as follows:

1. An in-memory SQLite database is created for testing
2. The database schema is created in the in-memory database
3. The FastAPI application is started with the test database
4. Test data (constituencies, etc.) is created in the database
5. The tests are run against the running API
6. The in-memory database is automatically cleaned up when the tests finish

## Running the End-to-End Tests

To run the end-to-end tests, use the provided script:

```bash
cd backend
python run_e2e_tests.py
```

This script will:

1. Set up the test database
2. Start the FastAPI application
3. Run the end-to-end tests
4. Clean up the test environment

Alternatively, you can run the tests manually:

```bash
cd backend
# Set the TESTING environment variable
export TESTING=1

# Start the FastAPI application with the test database
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait for the server to start
sleep 2

# Run the tests
python -m pytest -xvs tests/api/test_files.py -m integration

# Clean up
kill $SERVER_PID  # Kill the FastAPI application
```

## Test Data

The end-to-end tests use sample CSV files from the `data/sample-data/` directory. These files contain real transaction data that can be used to test the File Processing System.

The main sample file used is:
- `data/sample-data/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv`

The tests use relative paths to locate these files, so they should work regardless of where the project is located on your system.

This file contains a mix of `blindSigIssue` and `vote` transactions, which are used to test the complete flow of the File Processing System.

## Interpreting Test Results

The end-to-end tests will output detailed information about each test case, including:

- The HTTP status code of each API request
- The response body of each API request
- The number of transactions processed
- The constituency metrics after processing

A successful test run will show all tests passing with no errors. If a test fails, the output will show the specific assertion that failed and the expected vs. actual values.

## Adding New End-to-End Tests

To add new end-to-end tests, follow these steps:

1. Add a new test function to `tests/api/test_files.py`
2. Use the `@pytest.mark.integration` decorator to mark it as an integration test
3. Use the `client` fixture to make API requests
4. Use the `clean_db` fixture to get a clean database session
5. Add assertions to verify the expected behavior

Example:

```python
@pytest.mark.integration
def test_new_feature(client, clean_db):
    """Test a new feature."""
    # Make API requests
    response = client.post("/api/files/new-feature", json={"param": "value"})
    
    # Check response
    assert response.status_code == 200
    
    # Verify database changes
    db_session = clean_db
    # Query the database and make assertions
    
    # Verify API behavior
    response = client.get("/api/files/result")
    assert response.status_code == 200
    assert response.json()["result"] == "expected"
```

## Common Issues and Troubleshooting

### Test Database Not Clean

If tests are failing because the database is not in the expected state, make sure you're using the `clean_db` fixture in your test function. This fixture ensures that the database is clean before each test.

Since the tests use an in-memory database, each test run starts with a fresh database. However, within a single test run, the `clean_db` fixture is used to ensure that each test function starts with a clean database state.

### API Server Not Starting

If the API server fails to start, check the following:

1. Make sure no other process is using port 8000
2. Make sure the `TESTING` environment variable is set to `1`
3. Check the server logs for any errors

### File Not Found

If tests are failing because a file is not found, make sure the file paths in the tests are correct. The tests use relative paths from the project root directory to locate the sample files. If you've moved the sample files or the project structure has changed, you may need to update the paths in the tests.

The sample files should be located at:
```
data/sample-data/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
```

### Metadata Extraction Error

If tests are failing with a "Failed to extract metadata from filename" error, it might be because the file service is trying to extract metadata from a temporary file with a random name. The file service expects filenames in the format `[SmartContractID]_[Date]_[TimeRange].csv`.

To fix this issue, we've modified the `process_file` method in the `FileService` class to accept an optional `original_filename` parameter. When uploading files via the API, we pass the original filename to the `process_file` method, which uses it for metadata extraction.

### Data Type Mismatch

If tests are failing with a "Failed to save transactions" error and a validation error about `raw_data` or `operation_data` not being valid dictionaries, it might be because the `_parse_json_like_structure` method returns lists of dictionaries, but the `TransactionData` class expects these fields to be dictionaries.

To fix this issue, we've modified the `extract_transactions_from_csv` method to convert the lists to dictionaries before passing them to the `TransactionData` constructor. The conversion uses the `key` field of each item in the list as the dictionary key.

### Database Sharing Issue

If tests are failing with a "Constituency not found" error when trying to update constituency metrics, it might be because the in-memory SQLite database created in the main process isn't accessible to the API server running in a separate process.

To fix this issue, we've modified the `run_e2e_tests.py` script to use a file-based SQLite database instead of an in-memory database, so that both processes can access the same database. The script creates a temporary database file, uses it for testing, and then removes it when the tests are done.

### Test Data Creation Issue

If tests are still failing with a "Constituency not found" error even after switching to a file-based database, it might be because the test data (election and constituency) is not being created in the database before the API server is started.

To fix this issue, we've added a `create_test_data` function to the `run_e2e_tests.py` script that creates the test data directly in the database before starting the API server. This ensures that the constituency exists in the database when the API tries to update its metrics.

## Conclusion

End-to-end testing is a crucial part of ensuring that the File Processing System works correctly from start to finish. By following the guidelines in this document, you can run the existing end-to-end tests and add new ones to test additional functionality.