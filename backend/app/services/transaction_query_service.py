"""
Transaction query service for the Election Monitoring System.

This module provides advanced query capabilities for transaction data.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, and_, or_, extract
from datetime import datetime, timedelta

from app.models.transaction import Transaction
from app.crud.transaction import transaction_crud

# Set up logging
logger = logging.getLogger(__name__)


class TransactionQueryService:
    """
    Query service for transaction data.
    
    This class provides methods for building and executing complex queries
    for transaction data.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the query service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def build_query(
        self,
        constituency_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: Optional[str] = None,
        anomaly_detected: Optional[bool] = None,
        source: Optional[str] = None,
        file_id: Optional[str] = None,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ):
        """
        Build a query for transactions.
        
        Args:
            constituency_id: Filter by constituency ID
            transaction_type: Filter by transaction type
            start_time: Filter by start time
            end_time: Filter by end time
            status: Filter by status
            anomaly_detected: Filter by anomaly detection
            source: Filter by source
            file_id: Filter by file ID
            sort_by: Field to sort by
            sort_order: Sort order (asc, desc)
            
        Returns:
            SQLAlchemy query
        """
        query = self.db.query(Transaction)
        
        # Apply filters
        filters = []
        
        if constituency_id:
            filters.append(Transaction.constituency_id == constituency_id)
        
        if transaction_type:
            filters.append(Transaction.type == transaction_type)
        
        if start_time:
            filters.append(Transaction.timestamp >= start_time)
        
        if end_time:
            filters.append(Transaction.timestamp <= end_time)
        
        if status:
            filters.append(Transaction.status == status)
        
        if anomaly_detected is not None:
            filters.append(Transaction.anomaly_detected == anomaly_detected)
        
        if source:
            filters.append(Transaction.source == source)
        
        if file_id:
            filters.append(Transaction.file_id == file_id)
        
        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Apply sorting
        if sort_by:
            sort_column = getattr(Transaction, sort_by, Transaction.timestamp)
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))
        
        return query
    
    def execute_query(self, query, page: int = 1, limit: int = 100) -> Tuple[List[Transaction], int]:
        """
        Execute a query with pagination.
        
        Args:
            query: SQLAlchemy query
            page: Page number
            limit: Items per page
            
        Returns:
            Tuple of (transactions, total_count)
        """
        # Get total count
        total = query.count()
        
        # Apply pagination
        query = query.offset((page - 1) * limit).limit(limit)
        
        # Execute query
        transactions = query.all()
        
        return transactions, total
    
    def get_transaction_counts_by_hour(self, constituency_id: str) -> Dict[int, int]:
        """
        Get transaction counts by hour for a constituency.
        
        Args:
            constituency_id: Constituency ID
            
        Returns:
            Dictionary mapping hour to transaction count
        """
        result = self.db.query(
            extract('hour', Transaction.timestamp).label('hour'),
            func.count(Transaction.id)
        ).filter(
            Transaction.constituency_id == constituency_id
        ).group_by('hour').all()
        
        return {int(hour): count for hour, count in result}
    
    def get_transaction_counts_by_day(self, constituency_id: str) -> Dict[str, int]:
        """
        Get transaction counts by day for a constituency.
        
        Args:
            constituency_id: Constituency ID
            
        Returns:
            Dictionary mapping day to transaction count
        """
        result = self.db.query(
            func.date(Transaction.timestamp).label('day'),
            func.count(Transaction.id)
        ).filter(
            Transaction.constituency_id == constituency_id
        ).group_by('day').all()
        
        return {str(day): count for day, count in result}
    
    def get_transaction_counts_by_type(self, constituency_id: Optional[str] = None) -> Dict[str, int]:
        """
        Get transaction counts by type.
        
        Args:
            constituency_id: Optional constituency ID to filter by
            
        Returns:
            Dictionary mapping type to transaction count
        """
        query = self.db.query(
            Transaction.type,
            func.count(Transaction.id)
        )
        
        if constituency_id:
            query = query.filter(Transaction.constituency_id == constituency_id)
        
        result = query.group_by(Transaction.type).all()
        
        return {type_: count for type_, count in result}
    
    def get_transaction_counts_by_status(self, constituency_id: Optional[str] = None) -> Dict[str, int]:
        """
        Get transaction counts by status.
        
        Args:
            constituency_id: Optional constituency ID to filter by
            
        Returns:
            Dictionary mapping status to transaction count
        """
        query = self.db.query(
            Transaction.status,
            func.count(Transaction.id)
        )
        
        if constituency_id:
            query = query.filter(Transaction.constituency_id == constituency_id)
        
        result = query.group_by(Transaction.status).all()
        
        return {status: count for status, count in result}
    
    def get_transaction_counts_by_source(self, constituency_id: Optional[str] = None) -> Dict[str, int]:
        """
        Get transaction counts by source.
        
        Args:
            constituency_id: Optional constituency ID to filter by
            
        Returns:
            Dictionary mapping source to transaction count
        """
        query = self.db.query(
            Transaction.source,
            func.count(Transaction.id)
        )
        
        if constituency_id:
            query = query.filter(Transaction.constituency_id == constituency_id)
        
        result = query.group_by(Transaction.source).all()
        
        return {source if source else "unknown": count for source, count in result}
    
    def get_transaction_rate(
        self,
        constituency_id: Optional[str] = None,
        hours: int = 1
    ) -> float:
        """
        Get transaction rate (transactions per hour).
        
        Args:
            constituency_id: Optional constituency ID to filter by
            hours: Number of hours to look back
            
        Returns:
            Transactions per hour
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        query = self.db.query(func.count(Transaction.id))
        
        query = query.filter(
            Transaction.timestamp >= start_time,
            Transaction.timestamp <= end_time
        )
        
        if constituency_id:
            query = query.filter(Transaction.constituency_id == constituency_id)
        
        count = query.scalar() or 0
        
        return count / hours if hours > 0 else 0
    
    def get_anomaly_statistics(self, constituency_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about anomalies.
        
        Args:
            constituency_id: Optional constituency ID to filter by
            
        Returns:
            Dictionary with anomaly statistics
        """
        # Base query
        query = self.db.query(Transaction)
        
        if constituency_id:
            query = query.filter(Transaction.constituency_id == constituency_id)
        
        # Total transactions
        total_count = query.count()
        
        # Anomaly count
        anomaly_count = query.filter(Transaction.anomaly_detected == True).count()
        
        # Anomaly percentage
        anomaly_percentage = (anomaly_count / total_count * 100) if total_count > 0 else 0
        
        # Anomaly reasons
        reason_query = self.db.query(
            Transaction.anomaly_reason,
            func.count(Transaction.id)
        ).filter(
            Transaction.anomaly_detected == True
        )
        
        if constituency_id:
            reason_query = reason_query.filter(Transaction.constituency_id == constituency_id)
        
        reason_result = reason_query.group_by(Transaction.anomaly_reason).all()
        
        anomaly_reasons = {
            reason if reason else "unknown": count
            for reason, count in reason_result
        }
        
        return {
            "total_transactions": total_count,
            "anomaly_count": anomaly_count,
            "anomaly_percentage": anomaly_percentage,
            "anomaly_reasons": anomaly_reasons
        }
    
    def get_transaction_statistics(self, constituency_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive transaction statistics.
        
        Args:
            constituency_id: Optional constituency ID to filter by
            
        Returns:
            Dictionary with transaction statistics
        """
        stats = {}
        
        # Basic counts
        stats["counts_by_type"] = self.get_transaction_counts_by_type(constituency_id)
        stats["counts_by_status"] = self.get_transaction_counts_by_status(constituency_id)
        stats["counts_by_source"] = self.get_transaction_counts_by_source(constituency_id)
        
        # Total counts
        stats["total_transactions"] = sum(stats["counts_by_type"].values())
        stats["total_bulletins"] = stats["counts_by_type"].get("blindSigIssue", 0)
        stats["total_votes"] = stats["counts_by_type"].get("vote", 0)
        
        # Rates
        stats["transactions_per_hour"] = self.get_transaction_rate(constituency_id, 1)
        stats["transactions_per_day"] = self.get_transaction_rate(constituency_id, 24)
        
        # Time-based statistics
        if constituency_id:
            stats["counts_by_hour"] = self.get_transaction_counts_by_hour(constituency_id)
            stats["counts_by_day"] = self.get_transaction_counts_by_day(constituency_id)
        
        # Anomaly statistics
        stats["anomalies"] = self.get_anomaly_statistics(constituency_id)
        
        return stats
    
    def search_transactions(self, search_term: str, page: int = 1, limit: int = 100) -> Tuple[List[Transaction], int]:
        """
        Search for transactions.
        
        Args:
            search_term: Search term
            page: Page number
            limit: Items per page
            
        Returns:
            Tuple of (transactions, total_count)
        """
        # Build query with OR conditions for different fields
        query = self.db.query(Transaction).filter(
            or_(
                Transaction.id.ilike(f"%{search_term}%"),
                Transaction.constituency_id.ilike(f"%{search_term}%"),
                Transaction.type.ilike(f"%{search_term}%"),
                Transaction.status.ilike(f"%{search_term}%"),
                Transaction.source.ilike(f"%{search_term}%"),
                Transaction.file_id.ilike(f"%{search_term}%"),
                Transaction.anomaly_reason.ilike(f"%{search_term}%")
            )
        )
        
        return self.execute_query(query, page, limit)