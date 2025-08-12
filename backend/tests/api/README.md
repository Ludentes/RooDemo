# API End-to-End Tests

This directory contains end-to-end tests for the Election Monitoring System API. These tests verify the complete flow from API requests to database storage and metrics updates.

## File Processing System Tests

The `test_files.py` file contains end-to-end tests for the File Processing System, which is responsible for:

1. Uploading CSV files via the API
2. Extracting transactions from the files
3. Storing transactions in the database
4. Updating constituency metrics based on the transactions
5. Providing transaction statistics

## Running the Tests

To run the end-to-end tests, use the provided script:

```bash
cd backend
python run_e2e_tests.py
```

This script will:

1. Set up an in-memory test database
2. Start the FastAPI application
3. Run the end-to-end tests
4. Clean up the test environment

## Test Data

The tests use sample CSV files from the `data/sample-data/` directory. These files contain real transaction data that can be used to test the File Processing System.

## Adding New Tests

To add new end-to-end tests:

1. Add a new test function to `test_files.py`
2. Use the `@pytest.mark.integration` decorator to mark it as an integration test
3. Use the `client` fixture to make API requests
4. Use the `clean_db` fixture to get a clean database session
5. Add assertions to verify the expected behavior

## Troubleshooting

If the tests are failing, check the following:

1. Make sure the sample CSV files exist in the `data/sample-data/` directory
2. Make sure the test database is being set up correctly
3. Check the API server logs for any errors
4. Make sure the test fixtures are being used correctly

For more detailed information, see the [End-to-End Testing Documentation](../../docs/end_to_end_testing.md).