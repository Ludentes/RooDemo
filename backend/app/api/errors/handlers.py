from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from app.api.errors.exceptions import (
    NotFoundError, ValidationError, DatabaseError,
    FileProcessingError, MetadataExtractionError, TransactionExtractionError,
    DirectoryProcessingError, TransactionSaveError, MetricsUpdateError
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

def register_exception_handlers(app: FastAPI):
    """Register all exception handlers with the FastAPI application."""
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.add_exception_handler(FileProcessingError, file_processing_exception_handler)
    app.add_exception_handler(MetadataExtractionError, metadata_extraction_exception_handler)
    app.add_exception_handler(TransactionExtractionError, transaction_extraction_exception_handler)
    app.add_exception_handler(DirectoryProcessingError, directory_processing_exception_handler)
    app.add_exception_handler(TransactionSaveError, transaction_save_exception_handler)
    app.add_exception_handler(MetricsUpdateError, metrics_update_exception_handler)