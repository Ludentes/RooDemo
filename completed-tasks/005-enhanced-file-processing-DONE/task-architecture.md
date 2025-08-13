# File Processing System Enhancement - Architecture Design

## 1. System Architecture Overview

The enhanced file processing system will consist of the following components:

1. **Data Models and Schemas**: Enhanced to capture folder structure information
2. **Services**: Enhanced to process folder structure and watch for file changes
3. **API Endpoints**: Enhanced to support new functionality
4. **Background Services**: New components for file watching

### 1.1 Component Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  API Endpoints  │────▶│    Services     │────▶│  Data Models    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              │
                              ▼
                        ┌─────────────────┐
                        │                 │
                        │  File System    │
                        │                 │
                        └─────────────────┘
```

## 2. Data Models and Schemas

### 2.1 New Models

#### 2.1.1 Region Model

```python
# backend/app/models/region.py
from sqlalchemy import Column, String
from app.models.database import Base

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Russia")
```

#### 2.1.2 Region Schema

```python
# backend/app/models/schemas/region.py
from pydantic import BaseModel, Field

class RegionBase(BaseModel):
    id: str
    name: str
    country: str = "Russia"

class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    pass

class Region(RegionBase):
    class Config:
        orm_mode = True
```

### 2.2 Enhanced Models

#### 2.2.1 Enhanced File Metadata Schema

```python
# backend/app/models/schemas/file_metadata.py
from datetime import date
from pydantic import BaseModel, Field

class EnhancedFileMetadata(BaseModel):
    # Original fields
    constituency_id: str
    date: date
    time_range: str
    
    # New fields
    region_id: str
    region_name: str
    election_name: str
    constituency_name: str
    
    class Config:
        schema_extra = {
            "example": {
                "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
                "date": "2024-09-06",
                "time_range": "0800-0900",
                "region_id": "90",
                "region_name": "Пермский край",
                "election_name": "Выборы депутатов Думы Красновишерского городского округа",
                "constituency_name": "Округ №1_3"
            }
        }
```

#### 2.2.2 Enhanced Processing Result Schema

```python
# backend/app/models/schemas/processing_result.py
from datetime import date
from pydantic import BaseModel

class EnhancedProcessingResult(BaseModel):
    # Original fields
    filename: str
    transactions_processed: int
    constituency_id: str
    date: date
    time_range: str
    
    # New fields
    region_id: str
    region_name: str
    election_name: str
    constituency_name: str

class EnhancedDirectoryProcessingResult(BaseModel):
    # Original fields
    files_processed: int
    transactions_processed: int
    constituency_id: str
    
    # New fields
    region_id: str
    region_name: str
    election_name: str
    constituency_name: str
```

## 3. Services

### 3.1 New Services

#### 3.1.1 Region Service

```python
# backend/app/services/region_service.py
from typing import Optional
from sqlalchemy.orm import Session
from app.models.region import Region
from app.models.schemas.region import RegionCreate, RegionUpdate

class RegionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_region(self, region_id: str) -> Optional[Region]:
        return self.db.query(Region).filter(Region.id == region_id).first()
    
    def create_region(self, region: RegionCreate) -> Region:
        db_region = Region(
            id=region.id,
            name=region.name,
            country=region.country
        )
        self.db.add(db_region)
        self.db.commit()
        self.db.refresh(db_region)
        return db_region
    
    def update_region(self, region_id: str, region: RegionUpdate) -> Optional[Region]:
        db_region = self.get_region(region_id)
        if db_region:
            db_region.name = region.name
            db_region.country = region.country
            self.db.commit()
            self.db.refresh(db_region)
        return db_region
    
    def create_or_update_region(self, region_id: str, region_name: str, country: str = "Russia") -> Region:
        db_region = self.get_region(region_id)
        if db_region:
            db_region.name = region_name
            db_region.country = country
            self.db.commit()
            self.db.refresh(db_region)
            return db_region
        else:
            return self.create_region(RegionCreate(
                id=region_id,
                name=region_name,
                country=country
            ))
```

#### 3.1.2 File Watcher Service

```python
# backend/app/services/file_watcher_service.py
import os
import time
import logging
from pathlib import Path
from typing import Dict, Optional
from threading import Thread, Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from sqlalchemy.orm import Session

from app.services.file_service import FileService
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_service: FileService, transaction_service: TransactionService, db: Session):
        self.file_service = file_service
        self.transaction_service = transaction_service
        self.db = db
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            try:
                logger.info(f"New file detected: {event.src_path}")
                file_path = Path(event.src_path)
                result, transactions = self.file_service.process_file(file_path)
                saved_count = self.transaction_service.save_transactions(transactions)
                self.transaction_service.update_constituency_metrics(result.constituency_id)
                logger.info(f"Processed {saved_count} transactions from {file_path}")
            except Exception as e:
                logger.error(f"Error processing file {event.src_path}: {e}")

class FileWatcherService:
    _instances: Dict[str, 'FileWatcherService'] = {}
    
    @classmethod
    def get_instance(cls, directory_path: str, db: Session) -> 'FileWatcherService':
        if directory_path not in cls._instances:
            cls._instances[directory_path] = cls(directory_path, db)
        return cls._instances[directory_path]
    
    @classmethod
    def stop_all(cls):
        for instance in cls._instances.values():
            instance.stop()
        cls._instances.clear()
    
    def __init__(self, directory_path: str, db: Session):
        self.directory_path = directory_path
        self.db = db
        self.observer = None
        self.stop_event = Event()
        self.thread = None
    
    def start(self):
        if self.observer:
            logger.warning(f"Watcher for {self.directory_path} already running")
            return
        
        try:
            file_service = FileService()
            transaction_service = TransactionService(self.db)
            
            event_handler = FileEventHandler(file_service, transaction_service, self.db)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.directory_path, recursive=True)
            
            self.thread = Thread(target=self._run_observer)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info(f"Started watching directory: {self.directory_path}")
        except Exception as e:
            logger.error(f"Error starting file watcher: {e}")
            raise
    
    def _run_observer(self):
        self.observer.start()
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error in file watcher thread: {e}")
        finally:
            self.observer.stop()
            self.observer.join()
    
    def stop(self):
        if not self.observer:
            logger.warning(f"No watcher running for {self.directory_path}")
            return
        
        try:
            self.stop_event.set()
            if self.thread:
                self.thread.join(timeout=5)
            self.observer = None
            self.thread = None
            logger.info(f"Stopped watching directory: {self.directory_path}")
        except Exception as e:
            logger.error(f"Error stopping file watcher: {e}")
            raise
```

### 3.2 Enhanced Services

#### 3.2.1 Enhanced File Service

```python
# backend/app/services/file_service.py
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from app.models.schemas.file_metadata import EnhancedFileMetadata
from app.models.schemas.processing_result import EnhancedProcessingResult, EnhancedDirectoryProcessingResult, TransactionData
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError,
    TransactionExtractionError, DirectoryProcessingError
)

class EnhancedFileService:
    def extract_metadata_from_path(self, file_path: Path) -> Dict[str, str]:
        """
        Extract metadata from a file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with extracted metadata
            
        Raises:
            MetadataExtractionError: If metadata cannot be extracted
        """
        try:
            # Convert to absolute path to ensure we have the full path
            abs_path = file_path.absolute()
            
            # Get parts of the path
            parts = abs_path.parts
            
            # Find the index of the data directory
            data_index = -1
            for i, part in enumerate(parts):
                if part == "data" or part == "sample-data":
                    data_index = i
                    break
            
            if data_index == -1 or data_index + 4 >= len(parts):
                raise ValueError(f"Invalid path structure: {file_path}")
            
            # Extract region information
            region_part = parts[data_index + 1]
            region_match = re.match(r"(\d+)\s*-\s*(.*)", region_part)
            if not region_match:
                raise ValueError(f"Invalid region format: {region_part}")
            
            region_id = region_match.group(1)
            region_name = region_match.group(2)
            
            # Extract election name
            election_name = parts[data_index + 2]
            
            # Extract constituency name
            constituency_name = parts[data_index + 3]
            
            # Extract constituency ID (smart contract ID)
            constituency_id = parts[data_index + 4]
            
            return {
                "region_id": region_id,
                "region_name": region_name,
                "election_name": election_name,
                "constituency_name": constituency_name,
                "constituency_id": constituency_id
            }
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from path: {e}")
    
    def extract_metadata_from_filename(self, filename: str) -> Dict[str, Any]:
        """
        Extract metadata from a file name.
        
        Args:
            filename: The name of the file
            
        Returns:
            Dictionary with extracted metadata
            
        Raises:
            MetadataExtractionError: If metadata cannot be extracted
        """
        try:
            # Expected format: [SmartContractID]_[Date]_[TimeRange].csv
            # Example: AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
            
            # Remove file extension and path
            filename = Path(filename).stem
            
            # Split by underscore
            parts = filename.split('_')
            if len(parts) != 3:
                raise ValueError(f"Invalid filename format: {filename}")
            
            constituency_id = parts[0]
            date_str = parts[1]
            time_range = parts[2]
            
            # Parse date
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            return {
                "constituency_id": constituency_id,
                "date": date_obj,
                "time_range": time_range
            }
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from filename: {e}")
    
    def process_file(self, file_path: Path, original_filename: str = None) -> Tuple[EnhancedProcessingResult, List[TransactionData]]:
        """
        Process a CSV file and extract transactions with enhanced metadata.
        
        Args:
            file_path: Path to the file
            original_filename: Original filename to use for metadata extraction (optional)
            
        Returns:
            EnhancedProcessingResult with statistics and list of transactions
            
        Raises:
            FileProcessingError: If processing fails
        """
        try:
            # Extract metadata from path
            path_metadata = self.extract_metadata_from_path(file_path)
            
            # Extract metadata from filename
            filename_for_metadata = original_filename if original_filename else file_path.name
            filename_metadata = self.extract_metadata_from_filename(filename_for_metadata)
            
            # Combine metadata
            metadata = EnhancedFileMetadata(
                constituency_id=path_metadata["constituency_id"],
                date=filename_metadata["date"],
                time_range=filename_metadata["time_range"],
                region_id=path_metadata["region_id"],
                region_name=path_metadata["region_name"],
                election_name=path_metadata["election_name"],
                constituency_name=path_metadata["constituency_name"]
            )
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract transactions
            transactions = self.extract_transactions_from_csv(content, metadata)
            
            # Create processing result
            result = EnhancedProcessingResult(
                filename=original_filename if original_filename else file_path.name,
                transactions_processed=len(transactions),
                constituency_id=metadata.constituency_id,
                date=metadata.date,
                time_range=metadata.time_range,
                region_id=metadata.region_id,
                region_name=metadata.region_name,
                election_name=metadata.election_name,
                constituency_name=metadata.constituency_name
            )
            
            return result, transactions
        except Exception as e:
            raise FileProcessingError(f"Failed to process file {file_path}: {e}")
    
    def process_directory(self, directory_path: str) -> Tuple[EnhancedDirectoryProcessingResult, List[TransactionData]]:
        """
        Process all CSV files in a directory with enhanced metadata extraction.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            EnhancedDirectoryProcessingResult with statistics and list of all transactions
            
        Raises:
            DirectoryProcessingError: If processing fails
        """
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                raise DirectoryProcessingError(f"Directory not found: {directory_path}")
            
            # Find all CSV files in the directory
            csv_files = list(directory.glob('**/*.csv'))
            if not csv_files:
                raise DirectoryProcessingError(f"No CSV files found in directory: {directory_path}")
            
            # Process each file
            total_transactions_processed = 0
            all_transactions = []
            
            # Extract path metadata from the first file to get common information
            path_metadata = None
            
            for file_path in csv_files:
                try:
                    result, transactions = self.process_file(file_path)
                    total_transactions_processed += result.transactions_processed
                    all_transactions.extend(transactions)
                    
                    # Set path metadata from the first successful file
                    if path_metadata is None:
                        path_metadata = {
                            "region_id": result.region_id,
                            "region_name": result.region_name,
                            "election_name": result.election_name,
                            "constituency_name": result.constituency_name,
                            "constituency_id": result.constituency_id
                        }
                except Exception as e:
                    # Log error but continue processing other files
                    import logging
                    logging.error(f"Error processing file {file_path}: {e}")
            
            # Create directory processing result
            if path_metadata is None:
                raise DirectoryProcessingError("Failed to process any files in the directory")
            
            result = EnhancedDirectoryProcessingResult(
                files_processed=len(csv_files),
                transactions_processed=total_transactions_processed,
                constituency_id=path_metadata["constituency_id"],
                region_id=path_metadata["region_id"],
                region_name=path_metadata["region_name"],
                election_name=path_metadata["election_name"],
                constituency_name=path_metadata["constituency_name"]
            )
            
            return result, all_transactions
        except Exception as e:
            raise DirectoryProcessingError(f"Failed to process directory {directory_path}: {e}")
```

## 4. API Endpoints

### 4.1 Enhanced File Routes

```python
# backend/app/api/routes/files.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError, TransactionExtractionError,
    DirectoryProcessingError, TransactionSaveError, MetricsUpdateError
)
from app.services.file_watcher_service import FileWatcherService

router = APIRouter()

@router.post("/watch-directory")
async def watch_directory(
    directory_path: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Start watching a directory for new files.
    
    Args:
        directory_path: Path to the directory to watch
        db: Database session
        
    Returns:
        Success message
    """
    try:
        watcher = FileWatcherService.get_instance(directory_path, db)
        watcher.start()
        return {"message": f"Started watching directory: {directory_path}"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start watching directory: {str(e)}"
        )

@router.post("/stop-watching")
async def stop_watching(
    directory_path: str = Form(None)
):
    """
    Stop watching a directory or all directories.
    
    Args:
        directory_path: Path to the directory to stop watching (optional)
        
    Returns:
        Success message
    """
    try:
        if directory_path:
            watcher = FileWatcherService.get_instance(directory_path, None)
            watcher.stop()
            return {"message": f"Stopped watching directory: {directory_path}"}
        else:
            FileWatcherService.stop_all()
            return {"message": "Stopped watching all directories"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop watching directory: {str(e)}"
        )
```

## 5. Database Migrations

### 5.1 Region Table Migration

```python
# backend/alembic/versions/add_region_table.py
"""Add region table

Revision ID: add_region_table
Revises: [previous_revision]
Create Date: 2025-08-13

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_region_table'
down_revision = '[previous_revision]'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'regions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('regions')
```

## 6. Testing Strategy

### 6.1 Unit Tests

- Test metadata extraction from paths
- Test metadata extraction from filenames
- Test file processing with enhanced metadata
- Test directory processing with enhanced metadata
- Test file watcher service

### 6.2 Integration Tests

- Test creating/updating regions, elections, and constituencies from folder structure
- Test file watching and automatic processing

### 6.3 End-to-End Tests

- Test complete flow from file upload to database storage with enhanced metadata
- Test complete flow from directory processing to database storage with enhanced metadata
- Test file watching and automatic processing

## 7. Implementation Plan

### 7.1 Phase 1: Folder Structure Processing

1. Create Region model and schema
2. Enhance FileMetadata and ProcessingResult schemas
3. Implement metadata extraction from paths
4. Update file processing logic to use enhanced metadata
5. Update API endpoints to use enhanced services
6. Create tests for enhanced functionality

### 7.2 Phase 2: Code Refactoring

1. Remove debug print statements
2. Consolidate error handling
3. Simplify complex methods
4. Move test code to proper test files
5. Improve documentation

### 7.3 Phase 3: File Watching

1. Add watchdog dependency to requirements.txt
2. Implement FileWatcherService
3. Add API endpoints for controlling file watching
4. Create tests for file watching functionality
5. Update documentation