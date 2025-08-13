# Transaction Processing System - Interfaces

This document defines the interfaces for the Transaction Processing System, including API endpoints, service interfaces, and data models.

## API Endpoints

### Transaction API

#### `GET /api/transactions`

List transactions with filtering and pagination.

**Query Parameters:**
- `constituency_id` (optional): Filter by constituency ID
- `type` (optional): Filter by transaction type
- `start_time` (optional): Filter by start time
- `end_time` (optional): Filter by end time
- `page` (optional, default=1): Page number
- `limit` (optional, default=100): Items per page
- `sort_by` (optional, default="timestamp"): Field to sort by
- `sort_order` (optional, default="desc"): Sort order (asc, desc)

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "constituency_id": "string",
      "block_height": 0,
      "timestamp": "2025-08-13T00:00:00.000Z",
      "type": "blindSigIssue",
      "raw_data": {},
      "operation_data": {},
      "created_at": "2025-08-13T00:00:00.000Z",
      "updated_at": "2025-08-13T00:00:00.000Z"
    }
  ],
  "total": 0,
  "page": 1,
  "limit": 100
}
```

#### `GET /api/transactions/{id}`

Get a specific transaction by ID.

**Path Parameters:**
- `id`: Transaction ID

**Response:**
```json
{
  "id": "string",
  "constituency_id": "string",
  "block_height": 0,
  "timestamp": "2025-08-13T00:00:00.000Z",
  "type": "blindSigIssue",
  "raw_data": {},
  "operation_data": {},
  "created_at": "2025-08-13T00:00:00.000Z",
  "updated_at": "2025-08-13T00:00:00.000Z"
}
```

#### `POST /api/transactions`

Create a new transaction.

**Request Body:**
```json
{
  "constituency_id": "string",
  "block_height": 0,
  "timestamp": "2025-08-13T00:00:00.000Z",
  "type": "blindSigIssue",
  "raw_data": {},
  "operation_data": {}
}
```

**Response:**
```json
{
  "id": "string",
  "constituency_id": "string",
  "block_height": 0,
  "timestamp": "2025-08-13T00:00:00.000Z",
  "type": "blindSigIssue",
  "raw_data": {},
  "operation_data": {},
  "created_at": "2025-08-13T00:00:00.000Z",
  "updated_at": "2025-08-13T00:00:00.000Z"
}
```

#### `PUT /api/transactions/{id}`

Update an existing transaction.

**Path Parameters:**
- `id`: Transaction ID

**Request Body:**
```json
{
  "block_height": 0,
  "timestamp": "2025-08-13T00:00:00.000Z",
  "type": "blindSigIssue",
  "raw_data": {},
  "operation_data": {}
}
```

**Response:**
```json
{
  "id": "string",
  "constituency_id": "string",
  "block_height": 0,
  "timestamp": "2025-08-13T00:00:00.000Z",
  "type": "blindSigIssue",
  "raw_data": {},
  "operation_data": {},
  "created_at": "2025-08-13T00:00:00.000Z",
  "updated_at": "2025-08-13T00:00:00.000Z"
}
```

#### `DELETE /api/transactions/{id}`

Delete a transaction.

**Path Parameters:**
- `id`: Transaction ID

**Response:**
```json
{
  "success": true,
  "message": "Transaction deleted successfully"
}
```

#### `GET /api/transactions/by-constituency/{constituency_id}`

Get transactions for a specific constituency.

**Path Parameters:**
- `constituency_id`: Constituency ID

**Query Parameters:**
- `page` (optional, default=1): Page number
- `limit` (optional, default=100): Items per page
- `sort_by` (optional, default="timestamp"): Field to sort by
- `sort_order` (optional, default="desc"): Sort order (asc, desc)

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "constituency_id": "string",
      "block_height": 0,
      "timestamp": "2025-08-13T00:00:00.000Z",
      "type": "blindSigIssue",
      "raw_data": {},
      "operation_data": {},
      "created_at": "2025-08-13T00:00:00.000Z",
      "updated_at": "2025-08-13T00:00:00.000Z"
    }
  ],
  "total": 0,
  "page": 1,
  "limit": 100
}
```

#### `GET /api/transactions/by-type/{type}`

Get transactions of a specific type.

**Path Parameters:**
- `type`: Transaction type (blindSigIssue, vote)

**Query Parameters:**
- `page` (optional, default=1): Page number
- `limit` (optional, default=100): Items per page
- `sort_by` (optional, default="timestamp"): Field to sort by
- `sort_order` (optional, default="desc"): Sort order (asc, desc)

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "constituency_id": "string",
      "block_height": 0,
      "timestamp": "2025-08-13T00:00:00.000Z",
      "type": "blindSigIssue",
      "raw_data": {},
      "operation_data": {},
      "created_at": "2025-08-13T00:00:00.000Z",
      "updated_at": "2025-08-13T00:00:00.000Z"
    }
  ],
  "total": 0,
  "page": 1,
  "limit": 100
}
```

#### `GET /api/transactions/recent`

Get recent transactions.

**Query Parameters:**
- `limit` (optional, default=10): Number of transactions to return

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "constituency_id": "string",
      "block_height": 0,
      "timestamp": "2025-08-13T00:00:00.000Z",
      "type": "blindSigIssue",
      "raw_data": {},
      "operation_data": {},
      "created_at": "2025-08-13T00:00:00.000Z",
      "updated_at": "2025-08-13T00:00:00.000Z"
    }
  ],
  "total": 0
}
```

#### `POST /api/transactions/batch`

Create multiple transactions in a batch.

**Request Body:**
```json
{
  "transactions": [
    {
      "constituency_id": "string",
      "block_height": 0,
      "timestamp": "2025-08-13T00:00:00.000Z",
      "type": "blindSigIssue",
      "raw_data": {},
      "operation_data": {}
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "processed": 0,
  "failed": 0,
  "errors": []
}
```

#### `GET /api/transactions/statistics`

Get transaction statistics.

**Query Parameters:**
- `constituency_id` (optional): Filter by constituency ID
- `start_time` (optional): Filter by start time
- `end_time` (optional): Filter by end time

**Response:**
```json
{
  "total_transactions": 0,
  "total_bulletins": 0,
  "total_votes": 0,
  "transactions_per_hour": 0.0,
  "bulletins_per_hour": 0.0,
  "votes_per_hour": 0.0
}
```

## Service Interfaces

### TransactionService

```python
class TransactionService:
    def __init__(self, db: Session):
        """Initialize the service with a database session."""
        self.db = db
    
    def save_transactions(self, transactions: List[TransactionData]) -> int:
        """
        Save transactions to the database.
        
        Args:
            transactions: List of transactions to save
            
        Returns:
            Number of transactions saved
            
        Raises:
            TransactionSaveError: If saving fails
        """
        pass
    
    def update_constituency_metrics(self, constituency_id: str) -> None:
        """
        Update constituency metrics based on transactions.
        
        Args:
            constituency_id: ID of the constituency
            
        Raises:
            MetricsUpdateError: If update fails
        """
        pass
    
    def get_transaction_statistics(self, constituency_id: str) -> Dict[str, Any]:
        """
        Get transaction statistics for a constituency.
        
        Args:
            constituency_id: ID of the constituency
            
        Returns:
            Dictionary of transaction statistics
        """
        pass
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """
        Get a transaction by ID.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            Transaction or None if not found
        """
        pass
    
    def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction_data: Transaction data
            
        Returns:
            Created transaction
            
        Raises:
            TransactionCreateError: If creation fails
        """
        pass
    
    def update_transaction(self, transaction_id: str, transaction_data: TransactionUpdate) -> Optional[Transaction]:
        """
        Update a transaction.
        
        Args:
            transaction_id: ID of the transaction
            transaction_data: Transaction data
            
        Returns:
            Updated transaction or None if not found
            
        Raises:
            TransactionUpdateError: If update fails
        """
        pass
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """
        Delete a transaction.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            TransactionDeleteError: If deletion fails
        """
        pass
    
    def get_transactions(
        self,
        constituency_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Tuple[List[Transaction], int]:
        """
        Get transactions with filtering and pagination.
        
        Args:
            constituency_id: Filter by constituency ID
            transaction_type: Filter by transaction type
            start_time: Filter by start time
            end_time: Filter by end time
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (asc, desc)
            
        Returns:
            Tuple of (transactions, total_count)
        """
        pass
    
    def process_transaction_batch(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a batch of transactions.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        pass
```

### TransactionValidator

```python
class TransactionValidator:
    def validate_transaction(self, transaction_data: TransactionCreate) -> List[str]:
        """
        Validate a transaction.
        
        Args:
            transaction_data: Transaction data to validate
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
    
    def validate_transaction_batch(self, transactions: List[TransactionCreate]) -> Dict[int, List[str]]:
        """
        Validate a batch of transactions.
        
        Args:
            transactions: List of transactions to validate
            
        Returns:
            Dictionary mapping transaction index to validation errors
        """
        pass
    
    def check_duplicate(self, transaction_id: str, db: Session) -> bool:
        """
        Check if a transaction with the given ID already exists.
        
        Args:
            transaction_id: Transaction ID to check
            db: Database session
            
        Returns:
            True if duplicate, False otherwise
        """
        pass
```

### TransactionBatchProcessor

```python
class TransactionBatchProcessor:
    def __init__(self, db: Session, batch_size: int = 100):
        """
        Initialize the batch processor.
        
        Args:
            db: Database session
            batch_size: Size of each batch
        """
        self.db = db
        self.batch_size = batch_size
    
    def process_batch(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a batch of transactions.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        pass
    
    def split_into_batches(self, transactions: List[TransactionCreate]) -> List[List[TransactionCreate]]:
        """
        Split transactions into batches.
        
        Args:
            transactions: List of transactions to split
            
        Returns:
            List of transaction batches
        """
        pass
```

### TransactionQueryService

```python
class TransactionQueryService:
    def __init__(self, db: Session):
        """
        Initialize the query service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def build_query(
        self,
        constituency_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Query:
        """
        Build a query for transactions.
        
        Args:
            constituency_id: Filter by constituency ID
            transaction_type: Filter by transaction type
            start_time: Filter by start time
            end_time: Filter by end time
            sort_by: Field to sort by
            sort_order: Sort order (asc, desc)
            
        Returns:
            SQLAlchemy query
        """
        pass
    
    def execute_query(self, query: Query, page: int = 1, limit: int = 100) -> Tuple[List[Transaction], int]:
        """
        Execute a query with pagination.
        
        Args:
            query: SQLAlchemy query
            page: Page number
            limit: Items per page
            
        Returns:
            Tuple of (transactions, total_count)
        """
        pass
    
    def get_transaction_counts_by_hour(self, constituency_id: str) -> Dict[int, int]:
        """
        Get transaction counts by hour for a constituency.
        
        Args:
            constituency_id: Constituency ID
            
        Returns:
            Dictionary mapping hour to transaction count
        """
        pass
```

## Data Models

### Transaction Model (SQLAlchemy)

```python
class Transaction(Base, UUIDMixin, TimestampMixin):
    """
    Transaction model representing a blockchain transaction.
    
    Attributes:
        id (str): Primary key, UUID
        constituency_id (str): Foreign key to Constituency
        block_height (int): Blockchain block height
        timestamp (datetime): Transaction timestamp
        type (str): Transaction type (blindSigIssue, vote)
        raw_data (dict): Raw transaction data
        operation_data (dict): Processed operation data
        created_at (datetime): Record creation timestamp
        constituency (Constituency): The constituency this transaction belongs to
    """
    
    __tablename__ = "transactions"
    
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False, index=True)
    block_height = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # blindSigIssue, vote
    raw_data = Column(JSON)
    operation_data = Column(JSON)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="transactions")
```

### Transaction Schemas (Pydantic)

```python
class TransactionBase(BaseSchema):
    """
    Base schema for Transaction model.
    
    Attributes:
        constituency_id (str): ID of the constituency this transaction belongs to
        block_height (int): Blockchain block height
        timestamp (datetime): Transaction timestamp
        type (str): Transaction type (blindSigIssue, vote)
        raw_data (dict): Raw transaction data
        operation_data (dict): Processed operation data
    """
    
    constituency_id: str = Field(..., description="ID of the constituency this transaction belongs to")
    block_height: int = Field(..., description="Blockchain block height")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    type: str = Field(..., description="Transaction type (blindSigIssue, vote)")
    raw_data: Dict[str, Any] = Field(..., description="Raw transaction data")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="Processed operation data")
    
    @validator("type")
    def validate_type(cls, v: str) -> str:
        """Validate transaction type."""
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v


class TransactionCreate(TransactionBase):
    """
    Schema for creating a Transaction.
    
    This schema is used for creating a new Transaction.
    """
    
    pass


class TransactionUpdate(BaseSchema):
    """
    Schema for updating a Transaction.
    
    This schema is used for updating an existing Transaction.
    All fields are optional to allow partial updates.
    """
    
    block_height: Optional[int] = Field(None, description="Blockchain block height")
    timestamp: Optional[datetime] = Field(None, description="Transaction timestamp")
    type: Optional[str] = Field(None, description="Transaction type (blindSigIssue, vote)")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw transaction data")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="Processed operation data")
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction type."""
        if v is None:
            return v
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v


class TransactionResponse(ResponseBase, TransactionBase):
    """
    Schema for Transaction response.
    
    This schema is used for returning a Transaction in API responses.
    """
    
    pass


class TransactionList(BaseSchema):
    """
    Schema for list of Transactions.
    
    This schema is used for returning a list of Transactions in API responses.
    """
    
    data: List[TransactionResponse]
    total: int
    page: int
    limit: int


class TransactionStats(BaseSchema):
    """
    Schema for Transaction statistics.
    
    This schema is used for returning statistics about Transactions.
    """
    
    total_transactions: int = Field(..., description="Total number of transactions")
    total_bulletins: int = Field(..., description="Total number of bulletin transactions")
    total_votes: int = Field(..., description="Total number of vote transactions")
    transactions_per_hour: float = Field(..., description="Average transactions per hour")
    bulletins_per_hour: float = Field(..., description="Average bulletins per hour")
    votes_per_hour: float = Field(..., description="Average votes per hour")


class TransactionBatchRequest(BaseSchema):
    """
    Schema for batch transaction request.
    
    This schema is used for creating multiple transactions in a batch.
    """
    
    transactions: List[TransactionCreate] = Field(..., description="List of transactions to create")


class TransactionBatchResponse(BaseSchema):
    """
    Schema for batch transaction response.
    
    This schema is used for returning the result of a batch transaction operation.
    """
    
    success: bool = Field(..., description="Whether the operation was successful")
    processed: int = Field(..., description="Number of transactions processed")
    failed: int = Field(..., description="Number of transactions that failed")
    errors: List[Dict[str, Any]] = Field(..., description="List of errors")
```

## Error Handling

### Custom Exceptions

```python
class TransactionError(Exception):
    """Base exception for transaction errors."""
    pass


class TransactionSaveError(TransactionError):
    """Exception raised when saving a transaction fails."""
    pass


class TransactionCreateError(TransactionError):
    """Exception raised when creating a transaction fails."""
    pass


class TransactionUpdateError(TransactionError):
    """Exception raised when updating a transaction fails."""
    pass


class TransactionDeleteError(TransactionError):
    """Exception raised when deleting a transaction fails."""
    pass


class TransactionValidationError(TransactionError):
    """Exception raised when transaction validation fails."""
    pass


class BatchProcessingError(TransactionError):
    """Exception raised when batch processing fails."""
    pass


class MetricsUpdateError(TransactionError):
    """Exception raised when updating metrics fails."""
    pass
```

### Error Responses

```python
class ErrorResponse(BaseSchema):
    """
    Schema for error response.
    
    This schema is used for returning error responses.
    """
    
    detail: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
```

## Dependencies

```python
def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    """
    Get a TransactionService instance.
    
    Args:
        db: Database session
        
    Returns:
        TransactionService instance
    """
    return TransactionService(db)


def get_transaction_validator() -> TransactionValidator:
    """
    Get a TransactionValidator instance.
    
    Returns:
        TransactionValidator instance
    """
    return TransactionValidator()


def get_transaction_batch_processor(db: Session = Depends(get_db)) -> TransactionBatchProcessor:
    """
    Get a TransactionBatchProcessor instance.
    
    Args:
        db: Database session
        
    Returns:
        TransactionBatchProcessor instance
    """
    return TransactionBatchProcessor(db)


def get_transaction_query_service(db: Session = Depends(get_db)) -> TransactionQueryService:
    """
    Get a TransactionQueryService instance.
    
    Args:
        db: Database session
        
    Returns:
        TransactionQueryService instance
    """
    return TransactionQueryService(db)