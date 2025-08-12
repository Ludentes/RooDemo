"""
Base schemas for the Election Monitoring System.

This module provides base Pydantic models and common validators for the application.
"""

from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any, TypeVar, Generic, Type
from datetime import datetime
import uuid


class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.
    
    This class provides common configuration for all schemas.
    """
    
    class Config:
        """Configuration for all schemas."""
        
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


class IDSchema(BaseSchema):
    """
    Schema with ID field.
    
    This class provides a common ID field for schemas that need it.
    """
    
    id: str = Field(..., description="Unique identifier")


class TimestampSchema(BaseSchema):
    """
    Schema with timestamp fields.
    
    This class provides common timestamp fields for schemas that need them.
    """
    
    created_at: datetime = Field(..., description="Record creation timestamp")


class ResponseBase(IDSchema, TimestampSchema):
    """
    Base schema for all response models.
    
    This class combines ID and timestamp fields for response schemas.
    """
    
    pass


# Common validators
def validate_status(status: str, allowed_statuses: List[str]) -> str:
    """
    Validate that a status is in the allowed list.
    
    Args:
        status: The status to validate
        allowed_statuses: List of allowed statuses
        
    Returns:
        The validated status
        
    Raises:
        ValueError: If the status is not in the allowed list
    """
    if status not in allowed_statuses:
        raise ValueError(f"Status must be one of {allowed_statuses}")
    return status


def validate_date_range(start_date: datetime, end_date: datetime) -> None:
    """
    Validate that end_date is after start_date.
    
    Args:
        start_date: The start date
        end_date: The end date
        
    Raises:
        ValueError: If end_date is not after start_date
    """
    if end_date <= start_date:
        raise ValueError("End date must be after start date")


# Generic types for CRUD operations
T = TypeVar('T', bound=BaseSchema)


class CreateBase(Generic[T]):
    """
    Base schema for create operations.
    
    This class provides a common structure for create schemas.
    """
    
    pass


class UpdateBase(Generic[T]):
    """
    Base schema for update operations.
    
    This class provides a common structure for update schemas.
    """
    
    pass


class ListBase(Generic[T]):
    """
    Base schema for list responses.
    
    This class provides a common structure for list response schemas.
    """
    
    data: List[T]
    total: int
    page: int
    limit: int
    
    class Config:
        """Configuration for list response schemas."""
        
        from_attributes = True  # Renamed from orm_mode in Pydantic v2