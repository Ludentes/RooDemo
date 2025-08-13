"""
Tests for the metrics API endpoints.

This module contains tests for the metrics API endpoints.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.hourly_stats import HourlyStats
from app.models.constituency import Constituency
from app.models.election import Election
from app.services.hourly_stats_service import HourlyStatsService
from app.services.constituency_metrics_service import ConstituencyMetricsService
from app.services.metrics_cache_service import MetricsCacheService


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_hourly_stats_service():
    """Mock the hourly stats service."""
    with patch("app.api.routes.metrics.get_hourly_stats_service") as mock:
        service_mock = MagicMock()
        mock.return_value = service_mock
        yield service_mock


@pytest.fixture
def mock_constituency_metrics_service():
    """Mock the constituency metrics service."""
    with patch("app.api.routes.metrics.get_constituency_metrics_service") as mock:
        service_mock = MagicMock()
        mock.return_value = service_mock
        yield service_mock


@pytest.fixture
def mock_metrics_cache_service():
    """Mock the metrics cache service."""
    with patch("app.api.routes.metrics.get_metrics_cache_service") as mock:
        service_mock = MagicMock()
        mock.return_value = service_mock
        yield service_mock


def test_get_hourly_stats_by_constituency(client, mock_hourly_stats_service, mock_metrics_cache_service):
    """Test getting hourly stats by constituency."""
    # Setup
    constituency_id = "test-constituency"
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create test hourly stats
    stats = HourlyStats(
        id="test-stats",
        constituency_id=constituency_id,
        election_id="test-election",
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
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_hourly_stats_service.get_hourly_stats.return_value = [stats]
    
    # Make the request
    response = client.get(f"/api/metrics/hourly-stats/constituency/{constituency_id}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["data"][0]["constituency_id"] == constituency_id
    
    # Verify that the service was called with the correct parameters
    mock_hourly_stats_service.get_hourly_stats.assert_called_once_with(
        constituency_id=constituency_id,
        start_time=None,
        end_time=None
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_get_hourly_stats_by_constituency_cached(client, mock_hourly_stats_service, mock_metrics_cache_service):
    """Test getting hourly stats by constituency with cache hit."""
    # Setup
    constituency_id = "test-constituency"
    
    # Mock the cache hit
    cached_result = {
        "data": [{"id": "test-stats", "constituency_id": constituency_id}],
        "total": 1,
        "page": 1,
        "limit": 1
    }
    mock_metrics_cache_service.get.return_value = cached_result
    
    # Make the request
    response = client.get(f"/api/metrics/hourly-stats/constituency/{constituency_id}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == cached_result
    
    # Verify that the service was not called
    mock_hourly_stats_service.get_hourly_stats.assert_not_called()
    
    # Verify that the cache was checked
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_not_called()


def test_get_hourly_stats_by_election(client, mock_hourly_stats_service, mock_metrics_cache_service):
    """Test getting hourly stats by election."""
    # Setup
    election_id = "test-election"
    constituency_id = "test-constituency"
    hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    
    # Create test hourly stats
    stats = HourlyStats(
        id="test-stats",
        constituency_id=constituency_id,
        election_id=election_id,
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
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_hourly_stats_service.get_hourly_stats_for_election.return_value = {
        constituency_id: [stats]
    }
    
    # Make the request
    response = client.get(f"/api/metrics/hourly-stats/election/{election_id}")
    
    # Assertions
    assert response.status_code == 200
    assert constituency_id in response.json()
    assert len(response.json()[constituency_id]) == 1
    
    # Verify that the service was called with the correct parameters
    mock_hourly_stats_service.get_hourly_stats_for_election.assert_called_once_with(
        election_id=election_id,
        start_time=None,
        end_time=None
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_get_constituency_metrics(client, mock_constituency_metrics_service, mock_metrics_cache_service):
    """Test getting constituency metrics."""
    # Setup
    constituency_id = "test-constituency"
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_metrics = {
        "total_bulletins_issued": 100,
        "total_votes_cast": 80,
        "total_transactions": 200,
        "total_anomalies": 5,
        "participation_rate": 8.0,
        "anomaly_score": 2.5,
        "hourly_activity": []
    }
    mock_constituency_metrics_service.calculate_metrics.return_value = mock_metrics
    
    # Make the request
    response = client.get(f"/api/metrics/constituency/{constituency_id}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_metrics
    
    # Verify that the service was called with the correct parameters
    mock_constituency_metrics_service.calculate_metrics.assert_called_once_with(
        constituency_id=constituency_id,
        start_time=None,
        end_time=None,
        update_constituency=False
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_get_constituency_metrics_by_time_period(client, mock_constituency_metrics_service, mock_metrics_cache_service):
    """Test getting constituency metrics by time period."""
    # Setup
    constituency_id = "test-constituency"
    period = "day"
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_metrics = {
        "2025-08-13": {
            "total_bulletins_issued": 100,
            "total_votes_cast": 80,
            "total_transactions": 200,
            "total_anomalies": 5,
            "participation_rate": 8.0,
            "anomaly_score": 2.5,
            "hourly_activity": []
        }
    }
    mock_constituency_metrics_service.calculate_metrics_by_time_period.return_value = mock_metrics
    
    # Make the request
    response = client.get(f"/api/metrics/constituency/{constituency_id}/time-period?period={period}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_metrics
    
    # Verify that the service was called with the correct parameters
    mock_constituency_metrics_service.calculate_metrics_by_time_period.assert_called_once_with(
        constituency_id=constituency_id,
        period=period,
        start_time=None,
        end_time=None
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_get_election_metrics(client, mock_constituency_metrics_service, mock_metrics_cache_service):
    """Test getting election metrics."""
    # Setup
    election_id = "test-election"
    constituency_id = "test-constituency"
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_metrics = {
        constituency_id: {
            "total_bulletins_issued": 100,
            "total_votes_cast": 80,
            "total_transactions": 200,
            "total_anomalies": 5,
            "participation_rate": 8.0,
            "anomaly_score": 2.5,
            "hourly_activity": []
        }
    }
    mock_constituency_metrics_service.calculate_metrics_for_election.return_value = mock_metrics
    
    # Make the request
    response = client.get(f"/api/metrics/election/{election_id}")
    
    # Assertions
    assert response.status_code == 200
    assert constituency_id in response.json()
    
    # Verify that the service was called with the correct parameters
    mock_constituency_metrics_service.calculate_metrics_for_election.assert_called_once_with(
        election_id=election_id,
        start_time=None,
        end_time=None,
        update_constituencies=False
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_get_election_constituency_metrics(client, mock_constituency_metrics_service, mock_metrics_cache_service):
    """Test getting election constituency metrics."""
    # Setup
    election_id = "test-election"
    constituency_id = "test-constituency"
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_metrics = {
        constituency_id: {
            "total_bulletins_issued": 100,
            "total_votes_cast": 80,
            "total_transactions": 200,
            "total_anomalies": 5,
            "participation_rate": 8.0,
            "anomaly_score": 2.5,
            "hourly_activity": []
        }
    }
    mock_constituency_metrics_service.calculate_metrics_for_election.return_value = mock_metrics
    
    # Make the request
    response = client.get(f"/api/metrics/election/{election_id}/constituencies")
    
    # Assertions
    assert response.status_code == 200
    assert constituency_id in response.json()
    
    # Verify that the service was called with the correct parameters
    mock_constituency_metrics_service.calculate_metrics_for_election.assert_called_once_with(
        election_id=election_id,
        update_constituencies=False
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_compare_constituencies(client, mock_constituency_metrics_service, mock_metrics_cache_service):
    """Test comparing constituencies."""
    # Setup
    constituency_ids = ["constituency1", "constituency2"]
    
    # Mock the cache miss
    mock_metrics_cache_service.get.return_value = None
    
    # Mock the service response
    mock_metrics = {
        "constituency1": {
            "total_bulletins_issued": 100,
            "total_votes_cast": 80,
            "total_transactions": 200,
            "total_anomalies": 5,
            "participation_rate": 8.0,
            "anomaly_score": 2.5,
            "hourly_activity": []
        },
        "constituency2": {
            "total_bulletins_issued": 150,
            "total_votes_cast": 120,
            "total_transactions": 300,
            "total_anomalies": 10,
            "participation_rate": 12.0,
            "anomaly_score": 3.33,
            "hourly_activity": []
        }
    }
    mock_constituency_metrics_service.compare_constituencies.return_value = mock_metrics
    
    # Make the request
    response = client.get(f"/api/metrics/compare-constituencies?constituency_ids={constituency_ids[0]}&constituency_ids={constituency_ids[1]}")
    
    # Assertions
    assert response.status_code == 200
    assert "constituency1" in response.json()
    assert "constituency2" in response.json()
    
    # Verify that the service was called with the correct parameters
    mock_constituency_metrics_service.compare_constituencies.assert_called_once_with(
        constituency_ids=constituency_ids,
        start_time=None,
        end_time=None
    )
    
    # Verify that the cache was checked and set
    mock_metrics_cache_service.get.assert_called_once()
    mock_metrics_cache_service.set.assert_called_once()


def test_invalidate_constituency_cache(client, mock_metrics_cache_service):
    """Test invalidating constituency cache."""
    # Setup
    constituency_id = "test-constituency"
    
    # Mock the service response
    mock_metrics_cache_service.invalidate_constituency_cache.return_value = 5
    
    # Make the request
    response = client.post(f"/api/metrics/invalidate-cache/constituency/{constituency_id}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["invalidated"] == 5
    
    # Verify that the service was called with the correct parameters
    mock_metrics_cache_service.invalidate_constituency_cache.assert_called_once_with(constituency_id)


def test_invalidate_election_cache(client, mock_metrics_cache_service):
    """Test invalidating election cache."""
    # Setup
    election_id = "test-election"
    
    # Mock the service response
    mock_metrics_cache_service.invalidate_election_cache.return_value = 10
    
    # Make the request
    response = client.post(f"/api/metrics/invalidate-cache/election/{election_id}")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["invalidated"] == 10
    
    # Verify that the service was called with the correct parameters
    mock_metrics_cache_service.invalidate_election_cache.assert_called_once_with(election_id)


def test_invalidate_dashboard_cache(client, mock_metrics_cache_service):
    """Test invalidating dashboard cache."""
    # Mock the service response
    mock_metrics_cache_service.invalidate_dashboard_cache.return_value = 2
    
    # Make the request
    response = client.post("/api/metrics/invalidate-cache/dashboard")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["invalidated"] == 2
    
    # Verify that the service was called
    mock_metrics_cache_service.invalidate_dashboard_cache.assert_called_once()