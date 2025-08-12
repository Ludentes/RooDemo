"""
Constituency schemas for the Election Monitoring System.

This module provides Pydantic models for the Constituency entity.
"""

from pydantic import validator, Field
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema, ResponseBase, validate_status


class ConstituencyBase(BaseSchema):
    """
    Base schema for Constituency model.
    
    Attributes:
        election_id (str): ID of the election this constituency belongs to
        name (str): Name of the constituency
        region (str): Geographic region
        type (str): Type of constituency (urban, rural, suburban)
        registered_voters (int): Number of registered voters
        status (str): Status of the constituency (active, offline, completed)
    """
    
    election_id: str = Field(..., description="ID of the election this constituency belongs to")
    name: str = Field(..., description="Name of the constituency")
    region: str = Field(..., description="Geographic region")
    type: str = Field(..., description="Type of constituency (urban, rural, suburban)")
    registered_voters: int = Field(0, description="Number of registered voters")
    status: str = Field("active", description="Status of the constituency (active, offline, completed)")
    
    @validator("type")
    def validate_type(cls, v: str) -> str:
        """Validate constituency type."""
        allowed_types = ["urban", "rural", "suburban"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate constituency status."""
        allowed_statuses = ["active", "offline", "completed"]
        return validate_status(v, allowed_statuses)


class ConstituencyCreate(ConstituencyBase):
    """
    Schema for creating a Constituency.
    
    This schema is used for creating a new Constituency.
    
    Attributes:
        id (str): Smart contract address (primary key)
    """
    
    id: str = Field(..., description="Smart contract address (primary key)")


class ConstituencyUpdate(BaseSchema):
    """
    Schema for updating a Constituency.
    
    This schema is used for updating an existing Constituency.
    All fields are optional to allow partial updates.
    """
    
    name: Optional[str] = Field(None, description="Name of the constituency")
    region: Optional[str] = Field(None, description="Geographic region")
    type: Optional[str] = Field(None, description="Type of constituency (urban, rural, suburban)")
    registered_voters: Optional[int] = Field(None, description="Number of registered voters")
    status: Optional[str] = Field(None, description="Status of the constituency (active, offline, completed)")
    bulletins_issued: Optional[int] = Field(None, description="Number of electronic bulletins issued")
    votes_cast: Optional[int] = Field(None, description="Number of votes cast")
    participation_rate: Optional[float] = Field(None, description="Percentage of registered voters who voted")
    anomaly_score: Optional[float] = Field(None, description="Calculated anomaly score (0-1)")
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate constituency type."""
        if v is None:
            return v
        allowed_types = ["urban", "rural", "suburban"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate constituency status."""
        if v is None:
            return v
        allowed_statuses = ["active", "offline", "completed"]
        return validate_status(v, allowed_statuses)


class ConstituencyResponse(ResponseBase, ConstituencyBase):
    """
    Schema for Constituency response.
    
    This schema is used for returning a Constituency in API responses.
    
    Attributes:
        id (str): Smart contract address (primary key)
        last_update_time (datetime): Last data update timestamp
        bulletins_issued (int): Number of electronic bulletins issued
        votes_cast (int): Number of votes cast
        participation_rate (float): Percentage of registered voters who voted
        anomaly_score (float): Calculated anomaly score (0-1)
    """
    
    id: str = Field(..., description="Smart contract address (primary key)")
    last_update_time: datetime = Field(..., description="Last data update timestamp")
    bulletins_issued: int = Field(0, description="Number of electronic bulletins issued")
    votes_cast: int = Field(0, description="Number of votes cast")
    participation_rate: float = Field(0.0, description="Percentage of registered voters who voted")
    anomaly_score: float = Field(0.0, description="Calculated anomaly score (0-1)")


class ConstituencyList(BaseSchema):
    """
    Schema for list of Constituencies.
    
    This schema is used for returning a list of Constituencies in API responses.
    """
    
    data: List[ConstituencyResponse]
    total: int
    page: int
    limit: int


class ConstituencyDetail(ConstituencyResponse):
    """
    Schema for detailed Constituency information.
    
    This schema is used for returning detailed information about a Constituency,
    including related entities like hourly stats, transactions, and alerts.
    """
    
    # These fields will be populated by the API endpoint
    # hourly_stats: List["HourlyStatsResponse"] = []
    # recent_transactions: List["TransactionResponse"] = []
    # alerts: List["AlertResponse"] = []
    
    class Config:
        """Configuration for ConstituencyDetail schema."""
        
        orm_mode = True