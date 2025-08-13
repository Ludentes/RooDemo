# File Processing System Enhancement

## Overview

The current file processing system needs enhancements in three key areas:

1. **Folder Structure Processing**: Currently, the system only extracts metadata from filenames but ignores valuable information in the folder structure (region, election, constituency). This information should be preserved and used to create or update database records.

2. **Code Refactoring**: The current implementation contains debug print statements, duplicate error handling, complex parsing methods, and test code mixed with implementation. These issues should be addressed to improve code quality.

3. **File Watching**: The system should be able to automatically detect and process new files added to monitored directories.

## Requirements

### 1. Folder Structure Processing

The folder structure follows this hierarchy:
```
[Region ID and Name]/
└── [Election Name]/
    └── [Constituency Name]/
        └── [Constituency ID (Smart Contract ID)]/
            └── [Files with timestamp information]
```

- Extract region information (ID and name) from the top-level folder
- Extract election name from the second-level folder
- Extract constituency name from the third-level folder
- Extract constituency ID (smart contract ID) from the fourth-level folder
- Use this information to create or update database records
- Link transactions to the correct constituency

### 2. Code Refactoring

- Remove debug print statements
- Consolidate error handling
- Simplify complex methods
- Move test code to proper test files
- Improve documentation

### 3. File Watching

- Implement a file watching service that monitors specified directories for new files
- Process new files automatically
- Handle file system events (create, modify, delete)
- Run as a background service
- Provide API endpoints for controlling file watching

## Acceptance Criteria

1. The system correctly extracts and uses folder structure information when processing files
2. The system creates or updates database records based on folder structure information
3. The code is refactored to improve quality and maintainability
4. The system can watch directories for new files and process them automatically
5. The system provides API endpoints for controlling file watching
6. All functionality is covered by tests
7. Documentation is updated to reflect the new functionality