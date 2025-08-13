# File Watching Functionality

## Overview

The Election Monitoring System now includes a file watching capability that allows the system to automatically monitor directories for new files and process them as they are added. This feature is particularly useful for continuous monitoring of election data without requiring manual file uploads.

## Features

- **Directory Monitoring**: Watch one or more directories for new files
- **Recursive Monitoring**: Optionally monitor subdirectories
- **Pattern Matching**: Filter files by pattern (e.g., only process CSV files)
- **Automatic Processing**: Automatically process new files as they are added
- **Metadata Extraction**: Extract metadata from folder structure (region, election, constituency)
- **Database Integration**: Save processed data to the database

## API Endpoints

### Start Watching a Directory

```
POST /api/files/watch-directory
```

**Parameters:**
- `directory_path` (required): Path to the directory to watch
- `recursive` (optional, default: true): Whether to watch subdirectories
- `patterns` (optional, default: ["*.csv"]): List of file patterns to watch

**Example Request:**
```
POST /api/files/watch-directory
Content-Type: application/x-www-form-urlencoded

directory_path=/path/to/data&recursive=true&patterns=*.csv
```

**Example Response:**
```json
{
  "message": "Started watching directory: /path/to/data",
  "recursive": true,
  "patterns": ["*.csv"]
}
```

### Stop Watching a Directory

```
POST /api/files/stop-watching
```

**Parameters:**
- `directory_path` (optional): Path to the directory to stop watching. If not provided, all watchers will be stopped.

**Example Request (stop specific directory):**
```
POST /api/files/stop-watching
Content-Type: application/x-www-form-urlencoded

directory_path=/path/to/data
```

**Example Response:**
```json
{
  "message": "Stopped watching directory: /path/to/data"
}
```

**Example Request (stop all watchers):**
```
POST /api/files/stop-watching
```

**Example Response:**
```json
{
  "message": "Stopped watching all directories"
}
```

### Get Watching Directories

```
GET /api/files/watching-directories
```

**Example Response:**
```json
{
  "directories": ["/path/to/data1", "/path/to/data2"],
  "count": 2
}
```

## Folder Structure Metadata

The system now extracts metadata from the folder structure when processing files. The expected folder structure is:

```
data/
├── [RegionID] - [RegionName]/
│   ├── [ElectionName]/
│   │   ├── [ConstituencyName]/
│   │   │   ├── [ConstituencyID]/
│   │   │   │   ├── [ConstituencyID]_[Date]_[TimeRange]/
│   │   │   │   │   ├── [ConstituencyID]_[Date]_[TimeRange].csv
```

Example:
```
data/
├── 90 - Пермский край/
│   ├── Выборы депутатов Думы Красновишерского городского округа/
│   │   ├── Округ №1_3/
│   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/
│   │   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/
│   │   │   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
```

The system extracts the following metadata from the folder structure:
- Region ID and name (e.g., "90" and "Пермский край")
- Election name (e.g., "Выборы депутатов Думы Красновишерского городского округа")
- Constituency name (e.g., "Округ №1_3")
- Constituency ID (e.g., "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM")

This metadata is stored in the database along with the transaction data, allowing for better organization and filtering of election data.

## Implementation Details

### FileWatcherService

The `FileWatcherService` class provides methods for starting and stopping file watchers. It uses the watchdog library to monitor directories for file system events.

Key features:
- Singleton pattern to manage multiple watchers
- Thread-safe implementation
- Automatic cleanup of resources when stopping watchers

### FileEventHandler

The `FileEventHandler` class handles file system events, such as file creation, and processes new files automatically.

Key features:
- Filters files by pattern
- Waits for files to be fully written before processing
- Extracts metadata from folder structure
- Processes files and saves data to the database
- Updates constituency metrics

## Usage Examples

### Start Watching a Directory

```python
from app.services.file_watcher_service import FileWatcherService
from sqlalchemy.orm import Session

# Get a database session
db = Session()

# Start watching a directory
watcher = FileWatcherService.get_instance("/path/to/data", db)
watcher.start(recursive=True, patterns=["*.csv"])
```

### Stop Watching a Directory

```python
from app.services.file_watcher_service import FileWatcherService

# Stop watching a specific directory
watcher = FileWatcherService.get_instance("/path/to/data", None)
watcher.stop()

# Or stop all watchers
FileWatcherService.stop_all()
```

### Get Watching Directories

```python
from app.services.file_watcher_service import FileWatcherService

# Get a list of directories being watched
directories = FileWatcherService.get_watching_directories()