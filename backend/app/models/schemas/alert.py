"""
Alert schemas for the Election Monitoring System.

This module provides Pydantic models for the Alert entity.
"""

from pydantic import validator, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import BaseSchema, ResponseBase, validate_status


class AlertBase(BaseSchema):
    """
    Base schema for Alert model.
    
    Attributes:
        constituency_id (str): ID of the constituency this alert belongs to
        type (str): Alert type (votes_exceed_bulletins, unusual_spike, etc.)
        severity (str): Alert severity (critical, warning, info)
        status (str): Alert status (active, investigating, resolved, snoozed)
        title (str): Short alert title
        description (str): Detailed alert description
        details (dict): Additional alert details
        notes (list): List of investigation notes
        detected_at (datetime): When the anomaly was detected
        resolved_at (datetime): When the alert was resolved (nullable)
        assigned_to (str): Person assigned to investigate (nullable)
    """
    
    constituency_id: str = Field(..., description="ID of the constituency this alert belongs to")
    type: str = Field(..., description="Alert type (votes_exceed_bulletins, unusual_spike, etc.)")
    severity: str = Field(..., description="Alert severity (critical, warning, info)")
    status: str = Field("active", description="Alert status (active, investigating, resolved, snoozed)")
    title: str = Field(..., description="Short alert title")
    description: Optional[str] = Field(None, description="Detailed alert description")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional alert details")
    notes: List[str] = Field(default_factory=list, description="List of investigation notes")
    detected_at: datetime = Field(..., description="When the anomaly was detected")
    resolved_at: Optional[datetime] = Field(None, description="When the alert was resolved (nullable)")
    assigned_to: Optional[str] = Field(None, description="Person assigned to investigate (nullable)")
    
    @validator("severity")
    def validate_severity(cls, v: str) -> str:
        """Validate alert severity."""
        allowed_severities = ["critical", "warning", "info"]
        if v not in allowed_severities:
            raise ValueError(f"Severity must be one of {allowed_severities}")
        return v
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate alert status."""
        allowed_statuses = ["active", "investigating", "resolved", "snoozed"]
        return validate_status(v, allowed_statuses)


class AlertCreate(AlertBase):
    """
    Schema for creating an Alert.
    
    This schema is used for creating a new Alert.
    """
    
    pass


class AlertUpdate(BaseSchema):
    """
    Schema for updating an Alert.
    
    This schema is used for updating an existing Alert.
    All fields are optional to allow partial updates.
    """
    
    status: Optional[str] = Field(None, description="Alert status (active, investigating, resolved, snoozed)")
    notes: Optional[List[str]] = Field(None, description="List of investigation notes")
    resolved_at: Optional[datetime] = Field(None, description="When the alert was resolved")
    assigned_to: Optional[str] = Field(None, description="Person assigned to investigate")
    
    @validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate alert status."""
        if v is None:
            return v
        allowed_statuses = ["active", "investigating", "resolved", "snoozed"]
        return validate_status(v, allowed_statuses)


class AlertResponse(ResponseBase, AlertBase):
    """
    Schema for Alert response.
    
    This schema is used for returning an Alert in API responses.
    """
    
    constituency_name: Optional[str] = Field(None, description="Name of the constituency this alert belongs to")


class AlertList(BaseSchema):
    """
    Schema for list of Alerts.
    
    This schema is used for returning a list of Alerts in API responses.
    """
    
    data: List[AlertResponse]
    total: int
    page: int
    limit: int


class AlertDetail(AlertResponse):
    """
    Schema for detailed Alert information.
    
    This schema is used for returning detailed information about an Alert.
    """
    
    pass


class AddNoteRequest(BaseSchema):
    """
    Schema for adding a note to an Alert.
    
    This schema is used for adding a note to an existing Alert.
    """
    
    note: str = Field(..., description="Note to add to the alert")


class UpdateStatusRequest(BaseSchema):
    """
    Schema for updating the status of an Alert.
    
    This schema is used for updating the status of an existing Alert.
    """
    
    status: str = Field(..., description="New status for the alert (investigating, resolved, snoozed)")
    notes: Optional[str] = Field(None, description="Optional note to add with the status update")
    
    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate alert status."""
        allowed_statuses = ["investigating", "resolved", "snoozed"]
        return validate_status(v, allowed_statuses)