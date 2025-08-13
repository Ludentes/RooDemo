from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from app.api.errors.exceptions import (
    NotFoundError, ValidationError, DatabaseError,
    FileProcessingError, MetadataExtractionError, TransactionExtractionError,
    DirectoryProcessingError, TransactionSaveError, MetricsUpdateError
)
from app.api.errors.transaction_errors import (
    TransactionError, TransactionCreateError, TransactionUpdateError,
    TransactionDeleteError, TransactionNotFoundError, TransactionValidationError,
    BatchProcessingError, QueryExecutionError, InvalidQueryParameterError
)

async def not_found_exception_handler(request: Request, exc: NotFoundError):
    """Handler for NotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.detail}}
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handler for ValidationError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.detail}}
    )

async def database_exception_handler(request: Request, exc: DatabaseError):
    """Handler for DatabaseError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": exc.detail}}
    )

async def file_processing_exception_handler(request: Request, exc: FileProcessingError):
    """Handler for FileProcessingError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": exc.detail}}
    )

async def metadata_extraction_exception_handler(request: Request, exc: MetadataExtractionError):
    """Handler for MetadataExtractionError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.detail}}
    )

async def transaction_extraction_exception_handler(request: Request, exc: TransactionExtractionError):
    """Handler for TransactionExtractionError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.detail}}
    )

async def directory_processing_exception_handler(request: Request, exc: DirectoryProcessingError):
    """Handler for DirectoryProcessingError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": exc.detail}}
    )

async def transaction_save_exception_handler(request: Request, exc: TransactionSaveError):
    """Handler for TransactionSaveError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": exc.detail}}
    )

async def metrics_update_exception_handler(request: Request, exc: MetricsUpdateError):
    """Handler for MetricsUpdateError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": exc.detail}}
    )

async def transaction_error_handler(request: Request, exc: TransactionError):
    """Handler for TransactionError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc)}}
    )

async def transaction_create_error_handler(request: Request, exc: TransactionCreateError):
    """Handler for TransactionCreateError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc)}}
    )

async def transaction_update_error_handler(request: Request, exc: TransactionUpdateError):
    """Handler for TransactionUpdateError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc)}}
    )

async def transaction_delete_error_handler(request: Request, exc: TransactionDeleteError):
    """Handler for TransactionDeleteError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc)}}
    )

async def transaction_not_found_error_handler(request: Request, exc: TransactionNotFoundError):
    """Handler for TransactionNotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": str(exc)}}
    )

async def transaction_validation_error_handler(request: Request, exc: TransactionValidationError):
    """Handler for TransactionValidationError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": str(exc), "errors": getattr(exc, "errors", [])}}
    )

async def batch_processing_error_handler(request: Request, exc: BatchProcessingError):
    """Handler for BatchProcessingError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc), "errors": getattr(exc, "errors", [])}}
    )

async def query_execution_error_handler(request: Request, exc: QueryExecutionError):
    """Handler for QueryExecutionError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc)}}
    )

async def invalid_query_parameter_error_handler(request: Request, exc: InvalidQueryParameterError):
    """Handler for InvalidQueryParameterError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": {"message": str(exc), "parameter": getattr(exc, "parameter", None)}}
    )

def register_exception_handlers(app: FastAPI):
    """Register all exception handlers with the FastAPI application."""
    # Register existing handlers
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.add_exception_handler(FileProcessingError, file_processing_exception_handler)
    app.add_exception_handler(MetadataExtractionError, metadata_extraction_exception_handler)
    app.add_exception_handler(TransactionExtractionError, transaction_extraction_exception_handler)
    app.add_exception_handler(DirectoryProcessingError, directory_processing_exception_handler)
    app.add_exception_handler(TransactionSaveError, transaction_save_exception_handler)
    app.add_exception_handler(MetricsUpdateError, metrics_update_exception_handler)
    
    # Register new transaction error handlers
    app.add_exception_handler(TransactionError, transaction_error_handler)
    app.add_exception_handler(TransactionCreateError, transaction_create_error_handler)
    app.add_exception_handler(TransactionUpdateError, transaction_update_error_handler)
    app.add_exception_handler(TransactionDeleteError, transaction_delete_error_handler)
    app.add_exception_handler(TransactionNotFoundError, transaction_not_found_error_handler)
    app.add_exception_handler(TransactionValidationError, transaction_validation_error_handler)
    app.add_exception_handler(BatchProcessingError, batch_processing_error_handler)
    app.add_exception_handler(QueryExecutionError, query_execution_error_handler)
    app.add_exception_handler(InvalidQueryParameterError, invalid_query_parameter_error_handler)