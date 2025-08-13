"""
Transaction errors for the Election Monitoring System.

This module defines custom exceptions for transaction operations.
"""

from fastapi import HTTPException, status


class TransactionError(Exception):
    """Base exception for transaction errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TransactionSaveError(TransactionError):
    """Exception raised when saving a transaction fails."""
    
    def __init__(self, message: str = "Failed to save transaction"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class TransactionCreateError(TransactionError):
    """Exception raised when creating a transaction fails."""
    
    def __init__(self, message: str = "Failed to create transaction"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class TransactionUpdateError(TransactionError):
    """Exception raised when updating a transaction fails."""
    
    def __init__(self, message: str = "Failed to update transaction"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class TransactionDeleteError(TransactionError):
    """Exception raised when deleting a transaction fails."""
    
    def __init__(self, message: str = "Failed to delete transaction"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class TransactionNotFoundError(TransactionError):
    """Exception raised when a transaction is not found."""
    
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        message = f"Transaction not found: {transaction_id}"
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.message
        )


class TransactionValidationError(TransactionError):
    """Exception raised when transaction validation fails."""
    
    def __init__(self, message: str = "Transaction validation failed", errors: list = None):
        self.errors = errors or []
        if errors:
            message = f"{message}: {', '.join(errors)}"
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": self.message,
                "errors": self.errors
            }
        )


class BatchProcessingError(TransactionError):
    """Exception raised when batch processing fails."""
    
    def __init__(self, message: str = "Failed to process transaction batch", errors: list = None):
        self.errors = errors or []
        if errors:
            message = f"{message}: {', '.join(errors)}"
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": self.message,
                "errors": self.errors
            }
        )


class MetricsUpdateError(TransactionError):
    """Exception raised when updating metrics fails."""
    
    def __init__(self, message: str = "Failed to update metrics"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class QueryExecutionError(TransactionError):
    """Exception raised when executing a query fails."""
    
    def __init__(self, message: str = "Failed to execute query"):
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=self.message
        )


class InvalidQueryParameterError(TransactionError):
    """Exception raised when a query parameter is invalid."""
    
    def __init__(self, parameter: str, message: str = "Invalid query parameter"):
        self.parameter = parameter
        message = f"{message}: {parameter}"
        super().__init__(message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to HTTPException."""
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.message
        )