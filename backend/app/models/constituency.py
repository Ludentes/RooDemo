"""
Constituency model for the Election Monitoring System.

This module defines the Constituency model, which represents a voting district
with its own smart contract.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, TimestampMixin


class Constituency(Base, TimestampMixin):
    """
    Constituency model representing a voting district.
    
    Attributes:
        id (str): Primary key, smart contract address
        election_id (str): Foreign key to Election
        name (str): Name of the constituency
        region (str): Geographic region
        type (str): Type of constituency (urban, rural, suburban, district)
        registered_voters (int): Number of registered voters
        status (str): Status of the constituency (active, offline, completed)
        last_update_time (datetime): Last data update timestamp
        created_at (datetime): Record creation timestamp
        bulletins_issued (int): Number of electronic bulletins issued
        votes_cast (int): Number of votes cast
        participation_rate (float): Percentage of registered voters who voted
        anomaly_score (float): Calculated anomaly score (0-1)
        election (Election): The election this constituency belongs to
        transactions (List[Transaction]): Transactions in this constituency
        alerts (List[Alert]): Alerts for this constituency
        hourly_stats (List[HourlyStats]): Hourly statistics for this constituency
    """
    
    __tablename__ = "constituencies"
    
    id = Column(String, primary_key=True)  # Smart contract address
    election_id = Column(String, ForeignKey("elections.id"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    type = Column(String, default="district", nullable=False, index=True)  # urban, rural, suburban, district
    registered_voters = Column(Integer, default=0)
    status = Column(String, default="inactive", index=True)  # active, offline, completed, inactive
    last_update_time = Column(DateTime, default=datetime.utcnow)
    
    # Calculated fields (updated by background jobs)
    bulletins_issued = Column(Integer, default=0)
    votes_cast = Column(Integer, default=0)
    participation_rate = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0)
    
    # Relationships
    election = relationship("Election", back_populates="constituencies")
    transactions = relationship("Transaction", back_populates="constituency", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="constituency", cascade="all, delete-orphan")
    hourly_stats = relationship("HourlyStats", back_populates="constituency", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of the Constituency model."""
        return f"<Constituency(id='{self.id}', name='{self.name}', region='{self.region}', status='{self.status}')>"