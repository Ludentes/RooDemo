"""
Election CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the Election model.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .base import BaseCRUD
from app.models.election import Election
from app.models.schemas.election import ElectionCreate, ElectionUpdate


class ElectionCRUD(BaseCRUD[Election, ElectionCreate, ElectionUpdate]):
    """
    CRUD operations for Election model.
    
    This class provides CRUD operations specific to the Election model.
    """
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Election]:
        """
        Get an election by name.
        
        Args:
            db: Database session
            name: Name of the election to get
            
        Returns:
            The election if found, None otherwise
        """
        return db.query(Election).filter(Election.name == name).first()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Election]:
        """
        Get elections by status.
        
        Args:
            db: Database session
            status: Status of the elections to get
            
        Returns:
            List of elections with the specified status
        """
        return db.query(Election).filter(Election.status == status).all()
    
    def get_by_country(self, db: Session, *, country: str) -> List[Election]:
        """
        Get elections by country.
        
        Args:
            db: Database session
            country: Country of the elections to get
            
        Returns:
            List of elections in the specified country
        """
        return db.query(Election).filter(Election.country == country).all()
    
    def get_by_type(self, db: Session, *, type: str) -> List[Election]:
        """
        Get elections by type.
        
        Args:
            db: Database session
            type: Type of the elections to get
            
        Returns:
            List of elections of the specified type
        """
        return db.query(Election).filter(Election.type == type).all()
    
    def get_active_elections(self, db: Session) -> List[Election]:
        """
        Get all active elections.
        
        Args:
            db: Database session
            
        Returns:
            List of active elections
        """
        return db.query(Election).filter(Election.status == "active").all()
    
    def get_by_date_range(
        self, db: Session, *, start_date: datetime, end_date: datetime
    ) -> List[Election]:
        """
        Get elections within a date range.
        
        Args:
            db: Database session
            start_date: Start date of the range
            end_date: End date of the range
            
        Returns:
            List of elections within the date range
        """
        return db.query(Election).filter(
            Election.start_date >= start_date,
            Election.end_date <= end_date
        ).all()
    
    def get_upcoming_elections(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Election]:
        """
        Get upcoming elections with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of upcoming elections (status is 'upcoming' or 'scheduled')
        """
        return db.query(Election).filter(
            Election.status.in_(["upcoming", "scheduled"])
        ).offset(skip).limit(limit).all()
    
    def count_upcoming_elections(self, db: Session) -> int:
        """
        Count the number of upcoming elections.
        
        Args:
            db: Database session
            
        Returns:
            The number of upcoming elections
        """
        return db.query(Election).filter(
            Election.status.in_(["upcoming", "scheduled"])
        ).count()
    
    def get_completed_elections(self, db: Session) -> List[Election]:
        """
        Get all completed elections.
        
        Args:
            db: Database session
            
        Returns:
            List of completed elections
        """
        return db.query(Election).filter(Election.status == "completed").all()
    
    def update_total_constituencies(
        self, db: Session, *, id: str, total: int
    ) -> Election:
        """
        Update the total constituencies count for an election.
        
        Args:
            db: Database session
            id: ID of the election to update
            total: New total constituencies count
            
        Returns:
            The updated election
        """
        election = self.get(db, id)
        if election:
            election.total_constituencies = total
            db.add(election)
            db.commit()
            db.refresh(election)
        return election
    
    def count(self, db: Session, *, status: Optional[str] = None) -> int:
        """
        Count elections, optionally filtered by status.
        
        Args:
            db: Database session
            status: Optional status filter
            
        Returns:
            Count of elections
        """
        from sqlalchemy import func
        
        query = db.query(func.count(Election.id))
        if status:
            query = query.filter(Election.status == status)
        return query.scalar() or 0


# Create an instance of ElectionCRUD
election_crud = ElectionCRUD(Election)