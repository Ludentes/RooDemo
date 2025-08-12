"""
Alert CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the Alert model.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from .base import BaseCRUD
from app.models.alert import Alert
from app.models.schemas.alert import AlertCreate, AlertUpdate


class AlertCRUD(BaseCRUD[Alert, AlertCreate, AlertUpdate]):
    """
    CRUD operations for Alert model.
    
    This class provides CRUD operations specific to the Alert model.
    """
    
    def get_by_constituency(self, db: Session, *, constituency_id: str) -> List[Alert]:
        """
        Get alerts by constituency ID.
        
        Args:
            db: Database session
            constituency_id: ID of the constituency to get alerts for
            
        Returns:
            List of alerts for the constituency
        """
        return db.query(Alert).filter(Alert.constituency_id == constituency_id).all()
    
    def get_by_election(self, db: Session, *, election_id: str) -> List[Alert]:
        """
        Get alerts by election ID.
        
        Args:
            db: Database session
            election_id: ID of the election to get alerts for
            
        Returns:
            List of alerts for the election
        """
        return db.query(Alert).filter(Alert.election_id == election_id).all()
    
    def get_by_type(self, db: Session, *, type: str) -> List[Alert]:
        """
        Get alerts by type.
        
        Args:
            db: Database session
            type: Type of alerts to get
            
        Returns:
            List of alerts of the specified type
        """
        return db.query(Alert).filter(Alert.type == type).all()
    
    def get_by_severity(self, db: Session, *, severity: str) -> List[Alert]:
        """
        Get alerts by severity.
        
        Args:
            db: Database session
            severity: Severity of alerts to get
            
        Returns:
            List of alerts with the specified severity
        """
        return db.query(Alert).filter(Alert.severity == severity).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Alert]:
        """
        Get alerts by status.
        
        Args:
            db: Database session
            status: Status of alerts to get
            
        Returns:
            List of alerts with the specified status
        """
        return db.query(Alert).filter(Alert.status == status).all()
    
    def get_by_time_range(
        self, db: Session, *, start_time: datetime, end_time: datetime
    ) -> List[Alert]:
        """
        Get alerts within a time range.
        
        Args:
            db: Database session
            start_time: Start time of the range
            end_time: End time of the range
            
        Returns:
            List of alerts within the time range
        """
        return db.query(Alert).filter(
            Alert.timestamp >= start_time,
            Alert.timestamp <= end_time
        ).all()
    
    def get_latest(self, db: Session, *, limit: int = 10) -> List[Alert]:
        """
        Get the latest alerts.
        
        Args:
            db: Database session
            limit: Maximum number of alerts to return
            
        Returns:
            List of the latest alerts
        """
        return db.query(Alert).order_by(desc(Alert.timestamp)).limit(limit).all()
    
    def get_active_alerts(self, db: Session) -> List[Alert]:
        """
        Get all active alerts.
        
        Args:
            db: Database session
            
        Returns:
            List of active alerts
        """
        return db.query(Alert).filter(Alert.status == "active").all()
    
    def get_resolved_alerts(self, db: Session) -> List[Alert]:
        """
        Get all resolved alerts.
        
        Args:
            db: Database session
            
        Returns:
            List of resolved alerts
        """
        return db.query(Alert).filter(Alert.status == "resolved").all()
    
    def get_high_severity_alerts(self, db: Session) -> List[Alert]:
        """
        Get all high severity alerts.
        
        Args:
            db: Database session
            
        Returns:
            List of high severity alerts
        """
        return db.query(Alert).filter(Alert.severity == "high").all()
    
    def update_status(
        self, db: Session, *, id: str, status: str, resolution_notes: Optional[str] = None
    ) -> Alert:
        """
        Update alert status.
        
        Args:
            db: Database session
            id: ID of the alert to update
            status: New status
            resolution_notes: Notes on how the alert was resolved
            
        Returns:
            The updated alert
        """
        alert = self.get(db, id)
        if alert:
            alert.status = status
            if status == "resolved" and resolution_notes:
                alert.resolution_notes = resolution_notes
                alert.resolved_at = datetime.utcnow()
            db.add(alert)
            db.commit()
            db.refresh(alert)
        return alert
    
    def escalate_alert(self, db: Session, *, id: str, new_severity: str) -> Alert:
        """
        Escalate an alert by increasing its severity.
        
        Args:
            db: Database session
            id: ID of the alert to escalate
            new_severity: New severity level
            
        Returns:
            The updated alert
        """
        alert = self.get(db, id)
        if alert:
            alert.severity = new_severity
            alert.updated_at = datetime.utcnow()
            db.add(alert)
            db.commit()
            db.refresh(alert)
        return alert
    
    def add_comment(self, db: Session, *, id: str, comment: str) -> Alert:
        """
        Add a comment to an alert.
        
        Args:
            db: Database session
            id: ID of the alert to add a comment to
            comment: Comment to add
            
        Returns:
            The updated alert
        """
        alert = self.get(db, id)
        if alert:
            if alert.comments:
                alert.comments.append(comment)
            else:
                alert.comments = [comment]
            alert.updated_at = datetime.utcnow()
            db.add(alert)
            db.commit()
            db.refresh(alert)
        return alert
    
    def get_alert_counts_by_type(self, db: Session) -> Dict[str, int]:
        """
        Get alert counts by type.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of alert counts by type
        """
        result = db.query(
            Alert.type, func.count(Alert.id)
        ).group_by(Alert.type).all()
        
        return {type_: count for type_, count in result}
    
    def get_alert_counts_by_severity(self, db: Session) -> Dict[str, int]:
        """
        Get alert counts by severity.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of alert counts by severity
        """
        result = db.query(
            Alert.severity, func.count(Alert.id)
        ).group_by(Alert.severity).all()
        
        return {severity: count for severity, count in result}
    
    def get_alert_counts_by_status(self, db: Session) -> Dict[str, int]:
        """
        Get alert counts by status.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of alert counts by status
        """
        result = db.query(
            Alert.status, func.count(Alert.id)
        ).group_by(Alert.status).all()
        
        return {status: count for status, count in result}


# Create an instance of AlertCRUD
alert_crud = AlertCRUD(Alert)