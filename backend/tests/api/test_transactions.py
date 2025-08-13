"""
Tests for the Transaction API endpoints.

This module contains tests for the transaction API endpoints.
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime
import json

from app.main import app
from app.models.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionBatchRequest,
    TransactionBatchResponse
)


@pytest.fixture
def client():
    """Create a test client for the API."""
    from app.api import setup_routes
    setup_routes()  # Ensure routes are set up before creating the client
    return TestClient(app)


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing."""
    return {
        "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        "block_height": 104,
        "timestamp": "2024-09-06T08:30:28.819Z",
        "type": "blindSigIssue",
        "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
        "operation_data": {"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
        "status": "processed",
        "source": "api"
    }


@pytest.fixture
def sample_transaction_response(sample_transaction):
    """Create a sample transaction response for testing."""
    return {
        "id": "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
        **sample_transaction,
        "created_at": "2024-09-06T08:30:28.819Z",
        "updated_at": "2024-09-06T08:30:28.819Z"
    }


def test_list_transactions(client):
    """Test listing transactions."""
    # Arrange
    with patch('app.services.transaction_service.TransactionService.get_transactions') as mock_get_transactions:
        # Create properly structured mock transactions
        mock_transaction1 = {
            "id": "tx1",
            "constituency_id": "const1",
            "block_height": 100,
            "timestamp": datetime.utcnow(),
            "type": "blindSigIssue",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transaction2 = {
            "id": "tx2",
            "constituency_id": "const2",
            "block_height": 101,
            "timestamp": datetime.utcnow(),
            "type": "vote",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transactions = [mock_transaction1, mock_transaction2]
        mock_get_transactions.return_value = (mock_transactions, 2)
        
        # Act
        response = client.get("/api/transactions")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert data["total"] == 2
        assert data["page"] == 1
        mock_get_transactions.assert_called_once()


def test_list_transactions_with_filters(client):
    """Test listing transactions with filters."""
    # Arrange
    with patch('app.services.transaction_service.TransactionService.get_transactions') as mock_get_transactions:
        # Create properly structured mock transactions
        mock_transaction1 = {
            "id": "tx1",
            "constituency_id": "const1",
            "block_height": 100,
            "timestamp": datetime.utcnow(),
            "type": "blindSigIssue",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transaction2 = {
            "id": "tx2",
            "constituency_id": "const2",
            "block_height": 101,
            "timestamp": datetime.utcnow(),
            "type": "vote",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transactions = [mock_transaction1, mock_transaction2]
        mock_get_transactions.return_value = (mock_transactions, 2)
        
        # Act
        response = client.get(
            "/api/transactions",
            params={
                "constituency_id": "test_constituency",
                "transaction_type": "blindSigIssue",
                "start_time": "2024-09-01T00:00:00Z",
                "end_time": "2024-09-30T23:59:59Z",
                "status": "processed",
                "anomaly_detected": "true",
                "source": "file_upload",
                "file_id": "test_file",
                "page": "2",
                "limit": "10",
                "sort_by": "timestamp",
                "sort_order": "asc"
            }
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        mock_get_transactions.assert_called_once()


def test_get_transaction(client, sample_transaction_response):
    """Test getting a transaction by ID."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.services.transaction_service.TransactionService.get_transaction') as mock_get_transaction:
        mock_get_transaction.return_value = sample_transaction_response
        
        # Act
        response = client.get(f"/api/transactions/{transaction_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        mock_get_transaction.assert_called_once_with(transaction_id)


def test_get_transaction_not_found(client):
    """Test getting a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    
    with patch('app.services.transaction_service.TransactionService.get_transaction') as mock_get_transaction:
        mock_get_transaction.return_value = None
        
        # Act
        response = client.get(f"/api/transactions/{transaction_id}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "not found" in data["error"]["message"].lower()
        mock_get_transaction.assert_called_once_with(transaction_id)


def test_create_transaction(client, sample_transaction, sample_transaction_response):
    """Test creating a transaction."""
    # Arrange
    with patch('app.services.transaction_service.TransactionService.create_transaction') as mock_create_transaction:
        mock_create_transaction.return_value = sample_transaction_response
        
        # Act
        response = client.post(
            "/api/transactions",
            json=sample_transaction
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
        mock_create_transaction.assert_called_once()


def test_create_transaction_validation_error(client, sample_transaction):
    """Test creating a transaction with validation errors."""
    # Arrange
    with patch('app.services.transaction_service.TransactionService.create_transaction') as mock_create_transaction:
        mock_create_transaction.side_effect = ValueError("Validation error")
        
        # Act
        response = client.post(
            "/api/transactions",
            json=sample_transaction
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        mock_create_transaction.assert_called_once()


def test_update_transaction(client, sample_transaction_response):
    """Test updating a transaction."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    update_data = {
        "status": "failed",
        "anomaly_detected": True,
        "anomaly_reason": "Invalid signature"
    }
    
    with patch('app.services.transaction_service.TransactionService.update_transaction') as mock_update_transaction:
        updated_transaction = {**sample_transaction_response, **update_data}
        mock_update_transaction.return_value = updated_transaction
        
        # Act
        response = client.put(
            f"/api/transactions/{transaction_id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id
        assert data["status"] == "failed"
        assert data["anomaly_detected"] is True
        assert data["anomaly_reason"] == "Invalid signature"
        # Don't check the exact argument since it's converted to a TransactionUpdate object
        mock_update_transaction.assert_called_once()
        # Check that the first argument is the transaction_id
        assert mock_update_transaction.call_args[0][0] == transaction_id
        # Check that the second argument is a TransactionUpdate object with the expected values
        assert mock_update_transaction.call_args[0][1].status == update_data["status"]
        assert mock_update_transaction.call_args[0][1].anomaly_detected == update_data["anomaly_detected"]
        assert mock_update_transaction.call_args[0][1].anomaly_reason == update_data["anomaly_reason"]


def test_update_transaction_not_found(client):
    """Test updating a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    update_data = {
        "status": "failed",
        "anomaly_detected": True,
        "anomaly_reason": "Invalid signature"
    }
    
    with patch('app.services.transaction_service.TransactionService.update_transaction') as mock_update_transaction:
        mock_update_transaction.return_value = None
        
        # Act
        response = client.put(
            f"/api/transactions/{transaction_id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "not found" in data["error"]["message"].lower()
        mock_update_transaction.assert_called_once_with(transaction_id, update_data)


def test_delete_transaction(client):
    """Test deleting a transaction."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.services.transaction_service.TransactionService.delete_transaction') as mock_delete_transaction:
        mock_delete_transaction.return_value = True
        
        # Act
        response = client.delete(f"/api/transactions/{transaction_id}")
        
        # Assert
        assert response.status_code == 204
        assert response.content == b''  # No content
        mock_delete_transaction.assert_called_once_with(transaction_id)


def test_delete_transaction_not_found(client):
    """Test deleting a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    
    with patch('app.services.transaction_service.TransactionService.delete_transaction') as mock_delete_transaction:
        mock_delete_transaction.return_value = False
        
        # Act
        response = client.delete(f"/api/transactions/{transaction_id}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "not found" in data["error"]["message"].lower()
        mock_delete_transaction.assert_called_once_with(transaction_id)


def test_process_batch(client, sample_transaction):
    """Test processing a batch of transactions."""
    # Arrange
    batch_request = {
        "transactions": [sample_transaction, sample_transaction]
    }
    
    with patch('app.services.transaction_batch_processor.TransactionBatchProcessor.process_batch_request') as mock_process_batch:
        mock_process_batch.return_value = TransactionBatchResponse(
            success=True,
            processed=2,
            failed=0,
            errors=[]
        )
        
        # Act
        response = client.post(
            "/api/transactions/batch",
            json=batch_request
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["processed"] == 2
        assert data["failed"] == 0
        assert data["errors"] == []
        mock_process_batch.assert_called_once()


def test_process_batch_with_errors(client, sample_transaction):
    """Test processing a batch of transactions with errors."""
    # Arrange
    batch_request = {
        "transactions": [sample_transaction, sample_transaction]
    }
    
    with patch('app.services.transaction_batch_processor.TransactionBatchProcessor.process_batch_request') as mock_process_batch:
        mock_process_batch.return_value = TransactionBatchResponse(
            success=False,
            processed=1,
            failed=1,
            errors=[{
                "index": 1,
                "error": "Database error",
                "validation_errors": ["Constituency not found"]
            }]
        )
        
        # Act
        response = client.post(
            "/api/transactions/batch",
            json=batch_request
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["processed"] == 1
        assert data["failed"] == 1
        assert len(data["errors"]) == 1
        assert data["errors"][0]["index"] == 1
        assert "Database error" in data["errors"][0]["error"]
        mock_process_batch.assert_called_once()


def test_get_statistics(client):
    """Test getting transaction statistics."""
    # Arrange
    with patch('app.services.transaction_query_service.TransactionQueryService.get_transaction_statistics') as mock_get_stats:
        mock_get_stats.return_value = {
            "total_transactions": 350,
            "total_bulletins": 200,
            "total_votes": 150,
            "transactions_per_hour": 15.0,
            "bulletins_per_hour": 8.5,
            "votes_per_hour": 6.5
        }
        
        # Act
        response = client.get("/api/transactions/statistics")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_transactions"] == 350
        assert data["total_bulletins"] == 200
        assert data["total_votes"] == 150
        assert data["transactions_per_hour"] == 15.0
        mock_get_stats.assert_called_once_with(None)


def test_get_statistics_with_constituency(client):
    """Test getting transaction statistics for a specific constituency."""
    # Arrange
    constituency_id = "test_constituency"
    
    with patch('app.services.transaction_query_service.TransactionQueryService.get_transaction_statistics') as mock_get_stats:
        mock_get_stats.return_value = {
            "total_transactions": 150,
            "total_bulletins": 100,
            "total_votes": 50,
            "transactions_per_hour": 7.5,
            "bulletins_per_hour": 5.0,
            "votes_per_hour": 2.5
        }
        
        # Act
        response = client.get(f"/api/transactions/statistics?constituency_id={constituency_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_transactions"] == 150
        assert data["total_bulletins"] == 100
        assert data["total_votes"] == 50
        assert data["transactions_per_hour"] == 7.5
        mock_get_stats.assert_called_once_with(constituency_id)


def test_search_transactions(client):
    """Test searching for transactions."""
    # Arrange
    search_term = "test"
    
    with patch('app.services.transaction_query_service.TransactionQueryService.search_transactions') as mock_search:
        # Create properly structured mock transactions
        mock_transaction1 = {
            "id": "tx1",
            "constituency_id": "const1",
            "block_height": 100,
            "timestamp": datetime.utcnow(),
            "type": "blindSigIssue",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transaction2 = {
            "id": "tx2",
            "constituency_id": "const2",
            "block_height": 101,
            "timestamp": datetime.utcnow(),
            "type": "vote",
            "raw_data": {"key": "value"},
            "operation_data": {"key": "value"},
            "status": "processed",
            "anomaly_detected": False,
            "anomaly_reason": None,
            "source": "api",
            "file_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mock_transactions = [mock_transaction1, mock_transaction2]
        mock_search.return_value = (mock_transactions, 2)
        
        # Act
        response = client.get(f"/api/transactions/search?q={search_term}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert data["total"] == 2
        assert data["page"] == 1
        mock_search.assert_called_once_with(search_term, 1, 100)