"""
FileProcessingJob model for the Election Monitoring System.

This module defines the FileProcessingJob model, which tracks the status
of CSV file processing jobs.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime

from .database import Base, UUIDMixin


class FileProcessingJob(Base, UUIDMixin):
    """
    FileProcessingJob model tracking CSV file processing.
    
    Attributes:
        id (str): Primary key, UUID
        filename (str): Name of the processed file
        status (str): Job status (processing, completed, failed)
        details (str): Processing details or error messages
        transactions_processed (int): Number of transactions processed
        started_at (datetime): Job start timestamp
        completed_at (datetime): Job completion timestamp (nullable)
    """
    
    __tablename__ = "file_processing_jobs"
    
    filename = Column(String, nullable=False, index=True)
    status = Column(String, default="processing", index=True)  # processing, completed, failed
    details = Column(Text)
    transactions_processed = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        """String representation of the FileProcessingJob model."""
        return f"<FileProcessingJob(id='{self.id}', filename='{self.filename}', status='{self.status}')>"
    
    def mark_completed(self) -> None:
        """Mark the job as completed and set the completed_at timestamp."""
        self.status = "completed"
        self.completed_at = datetime.utcnow()
    
    def mark_failed(self, error_details: str) -> None:
        """
        Mark the job as failed and set the error details.
        
        Args:
            error_details (str): Details about the error
        """
        self.status = "failed"
        self.details = error_details
        self.completed_at = datetime.utcnow()
    
    def increment_processed_count(self, count: int = 1) -> None:
        """
        Increment the processed transaction count.
        
        Args:
            count (int): Number of transactions to add to the count
        """
        self.transactions_processed += count