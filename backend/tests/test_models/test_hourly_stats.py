"""
Tests for the HourlyStats model.

This module contains tests for the HourlyStats model.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from app.models.hourly_stats import HourlyStats
from app.models.constituency import Constituency
from app.models.election import Election


def test_hourly_stats_creation(db_session):
    """Test creating a HourlyStats instance."""
    # Create an election
    election = Election(
        id="test-election",
        name="Test Election",
        country="Test Country",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        status="ACTIVE",
        type="GENERAL",
        description="Test election description",
        timezone="UTC",
        total_constituencies=1
    )
    db_session.add(election)
    db_session.commit()
    
    # Create a constituency
    constituency = Constituency(
        id="test-constituency",
        election_id=election.id,
        name="Test Constituency",
        region="Test Region",
        type="REGULAR",
        registered_voters=1000,
        status="ACTIVE"
    )
    db_session.add(constituency)
    db_session.commit()
    
    # Create hourly stats
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hourly_stats = HourlyStats(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour,
        timestamp=datetime.utcnow(),
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    db_session.add(hourly_stats)
    db_session.commit()
    
    # Retrieve the hourly stats from the database
    retrieved_stats = db_session.query(HourlyStats).filter(HourlyStats.id == hourly_stats.id).first()
    
    # Check that the retrieved stats match the created stats
    assert retrieved_stats is not None
    assert retrieved_stats.constituency_id == constituency.id
    assert retrieved_stats.election_id == election.id
    assert retrieved_stats.hour == hour
    assert retrieved_stats.bulletins_issued == 100
    assert retrieved_stats.votes_cast == 80
    assert retrieved_stats.transaction_count == 200
    assert retrieved_stats.bulletin_velocity == 100.0
    assert retrieved_stats.vote_velocity == 80.0
    assert retrieved_stats.participation_rate == 8.0
    assert retrieved_stats.anomaly_count == 5


def test_hourly_stats_relationships(db_session):
    """Test HourlyStats relationships."""
    # Create an election
    election = Election(
        id="test-election",
        name="Test Election",
        country="Test Country",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        status="ACTIVE",
        type="GENERAL",
        description="Test election description",
        timezone="UTC",
        total_constituencies=1
    )
    db_session.add(election)
    db_session.commit()
    
    # Create a constituency
    constituency = Constituency(
        id="test-constituency",
        election_id=election.id,
        name="Test Constituency",
        region="Test Region",
        type="REGULAR",
        registered_voters=1000,
        status="ACTIVE"
    )
    db_session.add(constituency)
    db_session.commit()
    
    # Create hourly stats
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hourly_stats = HourlyStats(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour,
        timestamp=datetime.utcnow(),
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    db_session.add(hourly_stats)
    db_session.commit()
    
    # Check relationships
    assert hourly_stats.constituency is not None
    assert hourly_stats.constituency.id == constituency.id
    assert hourly_stats.election is not None
    assert hourly_stats.election.id == election.id
    
    # Check reverse relationships
    assert hourly_stats in constituency.hourly_stats
    assert hourly_stats in election.hourly_stats


def test_hourly_stats_required_fields(db_session):
    """Test that required fields are enforced."""
    # Create hourly stats without required fields
    hourly_stats = HourlyStats()
    db_session.add(hourly_stats)
    
    # Expect an integrity error when committing
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback the session
    db_session.rollback()


def test_hourly_stats_round_hour():
    """Test the round_hour method."""
    # Test rounding to the nearest hour
    dt = datetime(2025, 1, 1, 12, 30, 45)
    rounded = HourlyStats.round_hour(dt)
    assert rounded == datetime(2025, 1, 1, 12, 0, 0)
    
    # Test rounding at the start of an hour
    dt = datetime(2025, 1, 1, 12, 0, 0)
    rounded = HourlyStats.round_hour(dt)
    assert rounded == dt
    
    # Test rounding at the end of an hour
    dt = datetime(2025, 1, 1, 12, 59, 59, 999999)
    rounded = HourlyStats.round_hour(dt)
    assert rounded == datetime(2025, 1, 1, 12, 0, 0)