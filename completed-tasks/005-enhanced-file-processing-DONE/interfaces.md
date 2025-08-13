# File Processing System Enhancement - Interfaces

This document defines the key interfaces and data structures for the file processing system enhancement.

## 1. Data Models and Schemas

### 1.1 Region Model

```python
class Region(Base):
    __tablename__ = "regions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Russia")
```

### 1.2 Region Schema

```python
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

### 1.3 Enhanced File Metadata Schema

```python
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
```

### 1.4 Enhanced Processing Result Schema

```python
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

## 2. Service Interfaces

### 2.1 Region Service Interface

```python
class RegionService:
    def __init__(self, db: Session):
        """Initialize the service with a database session."""
        pass
    
    def get_region(self, region_id: str) -> Optional[Region]:
        """Get a region by ID."""
        pass
    
    def create_region(self, region: RegionCreate) -> Region:
        """Create a new region."""
        pass
    
    def update_region(self, region_id: str, region: RegionUpdate) -> Optional[Region]:
        """Update an existing region."""
        pass
    
    def create_or_update_region(self, region_id: str, region_name: str, country: str = "Russia") -> Region:
        """Create a new region or update an existing one."""
        pass
```

### 2.2 Enhanced File Service Interface

```python
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
        pass
    
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
        pass
    
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
        pass
    
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
        pass
```

### 2.3 File Watcher Service Interface

```python
class FileWatcherService:
    @classmethod
    def get_instance(cls, directory_path: str, db: Session) -> 'FileWatcherService':
        """
        Get or create a FileWatcherService instance for a directory.
        
        Args:
            directory_path: Path to the directory to watch
            db: Database session
            
        Returns:
            FileWatcherService instance
        """
        pass
    
    @classmethod
    def stop_all(cls):
        """Stop all file watchers."""
        pass
    
    def __init__(self, directory_path: str, db: Session):
        """
        Initialize the service with a directory path and database session.
        
        Args:
            directory_path: Path to the directory to watch
            db: Database session
        """
        pass
    
    def start(self):
        """
        Start watching the directory.
        
        Raises:
            Exception: If starting the watcher fails
        """
        pass
    
    def stop(self):
        """
        Stop watching the directory.
        
        Raises:
            Exception: If stopping the watcher fails
        """
        pass
```

## 3. API Endpoints

### 3.1 File Routes

```python
@router.post("/upload", response_model=None)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a transaction file for processing.
    
    Args:
        file: The file to upload
        db: Database session
        
    Returns:
        Processing result with statistics
    """
    pass

@router.post("/process-directory", response_model=None)
async def process_directory(
    directory_path: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Process all files in a directory.
    
    Args:
        directory_path: Path to the directory
        db: Database session
        
    Returns:
        Processing result with statistics
    """
    pass

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
    pass

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
    pass

@router.get("/statistics/{constituency_id}")
async def get_transaction_statistics(
    constituency_id: str,
    db: Session = Depends(get_db)
):
    """
    Get transaction statistics for a constituency.
    
    Args:
        constituency_id: ID of the constituency
        db: Database session
        
    Returns:
        Transaction statistics
    """
    pass
```

## 4. Database Schema Changes

### 4.1 Region Table

```sql
CREATE TABLE regions (
    id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    PRIMARY KEY (id)
);
```

## 5. Dependencies

### 5.1 Python Packages

```
watchdog==3.0.0  # For file system monitoring
```

## 6. Configuration

### 6.1 File Watcher Configuration

```python
# Configuration for file watcher
FILE_WATCHER_CONFIG = {
    "polling_interval": 1,  # seconds
    "recursive": True,  # Watch subdirectories
    "patterns": ["*.csv"],  # File patterns to watch
    "ignore_patterns": [".*"],  # Patterns to ignore
    "ignore_directories": True,  # Ignore directory events
    "case_sensitive": True  # Case sensitive patterns
}