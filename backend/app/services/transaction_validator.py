"""
Transaction validator for the Election Monitoring System.

This module provides validation services for transaction data.
"""

from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.schemas.transaction import TransactionCreate
from app.crud.transaction import transaction_crud
from app.crud.constituency import constituency_crud


class TransactionValidator:
    """
    Validator for transaction data.
    
    This class provides methods for validating transaction data against business rules.
    """
    
    def validate_transaction(self, db: Session, transaction_data: TransactionCreate) -> List[str]:
        """
        Validate a transaction.
        
        Args:
            db: Database session
            transaction_data: Transaction data to validate
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate constituency existence
        if not self._validate_constituency_exists(db, transaction_data.constituency_id):
            errors.append(f"Constituency with ID {transaction_data.constituency_id} does not exist")
        
        # Validate timestamp
        if not self._validate_timestamp(transaction_data.timestamp):
            errors.append("Timestamp is invalid or in the future")
        
        # Validate block height
        if not self._validate_block_height(transaction_data.block_height):
            errors.append("Block height must be a positive integer")
        
        # Validate raw_data structure
        if not self._validate_raw_data(transaction_data.raw_data):
            errors.append("Raw data has invalid structure")
        
        # Validate transaction type
        # Note: This is already validated by Pydantic schema, but we include it here for completeness
        if transaction_data.type not in ["blindSigIssue", "vote"]:
            errors.append("Transaction type must be one of: blindSigIssue, vote")
        
        # Validate status
        # Note: This is already validated by Pydantic schema, but we include it here for completeness
        if transaction_data.status not in ["pending", "processed", "failed"]:
            errors.append("Status must be one of: pending, processed, failed")
        
        # Validate source
        if transaction_data.source and transaction_data.source not in ["file_upload", "api", "batch"]:
            errors.append("Source must be one of: file_upload, api, batch")
        
        return errors
    
    def validate_transaction_batch(
        self, db: Session, transactions: List[TransactionCreate]
    ) -> Dict[int, List[str]]:
        """
        Validate a batch of transactions.
        
        Args:
            db: Database session
            transactions: List of transactions to validate
            
        Returns:
            Dictionary mapping transaction index to validation errors
        """
        validation_results = {}
        
        for i, transaction in enumerate(transactions):
            errors = self.validate_transaction(db, transaction)
            if errors:
                validation_results[i] = errors
        
        return validation_results
    
    def check_duplicate(self, db: Session, transaction_id: str) -> bool:
        """
        Check if a transaction with the given ID already exists.
        
        Args:
            db: Database session
            transaction_id: Transaction ID to check
            
        Returns:
            True if duplicate, False otherwise
        """
        transaction = transaction_crud.get(db, transaction_id)
        return transaction is not None
    
    def _validate_constituency_exists(self, db: Session, constituency_id: str) -> bool:
        """
        Validate that a constituency exists.
        
        Args:
            db: Database session
            constituency_id: Constituency ID to check
            
        Returns:
            True if constituency exists, False otherwise
        """
        constituency = constituency_crud.get(db, constituency_id)
        return constituency is not None
    
    def _validate_timestamp(self, timestamp: datetime) -> bool:
        """
        Validate that a timestamp is valid and not in the future.
        
        Args:
            timestamp: Timestamp to validate
            
        Returns:
            True if timestamp is valid, False otherwise
        """
        now = datetime.utcnow()
        return timestamp <= now
    
    def _validate_block_height(self, block_height: int) -> bool:
        """
        Validate that a block height is a positive integer.
        
        Args:
            block_height: Block height to validate
            
        Returns:
            True if block height is valid, False otherwise
        """
        return block_height > 0
    
    def _validate_raw_data(self, raw_data: Dict) -> bool:
        """
        Validate that raw data has a valid structure.
        
        Args:
            raw_data: Raw data to validate
            
        Returns:
            True if raw data is valid, False otherwise
        """
        # Basic validation - ensure raw_data is a dictionary
        if not isinstance(raw_data, dict):
            return False
        
        # Additional validation can be added here based on specific requirements
        # For example, checking for required fields, data types, etc.
        
        return True