"""
Tests for the ConstituencyMetricsService.

This module contains tests for the ConstituencyMetricsService.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.models.hourly_stats import HourlyStats
from app.models.constituency import Constituency
from app.models.election import Election
from app.services.constituency_metrics_service import ConstituencyMetricsService


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
def hourly_stats(constituency):
    """Create test hourly stats."""
    hour1 = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    hour2 = hour1 - timedelta(hours=1)
    hour3 = hour1 - timedelta(hours=2)
    
    return [
        HourlyStats(
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
        ),
        HourlyStats(
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
        ),
        HourlyStats(
            id="stats3",
            constituency_id=constituency.id,
            election_id=constituency.election_id,
            hour=hour3,
            timestamp=datetime.utcnow(),
            bulletins_issued=200,
            votes_cast=180,
            transaction_count=400,
            bulletin_velocity=200.0,
            vote_velocity=180.0,
            participation_rate=18.0,
            anomaly_count=15
        )
    ]


def test_calculate_metrics(db_session_mock, constituency, hourly_stats):
    """Test calculating metrics for a constituency."""
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.first.return_value = constituency
    
    # Mock the hourly_stats_service.get_hourly_stats method
    hourly_stats_service_mock = MagicMock()
    hourly_stats_service_mock.get_hourly_stats.return_value = hourly_stats
    
    # Create the service with the mocked hourly_stats_service
    service = ConstituencyMetricsService(db_session_mock)
    service.hourly_stats_service = hourly_stats_service_mock
    
    # Call the method
    metrics = service.calculate_metrics(
        constituency_id=constituency.id,
        update_constituency=False
    )
    
    # Assertions
    assert metrics is not None
    assert metrics["total_bulletins_issued"] == 450  # 100 + 150 + 200
    assert metrics["total_votes_cast"] == 380  # 80 + 120 + 180
    assert metrics["total_transactions"] == 900  # 200 + 300 + 400
    assert metrics["total_anomalies"] == 30  # 5 + 10 + 15
    assert metrics["participation_rate"] == 38.0  # (380 / 1000) * 100
    assert metrics["anomaly_score"] == 3.33  # (30 / 900) * 100, rounded to 2 decimal places
    assert metrics["average_votes_per_hour"] == 126.67  # 380 / 3, rounded to 2 decimal places
    assert metrics["average_bulletins_per_hour"] == 150.0  # 450 / 3
    assert len(metrics["hourly_activity"]) == 3
    
    # Verify that hourly_stats_service.get_hourly_stats was called with the correct parameters
    hourly_stats_service_mock.get_hourly_stats.assert_called_once_with(
        constituency_id=constituency.id,
        start_time=None,
        end_time=None
    )


def test_calculate_metrics_update_constituency(db_session_mock, constituency, hourly_stats):
    """Test calculating metrics and updating the constituency."""
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.first.return_value = constituency
    
    # Mock the hourly_stats_service.get_hourly_stats method
    hourly_stats_service_mock = MagicMock()
    hourly_stats_service_mock.get_hourly_stats.return_value = hourly_stats
    
    # Create the service with the mocked hourly_stats_service
    service = ConstituencyMetricsService(db_session_mock)
    service.hourly_stats_service = hourly_stats_service_mock
    
    # Call the method
    metrics = service.calculate_metrics(
        constituency_id=constituency.id,
        update_constituency=True
    )
    
    # Assertions
    assert metrics is not None
    
    # Verify that the constituency was updated
    assert constituency.bulletins_issued == 450
    assert constituency.votes_cast == 380
    assert constituency.participation_rate == 38.0
    assert constituency.anomaly_score == 3.33
    assert constituency.last_update_time is not None
    
    # Verify that the constituency was saved to the database
    db_session_mock.add.assert_called_once_with(constituency)
    db_session_mock.commit.assert_called_once()
    db_session_mock.refresh.assert_called_once_with(constituency)


def test_calculate_metrics_with_time_range(db_session_mock, constituency, hourly_stats):
    """Test calculating metrics with a time range."""
    # Setup
    start_time = datetime.utcnow() - timedelta(hours=2)
    end_time = datetime.utcnow()
    
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.first.return_value = constituency
    
    # Mock the hourly_stats_service.get_hourly_stats method
    hourly_stats_service_mock = MagicMock()
    hourly_stats_service_mock.get_hourly_stats.return_value = hourly_stats
    
    # Create the service with the mocked hourly_stats_service
    service = ConstituencyMetricsService(db_session_mock)
    service.hourly_stats_service = hourly_stats_service_mock
    
    # Call the method
    metrics = service.calculate_metrics(
        constituency_id=constituency.id,
        start_time=start_time,
        end_time=end_time,
        update_constituency=False
    )
    
    # Assertions
    assert metrics is not None
    
    # Verify that hourly_stats_service.get_hourly_stats was called with the correct parameters
    hourly_stats_service_mock.get_hourly_stats.assert_called_once_with(
        constituency_id=constituency.id,
        start_time=start_time,
        end_time=end_time
    )


def test_calculate_metrics_by_time_period(db_session_mock, constituency, hourly_stats):
    """Test calculating metrics by time period."""
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.first.return_value = constituency
    
    # Mock the hourly_stats_service.get_hourly_stats method
    hourly_stats_service_mock = MagicMock()
    hourly_stats_service_mock.get_hourly_stats.return_value = hourly_stats
    
    # Create the service with the mocked hourly_stats_service
    service = ConstituencyMetricsService(db_session_mock)
    service.hourly_stats_service = hourly_stats_service_mock
    
    # Call the method
    metrics = service.calculate_metrics_by_time_period(
        constituency_id=constituency.id,
        period="day"
    )
    
    # Assertions
    assert metrics is not None
    assert len(metrics) == 1  # All hourly stats are from the same day
    
    # Get the metrics for the day
    day_key = list(metrics.keys())[0]
    day_metrics = metrics[day_key]
    
    # Verify the metrics
    assert day_metrics["total_bulletins_issued"] == 450
    assert day_metrics["total_votes_cast"] == 380
    assert day_metrics["total_transactions"] == 900
    assert day_metrics["total_anomalies"] == 30
    assert day_metrics["participation_rate"] == 38.0
    assert day_metrics["anomaly_score"] == 3.33
    
    # Verify that hourly_stats_service.get_hourly_stats was called with the correct parameters
    hourly_stats_service_mock.get_hourly_stats.assert_called_once_with(
        constituency_id=constituency.id,
        start_time=None,
        end_time=None
    )


def test_calculate_metrics_for_election(db_session_mock, election, constituency):
    """Test calculating metrics for an election."""
    # Mock the database query results
    db_session_mock.query.return_value.filter.return_value.all.return_value = [constituency]
    
    # Mock the calculate_metrics method
    with patch.object(ConstituencyMetricsService, 'calculate_metrics') as mock_calculate:
        mock_calculate.return_value = {"test": "metrics"}
        
        # Create the service
        service = ConstituencyMetricsService(db_session_mock)
        
        # Call the method
        results = service.calculate_metrics_for_election(
            election_id=election.id,
            update_constituencies=False
        )
        
        # Assertions
        assert constituency.id in results
        assert results[constituency.id] == {"test": "metrics"}
        
        # Verify that calculate_metrics was called with the correct parameters
        mock_calculate.assert_called_once_with(
            constituency_id=constituency.id,
            start_time=None,
            end_time=None,
            update_constituency=False
        )


def test_compare_constituencies(db_session_mock, constituency):
    """Test comparing constituencies."""
    # Mock the calculate_metrics method
    with patch.object(ConstituencyMetricsService, 'calculate_metrics') as mock_calculate:
        mock_calculate.return_value = {"test": "metrics"}
        
        # Create the service
        service = ConstituencyMetricsService(db_session_mock)
        
        # Call the method
        results = service.compare_constituencies(
            constituency_ids=[constituency.id, "another-constituency"]
        )
        
        # Assertions
        assert constituency.id in results
        assert "another-constituency" in results
        assert results[constituency.id] == {"test": "metrics"}
        assert results["another-constituency"] == {"test": "metrics"}
        
        # Verify that calculate_metrics was called with the correct parameters
        assert mock_calculate.call_count == 2
        mock_calculate.assert_any_call(
            constituency_id=constituency.id,
            start_time=None,
            end_time=None,
            update_constituency=False
        )
        mock_calculate.assert_any_call(
            constituency_id="another-constituency",
            start_time=None,
            end_time=None,
            update_constituency=False
        )


def test_calculate_trend():
    """Test calculating trend."""
    # Create the service
    service = ConstituencyMetricsService(MagicMock())
    
    # Test with increasing values
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    trend = service._calculate_trend(values)
    assert trend == 1.0  # Perfect linear increase
    
    # Test with decreasing values
    values = [5.0, 4.0, 3.0, 2.0, 1.0]
    trend = service._calculate_trend(values)
    assert trend == -1.0  # Perfect linear decrease
    
    # Test with constant values
    values = [3.0, 3.0, 3.0, 3.0, 3.0]
    trend = service._calculate_trend(values)
    assert trend == 0.0  # No trend
    
    # Test with empty list
    values = []
    trend = service._calculate_trend(values)
    assert trend == 0.0  # Default value for empty list
    
    # Test with single value
    values = [5.0]
    trend = service._calculate_trend(values)
    assert trend == 0.0  # Default value for single value