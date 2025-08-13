"""
End-to-End tests for the Transaction API endpoints.

This module contains E2E tests for the transaction API endpoints.
These tests are designed to be run against a running server with a test database.
"""

import os
import sys
import requests
import json
import pytest
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Base URL for the API
BASE_URL = "http://localhost:8000/api"


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing."""
    return {
        "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        "block_height": 104,
        "timestamp": datetime.utcnow().isoformat(),
        "type": "blindSigIssue",
        "raw_data": {"key": "operation", "stringValue": "blindSigIssue"},
        "operation_data": {"key": f"BLINDSIG_E2E_TEST_{datetime.utcnow().timestamp()}"},
        "status": "processed",
        "source": "api"
    }


def test_create_and_get_transaction(sample_transaction):
    """Test creating and then retrieving a transaction."""
    # Create a transaction
    response = requests.post(f"{BASE_URL}/transactions", json=sample_transaction)
    assert response.status_code == 201, f"Failed to create transaction: {response.text}"
    
    # Get the created transaction ID
    transaction_data = response.json()
    transaction_id = transaction_data["id"]
    
    # Get the transaction by ID
    response = requests.get(f"{BASE_URL}/transactions/{transaction_id}")
    assert response.status_code == 200, f"Failed to get transaction: {response.text}"
    
    # Verify the transaction data
    retrieved_transaction = response.json()
    assert retrieved_transaction["id"] == transaction_id
    assert retrieved_transaction["constituency_id"] == sample_transaction["constituency_id"]
    assert retrieved_transaction["block_height"] == sample_transaction["block_height"]
    assert retrieved_transaction["type"] == sample_transaction["type"]
    assert retrieved_transaction["status"] == sample_transaction["status"]
    assert retrieved_transaction["source"] == sample_transaction["source"]


def test_list_transactions():
    """Test listing transactions with filtering."""
    # List all transactions
    response = requests.get(f"{BASE_URL}/transactions")
    assert response.status_code == 200, f"Failed to list transactions: {response.text}"
    
    # Verify the response structure
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    
    # List transactions with filtering
    params = {
        "page": 1,
        "limit": 10,
        "sort_by": "timestamp",
        "sort_order": "desc"
    }
    response = requests.get(f"{BASE_URL}/transactions", params=params)
    assert response.status_code == 200, f"Failed to list transactions with filtering: {response.text}"
    
    # Verify the response structure
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 10


def test_update_transaction(sample_transaction):
    """Test updating a transaction."""
    # Create a transaction
    response = requests.post(f"{BASE_URL}/transactions", json=sample_transaction)
    assert response.status_code == 201, f"Failed to create transaction: {response.text}"
    
    # Get the created transaction ID
    transaction_data = response.json()
    transaction_id = transaction_data["id"]
    
    # Update the transaction
    update_data = {
        "status": "failed",
        "anomaly_detected": True,
        "anomaly_reason": "E2E Test Anomaly"
    }
    response = requests.put(f"{BASE_URL}/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 200, f"Failed to update transaction: {response.text}"
    
    # Verify the updated transaction
    updated_transaction = response.json()
    assert updated_transaction["id"] == transaction_id
    assert updated_transaction["status"] == "failed"
    assert updated_transaction["anomaly_detected"] is True
    assert updated_transaction["anomaly_reason"] == "E2E Test Anomaly"


def test_delete_transaction(sample_transaction):
    """Test deleting a transaction."""
    # Create a transaction
    response = requests.post(f"{BASE_URL}/transactions", json=sample_transaction)
    assert response.status_code == 201, f"Failed to create transaction: {response.text}"
    
    # Get the created transaction ID
    transaction_data = response.json()
    transaction_id = transaction_data["id"]
    
    # Delete the transaction
    response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}")
    assert response.status_code == 204, f"Failed to delete transaction: {response.text}"
    
    # Verify the transaction is deleted
    response = requests.get(f"{BASE_URL}/transactions/{transaction_id}")
    assert response.status_code == 404, f"Transaction was not deleted: {response.text}"


def test_batch_processing(sample_transaction):
    """Test batch processing of transactions."""
    # Create a batch of transactions
    batch_request = {
        "transactions": [
            sample_transaction,
            {**sample_transaction, "operation_data": {"key": f"BLINDSIG_E2E_TEST_BATCH_{datetime.utcnow().timestamp()}"}}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/transactions/batch", json=batch_request)
    assert response.status_code == 200, f"Failed to process batch: {response.text}"
    
    # Verify the batch processing result
    result = response.json()
    assert "success" in result
    assert "processed" in result
    assert "failed" in result
    assert "errors" in result


def test_get_statistics():
    """Test getting transaction statistics."""
    # Get transaction statistics
    response = requests.get(f"{BASE_URL}/transactions/statistics")
    assert response.status_code == 200, f"Failed to get statistics: {response.text}"
    
    # Verify the statistics
    stats = response.json()
    assert "total_transactions" in stats
    assert "total_bulletins" in stats
    assert "total_votes" in stats
    assert "transactions_per_hour" in stats


def test_search_transactions():
    """Test searching for transactions."""
    # Search for transactions
    response = requests.get(f"{BASE_URL}/transactions/search?q=blindSigIssue")
    assert response.status_code == 200, f"Failed to search transactions: {response.text}"
    
    # Verify the search results
    results = response.json()
    assert "data" in results
    assert "total" in results
    assert "page" in results
    assert "limit" in results


if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__])