"""
Region schemas for the Election Monitoring System.

This module provides Pydantic schemas for validating region data.
"""

from pydantic import BaseModel, Field


class RegionBase(BaseModel):
    """
    Base schema for Region data.
    
    Attributes:
        id (str): Region ID (e.g., "90")
        name (str): Region name (e.g., "Пермский край")
        country (str): Country name (default: "Russia")
    """
    
    id: str = Field(..., description="Region ID (e.g., '90')")
    name: str = Field(..., description="Region name (e.g., 'Пермский край')")
    country: str = Field(default="Russia", description="Country name")


class RegionCreate(RegionBase):
    """Schema for creating a new Region."""
    pass


class RegionUpdate(RegionBase):
    """Schema for updating an existing Region."""
    pass


class Region(RegionBase):
    """
    Schema for Region response.
    
    This schema is used for returning Region data from the API.
    """
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "90",
                "name": "Пермский край",
                "country": "Russia"
            }
        }