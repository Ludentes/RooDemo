"""
HourlyStats CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the HourlyStats model.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from .base import BaseCRUD
from app.models.hourly_stats import HourlyStats
from app.models.schemas.hourly_stats import HourlyStatsCreate, HourlyStatsUpdate


class HourlyStatsCRUD(BaseCRUD[HourlyStats, HourlyStatsCreate, HourlyStatsUpdate]):
    """
    CRUD operations for HourlyStats model.
    
    This class provides CRUD operations specific to the HourlyStats model.
    """
    
    def get_by_constituency(self, db: Session, *, constituency_id: str) -> List[HourlyStats]:
        """
        Get hourly stats by constituency ID.
        
        Args:
            db: Database session
            constituency_id: ID of the constituency to get stats for
            
        Returns:
            List of hourly stats for the constituency
        """
        return db.query(HourlyStats).filter(HourlyStats.constituency_id == constituency_id).all()
    
    def get_by_election(self, db: Session, *, election_id: str) -> List[HourlyStats]:
        """
        Get hourly stats by election ID.
        
        Args:
            db: Database session
            election_id: ID of the election to get stats for
            
        Returns:
            List of hourly stats for the election
        """
        return db.query(HourlyStats).filter(HourlyStats.election_id == election_id).all()
    
    def get_by_hour(
        self, db: Session, *, election_id: str, hour: int
    ) -> List[HourlyStats]:
        """
        Get hourly stats for a specific hour.
        
        Args:
            db: Database session
            election_id: ID of the election
            hour: Hour to get stats for (0-23)
            
        Returns:
            List of hourly stats for the hour
        """
        return db.query(HourlyStats).filter(
            HourlyStats.election_id == election_id,
            HourlyStats.hour == hour
        ).all()
    
    def get_by_date(
        self, db: Session, *, election_id: str, date: datetime
    ) -> List[HourlyStats]:
        """
        Get hourly stats for a specific date.
        
        Args:
            db: Database session
            election_id: ID of the election
            date: Date to get stats for
            
        Returns:
            List of hourly stats for the date
        """
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        return db.query(HourlyStats).filter(
            HourlyStats.election_id == election_id,
            HourlyStats.timestamp >= start_date,
            HourlyStats.timestamp < end_date
        ).all()
    
    def get_latest_for_constituency(
        self, db: Session, *, constituency_id: str
    ) -> Optional[HourlyStats]:
        """
        Get the latest hourly stats for a constituency.
        
        Args:
            db: Database session
            constituency_id: ID of the constituency
            
        Returns:
            The latest hourly stats for the constituency
        """
        return db.query(HourlyStats).filter(
            HourlyStats.constituency_id == constituency_id
        ).order_by(desc(HourlyStats.timestamp)).first()
    
    def get_latest_for_election(
        self, db: Session, *, election_id: str
    ) -> List[HourlyStats]:
        """
        Get the latest hourly stats for each constituency in an election.
        
        Args:
            db: Database session
            election_id: ID of the election
            
        Returns:
            List of the latest hourly stats for each constituency
        """
        # This is a more complex query that requires a subquery
        # to get the latest timestamp for each constituency
        latest_timestamps = db.query(
            HourlyStats.constituency_id,
            func.max(HourlyStats.timestamp).label('max_timestamp')
        ).filter(
            HourlyStats.election_id == election_id
        ).group_by(HourlyStats.constituency_id).subquery()
        
        return db.query(HourlyStats).join(
            latest_timestamps,
            and_(
                HourlyStats.constituency_id == latest_timestamps.c.constituency_id,
                HourlyStats.timestamp == latest_timestamps.c.max_timestamp
            )
        ).all()
    
    def get_hourly_participation_rates(
        self, db: Session, *, election_id: str
    ) -> Dict[int, float]:
        """
        Get average participation rates by hour for an election.
        
        Args:
            db: Database session
            election_id: ID of the election
            
        Returns:
            Dictionary of average participation rates by hour
        """
        result = db.query(
            HourlyStats.hour,
            func.avg(HourlyStats.participation_rate).label('avg_rate')
        ).filter(
            HourlyStats.election_id == election_id
        ).group_by(HourlyStats.hour).all()
        
        return {hour: float(rate) for hour, rate in result}
    
    def get_hourly_transaction_counts(
        self, db: Session, *, election_id: str
    ) -> Dict[int, int]:
        """
        Get total transaction counts by hour for an election.
        
        Args:
            db: Database session
            election_id: ID of the election
            
        Returns:
            Dictionary of total transaction counts by hour
        """
        result = db.query(
            HourlyStats.hour,
            func.sum(HourlyStats.transaction_count).label('total_count')
        ).filter(
            HourlyStats.election_id == election_id
        ).group_by(HourlyStats.hour).all()
        
        return {hour: int(count) for hour, count in result}
    
    def get_hourly_anomaly_counts(
        self, db: Session, *, election_id: str
    ) -> Dict[int, int]:
        """
        Get total anomaly counts by hour for an election.
        
        Args:
            db: Database session
            election_id: ID of the election
            
        Returns:
            Dictionary of total anomaly counts by hour
        """
        result = db.query(
            HourlyStats.hour,
            func.sum(HourlyStats.anomaly_count).label('total_count')
        ).filter(
            HourlyStats.election_id == election_id
        ).group_by(HourlyStats.hour).all()
        
        return {hour: int(count) for hour, count in result}
    
    def get_constituency_with_highest_anomalies(
        self, db: Session, *, election_id: str, hour: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get constituencies with the highest anomaly counts.
        
        Args:
            db: Database session
            election_id: ID of the election
            hour: Optional hour to filter by
            
        Returns:
            List of dictionaries with constituency_id and anomaly_count
        """
        query = db.query(
            HourlyStats.constituency_id,
            func.sum(HourlyStats.anomaly_count).label('total_anomalies')
        ).filter(
            HourlyStats.election_id == election_id
        )
        
        if hour is not None:
            query = query.filter(HourlyStats.hour == hour)
        
        result = query.group_by(
            HourlyStats.constituency_id
        ).order_by(desc('total_anomalies')).all()
        
        return [
            {"constituency_id": constituency_id, "anomaly_count": int(count)}
            for constituency_id, count in result
        ]
    
    def create_or_update_stats(
        self, db: Session, *, obj_in: HourlyStatsCreate
    ) -> HourlyStats:
        """
        Create or update hourly stats.
        
        If stats for the given constituency, election, and hour already exist,
        update them. Otherwise, create new stats.
        
        Args:
            db: Database session
            obj_in: Stats data to create or update
            
        Returns:
            The created or updated stats
        """
        # Check if stats already exist
        existing_stats = db.query(HourlyStats).filter(
            HourlyStats.constituency_id == obj_in.constituency_id,
            HourlyStats.election_id == obj_in.election_id,
            HourlyStats.hour == obj_in.hour,
            func.date(HourlyStats.timestamp) == func.date(obj_in.timestamp)
        ).first()
        
        if existing_stats:
            # Update existing stats
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(existing_stats, field, value)
            db.add(existing_stats)
            db.commit()
            db.refresh(existing_stats)
            return existing_stats
        else:
            # Create new stats
            return super().create(db, obj_in=obj_in)


# Create an instance of HourlyStatsCRUD
hourly_stats_crud = HourlyStatsCRUD(HourlyStats)