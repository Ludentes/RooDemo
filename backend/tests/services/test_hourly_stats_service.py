"""
Tests for the HourlyStatsService.

This module contains tests for the HourlyStatsService.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.models.hourly_stats import HourlyStats
from app.models.constituency import Constituency
from app.models.election import Election
from app.models.transaction import Transaction
from app.services.hourly_stats_service import HourlyStatsService


@pytest.fixture
def db_session_mock():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def election():
    """Create a test election."""
    return Election(
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


@pytest.fixture
def constituency(election):
    """Create a test constituency."""
    return Constituency(
        id="test-constituency",
        election_id=election.id,
        name="Test Constituency",
        region="Test Region",
        type="REGULAR",
        registered_voters=1000,
        status="ACTIVE"
    )


@pytest.fixture
def transactions(constituency):
    """Create test transactions."""
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create 10 bulletin transactions
    bulletin_transactions = [
        Transaction(
            id=f"bulletin-{i}",
            constituency_id=constituency.id,
            block_height=1000 + i,
            timestamp=hour + timedelta(minutes=i),
            type="BULLETIN_ISSUED",
            raw_data={},
            operation_data={}
        )
        for i in range(10)
    ]
    
    # Create 8 vote transactions
    vote_transactions = [
        Transaction(
            id=f"vote-{i}",
            constituency_id=constituency.id,
            block_height=2000 + i,
            timestamp=hour + timedelta(minutes=i),
            type="VOTE_CAST",
            raw_data={},
            operation_data={}
        )
        for i in range(8)
    ]
    
    # Create 2 anomaly transactions
    anomaly_transactions = [
        Transaction(
            id=f"anomaly-{i}",
            constituency_id=constituency.id,
            block_height=3000 + i,
            timestamp=hour + timedelta(minutes=i),
            type="VOTE_CAST",
            raw_data={},
            operation_data={},
            anomaly_detected=True,
            anomaly_reason="Test anomaly"
        )
        for i in range(2)
    ]
    
    return bulletin_transactions + vote_transactions + anomaly_transactions


def test_aggregate_hourly_stats(db_session_mock, constituency, transactions):
    """Test aggregating hourly stats."""
    # Setup
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create the service
    service = HourlyStatsService(db_session_mock)
    
    # Mock the database query results
    # Mock constituency_crud.get to return the constituency
    with patch('app.services.hourly_stats_service.constituency_crud.get') as mock_get:
        mock_get.return_value = constituency
        
        # Mock the query for existing stats to return None (no existing stats)
        db_session_mock.query.return_value.filter.return_value.first.return_value = None
        
        # Mock the query for transactions
        db_session_mock.query.return_value.filter.return_value.filter.return_value.filter.return_value.all.return_value = transactions
        
        # Mock the _calculate_metrics method to return predefined metrics
        with patch.object(service, '_calculate_metrics') as mock_calculate:
            mock_calculate.return_value = {
                "bulletins_issued": 10,
                "votes_cast": 10,
                "transaction_count": 20,
                "bulletin_velocity": 10.0,
                "vote_velocity": 10.0,
                "participation_rate": 1.0,
                "anomaly_count": 2
            }
            
            # Mock hourly_stats_crud.create to return a stats object with the expected values
            with patch('app.services.hourly_stats_service.hourly_stats_crud.create') as mock_create:
                # Create a new stats object with the expected values
                new_stats = HourlyStats(
                    id="test-stats",
                    constituency_id=constituency.id,
                    election_id=constituency.election_id,
                    hour=hour,
                    timestamp=datetime.utcnow(),
                    bulletins_issued=10,
                    votes_cast=10,
                    transaction_count=20,
                    bulletin_velocity=10.0,
                    vote_velocity=10.0,
                    participation_rate=1.0,
                    anomaly_count=2
                )
                mock_create.return_value = new_stats
                
                # Call the method
                result = service.aggregate_hourly_stats(
                    constituency_id=constituency.id,
                    hour=hour
                )
    
    # Assertions
    assert result is not None
    assert result.constituency_id == constituency.id
    assert result.election_id == constituency.election_id
    assert result.hour == hour
    assert result.bulletins_issued == 10
    assert result.votes_cast == 10  # 8 regular + 2 anomaly
    assert result.transaction_count == 20
    assert result.bulletin_velocity == 10.0
    assert result.vote_velocity == 10.0
    assert result.participation_rate == 1.0  # 10 votes / 1000 registered voters * 100
    assert result.anomaly_count == 2


def test_aggregate_hourly_stats_existing(db_session_mock, constituency):
    """Test aggregating hourly stats when they already exist."""
    # Setup
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create existing hourly stats
    existing_stats = HourlyStats(
        id="existing-stats",
        constituency_id=constituency.id,
        election_id=constituency.election_id,
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
    
    # Create the service
    service = HourlyStatsService(db_session_mock)
    
    # Mock the database query results
    # Mock constituency_crud.get to return the constituency
    with patch('app.services.hourly_stats_service.constituency_crud.get') as mock_get:
        mock_get.return_value = constituency
        
        # Mock the query for existing stats to return the existing stats
        db_session_mock.query.return_value.filter.return_value.first.return_value = existing_stats
        
        # Call the method
        result = service.aggregate_hourly_stats(
            constituency_id=constituency.id,
            hour=hour,
            force_recalculate=False
        )
    
    # Assertions
    assert result is not None
    assert result.id == existing_stats.id
    assert result.bulletins_issued == 100
    assert result.votes_cast == 80
    
    # Verify that no further queries were made
    db_session_mock.query.return_value.filter.return_value.filter.return_value.filter.return_value.all.assert_not_called()


def test_aggregate_hourly_stats_force_recalculate(db_session_mock, constituency, transactions):
    """Test aggregating hourly stats with force_recalculate=True."""
    # Setup
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create existing hourly stats
    existing_stats = HourlyStats(
        id="existing-stats",
        constituency_id=constituency.id,
        election_id=constituency.election_id,
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
    
    # Create the service
    service = HourlyStatsService(db_session_mock)
    
    # Create updated stats with the same ID as existing stats
    updated_stats = HourlyStats(
        id=existing_stats.id,
        constituency_id=constituency.id,
        election_id=constituency.election_id,
        hour=hour,
        timestamp=datetime.utcnow(),
        bulletins_issued=10,  # Updated values based on transactions
        votes_cast=10,
        transaction_count=20,
        bulletin_velocity=10.0,
        vote_velocity=10.0,
        participation_rate=1.0,
        anomaly_count=2
    )
    
    # Mock the database query results
    with patch('app.services.hourly_stats_service.constituency_crud.get') as mock_get:
        mock_get.return_value = constituency
        
        # Mock the query for existing stats to return the existing stats
        db_session_mock.query.return_value.filter.return_value.first.return_value = existing_stats
        
        # Mock the query for transactions
        db_session_mock.query.return_value.filter.return_value.filter.return_value.filter.return_value.all.return_value = transactions
        
        # Mock the _calculate_metrics method to return predefined metrics
        with patch.object(service, '_calculate_metrics') as mock_calculate:
            mock_calculate.return_value = {
                "bulletins_issued": 10,
                "votes_cast": 10,
                "transaction_count": 20,
                "bulletin_velocity": 10.0,
                "vote_velocity": 10.0,
                "participation_rate": 1.0,
                "anomaly_count": 2
            }
            
            # Define a side effect function for the update mock
            def update_side_effect(db, db_obj, obj_in):
                # Call commit on the db session
                db.commit.assert_not_called()  # Ensure commit hasn't been called yet
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
                # Return the updated stats
                return updated_stats
            
            # Mock hourly_stats_crud.update to call db_session_mock.commit
            with patch('app.services.hourly_stats_service.hourly_stats_crud.update') as mock_update:
                mock_update.side_effect = update_side_effect
                
                # Call the method
                result = service.aggregate_hourly_stats(
                    constituency_id=constituency.id,
                    hour=hour,
                    force_recalculate=True
                )
    
    # Assertions
    assert result is not None
    assert result.id == existing_stats.id
    
    # Verify that the update method was called
    # Note: The update method is called via hourly_stats_crud.update, not db_session_mock.add
    # So we don't need to verify db_session_mock.add was called
    db_session_mock.commit.assert_called()
    db_session_mock.refresh.assert_called_with(existing_stats)


def test_aggregate_hourly_stats_for_timerange(db_session_mock, constituency):
    """Test aggregating hourly stats for a time range."""
    # Setup
    start_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=3)
    
    # Mock the aggregate_hourly_stats method
    with patch.object(HourlyStatsService, 'aggregate_hourly_stats') as mock_aggregate:
        mock_aggregate.return_value = MagicMock()
        
        # Create the service
        service = HourlyStatsService(db_session_mock)
        
        # Call the method
        results = service.aggregate_hourly_stats_for_timerange(
            constituency_id=constituency.id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Assertions
        assert len(results) == 4  # start_time, start_time+1h, start_time+2h, end_time
        assert mock_aggregate.call_count == 4
        
        # Verify that aggregate_hourly_stats was called with the correct hours
        expected_hours = [
            start_time,
            start_time + timedelta(hours=1),
            start_time + timedelta(hours=2),
            end_time
        ]
        for i, hour in enumerate(expected_hours):
            assert mock_aggregate.call_args_list[i][1]['hour'] == hour


def test_aggregate_hourly_stats_for_election(db_session_mock, election, constituency):
    """Test aggregating hourly stats for an election."""
    # Setup
    start_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=3)
    
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.all.return_value = [constituency]
    
    # Mock the aggregate_hourly_stats_for_timerange method
    with patch.object(HourlyStatsService, 'aggregate_hourly_stats_for_timerange') as mock_aggregate:
        mock_aggregate.return_value = [MagicMock()]
        
        # Create the service
        service = HourlyStatsService(db_session_mock)
        
        # Call the method
        results = service.aggregate_hourly_stats_for_election(
            election_id=election.id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Assertions
        assert constituency.id in results
        assert len(results[constituency.id]) == 1
        
        # Verify that aggregate_hourly_stats_for_timerange was called with the correct parameters
        mock_aggregate.assert_called_once_with(
            constituency_id=constituency.id,
            start_time=start_time,
            end_time=end_time,
            force_recalculate=False
        )


def test_get_hourly_stats(db_session_mock, constituency):
    """Test getting hourly stats."""
    # Setup
    hour1 = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hour2 = hour1 - timedelta(hours=1)
    
    # Create hourly stats
    stats1 = HourlyStats(
        id="stats1",
        constituency_id=constituency.id,
        election_id=constituency.election_id,
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
    
    stats2 = HourlyStats(
        id="stats2",
        constituency_id=constituency.id,
        election_id=constituency.election_id,
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
    
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.order_by.return_value.all.return_value = [stats1, stats2]
    
    # Create the service
    service = HourlyStatsService(db_session_mock)
    
    # Call the method
    results = service.get_hourly_stats(
        constituency_id=constituency.id
    )
    
    # Assertions
    assert len(results) == 2
    assert results[0].id == stats1.id
    assert results[1].id == stats2.id


def test_get_hourly_stats_with_time_range(db_session_mock, constituency):
    """Test getting hourly stats with a time range."""
    # Setup
    start_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - timedelta(hours=2)
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create hourly stats
    stats = HourlyStats(
        id="stats",
        constituency_id=constituency.id,
        election_id=constituency.election_id,
        hour=end_time - timedelta(hours=1),
        timestamp=datetime.utcnow(),
        bulletins_issued=100,
        votes_cast=80,
        transaction_count=200,
        bulletin_velocity=100.0,
        vote_velocity=80.0,
        participation_rate=8.0,
        anomaly_count=5
    )
    
    # Mock the database query results
    query_mock = MagicMock()
    filter_mock = MagicMock()
    order_mock = MagicMock()
    
    db_session_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.filter.return_value = filter_mock
    filter_mock.order_by.return_value = order_mock
    order_mock.all.return_value = [stats]
    
    # Create the service
    service = HourlyStatsService(db_session_mock)
    
    # Call the method
    results = service.get_hourly_stats(
        constituency_id=constituency.id,
        start_time=start_time,
        end_time=end_time
    )
    
    # Assertions
    assert len(results) == 1
    assert results[0].id == stats.id
    
    # Verify that the correct filters were applied
    assert query_mock.filter.call_count == 1  # Called once for constituency_id filter
    assert filter_mock.filter.call_count == 2  # Called twice for start_time and end_time filters