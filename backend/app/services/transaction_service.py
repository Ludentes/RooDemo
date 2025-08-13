"""
Transaction service for the Election Monitoring System.

This module provides services for transaction processing, including saving
transactions to the database and updating constituency metrics.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.transaction import transaction_crud
from app.crud.constituency import constituency_crud
from app.models.schemas.processing_result import TransactionData
from app.models.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.models.transaction import Transaction
from app.api.errors.exceptions import (
    TransactionSaveError, MetricsUpdateError, TransactionCreateError,
    TransactionUpdateError, TransactionDeleteError, TransactionValidationError
)

# Set up logging
logger = logging.getLogger(__name__)


class TransactionService:
    """
    Service for transaction processing.
    
    This class provides methods for saving transactions to the database,
    updating constituency metrics, and managing transactions.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db: The database session
        """
        self.db = db
        # Lazy import to avoid circular dependencies
        from app.services.transaction_validator import TransactionValidator
        self.validator = TransactionValidator()
    
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
            
            logger.info(f"Saving {len(transactions)} transactions to database")
            
            for transaction_data in transactions:
                logger.debug(f"Processing transaction: {transaction_data.transaction_id}")
                
                # Check if transaction already exists using validator
                if self.validator.check_duplicate(self.db, transaction_data.transaction_id):
                    logger.debug(f"Transaction {transaction_data.transaction_id} already exists, skipping")
                    continue
                
                # Convert TransactionData to TransactionCreate
                transaction_create = TransactionCreate(
                    constituency_id=transaction_data.constituency_id,
                    block_height=transaction_data.block_height,
                    timestamp=datetime.fromisoformat(transaction_data.timestamp),
                    type=transaction_data.type,
                    raw_data=transaction_data.raw_data,
                    operation_data=transaction_data.operation_data,
                    status="processed",
                    source="file_upload",
                    file_id=getattr(transaction_data, 'file_id', None)
                )
                
                # Validate transaction data
                errors = self.validator.validate_transaction(self.db, transaction_create)
                if errors:
                    logger.warning(f"Transaction {transaction_data.transaction_id} validation failed: {errors}")
                    continue
                
                # Create transaction with the transaction_id as the ID
                from app.models.transaction import Transaction
                db_obj = Transaction(
                    id=transaction_data.transaction_id,
                    constituency_id=transaction_create.constituency_id,
                    block_height=transaction_create.block_height,
                    timestamp=transaction_create.timestamp,
                    type=transaction_create.type,
                    raw_data=transaction_create.raw_data,
                    operation_data=transaction_create.operation_data,
                    status=transaction_create.status,
                    source=transaction_create.source,
                    file_id=transaction_create.file_id
                )
                self.db.add(db_obj)
                self.db.commit()
                self.db.refresh(db_obj)
                saved_count += 1
                logger.debug(f"Saved transaction {transaction_data.transaction_id}")
            
            logger.info(f"Saved {saved_count} transactions to database")
            return saved_count
        except Exception as e:
            logger.exception("Failed to save transactions")
            self.db.rollback()
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
            
            logger.info(
                f"Updated metrics for constituency {constituency_id}: "
                f"bulletins_issued={bulletins_issued}, votes_cast={votes_cast}, "
                f"participation_rate={participation_rate:.2f}%"
            )
        except Exception as e:
            logger.exception(f"Failed to update constituency metrics for {constituency_id}")
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
                logger.warning(f"Constituency not found: {constituency_id}")
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
            
            logger.info(f"Retrieved statistics for constituency {constituency_id}")
            return statistics
        except Exception as e:
            logger.exception(f"Failed to get transaction statistics for {constituency_id}")
            return {}
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """
        Get a transaction by ID.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            Transaction or None if not found
        """
        try:
            transaction = transaction_crud.get(db=self.db, id=transaction_id)
            return transaction
        except Exception as e:
            logger.exception(f"Failed to get transaction {transaction_id}")
            return None
    
    def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction_data: Transaction data
            
        Returns:
            Created transaction
            
        Raises:
            TransactionCreateError: If creation fails
            TransactionValidationError: If validation fails
        """
        try:
            # Validate transaction data
            errors = self.validator.validate_transaction(self.db, transaction_data)
            if errors:
                raise TransactionValidationError(f"Transaction validation failed: {', '.join(errors)}")
            
            # Check for duplicate
            if hasattr(transaction_data, 'id') and transaction_data.id:
                if self.validator.check_duplicate(self.db, transaction_data.id):
                    raise TransactionValidationError(f"Transaction with ID {transaction_data.id} already exists")
            
            # Create transaction
            transaction = transaction_crud.create(db=self.db, obj_in=transaction_data)
            logger.info(f"Created transaction {transaction.id}")
            return transaction
        except TransactionValidationError as e:
            logger.warning(str(e))
            raise
        except Exception as e:
            logger.exception("Failed to create transaction")
            self.db.rollback()
            raise TransactionCreateError(f"Failed to create transaction: {e}")
    
    def update_transaction(self, transaction_id: str, transaction_data: TransactionUpdate) -> Optional[Transaction]:
        """
        Update a transaction.
        
        Args:
            transaction_id: ID of the transaction
            transaction_data: Transaction data
            
        Returns:
            Updated transaction or None if not found
            
        Raises:
            TransactionUpdateError: If update fails
        """
        try:
            # Get transaction
            transaction = transaction_crud.get(db=self.db, id=transaction_id)
            if not transaction:
                logger.warning(f"Transaction not found: {transaction_id}")
                return None
            
            # Update transaction
            transaction = transaction_crud.update(db=self.db, id=transaction_id, obj_in=transaction_data)
            logger.info(f"Updated transaction {transaction_id}")
            return transaction
        except Exception as e:
            logger.exception(f"Failed to update transaction {transaction_id}")
            self.db.rollback()
            raise TransactionUpdateError(f"Failed to update transaction: {e}")
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """
        Delete a transaction.
        
        Args:
            transaction_id: ID of the transaction
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            TransactionDeleteError: If deletion fails
        """
        try:
            # Get transaction
            transaction = transaction_crud.get(db=self.db, id=transaction_id)
            if not transaction:
                logger.warning(f"Transaction not found: {transaction_id}")
                return False
            
            # Delete transaction
            transaction_crud.remove(db=self.db, id=transaction_id)
            logger.info(f"Deleted transaction {transaction_id}")
            return True
        except Exception as e:
            logger.exception(f"Failed to delete transaction {transaction_id}")
            self.db.rollback()
            raise TransactionDeleteError(f"Failed to delete transaction: {e}")
    
    def get_transactions(
        self,
        constituency_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: Optional[str] = None,
        anomaly_detected: Optional[bool] = None,
        source: Optional[str] = None,
        file_id: Optional[str] = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Tuple[List[Transaction], int]:
        """
        Get transactions with filtering and pagination.
        
        Args:
            constituency_id: Filter by constituency ID
            transaction_type: Filter by transaction type
            start_time: Filter by start time
            end_time: Filter by end time
            status: Filter by status
            anomaly_detected: Filter by anomaly detection
            source: Filter by source
            file_id: Filter by file ID
            page: Page number
            limit: Items per page
            sort_by: Field to sort by
            sort_order: Sort order (asc, desc)
            
        Returns:
            Tuple of (transactions, total_count)
        """
        try:
            transactions, total = transaction_crud.get_transactions_with_filters(
                db=self.db,
                constituency_id=constituency_id,
                transaction_type=transaction_type,
                start_time=start_time,
                end_time=end_time,
                status=status,
                anomaly_detected=anomaly_detected,
                source=source,
                file_id=file_id,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order
            )
            logger.info(f"Retrieved {len(transactions)} transactions (total: {total})")
            return transactions, total
        except Exception as e:
            logger.exception("Failed to get transactions")
            return [], 0
    
    def process_transaction_batch(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a batch of transactions.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Validate transactions
            validation_results = self.validator.validate_transaction_batch(self.db, transactions)
            
            # Create batch
            result = transaction_crud.create_batch(db=self.db, obj_in_list=transactions)
            
            # Add validation errors to result
            for index, errors in validation_results.items():
                if index < len(result["errors"]):
                    result["errors"][index]["validation_errors"] = errors
                else:
                    result["errors"].append({
                        "index": index,
                        "validation_errors": errors
                    })
            
            logger.info(f"Processed {result['processed']} transactions in batch (failed: {result['failed']})")
            return result
        except Exception as e:
            logger.exception("Failed to process transaction batch")
            self.db.rollback()
            raise TransactionSaveError(f"Failed to process transaction batch: {e}")