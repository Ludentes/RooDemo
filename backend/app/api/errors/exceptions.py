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