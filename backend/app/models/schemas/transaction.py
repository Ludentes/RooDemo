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
    """
    
    constituency_id: str = Field(..., description="ID of the constituency this transaction belongs to")
    block_height: int = Field(..., description="Blockchain block height")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    type: str = Field(..., description="Transaction type (blindSigIssue, vote)")
    raw_data: Dict[str, Any] = Field(..., description="Raw transaction data")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="Processed operation data")
    
    @validator("type")
    def validate_type(cls, v: str) -> str:
        """Validate transaction type."""
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
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
    
    @validator("type")
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate transaction type."""
        if v is None:
            return v
        allowed_types = ["blindSigIssue", "vote"]
        if v not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}")
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