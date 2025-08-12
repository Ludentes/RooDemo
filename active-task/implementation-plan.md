# File Processing System - Implementation Plan

This document outlines the step-by-step implementation plan for the File Processing System. It includes the files to create or modify, the order of implementation, and any dependencies.

## Implementation Steps

### 1. Create Data Models and Schemas

**Files to Create/Modify:**
- `backend/app/models/schemas/file_metadata.py` - Schema for file metadata
- `backend/app/models/schemas/processing_result.py` - Schema for processing results

**Implementation Details:**
- Create Pydantic models for FileMetadata, ProcessingResult, and DirectoryProcessingResult
- Implement validators for each field
- Add documentation for each model and field

**Example Implementation (FileMetadata):**
```python
from datetime import date
from pydantic import BaseModel, validator
import re

class FileMetadata(BaseModel):
    constituency_id: str
    date: date
    time_range: str
    
    @validator('constituency_id')
    def validate_constituency_id(cls, v):
        if not re.match(r'^[A-Za-z0-9]{32,}$', v):
            raise ValueError('Invalid constituency ID format')
        return v
    
    @validator('date')
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError('Date cannot be in the future')
        return v
    
    @validator('time_range')
    def validate_time_range(cls, v):
        if not re.match(r'^[0-9]{4}-[0-9]{4}$', v):
            raise ValueError('Invalid time range format')
        return v
```

### 2. Implement File Service

**Files to Create/Modify:**
- `backend/app/services/file_service.py` - Service for file processing

**Implementation Details:**
- Create FileService class with methods for file processing
- Implement file metadata extraction from filenames
- Implement CSV parsing logic
- Implement directory processing logic
- Add error handling for file operations

**Example Implementation (extract_metadata_from_filename):**
```python
import re
from datetime import datetime
from pathlib import Path
from app.models.schemas.file_metadata import FileMetadata

class FileService:
    def extract_metadata_from_filename(self, filename: str) -> FileMetadata:
        """
        Extract metadata from a file name.
        
        Args:
            filename: The name of the file
            
        Returns:
            Extracted metadata (constituency_id, date, time_range)
            
        Raises:
            MetadataExtractionError: If metadata cannot be extracted
        """
        try:
            # Expected format: [SmartContractID]_[Date]_[TimeRange].csv
            # Example: AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
            
            # Remove file extension
            filename = Path(filename).stem
            
            # Split by underscore
            parts = filename.split('_')
            if len(parts) != 3:
                raise ValueError(f"Invalid filename format: {filename}")
            
            constituency_id = parts[0]
            date_str = parts[1]
            time_range = parts[2]
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            return FileMetadata(
                constituency_id=constituency_id,
                date=date_obj,
                time_range=time_range
            )
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from filename: {e}")
```

### 3. Implement Transaction Processing

**Files to Create/Modify:**
- `backend/app/services/transaction_service.py` - Service for transaction processing

**Implementation Details:**
- Create TransactionService class with methods for transaction processing
- Implement transaction parsing from CSV data
- Implement transaction storage in the database
- Implement constituency metrics update logic
- Add error handling for transaction operations

**Example Implementation (parse_transaction):**
```python
import json
from datetime import datetime
from typing import Dict, Any, List
from app.models.transaction import Transaction

class TransactionService:
    def parse_transaction(self, row: List[str]) -> Dict[str, Any]:
        """
        Parse a transaction from a CSV row.
        
        Args:
            row: List of fields from CSV row
            
        Returns:
            Parsed transaction data
            
        Raises:
            TransactionParsingError: If parsing fails
        """
        try:
            if len(row) < 12:
                raise ValueError(f"Invalid row length: {len(row)}")
            
            transaction_id = row[0]
            timestamp_ms = int(row[4])
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
            
            # Parse operation data (JSON-like structure)
            operation_data_str = row[8]
            operation_data = self._parse_json_like_structure(operation_data_str)
            
            # Determine transaction type
            transaction_type = None
            for item in operation_data:
                if item.get('key') == 'operation' and item.get('stringValue'):
                    transaction_type = item.get('stringValue')
                    break
            
            if not transaction_type:
                raise ValueError("Transaction type not found in operation data")
            
            # Parse operation-specific data
            specific_data_str = row[9]
            specific_data = self._parse_json_like_structure(specific_data_str)
            
            return {
                'transaction_id': transaction_id,
                'block_height': int(row[3]),
                'timestamp': timestamp,
                'type': transaction_type,
                'raw_data': operation_data,
                'operation_data': specific_data
            }
        except Exception as e:
            raise TransactionParsingError(f"Failed to parse transaction: {e}")
    
    def _parse_json_like_structure(self, data_str: str) -> List[Dict[str, Any]]:
        """
        Parse a JSON-like structure from a string.
        
        Args:
            data_str: String containing JSON-like structure
            
        Returns:
            Parsed data as a list of dictionaries
            
        Raises:
            ValueError: If parsing fails
        """
        # This is a simplified implementation
        # The actual implementation would need to handle the specific format
        try:
            # Remove square brackets at the beginning and end
            if data_str.startswith('[') and data_str.endswith(']'):
                data_str = data_str[1:-1]
            
            # Split by commas, but not within JSON objects
            # This is a simplified approach and may need to be more robust
            items = []
            current_item = ""
            brace_count = 0
            
            for char in data_str:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                
                if char == ',' and brace_count == 0:
                    if current_item:
                        items.append(current_item.strip())
                        current_item = ""
                else:
                    current_item += char
            
            if current_item:
                items.append(current_item.strip())
            
            # Parse each item as JSON
            return [json.loads(item) for item in items]
        except Exception as e:
            raise ValueError(f"Failed to parse JSON-like structure: {e}")
```

### 4. Implement API Endpoints

**Files to Create/Modify:**
- `backend/app/api/routes/files.py` - API routes for file processing

**Implementation Details:**
- Create API endpoints for file upload and directory processing
- Implement request validation
- Implement response formatting
- Add error handling for API operations

**Example Implementation (file upload endpoint):**
```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.file_service import FileService
from app.services.transaction_service import TransactionService
from app.models.schemas.processing_result import ProcessingResult

router = APIRouter()

@router.post("/upload", response_model=ProcessingResult)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a transaction file for processing.
    """
    try:
        # Check file extension
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Expected CSV file."
            )
        
        # Save file to temporary location
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process file
        file_service = FileService()
        transaction_service = TransactionService(db)
        
        # Extract metadata from filename
        metadata = file_service.extract_metadata_from_filename(file.filename)
        
        # Extract transactions from CSV
        with open(temp_file_path, "r") as f:
            content = f.read()
        
        transactions = file_service.extract_transactions_from_csv(content, metadata)
        
        # Save transactions to database
        transactions_processed = transaction_service.save_transactions(transactions)
        
        # Update constituency metrics
        transaction_service.update_constituency_metrics(metadata.constituency_id)
        
        # Return processing result
        return ProcessingResult(
            filename=file.filename,
            transactions_processed=transactions_processed,
            constituency_id=metadata.constituency_id,
            date=metadata.date,
            time_range=metadata.time_range
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )
```

### 5. Update API Router Configuration

**Files to Create/Modify:**
- `backend/app/api/routes/__init__.py` - Update to include new routes
- `backend/app/main.py` - Update to include new router

**Implementation Details:**
- Add the files router to the API router configuration
- Update the main application to include the new router

**Example Implementation (update __init__.py):**
```python
from fastapi import APIRouter
from app.api.routes import health, elections, constituencies, dashboard, files

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(elections.router, prefix="/elections", tags=["elections"])
api_router.include_router(constituencies.router, prefix="/constituencies", tags=["constituencies"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
```

### 6. Implement Error Handling

**Files to Create/Modify:**
- `backend/app/api/errors/exceptions.py` - Add new exception classes

**Implementation Details:**
- Create custom exception classes for file processing errors
- Update error handlers to handle new exceptions

**Example Implementation (new exceptions):**
```python
class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    pass

class MetadataExtractionError(FileProcessingError):
    """Exception raised when metadata extraction fails."""
    pass

class TransactionParsingError(FileProcessingError):
    """Exception raised when transaction parsing fails."""
    pass

class TransactionSaveError(FileProcessingError):
    """Exception raised when transaction saving fails."""
    pass

class MetricsUpdateError(FileProcessingError):
    """Exception raised when metrics update fails."""
    pass

class DirectoryProcessingError(FileProcessingError):
    """Exception raised when directory processing fails."""
    pass
```

### 7. Implement Unit Tests

**Files to Create/Modify:**
- `backend/tests/services/test_file_service.py` - Tests for file service
- `backend/tests/services/test_transaction_service.py` - Tests for transaction service
- `backend/tests/api/test_files.py` - Tests for file API endpoints

**Implementation Details:**
- Create unit tests for each service method
- Create API tests for each endpoint
- Create test fixtures for sample data

**Example Implementation (test file service):**
```python
import pytest
from datetime import date
from app.services.file_service import FileService
from app.models.schemas.file_metadata import FileMetadata

def test_extract_metadata_from_filename():
    # Arrange
    file_service = FileService()
    filename = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
    
    # Act
    metadata = file_service.extract_metadata_from_filename(filename)
    
    # Assert
    assert isinstance(metadata, FileMetadata)
    assert metadata.constituency_id == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    assert metadata.date == date(2024, 9, 6)
    assert metadata.time_range == "0800-0900"

def test_extract_metadata_from_invalid_filename():
    # Arrange
    file_service = FileService()
    filename = "invalid_filename.csv"
    
    # Act & Assert
    with pytest.raises(MetadataExtractionError):
        file_service.extract_metadata_from_filename(filename)
```

## Implementation Order

1. **Data Models and Schemas**
   - Create the necessary data models and schemas first
   - This provides the foundation for the rest of the implementation

2. **Services**
   - Implement the file service and transaction service
   - These contain the core business logic for file processing

3. **API Endpoints**
   - Implement the API endpoints for file upload and directory processing
   - These provide the interface for users to interact with the system

4. **Error Handling**
   - Implement custom exceptions and error handlers
   - This ensures that errors are handled gracefully

5. **Tests**
   - Implement unit tests and API tests
   - This ensures that the implementation works as expected

## Dependencies

- **Core Data Models**: The file processing system depends on the existing data models, particularly the Transaction and Constituency models
- **API Framework**: The API endpoints depend on the existing FastAPI setup
- **Database Access**: The transaction service depends on the existing database access layer

## Potential Challenges

1. **CSV Parsing**: The CSV format is complex with JSON-like structures that may be challenging to parse
   - Solution: Implement a robust parser that can handle the specific format
   - Fallback: Use a simplified parser that extracts only the essential fields

2. **File Handling**: Processing large files may cause memory issues
   - Solution: Implement streaming parsing to avoid loading the entire file into memory
   - Fallback: Implement batch processing for large files

3. **Error Handling**: Various errors may occur during file processing
   - Solution: Implement comprehensive error handling with detailed error messages
   - Fallback: Implement basic error handling with generic error messages

4. **Performance**: Processing many files may be slow
   - Solution: Implement parallel processing for multiple files
   - Fallback: Implement sequential processing with progress reporting

## Testing Strategy

1. **Unit Tests**: Test each component in isolation
   - Test file service methods
   - Test transaction service methods
   - Test API endpoints

2. **Integration Tests**: Test the interaction between components
   - Test file processing workflow
   - Test directory processing workflow

3. **End-to-End Tests**: Test the entire system
   - Test file upload and processing
   - Test directory processing

4. **Performance Tests**: Test the system under load
   - Test processing large files
   - Test processing many files

## Conclusion

This implementation plan provides a step-by-step guide for implementing the File Processing System. By following this plan, the system can be implemented in a structured and organized manner, ensuring that all requirements are met and potential challenges are addressed.