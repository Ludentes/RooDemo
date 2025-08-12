"""
HourlyStats model for the Election Monitoring System.

This module defines the HourlyStats model, which represents hourly
aggregated statistics for a constituency.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, UUIDMixin, TimestampMixin


class HourlyStats(Base, UUIDMixin, TimestampMixin):
    """
    HourlyStats model representing hourly aggregated statistics.
    
    Attributes:
        id (str): Primary key, UUID
        constituency_id (str): Foreign key to Constituency
        hour (datetime): Hour timestamp (rounded to hour)
        bulletins_issued (int): Number of bulletins issued in this hour
        votes_cast (int): Number of votes cast in this hour
        transaction_count (int): Total transactions in this hour
        bulletin_velocity (float): Rate of bulletin issuance per hour
        vote_velocity (float): Rate of vote casting per hour
        created_at (datetime): Record creation timestamp
        constituency (Constituency): The constituency these stats belong to
    """
    
    __tablename__ = "hourly_stats"
    
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False, index=True)
    hour = Column(DateTime, nullable=False, index=True)  # Rounded to hour
    
    bulletins_issued = Column(Integer, default=0)
    votes_cast = Column(Integer, default=0)
    transaction_count = Column(Integer, default=0)
    bulletin_velocity = Column(Float, default=0.0)  # per hour
    vote_velocity = Column(Float, default=0.0)  # per hour
    
    # Relationships
    constituency = relationship("Constituency", back_populates="hourly_stats")
    
    def __repr__(self):
        """String representation of the HourlyStats model."""
        return f"<HourlyStats(id='{self.id}', hour='{self.hour}', bulletins={self.bulletins_issued}, votes={self.votes_cast})>"
    
    @classmethod
    def round_hour(cls, dt: datetime) -> datetime:
        """
        Round a datetime to the nearest hour.
        
        Args:
            dt (datetime): The datetime to round
            
        Returns:
            datetime: The rounded datetime
        """
        return dt.replace(minute=0, second=0, microsecond=0)