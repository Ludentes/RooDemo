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