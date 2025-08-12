"""
FileProcessingJob schemas for the Election Monitoring System.

This module provides Pydantic models for the FileProcessingJob entity.
"""

from pydantic import validator, Field
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema, ResponseBase, validate_status


class FileProcessingJobBase(BaseSchema):
    """
    Base schema for FileProcessingJob model.
    
    Attributes:
        filename (str): Name of the processed file
        status (str): Job status (processing, completed, failed)
        details (str): Processing details or error messages
        transactions_processed (int): Number of transactions processed
        started_at (datetime): Job start timestamp
        completed_at (datetime): Job completion timestamp (nullable)
    """
    
    filename: str = Field(..., description="Name of the processed file")
    status: str = Field("processing", description="Job status (processing, completed, failed)")
    details: Optional[str] = Field(None, description="Processing details or error messages")
    transactions_processed: int = Field(0, description="Number of transactions processed")
    started_at: datetime = Field(..., description="Job start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp (nullable)")
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate job status."""
        allowed_statuses = ["processing", "completed", "failed"]
        return validate_status(v, allowed_statuses)


class FileProcessingJobCreate(FileProcessingJobBase):
    """
    Schema for creating a FileProcessingJob.
    
    This schema is used for creating a new FileProcessingJob.
    """
    
    pass


class FileProcessingJobUpdate(BaseSchema):
    """
    Schema for updating a FileProcessingJob.
    
    This schema is used for updating an existing FileProcessingJob.
    All fields are optional to allow partial updates.
    """
    
    status: Optional[str] = Field(None, description="Job status (processing, completed, failed)")
    details: Optional[str] = Field(None, description="Processing details or error messages")
    transactions_processed: Optional[int] = Field(None, description="Number of transactions processed")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate job status."""
        if v is None:
            return v
        allowed_statuses = ["processing", "completed", "failed"]
        return validate_status(v, allowed_statuses)


class FileProcessingJobResponse(ResponseBase, FileProcessingJobBase):
    """
    Schema for FileProcessingJob response.
    
    This schema is used for returning a FileProcessingJob in API responses.
    """
    
    pass


class FileProcessingJobList(BaseSchema):
    """
    Schema for list of FileProcessingJobs.
    
    This schema is used for returning a list of FileProcessingJobs in API responses.
    """
    
    data: List[FileProcessingJobResponse]
    total: int
    page: int
    limit: int


class FileUploadResponse(BaseSchema):
    """
    Schema for file upload response.
    
    This schema is used for returning the result of a file upload.
    """
    
    message: str = Field(..., description="Status message")
    job_id: str = Field(..., description="ID of the created job")


class FileStatusResponse(BaseSchema):
    """
    Schema for file status response.
    
    This schema is used for returning the status of a file processing job.
    """
    
    status: str = Field(..., description="Job status (processing, completed, failed)")
    details: Optional[str] = Field(None, description="Processing details or error messages")
    transactions_processed: int = Field(0, description="Number of transactions processed")
    started_at: datetime = Field(..., description="Job start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")