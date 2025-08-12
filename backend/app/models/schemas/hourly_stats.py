"""
HourlyStats schemas for the Election Monitoring System.

This module provides Pydantic models for the HourlyStats entity.
"""

from pydantic import Field
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema, ResponseBase


class HourlyStatsBase(BaseSchema):
    """
    Base schema for HourlyStats model.
    
    Attributes:
        constituency_id (str): ID of the constituency these stats belong to
        hour (datetime): Hour timestamp (rounded to hour)
        bulletins_issued (int): Number of bulletins issued in this hour
        votes_cast (int): Number of votes cast in this hour
        transaction_count (int): Total transactions in this hour
        bulletin_velocity (float): Rate of bulletin issuance per hour
        vote_velocity (float): Rate of vote casting per hour
    """
    
    constituency_id: str = Field(..., description="ID of the constituency these stats belong to")
    hour: datetime = Field(..., description="Hour timestamp (rounded to hour)")
    bulletins_issued: int = Field(0, description="Number of bulletins issued in this hour")
    votes_cast: int = Field(0, description="Number of votes cast in this hour")
    transaction_count: int = Field(0, description="Total transactions in this hour")
    bulletin_velocity: float = Field(0.0, description="Rate of bulletin issuance per hour")
    vote_velocity: float = Field(0.0, description="Rate of vote casting per hour")


class HourlyStatsCreate(HourlyStatsBase):
    """
    Schema for creating HourlyStats.
    
    This schema is used for creating new HourlyStats.
    """
    
    pass


class HourlyStatsUpdate(BaseSchema):
    """
    Schema for updating HourlyStats.
    
    This schema is used for updating existing HourlyStats.
    All fields are optional to allow partial updates.
    """
    
    bulletins_issued: Optional[int] = Field(None, description="Number of bulletins issued in this hour")
    votes_cast: Optional[int] = Field(None, description="Number of votes cast in this hour")
    transaction_count: Optional[int] = Field(None, description="Total transactions in this hour")
    bulletin_velocity: Optional[float] = Field(None, description="Rate of bulletin issuance per hour")
    vote_velocity: Optional[float] = Field(None, description="Rate of vote casting per hour")


class HourlyStatsResponse(ResponseBase, HourlyStatsBase):
    """
    Schema for HourlyStats response.
    
    This schema is used for returning HourlyStats in API responses.
    """
    
    pass


class HourlyStatsList(BaseSchema):
    """
    Schema for list of HourlyStats.
    
    This schema is used for returning a list of HourlyStats in API responses.
    """
    
    data: List[HourlyStatsResponse]
    total: int
    page: int
    limit: int


class ActivityPoint(BaseSchema):
    """
    Schema for activity point.
    
    This schema is used for returning activity data for a specific hour.
    """
    
    hour: datetime = Field(..., description="Hour timestamp")
    votes: int = Field(..., description="Number of votes in this hour")
    bulletins: int = Field(..., description="Number of bulletins in this hour")


class ActivityTimeline(BaseSchema):
    """
    Schema for activity timeline.
    
    This schema is used for returning activity data over time.
    """
    
    timeline: List[ActivityPoint] = Field(..., description="Activity points over time")
    total_votes: int = Field(..., description="Total votes in the timeline")
    total_bulletins: int = Field(..., description="Total bulletins in the timeline")
    votes_per_hour: float = Field(..., description="Average votes per hour")
    bulletins_per_hour: float = Field(..., description="Average bulletins per hour")