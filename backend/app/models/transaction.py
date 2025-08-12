"""
Transaction model for the Election Monitoring System.

This module defines the Transaction model, which represents a blockchain
transaction from the voting system.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, UUIDMixin, TimestampMixin


class Transaction(Base, UUIDMixin, TimestampMixin):
    """
    Transaction model representing a blockchain transaction.
    
    Attributes:
        id (str): Primary key, UUID
        constituency_id (str): Foreign key to Constituency
        block_height (int): Blockchain block height
        timestamp (datetime): Transaction timestamp
        type (str): Transaction type (blindSigIssue, vote)
        raw_data (dict): Raw transaction data
        operation_data (dict): Processed operation data
        created_at (datetime): Record creation timestamp
        constituency (Constituency): The constituency this transaction belongs to
    """
    
    __tablename__ = "transactions"
    
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False, index=True)
    block_height = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # blindSigIssue, vote
    raw_data = Column(JSON)
    operation_data = Column(JSON)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="transactions")
    
    def __repr__(self):
        """String representation of the Transaction model."""
        return f"<Transaction(id='{self.id}', type='{self.type}', block_height={self.block_height})>"