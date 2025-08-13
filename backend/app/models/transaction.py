"""
Transaction model for the Election Monitoring System.

This module defines the Transaction model, which represents a blockchain
transaction from the voting system.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Boolean, Index
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
        status (str): Transaction status (pending, processed, failed)
        anomaly_detected (bool): Whether an anomaly was detected
        anomaly_reason (str): Reason for the anomaly
        source (str): Source of the transaction (file_upload, api, batch)
        file_id (str): ID of the file that contained this transaction
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
    
    # New fields for status tracking and anomaly detection
    status = Column(String, default="processed", nullable=False, index=True)
    anomaly_detected = Column(Boolean, default=False, nullable=False, index=True)
    anomaly_reason = Column(String, nullable=True)
    
    # New fields for source tracking
    source = Column(String, nullable=True, index=True)
    file_id = Column(String, nullable=True, index=True)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="transactions")
    
    # Composite indexes for improved query performance
    __table_args__ = (
        Index('ix_transactions_constituency_timestamp', 'constituency_id', 'timestamp'),
    )
    
    def __repr__(self):
        """String representation of the Transaction model."""
        return f"<Transaction(id='{self.id}', type='{self.type}', status='{self.status}', block_height={self.block_height})>"