# End-to-End Tests for the Election Monitoring API

This directory contains end-to-end (E2E) tests for the Election Monitoring API. These tests are designed to test the API endpoints in a real-world scenario, with a running server and a test database.

## What are E2E Tests?

End-to-End tests verify that the entire application works as expected from the user's perspective. They test the complete flow of the application, from the API endpoints to the database and back, ensuring that all components work together correctly.

Unlike unit tests or integration tests, E2E tests:
- Run against a real server instance
- Use a real (test) database
- Test the entire application stack
- Simulate real user interactions

## Tests Included

The E2E tests in this directory test the following functionality:

- **Transaction API Endpoints**: Tests for creating, reading, updating, and deleting transactions, as well as batch processing, statistics, and search functionality.

## Running the Tests

To run the E2E tests, use the `run_e2e_tests.py` script in the root directory:

```bash
python backend/run_e2e_tests.py
```

This script will:
1. Set up a test database with initial schema and test data
2. Start the FastAPI application on localhost:8000
3. Run the E2E tests against the running server
4. Clean up the server process and exit with the test result

## Test Structure

Each test file in this directory follows a similar structure:

1. **Setup**: Create test data and prerequisites
2. **Action**: Perform the action being tested (e.g., create a transaction)
3. **Verification**: Verify that the action had the expected result (e.g., the transaction was created correctly)
4. **Cleanup**: Clean up any test data created during the test

## Adding New Tests

When adding new E2E tests, follow these guidelines:

1. Create a new test file with a descriptive name (e.g., `test_elections_e2e.py`)
2. Use the existing test files as a template
3. Ensure that each test is independent and can run on its own
4. Clean up any test data created during the test
5. Add the new test file to this README

## Troubleshooting

If the E2E tests fail, check the following:

1. Make sure the server is running on localhost:8000
2. Check that the test database is set up correctly
3. Verify that the test data is created correctly
4. Check the server logs for any errors
5. Ensure that the API endpoints are working correctly

## Dependencies

The E2E tests depend on the following packages:

- pytest
- requests
- json
- datetime

These dependencies are included in the project's requirements.txt file.