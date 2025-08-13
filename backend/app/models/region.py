"""
Region model for the Election Monitoring System.

This module provides the Region model for storing region information.
"""

from sqlalchemy import Column, String
from app.models.database import Base


class Region(Base):
    """
    Region model for storing region information.
    
    Attributes:
        id (str): Region ID (e.g., "90")
        name (str): Region name (e.g., "Пермский край")
        country (str): Country name (default: "Russia")
    """
    
    __tablename__ = "regions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Russia")
    
    def __repr__(self):
        """Return a string representation of the Region instance."""
        return f"Region(id={self.id}, name={self.name}, country={self.country})"