# File Processing System - Interfaces and Data Flow

This document defines the interfaces, data models, and data flow for the File Processing System. It provides detailed specifications for API endpoints, service interfaces, and data structures.

## API Interfaces

### File Upload API

#### `POST /api/files/upload`

Upload a transaction file for processing.

**Request:**
```
Content-Type: multipart/form-data

file: [binary file data]
```

**Response (Success):**
```json
{
  "status": "success",
  "data": {
    "filename": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv",
    "transactions_processed": 12,
    "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
    "date": "2024-09-06",
    "time_range": "0800-0900"
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "error": {
    "code": "invalid_file_format",
    "message": "Invalid file format. Expected CSV file."
  }
}
```

### Directory Processing API

#### `POST /api/files/process-directory`

Process all files in a specified directory.

**Request:**
```json
{
  "directory_path": "data/sample-data/90 - Пермский край/Выборы депутатов Думы Красновишерского городского округа/Округ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "data": {
    "files_processed": 5,
    "transactions_processed": 60,
    "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
  }
}
```

## Service Interfaces

### FileService

```python
class FileService:
    def process_file(self, file_path: Path) -> ProcessingResult:
        """
        Process a CSV file and extract transactions.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ProcessingResult with statistics
            
        Raises:
            FileProcessingError: If processing fails
        """
        
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
        
    def process_directory(self, directory_path: str) -> DirectoryProcessingResult:
        """
        Process all CSV files in a directory.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            DirectoryProcessingResult with statistics
            
        Raises:
            DirectoryProcessingError: If processing fails
        """
        
    def extract_transactions_from_csv(self, file_content: str, metadata: FileMetadata) -> List[Transaction]:
        """
        Extract transactions from CSV content.
        
        Args:
            file_content: Content of the CSV file
            metadata: Metadata extracted from filename
            
        Returns:
            List of extracted transactions
            
        Raises:
            TransactionExtractionError: If extraction fails
        """
```

### TransactionService

```python
class TransactionService:
    def save_transactions(self, transactions: List[Transaction]) -> int:
        """
        Save transactions to the database.
        
        Args:
            transactions: List of transactions to save
            
        Returns:
            Number of transactions saved
            
        Raises:
            TransactionSaveError: If saving fails
        """
        
    def update_constituency_metrics(self, constituency_id: str) -> None:
        """
        Update constituency metrics based on transactions.
        
        Args:
            constituency_id: ID of the constituency
            
        Raises:
            MetricsUpdateError: If update fails
        """
```

## Data Models

### FileMetadata

```python
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

### ProcessingResult

```python
class ProcessingResult(BaseModel):
    filename: str
    transactions_processed: int
    constituency_id: str
    date: date
    time_range: str
```

### DirectoryProcessingResult

```python
class DirectoryProcessingResult(BaseModel):
    files_processed: int
    transactions_processed: int
    constituency_id: str
```

### TransactionData

```python
class TransactionData(BaseModel):
    transaction_id: str
    constituency_id: str
    block_height: int
    timestamp: datetime
    type: str  # 'blindSigIssue' or 'vote'
    raw_data: Dict[str, Any]
    operation_data: Dict[str, Any]
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['blindSigIssue', 'vote']:
            raise ValueError('Transaction type must be either "blindSigIssue" or "vote"')
        return v
```

## Data Flow

### File Upload Flow

1. Client uploads a file to the `/api/files/upload` endpoint
2. API controller receives the file and passes it to the FileService
3. FileService extracts metadata from the file name
4. FileService parses the CSV file and extracts transactions
5. TransactionService saves the transactions to the database
6. TransactionService updates constituency metrics
7. API returns processing statistics to the client

### Directory Processing Flow

1. Client sends a request to process a directory
2. API controller receives the request and passes it to the FileService
3. FileService scans the directory for CSV files
4. For each file:
   a. FileService extracts metadata from the file name
   b. FileService parses the CSV file and extracts transactions
   c. TransactionService saves the transactions to the database
5. TransactionService updates constituency metrics
6. API returns processing statistics to the client

## CSV Parsing Logic

The CSV parser needs to handle the following format:

1. Semicolon-separated values
2. Each row represents a transaction
3. Fields include:
   - Transaction ID
   - Numeric value (104)
   - Signature or hash
   - Numeric value (4)
   - Timestamp (Unix timestamp in milliseconds)
   - Another ID or hash
   - Numeric value (0)
   - Empty field
   - JSON-like structure with operation data
   - JSON-like structure with operation-specific data
   - JSON object with contract version
   - Numeric value (1)

The parser should:
1. Split each line by semicolons
2. Extract the relevant fields
3. Parse the JSON-like structures
4. Create Transaction objects
5. Determine transaction type from the operation data

## Error Handling

The system should handle the following error cases:

1. Invalid file format
2. Invalid file name format
3. Missing or corrupt data in CSV
4. Database connection errors
5. File system access errors

Each error should be logged with appropriate context and returned to the client with a clear error message.