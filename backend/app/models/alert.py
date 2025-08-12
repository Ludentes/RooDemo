"""
Alert model for the Election Monitoring System.

This module defines the Alert model, which represents a detected anomaly
or issue requiring attention.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Dict, Any, Optional

from .database import Base, UUIDMixin, TimestampMixin


class Alert(Base, UUIDMixin, TimestampMixin):
    """
    Alert model representing a detected anomaly.
    
    Attributes:
        id (str): Primary key, UUID
        constituency_id (str): Foreign key to Constituency
        type (str): Alert type (votes_exceed_bulletins, unusual_spike, etc.)
        severity (str): Alert severity (critical, warning, info)
        status (str): Alert status (active, investigating, resolved, snoozed)
        title (str): Short alert title
        description (str): Detailed alert description
        details (dict): Additional alert details
        notes (list): List of investigation notes
        created_at (datetime): Record creation timestamp
        detected_at (datetime): When the anomaly was detected
        resolved_at (datetime): When the alert was resolved (nullable)
        assigned_to (str): Person assigned to investigate (nullable)
        constituency (Constituency): The constituency this alert belongs to
    """
    
    __tablename__ = "alerts"
    
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # votes_exceed_bulletins, unusual_spike, etc.
    severity = Column(String, nullable=False, index=True)  # critical, warning, info
    status = Column(String, default="active", index=True)  # active, investigating, resolved, snoozed
    
    title = Column(String, nullable=False)
    description = Column(Text)
    details = Column(JSON)
    notes = Column(JSON, default=list)  # List of note strings
    
    detected_at = Column(DateTime, nullable=False, index=True)
    resolved_at = Column(DateTime)
    assigned_to = Column(String)
    
    # Relationships
    constituency = relationship("Constituency", back_populates="alerts")
    
    def __repr__(self):
        """String representation of the Alert model."""
        return f"<Alert(id='{self.id}', type='{self.type}', severity='{self.severity}', status='{self.status}')>"
    
    def add_note(self, note: str) -> None:
        """
        Add a note to the alert.
        
        Args:
            note (str): The note to add
        """
        if self.notes is None:
            self.notes = []
        self.notes.append(note)