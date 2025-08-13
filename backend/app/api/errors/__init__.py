# Import exception handlers to make them available for registration
from app.api.errors.handlers import register_exception_handlers

# Import exceptions to make them available for import from app.api.errors
from app.api.errors.exceptions import (
    NotFoundError,
    ValidationError,
    DatabaseError,
    FileProcessingError,
    MetadataExtractionError,
    TransactionExtractionError,
    DirectoryProcessingError,
    TransactionSaveError,
    MetricsUpdateError,
    TransactionError,
    TransactionCreateError,
    TransactionUpdateError,
    TransactionDeleteError,
    TransactionNotFoundError,
    TransactionValidationError,
    BatchProcessingError,
    QueryExecutionError,
    InvalidQueryParameterError
)

# Import transaction errors directly for convenience
from app.api.errors.transaction_errors import (
    TransactionError,
    TransactionSaveError as NewTransactionSaveError,
    TransactionCreateError,
    TransactionUpdateError,
    TransactionDeleteError,
    TransactionNotFoundError,
    TransactionValidationError,
    BatchProcessingError,
    MetricsUpdateError as NewMetricsUpdateError,
    QueryExecutionError,
    InvalidQueryParameterError
)