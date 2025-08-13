"""
Hourly Statistics Service for the Election Monitoring System.

This module provides services for aggregating transaction data into hourly statistics.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.hourly_stats import HourlyStats
from app.models.transaction import Transaction
from app.models.constituency import Constituency
from app.models.election import Election
from app.models.schemas.hourly_stats import HourlyStatsCreate, HourlyStatsUpdate
from app.crud.hourly_stats import hourly_stats_crud
from app.crud.constituency import constituency_crud
from app.crud.transaction import transaction_crud

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HourlyStatsService:
    """
    Service for aggregating transaction data into hourly statistics.
    
    This service provides methods for calculating and storing hourly statistics
    based on transaction data.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def aggregate_hourly_stats(
        self, 
        constituency_id: str, 
        hour: datetime,
        force_recalculate: bool = False
    ) -> HourlyStats:
        """
        Aggregate transaction data for a specific constituency and hour.
        
        Args:
            constituency_id: ID of the constituency
            hour: Hour to aggregate data for (will be rounded to the nearest hour)
            force_recalculate: If True, recalculate even if stats already exist
            
        Returns:
            The created or updated hourly stats
        """
        # Round the hour to the nearest hour
        rounded_hour = HourlyStats.round_hour(hour)
        
        # Get the constituency to get the election_id
        constituency = constituency_crud.get(self.db, id=constituency_id)
        if not constituency:
            logger.error(f"Constituency not found: {constituency_id}")
            raise ValueError(f"Constituency not found: {constituency_id}")
        
        # Check if stats already exist for this constituency and hour
        existing_stats = self.db.query(HourlyStats).filter(
            HourlyStats.constituency_id == constituency_id,
            HourlyStats.hour == rounded_hour
        ).first()
        
        if existing_stats and not force_recalculate:
            logger.info(f"Hourly stats already exist for constituency {constituency_id} and hour {rounded_hour}")
            return existing_stats
        
        # Get transactions for this constituency and hour
        start_time = rounded_hour
        end_time = start_time + timedelta(hours=1)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.constituency_id == constituency_id,
            Transaction.timestamp >= start_time,
            Transaction.timestamp < end_time
        ).all()
        
        # Calculate metrics
        metrics = self._calculate_metrics(transactions, constituency)
        
        # Create or update hourly stats
        if existing_stats:
            # Update existing stats
            update_data = HourlyStatsUpdate(
                bulletins_issued=metrics["bulletins_issued"],
                votes_cast=metrics["votes_cast"],
                transaction_count=metrics["transaction_count"],
                bulletin_velocity=metrics["bulletin_velocity"],
                vote_velocity=metrics["vote_velocity"],
                participation_rate=metrics["participation_rate"],
                anomaly_count=metrics["anomaly_count"]
            )
            updated_stats = hourly_stats_crud.update(
                self.db, db_obj=existing_stats, obj_in=update_data
            )
            logger.info(f"Updated hourly stats for constituency {constituency_id} and hour {rounded_hour}")
            return updated_stats
        else:
            # Create new stats
            stats_data = HourlyStatsCreate(
                constituency_id=constituency_id,
                election_id=constituency.election_id,
                hour=rounded_hour,
                timestamp=datetime.utcnow(),
                bulletins_issued=metrics["bulletins_issued"],
                votes_cast=metrics["votes_cast"],
                transaction_count=metrics["transaction_count"],
                bulletin_velocity=metrics["bulletin_velocity"],
                vote_velocity=metrics["vote_velocity"],
                participation_rate=metrics["participation_rate"],
                anomaly_count=metrics["anomaly_count"]
            )
            new_stats = hourly_stats_crud.create(self.db, obj_in=stats_data)
            logger.info(f"Created hourly stats for constituency {constituency_id} and hour {rounded_hour}")
            return new_stats
    
    def _calculate_metrics(
        self, transactions: List[Transaction], constituency: Any
    ) -> Dict[str, Any]:
        """
        Calculate metrics based on transaction data.
        
        Args:
            transactions: List of transactions
            constituency: Constituency object or HourlyStats object
            
        Returns:
            Dictionary of calculated metrics
        """
        # Initialize metrics
        metrics = {
            "bulletins_issued": 0,
            "votes_cast": 0,
            "transaction_count": len(transactions),
            "bulletin_velocity": 0.0,
            "vote_velocity": 0.0,
            "participation_rate": 0.0,
            "anomaly_count": 0
        }
        
        # Count bulletins and votes
        for transaction in transactions:
            if transaction.type == "BULLETIN_ISSUED":
                metrics["bulletins_issued"] += 1
            elif transaction.type == "VOTE_CAST":
                metrics["votes_cast"] += 1
            
            # Count anomalies
            if transaction.anomaly_detected:
                metrics["anomaly_count"] += 1
        
        # Calculate velocities (per hour)
        metrics["bulletin_velocity"] = float(metrics["bulletins_issued"])
        metrics["vote_velocity"] = float(metrics["votes_cast"])
        
        # Calculate participation rate
        # Check if constituency is a Constituency object with registered_voters attribute
        if hasattr(constituency, 'registered_voters') and constituency.registered_voters and constituency.registered_voters > 0:
            metrics["participation_rate"] = (metrics["votes_cast"] / constituency.registered_voters) * 100.0
        
        return metrics
    
    def aggregate_hourly_stats_for_timerange(
        self, 
        constituency_id: str, 
        start_time: datetime, 
        end_time: datetime,
        force_recalculate: bool = False
    ) -> List[HourlyStats]:
        """
        Aggregate transaction data for a specific constituency and time range.
        
        Args:
            constituency_id: ID of the constituency
            start_time: Start time of the range
            end_time: End time of the range
            force_recalculate: If True, recalculate even if stats already exist
            
        Returns:
            List of created or updated hourly stats
        """
        # Round start and end times to the nearest hour
        start_hour = HourlyStats.round_hour(start_time)
        end_hour = HourlyStats.round_hour(end_time)
        
        # Generate a list of hours in the range
        current_hour = start_hour
        hours = []
        while current_hour <= end_hour:
            hours.append(current_hour)
            current_hour += timedelta(hours=1)
        
        # Aggregate stats for each hour
        results = []
        for hour in hours:
            try:
                stats = self.aggregate_hourly_stats(
                    constituency_id=constituency_id,
                    hour=hour,
                    force_recalculate=force_recalculate
                )
                results.append(stats)
            except Exception as e:
                logger.error(f"Error aggregating stats for hour {hour}: {str(e)}")
        
        return results
    
    def aggregate_hourly_stats_for_election(
        self, 
        election_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        force_recalculate: bool = False
    ) -> Dict[str, List[HourlyStats]]:
        """
        Aggregate transaction data for all constituencies in an election.
        
        Args:
            election_id: ID of the election
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            force_recalculate: If True, recalculate even if stats already exist
            
        Returns:
            Dictionary mapping constituency IDs to lists of hourly stats
        """
        # Get all constituencies for this election
        constituencies = self.db.query(Constituency).filter(
            Constituency.election_id == election_id
        ).all()
        
        # If start_time and end_time are not provided, use the election's start and end dates
        if not start_time or not end_time:
            election = self.db.query(Election).filter(Election.id == election_id).first()
            if not election:
                logger.error(f"Election not found: {election_id}")
                raise ValueError(f"Election not found: {election_id}")
            
            start_time = start_time or election.start_date
            end_time = end_time or election.end_date
        
        # Aggregate stats for each constituency
        results = {}
        for constituency in constituencies:
            try:
                stats = self.aggregate_hourly_stats_for_timerange(
                    constituency_id=constituency.id,
                    start_time=start_time,
                    end_time=end_time,
                    force_recalculate=force_recalculate
                )
                results[constituency.id] = stats
            except Exception as e:
                logger.error(f"Error aggregating stats for constituency {constituency.id}: {str(e)}")
        
        return results
    
    def get_hourly_stats(
        self, 
        constituency_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> List[HourlyStats]:
        """
        Get hourly stats for a specific constituency and time range.
        
        Args:
            constituency_id: ID of the constituency
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            List of hourly stats
        """
        query = self.db.query(HourlyStats).filter(
            HourlyStats.constituency_id == constituency_id
        )
        
        if start_time:
            query = query.filter(HourlyStats.hour >= HourlyStats.round_hour(start_time))
        
        if end_time:
            query = query.filter(HourlyStats.hour <= HourlyStats.round_hour(end_time))
        
        return query.order_by(HourlyStats.hour).all()
    
    def get_hourly_stats_for_election(
        self, 
        election_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> Dict[str, List[HourlyStats]]:
        """
        Get hourly stats for all constituencies in an election.
        
        Args:
            election_id: ID of the election
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            Dictionary mapping constituency IDs to lists of hourly stats
        """
        # Get all constituencies for this election
        constituencies = self.db.query(Constituency).filter(
            Constituency.election_id == election_id
        ).all()
        
        # Get stats for each constituency
        results = {}
        for constituency in constituencies:
            stats = self.get_hourly_stats(
                constituency_id=constituency.id,
                start_time=start_time,
                end_time=end_time
            )
            results[constituency.id] = stats
        
        return results


# Create a function to get the service
def get_hourly_stats_service(db: Session) -> HourlyStatsService:
    """
    Get an instance of the HourlyStatsService.
    
    Args:
        db: Database session
        
    Returns:
        HourlyStatsService instance
    """
    return HourlyStatsService(db)