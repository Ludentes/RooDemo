"""
Transaction service for the Election Monitoring System.

This module provides services for transaction processing, including saving
transactions to the database and updating constituency metrics.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.transaction import transaction_crud
from app.crud.constituency import constituency_crud
from app.models.schemas.processing_result import TransactionData
from app.models.schemas.transaction import TransactionCreate
from app.api.errors.exceptions import TransactionSaveError, MetricsUpdateError


class TransactionService:
    """
    Service for transaction processing.
    
    This class provides methods for saving transactions to the database
    and updating constituency metrics.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db: The database session
        """
        self.db = db
    
    def save_transactions(self, transactions: List[TransactionData]) -> int:
        """
        Save transactions to the database.
        
        Args:
            transactions: List of transactions to save
            
        Returns:
            Number of transactions saved
            
        Raises:
            TransactionSaveError: If saving fails
        """
        try:
            saved_count = 0
            
            print(f"Saving {len(transactions)} transactions to database")
            
            for transaction_data in transactions:
                print(f"Processing transaction: {transaction_data.transaction_id}")
                
                # Check if transaction already exists
                existing_transactions = transaction_crud.get_by_constituency(
                    db=self.db,
                    constituency_id=transaction_data.constituency_id
                )
                
                # Skip if transaction with same ID already exists
                if any(t.id == transaction_data.transaction_id for t in existing_transactions):
                    print(f"Transaction {transaction_data.transaction_id} already exists, skipping")
                    continue
                
                # Convert TransactionData to TransactionCreate
                transaction_create = TransactionCreate(
                    constituency_id=transaction_data.constituency_id,
                    block_height=transaction_data.block_height,
                    timestamp=datetime.fromisoformat(transaction_data.timestamp),
                    type=transaction_data.type,
                    raw_data=transaction_data.raw_data,
                    operation_data=transaction_data.operation_data
                )
                
                # Create transaction with the transaction_id as the ID
                from app.models.transaction import Transaction
                db_obj = Transaction(
                    id=transaction_data.transaction_id,
                    constituency_id=transaction_create.constituency_id,
                    block_height=transaction_create.block_height,
                    timestamp=transaction_create.timestamp,
                    type=transaction_create.type,
                    raw_data=transaction_create.raw_data,
                    operation_data=transaction_create.operation_data
                )
                self.db.add(db_obj)
                self.db.commit()
                self.db.refresh(db_obj)
                saved_count += 1
                print(f"Saved transaction {transaction_data.transaction_id}")
            
            print(f"Saved {saved_count} transactions to database")
            return saved_count
        except Exception as e:
            raise TransactionSaveError(f"Failed to save transactions: {e}")
    
    def update_constituency_metrics(self, constituency_id: str) -> None:
        """
        Update constituency metrics based on transactions.
        
        Args:
            constituency_id: ID of the constituency
            
        Raises:
            MetricsUpdateError: If update fails
        """
        try:
            # Get constituency
            constituency = constituency_crud.get(db=self.db, id=constituency_id)
            if not constituency:
                raise MetricsUpdateError(f"Constituency not found: {constituency_id}")
            
            # Get transactions for constituency
            transactions = transaction_crud.get_by_constituency(
                db=self.db,
                constituency_id=constituency_id
            )
            
            # Count bulletins and votes
            bulletins_issued = sum(1 for t in transactions if t.type == "blindSigIssue")
            votes_cast = sum(1 for t in transactions if t.type == "vote")
            
            # Calculate participation rate
            participation_rate = 0.0
            if constituency.registered_voters > 0 and bulletins_issued > 0:
                participation_rate = (votes_cast / constituency.registered_voters) * 100
            
            # Update constituency
            constituency.bulletins_issued = bulletins_issued
            constituency.votes_cast = votes_cast
            constituency.participation_rate = participation_rate
            constituency.last_update_time = datetime.utcnow()
            
            # Save changes
            self.db.add(constituency)
            self.db.commit()
            self.db.refresh(constituency)
        except Exception as e:
            self.db.rollback()
            raise MetricsUpdateError(f"Failed to update constituency metrics: {e}")
    
    def get_transaction_statistics(self, constituency_id: str) -> Dict[str, Any]:
        """
        Get transaction statistics for a constituency.
        
        Args:
            constituency_id: ID of the constituency
            
        Returns:
            Dictionary of transaction statistics
        """
        try:
            # Get constituency
            constituency = constituency_crud.get(db=self.db, id=constituency_id)
            if not constituency:
                return {}
            
            # Get transactions for constituency
            transactions = transaction_crud.get_by_constituency(
                db=self.db,
                constituency_id=constituency_id
            )
            
            # Count transactions by type
            transaction_counts = {}
            for t in transactions:
                transaction_counts[t.type] = transaction_counts.get(t.type, 0) + 1
            
            # Get latest transaction timestamp
            latest_timestamp = None
            if transactions:
                latest_transaction = max(transactions, key=lambda t: t.timestamp)
                latest_timestamp = latest_transaction.timestamp
            
            # Create statistics
            statistics = {
                "total_transactions": len(transactions),
                "bulletins_issued": constituency.bulletins_issued,
                "votes_cast": constituency.votes_cast,
                "participation_rate": constituency.participation_rate,
                "transaction_counts": transaction_counts,
                "latest_update": latest_timestamp,
                "registered_voters": constituency.registered_voters
            }
            
            return statistics
        except Exception as e:
            print(f"Failed to get transaction statistics: {e}")
            return {}