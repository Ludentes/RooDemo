"""
Transaction CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the Transaction model.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from .base import BaseCRUD
from app.models.transaction import Transaction
from app.models.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionCRUD(BaseCRUD[Transaction, TransactionCreate, TransactionUpdate]):
    """
    CRUD operations for Transaction model.
    
    This class provides CRUD operations specific to the Transaction model.
    """
    
    def get_by_constituency(self, db: Session, *, constituency_id: str) -> List[Transaction]:
        """
        Get transactions by constituency ID.
        
        Args:
            db: Database session
            constituency_id: ID of the constituency to get transactions for
            
        Returns:
            List of transactions for the constituency
        """
        return db.query(Transaction).filter(Transaction.constituency_id == constituency_id).all()
    
    def get_by_election(self, db: Session, *, election_id: str) -> List[Transaction]:
        """
        Get transactions by election ID.
        
        Args:
            db: Database session
            election_id: ID of the election to get transactions for
            
        Returns:
            List of transactions for the election
        """
        return db.query(Transaction).filter(Transaction.election_id == election_id).all()
    
    def get_by_type(self, db: Session, *, type: str) -> List[Transaction]:
        """
        Get transactions by type.
        
        Args:
            db: Database session
            type: Type of transactions to get
            
        Returns:
            List of transactions of the specified type
        """
        return db.query(Transaction).filter(Transaction.type == type).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Transaction]:
        """
        Get transactions by status.
        
        Args:
            db: Database session
            status: Status of transactions to get
            
        Returns:
            List of transactions with the specified status
        """
        return db.query(Transaction).filter(Transaction.status == status).all()
    
    def get_by_time_range(
        self, db: Session, *, start_time: datetime, end_time: datetime
    ) -> List[Transaction]:
        """
        Get transactions within a time range.
        
        Args:
            db: Database session
            start_time: Start time of the range
            end_time: End time of the range
            
        Returns:
            List of transactions within the time range
        """
        return db.query(Transaction).filter(
            Transaction.timestamp >= start_time,
            Transaction.timestamp <= end_time
        ).all()
    
    def get_latest(self, db: Session, *, limit: int = 10) -> List[Transaction]:
        """
        Get the latest transactions.
        
        Args:
            db: Database session
            limit: Maximum number of transactions to return
            
        Returns:
            List of the latest transactions
        """
        return db.query(Transaction).order_by(desc(Transaction.timestamp)).limit(limit).all()
    
    def get_with_anomalies(self, db: Session) -> List[Transaction]:
        """
        Get transactions with anomalies.
        
        Args:
            db: Database session
            
        Returns:
            List of transactions with anomalies
        """
        return db.query(Transaction).filter(Transaction.anomaly_detected == True).all()
    
    def get_by_source(self, db: Session, *, source: str) -> List[Transaction]:
        """
        Get transactions by source.
        
        Args:
            db: Database session
            source: Source of transactions to get
            
        Returns:
            List of transactions from the specified source
        """
        return db.query(Transaction).filter(Transaction.source == source).all()
    
    def update_status(self, db: Session, *, id: str, status: str) -> Transaction:
        """
        Update transaction status.
        
        Args:
            db: Database session
            id: ID of the transaction to update
            status: New status
            
        Returns:
            The updated transaction
        """
        transaction = self.get(db, id)
        if transaction:
            transaction.status = status
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
        return transaction
    
    def mark_as_anomaly(self, db: Session, *, id: str, reason: str) -> Transaction:
        """
        Mark a transaction as an anomaly.
        
        Args:
            db: Database session
            id: ID of the transaction to mark
            reason: Reason for marking as anomaly
            
        Returns:
            The updated transaction
        """
        transaction = self.get(db, id)
        if transaction:
            transaction.anomaly_detected = True
            transaction.anomaly_reason = reason
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
        return transaction
    
    def get_transaction_counts_by_type(self, db: Session) -> Dict[str, int]:
        """
        Get transaction counts by type.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of transaction counts by type
        """
        result = db.query(
            Transaction.type, func.count(Transaction.id)
        ).group_by(Transaction.type).all()
        
        return {type_: count for type_, count in result}
    
    def get_transaction_counts_by_status(self, db: Session) -> Dict[str, int]:
        """
        Get transaction counts by status.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of transaction counts by status
        """
        result = db.query(
            Transaction.status, func.count(Transaction.id)
        ).group_by(Transaction.status).all()
        
        return {status: count for status, count in result}
    
    def get_transaction_counts_by_hour(
        self, db: Session, *, election_id: str
    ) -> Dict[int, int]:
        """
        Get transaction counts by hour for an election.
        
        Args:
            db: Database session
            election_id: ID of the election
            
        Returns:
            Dictionary of transaction counts by hour
        """
        result = db.query(
            func.extract('hour', Transaction.timestamp).label('hour'),
            func.count(Transaction.id)
        ).filter(
            Transaction.election_id == election_id
        ).group_by('hour').all()
        
        return {int(hour): count for hour, count in result}
    
    def count_recent(self, db: Session, *, hours: int = 24) -> int:
        """
        Count transactions within the last specified hours.
        
        Args:
            db: Database session
            hours: Number of hours to look back
            
        Returns:
            Count of transactions within the time period
        """
        from datetime import datetime, timedelta
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        return db.query(func.count(Transaction.id)).filter(
            Transaction.timestamp >= start_time,
            Transaction.timestamp <= end_time
        ).scalar() or 0


# Create an instance of TransactionCRUD
transaction_crud = TransactionCRUD(Transaction)