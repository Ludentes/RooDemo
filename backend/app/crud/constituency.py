"""
Constituency CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the Constituency model.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .base import BaseCRUD
from app.models.constituency import Constituency
from app.models.schemas.constituency import ConstituencyCreate, ConstituencyUpdate


class ConstituencyCRUD(BaseCRUD[Constituency, ConstituencyCreate, ConstituencyUpdate]):
    """
    CRUD operations for Constituency model.
    
    This class provides CRUD operations specific to the Constituency model.
    """
    
    def get_by_election(self, db: Session, *, election_id: str) -> List[Constituency]:
        """
        Get constituencies by election ID.
        
        Args:
            db: Database session
            election_id: ID of the election to get constituencies for
            
        Returns:
            List of constituencies for the election
        """
        return db.query(Constituency).filter(Constituency.election_id == election_id).all()
    
    def get_by_region(self, db: Session, *, region: str) -> List[Constituency]:
        """
        Get constituencies by region.
        
        Args:
            db: Database session
            region: Region to get constituencies for
            
        Returns:
            List of constituencies in the region
        """
        return db.query(Constituency).filter(Constituency.region == region).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Constituency]:
        """
        Get constituencies by status.
        
        Args:
            db: Database session
            status: Status to get constituencies for
            
        Returns:
            List of constituencies with the status
        """
        return db.query(Constituency).filter(Constituency.status == status).all()
    
    def get_by_type(self, db: Session, *, type: str) -> List[Constituency]:
        """
        Get constituencies by type.
        
        Args:
            db: Database session
            type: Type to get constituencies for
            
        Returns:
            List of constituencies of the type
        """
        return db.query(Constituency).filter(Constituency.type == type).all()
    
    def update_metrics(
        self, db: Session, *, id: str, bulletins: int, votes: int
    ) -> Constituency:
        """
        Update constituency metrics.
        
        Args:
            db: Database session
            id: ID of the constituency to update
            bulletins: Number of bulletins issued
            votes: Number of votes cast
            
        Returns:
            The updated constituency
        """
        constituency = self.get(db, id)
        if constituency:
            constituency.bulletins_issued = bulletins
            constituency.votes_cast = votes
            if constituency.registered_voters > 0:
                constituency.participation_rate = votes / constituency.registered_voters
            else:
                constituency.participation_rate = 0.0
            db.add(constituency)
            db.commit()
            db.refresh(constituency)
        return constituency
    
    def update_anomaly_score(
        self, db: Session, *, id: str, score: float
    ) -> Constituency:
        """
        Update constituency anomaly score.
        
        Args:
            db: Database session
            id: ID of the constituency to update
            score: New anomaly score
            
        Returns:
            The updated constituency
        """
        constituency = self.get(db, id)
        if constituency:
            constituency.anomaly_score = score
            db.add(constituency)
            db.commit()
            db.refresh(constituency)
        return constituency
    
    def get_active_constituencies(self, db: Session) -> List[Constituency]:
        """
        Get all active constituencies.
        
        Args:
            db: Database session
            
        Returns:
            List of active constituencies
        """
        return db.query(Constituency).filter(Constituency.status == "active").all()
    
    def get_offline_constituencies(self, db: Session) -> List[Constituency]:
        """
        Get all offline constituencies.
        
        Args:
            db: Database session
            
        Returns:
            List of offline constituencies
        """
        return db.query(Constituency).filter(Constituency.status == "offline").all()
    
    def get_completed_constituencies(self, db: Session) -> List[Constituency]:
        """
        Get all completed constituencies.
        
        Args:
            db: Database session
            
        Returns:
            List of completed constituencies
        """
        return db.query(Constituency).filter(Constituency.status == "completed").all()
    
    def get_with_high_anomaly_score(
        self, db: Session, *, threshold: float = 0.7
    ) -> List[Constituency]:
        """
        Get constituencies with high anomaly scores.
        
        Args:
            db: Database session
            threshold: Anomaly score threshold
            
        Returns:
            List of constituencies with anomaly scores above the threshold
        """
        return db.query(Constituency).filter(Constituency.anomaly_score >= threshold).all()
    
    def get_with_alerts(self, db: Session) -> List[Constituency]:
        """
        Get constituencies with active alerts.
        
        Args:
            db: Database session
            
        Returns:
            List of constituencies with active alerts
        """
        return db.query(Constituency).filter(
            Constituency.alerts.any(status="active")
        ).all()
    
    def count(self, db: Session, *, status: Optional[str] = None) -> int:
        """
        Count constituencies, optionally filtered by status.
        
        Args:
            db: Database session
            status: Optional status filter
            
        Returns:
            Count of constituencies
        """
        query = db.query(func.count(Constituency.id))
        if status:
            query = query.filter(Constituency.status == status)
        return query.scalar() or 0


# Create an instance of ConstituencyCRUD
constituency_crud = ConstituencyCRUD(Constituency)