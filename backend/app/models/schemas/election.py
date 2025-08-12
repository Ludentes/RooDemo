"""
Election schemas for the Election Monitoring System.

This module provides Pydantic models for the Election entity.
"""

from pydantic import validator, Field
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema, ResponseBase, validate_status, IDSchema, TimestampSchema


class ElectionBase(BaseSchema):
    """
    Base schema for Election model.
    
    Attributes:
        name (str): Name of the election
        country (str): Country where the election is held
        start_date (datetime): Official start date of the election
        end_date (datetime): Official end date of the election
        status (str): Status of the election (active, completed, upcoming, scheduled)
        type (str): Type of election (presidential, parliamentary, etc.)
        description (str): Description of the election
        timezone (str): Timezone of the election
    """
    
    name: str = Field(..., description="Name of the election")
    country: str = Field(..., description="Country where the election is held")
    start_date: datetime = Field(..., description="Official start date of the election")
    end_date: datetime = Field(..., description="Official end date of the election")
    status: str = Field("scheduled", description="Status of the election (active, completed, upcoming, scheduled)")
    type: str = Field("general", description="Type of election (presidential, parliamentary, etc.)")
    description: Optional[str] = Field(None, description="Description of the election")
    timezone: str = Field("UTC", description="Timezone of the election")
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate election status."""
        allowed_statuses = ["active", "completed", "upcoming", "scheduled"]
        return validate_status(v, allowed_statuses)
    
    @validator("type")
    def validate_type(cls, v: str) -> str:
        """Validate election type."""
        allowed_types = ["presidential", "parliamentary", "general", "local", "referendum"]
        return validate_status(v, allowed_types)
    
    @validator("end_date")
    def validate_end_date(cls, v: datetime, values: dict) -> datetime:
        """Validate that end_date is after start_date."""
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class ElectionCreate(ElectionBase, IDSchema):
    """
    Schema for creating an Election.
    
    This schema is used for creating a new Election.
    """
    
    pass


class ElectionUpdate(BaseSchema):
    """
    Schema for updating an Election.
    
    This schema is used for updating an existing Election.
    All fields are optional to allow partial updates.
    """
    
    name: Optional[str] = Field(None, description="Name of the election")
    country: Optional[str] = Field(None, description="Country where the election is held")
    start_date: Optional[datetime] = Field(None, description="Official start date of the election")
    end_date: Optional[datetime] = Field(None, description="Official end date of the election")
    status: Optional[str] = Field(None, description="Status of the election (active, completed, upcoming, scheduled)")
    type: Optional[str] = Field(None, description="Type of election (presidential, parliamentary, etc.)")
    description: Optional[str] = Field(None, description="Description of the election")
    timezone: Optional[str] = Field(None, description="Timezone of the election")
    total_constituencies: Optional[int] = Field(None, description="Total number of constituencies in this election")
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate election status."""
        if v is None:
            return v
        allowed_statuses = ["active", "completed", "upcoming", "scheduled"]
        return validate_status(v, allowed_statuses)
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate election type."""
        if v is None:
            return v
        allowed_types = ["presidential", "parliamentary", "general", "local", "referendum"]
        return validate_status(v, allowed_types)
    
    @validator("end_date")
    def validate_end_date(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        """Validate that end_date is after start_date."""
        if v is None:
            return v
        if "start_date" in values and values["start_date"] is not None and v <= values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class ElectionInDB(ElectionBase, IDSchema, TimestampSchema):
    """
    Schema for Election in database.
    
    This schema is used for representing an Election as stored in the database.
    """
    
    total_constituencies: int = Field(0, description="Total number of constituencies in this election")


class ElectionResponse(ElectionInDB):
    """
    Schema for Election response.
    
    This schema is used for returning an Election in API responses.
    """
    
    constituencies: List = Field([], description="Constituencies in this election")


class ElectionList(BaseSchema):
    """
    Schema for list of Elections.
    
    This schema is used for returning a list of Elections in API responses.
    """
    
    data: List[ElectionResponse]
    total: int
    page: int
    limit: int