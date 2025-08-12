# Election Monitoring System Scripts

This directory contains utility scripts for the Election Monitoring System.

## Database Management Scripts

### Seed Database

The `seed_db.py` script populates the database with sample data for testing and development.

```bash
# Run from the backend directory
python -m scripts.seed_db
```

This script will:
1. Create all necessary database tables if they don't exist
2. Create sample elections (active, upcoming, and completed)
3. Create sample constituencies for each election
4. Create sample transactions for the active and completed elections

### Clear Database

The `clear_db.py` script removes all data from the database.

```bash
# Run from the backend directory
python -m scripts.clear_db

# To also delete the database file
python -m scripts.clear_db --delete-file
```

This script will:
1. Drop all tables from the database
2. Optionally delete the database file completely (with the `--delete-file` flag)

## Usage Workflow

A typical workflow for development and testing:

1. Clear the database to start fresh:
   ```bash
   python -m scripts.clear_db
   ```

2. Seed the database with sample data:
   ```bash
   python -m scripts.seed_db
   ```

3. Start the API server:
   ```bash
   python -m app.main
   ```

4. Test the API endpoints:
   ```bash
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/elections
   curl http://localhost:8000/api/constituencies
   curl http://localhost:8000/api/dashboard/summary
   ```

## File Processing Scripts

### Process File

The `process_file.py` script demonstrates how to use the File Processing System to process a CSV file and store the transactions in the database.

```bash
# Process a single file
python -m scripts.process_file path/to/file.csv

# Process all files in a directory
python -m scripts.process_file --directory path/to/directory
```

This script will:
1. Extract metadata from the filename
2. Extract transactions from the CSV file
3. Save transactions to the database
4. Update constituency metrics
5. Display transaction statistics

### Test File Service

The `test_file_service.py` script runs basic tests on the File Service to verify that it can extract metadata from filenames and transactions from CSV files.

```bash
# Run from the backend directory
python -m scripts.test_file_service
```

## End-to-End Testing

To run end-to-end tests for the File Processing System, use the `run_e2e_tests.py` script:

```bash
# Run from the backend directory
python run_e2e_tests.py
```

This script will:
1. Set up an in-memory test database
2. Start the FastAPI application
3. Run the end-to-end tests
4. Clean up the test environment

For more information on end-to-end testing, see the [End-to-End Testing Documentation](../docs/end_to_end_testing.md).