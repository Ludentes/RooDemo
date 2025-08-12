from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationError(HTTPException):
    """Exception raised when request validation fails."""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DatabaseError(HTTPException):
    """Exception raised when a database operation fails."""
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class FileProcessingError(HTTPException):
    """Exception raised when file processing fails."""
    def __init__(self, detail: str = "File processing error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class MetadataExtractionError(HTTPException):
    """Exception raised when metadata extraction fails."""
    def __init__(self, detail: str = "Failed to extract metadata from file"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class TransactionExtractionError(HTTPException):
    """Exception raised when transaction extraction fails."""
    def __init__(self, detail: str = "Failed to extract transactions from file"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DirectoryProcessingError(HTTPException):
    """Exception raised when directory processing fails."""
    def __init__(self, detail: str = "Failed to process directory"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class TransactionSaveError(HTTPException):
    """Exception raised when saving transactions fails."""
    def __init__(self, detail: str = "Failed to save transactions"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class MetricsUpdateError(HTTPException):
    """Exception raised when updating metrics fails."""
    def __init__(self, detail: str = "Failed to update metrics"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)