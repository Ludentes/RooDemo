"""
Constituency Metrics Service for the Election Monitoring System.

This module provides services for calculating metrics for constituencies.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.hourly_stats import HourlyStats
from app.models.transaction import Transaction
from app.models.constituency import Constituency
from app.models.election import Election
from app.crud.constituency import constituency_crud
from app.crud.hourly_stats import hourly_stats_crud
from app.crud.transaction import transaction_crud
from app.services.hourly_stats_service import HourlyStatsService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConstituencyMetricsService:
    """
    Service for calculating metrics for constituencies.
    
    This service provides methods for calculating and storing metrics
    for constituencies based on hourly stats and transaction data.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db: Database session
        """
        self.db = db
        self.hourly_stats_service = HourlyStatsService(db)
    
    def calculate_metrics(
        self, 
        constituency_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        update_constituency: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate metrics for a constituency.
        
        Args:
            constituency_id: ID of the constituency
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            update_constituency: If True, update the constituency with calculated metrics
            
        Returns:
            Dictionary of calculated metrics
        """
        # Get the constituency
        constituency = constituency_crud.get(self.db, id=constituency_id)
        if not constituency:
            logger.error(f"Constituency not found: {constituency_id}")
            raise ValueError(f"Constituency not found: {constituency_id}")
        
        # Get hourly stats for the constituency
        hourly_stats = self.hourly_stats_service.get_hourly_stats(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Calculate metrics
        metrics = self._calculate_metrics_from_hourly_stats(hourly_stats, constituency)
        
        # Update the constituency if requested
        if update_constituency:
            self._update_constituency_metrics(constituency, metrics)
        
        return metrics
    
    def _calculate_metrics_from_hourly_stats(
        self, hourly_stats: List[HourlyStats], constituency: Constituency
    ) -> Dict[str, Any]:
        """
        Calculate metrics based on hourly stats.
        
        Args:
            hourly_stats: List of hourly stats
            constituency: Constituency object
            
        Returns:
            Dictionary of calculated metrics
        """
        # Initialize metrics
        metrics = {
            "total_bulletins_issued": 0,
            "total_votes_cast": 0,
            "total_transactions": 0,
            "total_anomalies": 0,
            "participation_rate": 0.0,
            "anomaly_score": 0.0,
            "hourly_activity": [],
            "peak_hour": None,
            "peak_hour_votes": 0,
            "average_votes_per_hour": 0.0,
            "average_bulletins_per_hour": 0.0,
            "vote_velocity_trend": 0.0,  # Positive means increasing, negative means decreasing
            "bulletin_velocity_trend": 0.0
        }
        
        if not hourly_stats:
            return metrics
        
        # Calculate total metrics
        for stats in hourly_stats:
            metrics["total_bulletins_issued"] += stats.bulletins_issued
            metrics["total_votes_cast"] += stats.votes_cast
            metrics["total_transactions"] += stats.transaction_count
            metrics["total_anomalies"] += stats.anomaly_count
            
            # Track peak hour
            if stats.votes_cast > metrics["peak_hour_votes"]:
                metrics["peak_hour"] = stats.hour
                metrics["peak_hour_votes"] = stats.votes_cast
            
            # Add to hourly activity
            metrics["hourly_activity"].append({
                "hour": stats.hour,
                "bulletins_issued": stats.bulletins_issued,
                "votes_cast": stats.votes_cast,
                "transaction_count": stats.transaction_count,
                "bulletin_velocity": stats.bulletin_velocity,
                "vote_velocity": stats.vote_velocity,
                "participation_rate": stats.participation_rate,
                "anomaly_count": stats.anomaly_count
            })
        
        # Calculate averages
        num_hours = len(hourly_stats)
        if num_hours > 0:
            metrics["average_votes_per_hour"] = metrics["total_votes_cast"] / num_hours
            metrics["average_bulletins_per_hour"] = metrics["total_bulletins_issued"] / num_hours
        
        # Calculate participation rate
        if constituency.registered_voters and constituency.registered_voters > 0:
            metrics["participation_rate"] = (metrics["total_votes_cast"] / constituency.registered_voters) * 100.0
        
        # Calculate anomaly score
        if metrics["total_transactions"] > 0:
            metrics["anomaly_score"] = (metrics["total_anomalies"] / metrics["total_transactions"]) * 100.0
        
        # Calculate velocity trends
        if num_hours > 1:
            # Sort hourly stats by hour
            sorted_stats = sorted(hourly_stats, key=lambda x: x.hour)
            
            # Calculate linear regression for velocities
            vote_velocity_trend = self._calculate_trend([stats.vote_velocity for stats in sorted_stats])
            bulletin_velocity_trend = self._calculate_trend([stats.bulletin_velocity for stats in sorted_stats])
            
            metrics["vote_velocity_trend"] = vote_velocity_trend
            metrics["bulletin_velocity_trend"] = bulletin_velocity_trend
        
        return metrics
    
    def _calculate_trend(self, values: List[float]) -> float:
        """
        Calculate the trend of a series of values using linear regression.
        
        Args:
            values: List of values
            
        Returns:
            Slope of the linear regression line
        """
        if not values or len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        
        # Calculate means
        mean_x = sum(x) / n
        mean_y = sum(values) / n
        
        # Calculate slope
        numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _update_constituency_metrics(
        self, constituency: Constituency, metrics: Dict[str, Any]
    ) -> Constituency:
        """
        Update a constituency with calculated metrics.
        
        Args:
            constituency: Constituency object
            metrics: Dictionary of calculated metrics
            
        Returns:
            Updated constituency
        """
        # Update constituency fields
        constituency.bulletins_issued = metrics["total_bulletins_issued"]
        constituency.votes_cast = metrics["total_votes_cast"]
        constituency.participation_rate = metrics["participation_rate"]
        constituency.anomaly_score = metrics["anomaly_score"]
        constituency.last_update_time = datetime.utcnow()
        
        # Save to database
        self.db.add(constituency)
        self.db.commit()
        self.db.refresh(constituency)
        
        logger.info(f"Updated metrics for constituency {constituency.id}")
        return constituency
    
    def calculate_metrics_by_time_period(
        self, 
        constituency_id: str, 
        period: str = "day",
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate metrics for a constituency grouped by time period.
        
        Args:
            constituency_id: ID of the constituency
            period: Time period to group by (hour, day, week, month)
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            Dictionary mapping time periods to metrics
        """
        # Get the constituency
        constituency = constituency_crud.get(self.db, id=constituency_id)
        if not constituency:
            logger.error(f"Constituency not found: {constituency_id}")
            raise ValueError(f"Constituency not found: {constituency_id}")
        
        # Get hourly stats for the constituency
        hourly_stats = self.hourly_stats_service.get_hourly_stats(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Group hourly stats by time period
        grouped_stats = self._group_hourly_stats_by_period(hourly_stats, period)
        
        # Calculate metrics for each group
        results = {}
        for period_key, stats in grouped_stats.items():
            metrics = self._calculate_metrics_from_hourly_stats(stats, constituency)
            results[period_key] = metrics
        
        return results
    
    def _group_hourly_stats_by_period(
        self, hourly_stats: List[HourlyStats], period: str
    ) -> Dict[str, List[HourlyStats]]:
        """
        Group hourly stats by time period.
        
        Args:
            hourly_stats: List of hourly stats
            period: Time period to group by (hour, day, week, month)
            
        Returns:
            Dictionary mapping time periods to lists of hourly stats
        """
        grouped_stats = {}
        
        for stats in hourly_stats:
            if period == "hour":
                # Group by hour
                period_key = stats.hour.strftime("%Y-%m-%d %H:00")
                if period_key not in grouped_stats:
                    grouped_stats[period_key] = []
                grouped_stats[period_key].append(stats)
            elif period == "day":
                # Group by day
                period_key = stats.hour.strftime("%Y-%m-%d")
                if period_key not in grouped_stats:
                    grouped_stats[period_key] = []
                grouped_stats[period_key].append(stats)
            elif period == "week":
                # Group by ISO week
                year, week, _ = stats.hour.isocalendar()
                period_key = f"{year}-W{week:02d}"
                if period_key not in grouped_stats:
                    grouped_stats[period_key] = []
                grouped_stats[period_key].append(stats)
            elif period == "month":
                # Group by month
                period_key = stats.hour.strftime("%Y-%m")
                if period_key not in grouped_stats:
                    grouped_stats[period_key] = []
                grouped_stats[period_key].append(stats)
            else:
                # Invalid period, use day as default
                period_key = stats.hour.strftime("%Y-%m-%d")
                if period_key not in grouped_stats:
                    grouped_stats[period_key] = []
                grouped_stats[period_key].append(stats)
        
        return grouped_stats
    
    def calculate_metrics_for_election(
        self, 
        election_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        update_constituencies: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate metrics for all constituencies in an election.
        
        Args:
            election_id: ID of the election
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            update_constituencies: If True, update constituencies with calculated metrics
            
        Returns:
            Dictionary mapping constituency IDs to metrics
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
        
        # Calculate metrics for each constituency
        results = {}
        for constituency in constituencies:
            try:
                metrics = self.calculate_metrics(
                    constituency_id=constituency.id,
                    start_time=start_time,
                    end_time=end_time,
                    update_constituency=update_constituencies
                )
                results[constituency.id] = metrics
            except Exception as e:
                logger.error(f"Error calculating metrics for constituency {constituency.id}: {str(e)}")
        
        return results
    
    def compare_constituencies(
        self, 
        constituency_ids: List[str], 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare metrics for multiple constituencies.
        
        Args:
            constituency_ids: List of constituency IDs
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            Dictionary mapping constituency IDs to metrics
        """
        results = {}
        
        for constituency_id in constituency_ids:
            try:
                metrics = self.calculate_metrics(
                    constituency_id=constituency_id,
                    start_time=start_time,
                    end_time=end_time,
                    update_constituency=False
                )
                results[constituency_id] = metrics
            except Exception as e:
                logger.error(f"Error calculating metrics for constituency {constituency_id}: {str(e)}")
        
        return results


# Create a function to get the service
def get_constituency_metrics_service(db: Session) -> ConstituencyMetricsService:
    """
    Get an instance of the ConstituencyMetricsService.
    
    Args:
        db: Database session
        
    Returns:
        ConstituencyMetricsService instance
    """
    return ConstituencyMetricsService(db)