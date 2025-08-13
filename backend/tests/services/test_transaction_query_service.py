"""
Tests for the TransactionQueryService.

This module contains tests for the transaction query service.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy import desc, asc

from app.services.transaction_query_service import TransactionQueryService
from app.models.transaction import Transaction


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def query_service(mock_db):
    """Create a TransactionQueryService with a mock database session."""
    return TransactionQueryService(db=mock_db)


def test_build_query_no_filters(query_service, mock_db):
    """Test building a query with no filters."""
    # Arrange
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    
    # Act
    result = query_service.build_query()
    
    # Assert
    mock_db.query.assert_called_once_with(Transaction)
    mock_query.order_by.assert_called_once()
    assert result == mock_query


def test_build_query_with_filters(query_service, mock_db):
    """Test building a query with filters."""
    # Arrange
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    
    # Act
    result = query_service.build_query(
        constituency_id="test_constituency",
        transaction_type="blindSigIssue",
        start_time=datetime(2024, 9, 1),
        end_time=datetime(2024, 9, 30),
        status="processed",
        anomaly_detected=True,
        source="file_upload",
        file_id="test_file",
        sort_by="timestamp",
        sort_order="asc"
    )
    
    # Assert
    mock_db.query.assert_called_once_with(Transaction)
    mock_query.filter.assert_called_once()
    mock_query.order_by.assert_called_once()
    assert result == mock_query


def test_build_query_sort_order(query_service, mock_db):
    """Test building a query with different sort orders."""
    # Arrange
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    
    # Act - Test ascending order
    query_service.build_query(sort_by="timestamp", sort_order="asc")
    
    # Assert
    mock_query.order_by.assert_called_with(asc(Transaction.timestamp))
    
    # Reset mock
    mock_query.reset_mock()
    
    # Act - Test descending order
    query_service.build_query(sort_by="timestamp", sort_order="desc")
    
    # Assert
    mock_query.order_by.assert_called_with(desc(Transaction.timestamp))


def test_execute_query(query_service, mock_db):
    """Test executing a query with pagination."""
    # Arrange
    mock_query = MagicMock()
    mock_query.count.return_value = 100
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = ["transaction1", "transaction2"]
    
    # Act
    transactions, total = query_service.execute_query(mock_query, page=2, limit=10)
    
    # Assert
    assert total == 100
    assert transactions == ["transaction1", "transaction2"]
    mock_query.count.assert_called_once()
    mock_query.offset.assert_called_once_with(10)  # (page - 1) * limit
    mock_query.limit.assert_called_once_with(10)
    mock_query.all.assert_called_once()


def test_get_transaction_counts_by_hour(query_service, mock_db):
    """Test getting transaction counts by hour."""
    # Arrange
    constituency_id = "test_constituency"
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.all.return_value = [(8, 10), (9, 15), (10, 20)]  # (hour, count) pairs
    
    # Act
    result = query_service.get_transaction_counts_by_hour(constituency_id)
    
    # Assert
    assert result == {8: 10, 9: 15, 10: 20}
    mock_db.query.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_transaction_counts_by_day(query_service, mock_db):
    """Test getting transaction counts by day."""
    # Arrange
    constituency_id = "test_constituency"
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.all.return_value = [
        (datetime(2024, 9, 1).date(), 100),
        (datetime(2024, 9, 2).date(), 150)
    ]  # (day, count) pairs
    
    # Act
    result = query_service.get_transaction_counts_by_day(constituency_id)
    
    # Assert
    assert result == {"2024-09-01": 100, "2024-09-02": 150}
    mock_db.query.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_transaction_counts_by_type(query_service, mock_db):
    """Test getting transaction counts by type."""
    # Arrange
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.group_by.return_value = mock_query
    mock_query.all.return_value = [("blindSigIssue", 200), ("vote", 150)]  # (type, count) pairs
    
    # Act
    result = query_service.get_transaction_counts_by_type()
    
    # Assert
    assert result == {"blindSigIssue": 200, "vote": 150}
    mock_db.query.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_transaction_counts_by_type_with_constituency(query_service, mock_db):
    """Test getting transaction counts by type for a specific constituency."""
    # Arrange
    constituency_id = "test_constituency"
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.all.return_value = [("blindSigIssue", 100), ("vote", 75)]  # (type, count) pairs
    
    # Act
    result = query_service.get_transaction_counts_by_type(constituency_id)
    
    # Assert
    assert result == {"blindSigIssue": 100, "vote": 75}
    mock_db.query.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.group_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_transaction_rate(query_service, mock_db):
    """Test getting transaction rate."""
    # Arrange
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.scalar.return_value = 120  # 120 transactions in the last hour
    
    # Act
    result = query_service.get_transaction_rate(hours=1)
    
    # Assert
    assert result == 120.0  # 120 transactions per hour
    mock_db.query.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.scalar.assert_called_once()


def test_get_transaction_rate_with_constituency(query_service, mock_db):
    """Test getting transaction rate for a specific constituency."""
    # Arrange
    constituency_id = "test_constituency"
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.scalar.return_value = 60  # 60 transactions in the last hour
    
    # Act
    result = query_service.get_transaction_rate(constituency_id=constituency_id, hours=1)
    
    # Assert
    assert result == 60.0  # 60 transactions per hour
    mock_db.query.assert_called_once()
    mock_query.filter.assert_called_once()
    mock_query.scalar.assert_called_once()


def test_get_anomaly_statistics(query_service, mock_db):
    """Test getting anomaly statistics."""
    # Arrange
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.count.side_effect = [100, 10]  # Total: 100, Anomalies: 10
    
    mock_db.query.return_value = mock_query2 = MagicMock()
    mock_query2.filter.return_value = mock_query2
    mock_query2.group_by.return_value = mock_query2
    mock_query2.all.return_value = [
        ("Invalid signature", 5),
        ("Duplicate vote", 3),
        (None, 2)
    ]  # (reason, count) pairs
    
    # Act
    result = query_service.get_anomaly_statistics()
    
    # Assert
    assert result["total_transactions"] == 100
    assert result["anomaly_count"] == 10
    assert result["anomaly_percentage"] == 10.0
    assert result["anomaly_reasons"] == {
        "Invalid signature": 5,
        "Duplicate vote": 3,
        "unknown": 2
    }


def test_get_transaction_statistics(query_service, mock_db):
    """Test getting comprehensive transaction statistics."""
    # Arrange
    with patch.object(query_service, 'get_transaction_counts_by_type') as mock_by_type:
        mock_by_type.return_value = {"blindSigIssue": 200, "vote": 150}
        
        with patch.object(query_service, 'get_transaction_counts_by_status') as mock_by_status:
            mock_by_status.return_value = {"processed": 300, "pending": 50}
            
            with patch.object(query_service, 'get_transaction_counts_by_source') as mock_by_source:
                mock_by_source.return_value = {"file_upload": 250, "api": 100}
                
                with patch.object(query_service, 'get_transaction_rate') as mock_rate:
                    mock_rate.side_effect = [15.0, 360.0]  # per hour, per day
                    
                    with patch.object(query_service, 'get_anomaly_statistics') as mock_anomalies:
                        mock_anomalies.return_value = {
                            "total_transactions": 350,
                            "anomaly_count": 20,
                            "anomaly_percentage": 5.7,
                            "anomaly_reasons": {"Invalid signature": 12, "Duplicate vote": 8}
                        }
                        
                        # Act
                        result = query_service.get_transaction_statistics()
                        
                        # Assert
                        assert result["counts_by_type"] == {"blindSigIssue": 200, "vote": 150}
                        assert result["counts_by_status"] == {"processed": 300, "pending": 50}
                        assert result["counts_by_source"] == {"file_upload": 250, "api": 100}
                        assert result["total_transactions"] == 350
                        assert result["total_bulletins"] == 200
                        assert result["total_votes"] == 150
                        assert result["transactions_per_hour"] == 15.0
                        assert result["transactions_per_day"] == 360.0
                        assert result["anomalies"]["anomaly_count"] == 20
                        assert result["anomalies"]["anomaly_percentage"] == 5.7


def test_search_transactions(query_service, mock_db):
    """Test searching for transactions."""
    # Arrange
    search_term = "test"
    mock_db.query.return_value = mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    
    with patch.object(query_service, 'execute_query') as mock_execute:
        mock_execute.return_value = (["transaction1", "transaction2"], 2)
        
        # Act
        transactions, total = query_service.search_transactions(search_term)
        
        # Assert
        assert transactions == ["transaction1", "transaction2"]
        assert total == 2
        mock_db.query.assert_called_once_with(Transaction)
        mock_query.filter.assert_called_once()
        mock_execute.assert_called_once_with(mock_query, 1, 100)