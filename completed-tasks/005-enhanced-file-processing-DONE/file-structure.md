# File Processing System Enhancement - File Structure

This document outlines the files that need to be created or modified for the file processing system enhancement.

## New Files

### Models and Schemas

1. `backend/app/models/region.py`
   - Region model for storing region information

2. `backend/app/models/schemas/region.py`
   - Region schema for validating region data
   - Includes RegionBase, RegionCreate, RegionUpdate, and Region schemas

### Services

3. `backend/app/services/region_service.py`
   - Service for creating, updating, and retrieving regions
   - Includes methods for creating or updating regions based on folder structure

4. `backend/app/services/file_watcher_service.py`
   - Service for watching directories for new files
   - Includes methods for starting and stopping watchers
   - Handles file system events

### CRUD Operations

5. `backend/app/crud/region.py`
   - CRUD operations for regions
   - Includes methods for creating, reading, updating, and deleting regions

### Database Migrations

6. `backend/alembic/versions/add_region_table.py`
   - Migration for adding the region table to the database

### Tests

7. `backend/tests/models/test_region.py`
   - Tests for the Region model

8. `backend/tests/schemas/test_region_schema.py`
   - Tests for the Region schema

9. `backend/tests/services/test_region_service.py`
   - Tests for the RegionService

10. `backend/tests/services/test_file_watcher_service.py`
    - Tests for the FileWatcherService

11. `backend/tests/crud/test_region_crud.py`
    - Tests for the region CRUD operations

### Documentation

12. `backend/docs/file_watching.md`
    - Documentation for the file watching functionality

## Modified Files

### Models and Schemas

1. `backend/app/models/schemas/file_metadata.py`
   - Add fields for region, election, and constituency information
   - Update validation logic

2. `backend/app/models/schemas/processing_result.py`
   - Add fields for region, election, and constituency information
   - Update validation logic

### Services

3. `backend/app/services/file_service.py`
   - Add method for extracting metadata from folder structure
   - Update process_file method to use enhanced metadata
   - Update process_directory method to use enhanced metadata
   - Remove debug print statements
   - Consolidate error handling
   - Simplify complex methods
   - Move test code to proper test files
   - Improve documentation

4. `backend/app/services/transaction_service.py`
   - Remove debug print statements
   - Consolidate error handling
   - Improve documentation

5. `backend/app/services/election.py`
   - Add method for creating or updating elections based on folder structure

6. `backend/app/services/constituency.py`
   - Add method for creating or updating constituencies based on folder structure

### API Routes

7. `backend/app/api/routes/files.py`
   - Update file upload endpoint to use enhanced metadata
   - Update directory processing endpoint to use enhanced metadata
   - Add endpoints for starting and stopping file watching
   - Remove debug print statements
   - Consolidate error handling
   - Improve documentation

### Tests

8. `backend/tests/services/test_file_service.py`
   - Add tests for enhanced metadata extraction
   - Add tests for enhanced file processing
   - Add tests for enhanced directory processing

9. `backend/tests/api/test_files.py`
   - Add tests for enhanced file upload endpoint
   - Add tests for enhanced directory processing endpoint
   - Add tests for file watching endpoints

### Configuration

10. `backend/requirements.txt`
    - Add watchdog dependency

## File Structure Diagram

```
backend/
├── alembic/
│   └── versions/
│       └── add_region_table.py
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── files.py
│   ├── crud/
│   │   └── region.py
│   ├── models/
│   │   ├── region.py
│   │   └── schemas/
│   │       ├── file_metadata.py
│   │       ├── processing_result.py
│   │       └── region.py
│   └── services/
│       ├── constituency.py
│       ├── election.py
│       ├── file_service.py
│       ├── file_watcher_service.py
│       ├── region_service.py
│       └── transaction_service.py
├── docs/
│   └── file_watching.md
├── requirements.txt
└── tests/
    ├── api/
    │   └── test_files.py
    ├── crud/
    │   └── test_region_crud.py
    ├── models/
    │   └── test_region.py
    ├── schemas/
    │   └── test_region_schema.py
    └── services/
        ├── test_file_service.py
        ├── test_file_watcher_service.py
        └── test_region_service.py