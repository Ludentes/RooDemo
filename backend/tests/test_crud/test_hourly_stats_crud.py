"""
Tests for the HourlyStats CRUD operations.

This module contains tests for the HourlyStats CRUD operations.
"""

import pytest
from datetime import datetime, timedelta

from app.models.hourly_stats import HourlyStats
from app.models.constituency import Constituency
from app.models.election import Election
from app.crud.hourly_stats import hourly_stats_crud
from app.models.schemas.hourly_stats import HourlyStatsCreate, HourlyStatsUpdate


@pytest.fixture
def election(db_session):
    """Create a test election."""
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
    return election


@pytest.fixture
def constituency(db_session, election):
    """Create a test constituency."""
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
    return constituency


def test_create_hourly_stats(db_session, constituency, election):
    """Test creating hourly stats."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    stats_data = HourlyStatsCreate(
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
    
    stats = hourly_stats_crud.create(db_session, obj_in=stats_data)
    
    assert stats.id is not None
    assert stats.constituency_id == constituency.id
    assert stats.election_id == election.id
    assert stats.hour == hour
    assert stats.bulletins_issued == 100
    assert stats.votes_cast == 80
    assert stats.transaction_count == 200
    assert stats.bulletin_velocity == 100.0
    assert stats.vote_velocity == 80.0
    assert stats.participation_rate == 8.0
    assert stats.anomaly_count == 5


def test_get_hourly_stats(db_session, constituency, election):
    """Test getting hourly stats by ID."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    stats_data = HourlyStatsCreate(
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
    
    created_stats = hourly_stats_crud.create(db_session, obj_in=stats_data)
    
    retrieved_stats = hourly_stats_crud.get(db_session, id=created_stats.id)
    
    assert retrieved_stats is not None
    assert retrieved_stats.id == created_stats.id
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


def test_update_hourly_stats(db_session, constituency, election):
    """Test updating hourly stats."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    stats_data = HourlyStatsCreate(
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
    
    created_stats = hourly_stats_crud.create(db_session, obj_in=stats_data)
    
    update_data = HourlyStatsUpdate(
        bulletins_issued=150,
        votes_cast=120,
        transaction_count=300,
        bulletin_velocity=150.0,
        vote_velocity=120.0,
        participation_rate=12.0,
        anomaly_count=10
    )
    
    updated_stats = hourly_stats_crud.update(db_session, db_obj=created_stats, obj_in=update_data)
    
    assert updated_stats.id == created_stats.id
    assert updated_stats.constituency_id == constituency.id
    assert updated_stats.election_id == election.id
    assert updated_stats.hour == hour
    assert updated_stats.bulletins_issued == 150
    assert updated_stats.votes_cast == 120
    assert updated_stats.transaction_count == 300
    assert updated_stats.bulletin_velocity == 150.0
    assert updated_stats.vote_velocity == 120.0
    assert updated_stats.participation_rate == 12.0
    assert updated_stats.anomaly_count == 10


def test_delete_hourly_stats(db_session, constituency, election):
    """Test deleting hourly stats."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    stats_data = HourlyStatsCreate(
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
    
    created_stats = hourly_stats_crud.create(db_session, obj_in=stats_data)
    
    deleted_stats = hourly_stats_crud.remove(db_session, id=created_stats.id)
    
    assert deleted_stats.id == created_stats.id
    
    retrieved_stats = hourly_stats_crud.get(db_session, id=created_stats.id)
    assert retrieved_stats is None


def test_get_by_constituency(db_session, constituency, election):
    """Test getting hourly stats by constituency ID."""
    hour1 = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hour2 = hour1 - timedelta(hours=1)
    
    # Create two hourly stats for the same constituency
    stats_data1 = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour1,
        timestamp=datetime.utcnow(),
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    
    stats_data2 = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour2,
        timestamp=datetime.utcnow(),
        bulletins_issued=150,
        votes_cast=120,
        transaction_count=300,
        bulletin_velocity=150.0,
        vote_velocity=120.0,
        participation_rate=12.0,
        anomaly_count=10
    )
    
    hourly_stats_crud.create(db_session, obj_in=stats_data1)
    hourly_stats_crud.create(db_session, obj_in=stats_data2)
    
    # Get hourly stats by constituency ID
    stats_list = hourly_stats_crud.get_by_constituency(db_session, constituency_id=constituency.id)
    
    assert len(stats_list) == 2
    assert all(stats.constituency_id == constituency.id for stats in stats_list)


def test_get_by_election(db_session, constituency, election):
    """Test getting hourly stats by election ID."""
    hour1 = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hour2 = hour1 - timedelta(hours=1)
    
    # Create two hourly stats for the same election
    stats_data1 = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour1,
        timestamp=datetime.utcnow(),
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    
    stats_data2 = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour2,
        timestamp=datetime.utcnow(),
        bulletins_issued=150,
        votes_cast=120,
        transaction_count=300,
        bulletin_velocity=150.0,
        vote_velocity=120.0,
        participation_rate=12.0,
        anomaly_count=10
    )
    
    hourly_stats_crud.create(db_session, obj_in=stats_data1)
    hourly_stats_crud.create(db_session, obj_in=stats_data2)
    
    # Get hourly stats by election ID
    stats_list = hourly_stats_crud.get_by_election(db_session, election_id=election.id)
    
    assert len(stats_list) == 2
    assert all(stats.election_id == election.id for stats in stats_list)


def test_create_or_update_stats(db_session, constituency, election):
    """Test creating or updating hourly stats."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    timestamp = datetime.utcnow()
    
    # Create initial stats
    stats_data = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour,
        timestamp=timestamp,
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    
    created_stats = hourly_stats_crud.create_or_update_stats(db_session, obj_in=stats_data)
    
    assert created_stats.bulletins_issued == 100
    assert created_stats.votes_cast == 80
    
    # Update the stats
    update_data = HourlyStatsCreate(
        constituency_id=constituency.id,
        election_id=election.id,
        hour=hour,
        timestamp=timestamp,
        bulletins_issued=150,
        votes_cast=120,
        transaction_count=300,
        bulletin_velocity=150.0,
        vote_velocity=120.0,
        participation_rate=12.0,
        anomaly_count=10
    )
    
    updated_stats = hourly_stats_crud.create_or_update_stats(db_session, obj_in=update_data)
    
    assert updated_stats.id == created_stats.id
    assert updated_stats.bulletins_issued == 150
    assert updated_stats.votes_cast == 120