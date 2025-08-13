"""
Transaction schemas for the Election Monitoring System.

This module provides Pydantic models for the Transaction entity.
"""

from pydantic import validator, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import BaseSchema, ResponseBase, validate_status


class TransactionBase(BaseSchema):
    """
    Base schema for Transaction model.
    
    Attributes:
        constituency_id (str): ID of the constituency this transaction belongs to
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
    """
    
    constituency_id: str = Field(..., description="ID of the constituency this transaction belongs to")
    block_height: int = Field(..., description="Blockchain block height")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    type: str = Field(..., description="Transaction type (blindSigIssue, vote)")
    raw_data: Dict[str, Any] = Field(..., description="Raw transaction data")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="Processed operation data")
    
    # New fields for status tracking and anomaly detection
    status: str = Field("processed", description="Transaction status (pending, processed, failed)")
    anomaly_detected: bool = Field(False, description="Whether an anomaly was detected")
    anomaly_reason: Optional[str] = Field(None, description="Reason for the anomaly")
    
    # New fields for source tracking
    source: Optional[str] = Field(None, description="Source of the transaction (file_upload, api, batch)")
    file_id: Optional[str] = Field(None, description="ID of the file that contained this transaction")
    
    @validator("type")
    def validate_type(cls, v: str) -> str:
        """Validate transaction type."""
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate transaction status."""
        allowed_statuses = ["pending", "processed", "failed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v
    
    @validator("source")
    def validate_source(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction source."""
        if v is None:
            return v
        allowed_sources = ["file_upload", "api", "batch"]
        if v not in allowed_sources:
            raise ValueError(f"Source must be one of {allowed_sources}")
        return v


class TransactionCreate(TransactionBase):
    """
    Schema for creating a Transaction.
    
    This schema is used for creating a new Transaction.
    """
    
    pass


class TransactionUpdate(BaseSchema):
    """
    Schema for updating a Transaction.
    
    This schema is used for updating an existing Transaction.
    All fields are optional to allow partial updates.
    """
    
    block_height: Optional[int] = Field(None, description="Blockchain block height")
    timestamp: Optional[datetime] = Field(None, description="Transaction timestamp")
    type: Optional[str] = Field(None, description="Transaction type (blindSigIssue, vote)")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw transaction data")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="Processed operation data")
    status: Optional[str] = Field(None, description="Transaction status (pending, processed, failed)")
    anomaly_detected: Optional[bool] = Field(None, description="Whether an anomaly was detected")
    anomaly_reason: Optional[str] = Field(None, description="Reason for the anomaly")
    source: Optional[str] = Field(None, description="Source of the transaction (file_upload, api, batch)")
    file_id: Optional[str] = Field(None, description="ID of the file that contained this transaction")
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction type."""
        if v is None:
            return v
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction status."""
        if v is None:
            return v
        allowed_statuses = ["pending", "processed", "failed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v
    
    @validator("source")
    def validate_source(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction source."""
        if v is None:
            return v
        allowed_sources = ["file_upload", "api", "batch"]
        if v not in allowed_sources:
            raise ValueError(f"Source must be one of {allowed_sources}")
        return v


class TransactionResponse(ResponseBase, TransactionBase):
    """
    Schema for Transaction response.
    
    This schema is used for returning a Transaction in API responses.
    """
    
    pass


class TransactionList(BaseSchema):
    """
    Schema for list of Transactions.
    
    This schema is used for returning a list of Transactions in API responses.
    """
    
    data: List[TransactionResponse]
    total: int
    page: int
    limit: int


class TransactionStats(BaseSchema):
    """
    Schema for Transaction statistics.
    
    This schema is used for returning statistics about Transactions.
    """
    
    total_transactions: int = Field(..., description="Total number of transactions")
    total_bulletins: int = Field(..., description="Total number of bulletin transactions")
    total_votes: int = Field(..., description="Total number of vote transactions")
    transactions_per_hour: float = Field(..., description="Average transactions per hour")
    bulletins_per_hour: float = Field(..., description="Average bulletins per hour")
    votes_per_hour: float = Field(..., description="Average votes per hour")


class TransactionQueryParams(BaseSchema):
    """
    Schema for transaction query parameters.
    
    This schema is used for filtering transactions in API requests.
    """
    
    constituency_id: Optional[str] = Field(None, description="Filter by constituency ID")
    type: Optional[str] = Field(None, description="Filter by transaction type")
    start_time: Optional[datetime] = Field(None, description="Filter by start time")
    end_time: Optional[datetime] = Field(None, description="Filter by end time")
    status: Optional[str] = Field(None, description="Filter by status")
    anomaly_detected: Optional[bool] = Field(None, description="Filter by anomaly detection")
    source: Optional[str] = Field(None, description="Filter by source")
    file_id: Optional[str] = Field(None, description="Filter by file ID")
    page: int = Field(1, description="Page number")
    limit: int = Field(100, description="Items per page")
    sort_by: str = Field("timestamp", description="Field to sort by")
    sort_order: str = Field("desc", description="Sort order (asc, desc)")
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction type."""
        if v is None:
            return v
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
        return v
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction status."""
        if v is None:
            return v
        allowed_statuses = ["pending", "processed", "failed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v
    
    @validator("source")
    def validate_source(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction source."""
        if v is None:
            return v
        allowed_sources = ["file_upload", "api", "batch"]
        if v not in allowed_sources:
            raise ValueError(f"Source must be one of {allowed_sources}")
        return v
    
    @validator("sort_by")
    def validate_sort_by(cls, v: str) -> str:
        """Validate sort_by field."""
        allowed_fields = ["timestamp", "block_height", "type", "status", "created_at"]
        if v not in allowed_fields:
            raise ValueError(f"sort_by must be one of {allowed_fields}")
        return v
    
    @validator("sort_order")
    def validate_sort_order(cls, v: str) -> str:
        """Validate sort_order field."""
        allowed_orders = ["asc", "desc"]
        if v not in allowed_orders:
            raise ValueError(f"sort_order must be one of {allowed_orders}")
        return v


class TransactionBatchRequest(BaseSchema):
    """
    Schema for batch transaction request.
    
    This schema is used for creating multiple transactions in a batch.
    """
    
    transactions: List[TransactionCreate] = Field(..., description="List of transactions to create")


class TransactionBatchResponse(BaseSchema):
    """
    Schema for batch transaction response.
    
    This schema is used for returning the result of a batch transaction operation.
    """
    
    success: bool = Field(..., description="Whether the operation was successful")
    processed: int = Field(..., description="Number of transactions processed")
    failed: int = Field(..., description="Number of transactions that failed")
    errors: List[Dict[str, Any]] = Field([], description="List of errors")