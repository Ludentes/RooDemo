from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from app.api.errors.exceptions import NotFoundError, ValidationError, DatabaseError

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

def register_exception_handlers(app: FastAPI):
    """Register all exception handlers with the FastAPI application."""
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(DatabaseError, database_exception_handler)