"""
Election model for the Election Monitoring System.

This module defines the Election model, which represents an election event
that contains multiple constituencies.
"""

from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, UUIDMixin, TimestampMixin


class Election(Base, UUIDMixin, TimestampMixin):
    """
    Election model representing an election event.
    
    Attributes:
        id (str): Primary key, UUID
        name (str): Name of the election
        country (str): Country where the election is held
        start_date (datetime): Official start date of the election
        end_date (datetime): Official end date of the election
        status (str): Status of the election (active, completed, upcoming, scheduled)
        type (str): Type of election (presidential, parliamentary, etc.)
        description (str): Description of the election
        timezone (str): Timezone of the election
        total_constituencies (int): Total number of constituencies in this election
        created_at (datetime): Record creation timestamp
        constituencies (List[Constituency]): Constituencies in this election
    """
    
    __tablename__ = "elections"
    
    name = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="active", index=True)  # active, completed, upcoming, scheduled
    type = Column(String, default="general", index=True)  # presidential, parliamentary, etc.
    description = Column(Text, nullable=True)
    timezone = Column(String, nullable=False, default="UTC")
    total_constituencies = Column(Integer, default=0)
    
    # Relationships
    constituencies = relationship("Constituency", back_populates="election", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of the Election model."""
        return f"<Election(id='{self.id}', name='{self.name}', status='{self.status}')>"