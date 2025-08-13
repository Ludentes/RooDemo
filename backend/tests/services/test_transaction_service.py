"""
Tests for the TransactionService.

This module contains tests for the transaction processing service.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.services.transaction_service import TransactionService
from app.models.schemas.processing_result import TransactionData
from app.api.errors.exceptions import TransactionSaveError, MetricsUpdateError


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def transaction_service(mock_db):
    """Create a TransactionService with a mock database session."""
    return TransactionService(db=mock_db)


@pytest.fixture
def sample_transaction_data():
    """Create sample transaction data for testing."""
    return TransactionData(
        transaction_id="65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS",
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        block_height=104,
        timestamp="2024-09-06T08:30:28.819Z",
        type="blindSigIssue",
        raw_data={"key": "operation", "stringValue": "blindSigIssue"},
        operation_data={"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"}
    )


def test_save_transactions(transaction_service, sample_transaction_data, mock_db):
    """Test saving transactions to the database."""
    # Arrange
    with patch.object(transaction_service.validator, 'check_duplicate') as mock_check_duplicate:
        mock_check_duplicate.return_value = False  # Transaction doesn't exist
        
        with patch('app.crud.transaction.transaction_crud.get_by_constituency') as mock_get_by_constituency:
            mock_get_by_constituency.return_value = []  # No existing transactions
            
            with patch.object(transaction_service.validator, 'validate_transaction') as mock_validate:
                mock_validate.return_value = []  # No validation errors
                
                with patch('app.crud.transaction.transaction_crud.create') as mock_create:
                    # Act
                    result = transaction_service.save_transactions([sample_transaction_data])
                    
                    # Assert
                    assert result == 1
                    mock_check_duplicate.assert_called_once_with(mock_db, sample_transaction_data.transaction_id)
                    mock_validate.assert_called_once()


def test_save_transactions_duplicate(transaction_service, sample_transaction_data, mock_db):
    """Test saving duplicate transactions to the database."""
    # Arrange
    with patch('app.crud.transaction.transaction_crud.get_by_constituency') as mock_get_by_constituency:
        # Create a mock transaction with the same ID
        mock_transaction = MagicMock()
        mock_transaction.id = sample_transaction_data.transaction_id
        mock_get_by_constituency.return_value = [mock_transaction]
        
        with patch('app.crud.transaction.transaction_crud.create') as mock_create:
            # Act
            result = transaction_service.save_transactions([sample_transaction_data])
            
            # Assert
            assert result == 0  # No transactions saved
            mock_get_by_constituency.assert_called_once_with(
                db=mock_db,
                constituency_id=sample_transaction_data.constituency_id
            )
            mock_create.assert_not_called()


def test_save_transactions_error(transaction_service, sample_transaction_data, mock_db):
    """Test error handling when saving transactions."""
    # Arrange
    with patch('app.crud.transaction.transaction_crud.get_by_constituency') as mock_get_by_constituency:
        mock_get_by_constituency.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(TransactionSaveError):
            transaction_service.save_transactions([sample_transaction_data])


def test_update_constituency_metrics(transaction_service, mock_db):
    """Test updating constituency metrics."""
    # Arrange
    constituency_id = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    # Mock constituency
    mock_constituency = MagicMock()
    mock_constituency.registered_voters = 1000
    
    # Mock transactions
    mock_transaction1 = MagicMock()
    mock_transaction1.type = "blindSigIssue"
    mock_transaction2 = MagicMock()
    mock_transaction2.type = "blindSigIssue"
    mock_transaction3 = MagicMock()
    mock_transaction3.type = "vote"
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = mock_constituency
        
        with patch('app.crud.transaction.transaction_crud.get_by_constituency') as mock_get_by_constituency:
            mock_get_by_constituency.return_value = [mock_transaction1, mock_transaction2, mock_transaction3]
            
            # Act
            transaction_service.update_constituency_metrics(constituency_id)
            
            # Assert
            mock_get.assert_called_once_with(db=mock_db, id=constituency_id)
            mock_get_by_constituency.assert_called_once_with(
                db=mock_db,
                constituency_id=constituency_id
            )
            
            # Check that constituency was updated correctly
            assert mock_constituency.bulletins_issued == 2
            assert mock_constituency.votes_cast == 1
            assert mock_constituency.participation_rate == 0.1  # 1/1000 * 100
            assert mock_constituency.last_update_time is not None
            
            # Check that changes were saved
            assert mock_db.add.called
            assert mock_db.commit.called
            assert mock_db.refresh.called


def test_update_constituency_metrics_not_found(transaction_service, mock_db):
    """Test updating metrics for a constituency that doesn't exist."""
    # Arrange
    constituency_id = "NonexistentConstituency"
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = None
        
        # Act & Assert
        with pytest.raises(MetricsUpdateError):
            transaction_service.update_constituency_metrics(constituency_id)


def test_update_constituency_metrics_error(transaction_service, mock_db):
    """Test error handling when updating constituency metrics."""
    # Arrange
    constituency_id = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(MetricsUpdateError):
            transaction_service.update_constituency_metrics(constituency_id)
        
        # Check that transaction was rolled back
        assert mock_db.rollback.called


def test_get_transaction_statistics(transaction_service, mock_db):
    """Test getting transaction statistics."""
    # Arrange
    constituency_id = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    # Mock constituency
    mock_constituency = MagicMock()
    mock_constituency.bulletins_issued = 200
    mock_constituency.votes_cast = 150
    mock_constituency.participation_rate = 75.0
    mock_constituency.registered_voters = 200
    
    # Mock transactions
    mock_transaction1 = MagicMock()
    mock_transaction1.type = "blindSigIssue"
    mock_transaction1.timestamp = datetime(2024, 9, 6, 8, 0, 0)
    mock_transaction2 = MagicMock()
    mock_transaction2.type = "blindSigIssue"
    mock_transaction2.timestamp = datetime(2024, 9, 6, 8, 15, 0)
    mock_transaction3 = MagicMock()
    mock_transaction3.type = "vote"
    mock_transaction3.timestamp = datetime(2024, 9, 6, 8, 30, 0)
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = mock_constituency
        
        with patch('app.crud.transaction.transaction_crud.get_by_constituency') as mock_get_by_constituency:
            mock_get_by_constituency.return_value = [mock_transaction1, mock_transaction2, mock_transaction3]
            
            # Act
            result = transaction_service.get_transaction_statistics(constituency_id)
            
            # Assert
            assert result["total_transactions"] == 3
            assert result["bulletins_issued"] == 200
            assert result["votes_cast"] == 150
            assert result["participation_rate"] == 75.0
            assert result["transaction_counts"]["blindSigIssue"] == 2
            assert result["transaction_counts"]["vote"] == 1
            assert result["registered_voters"] == 200
            assert result["latest_update"] == datetime(2024, 9, 6, 8, 30, 0)


def test_get_transaction_statistics_constituency_not_found(transaction_service, mock_db):
    """Test getting statistics for a constituency that doesn't exist."""
    # Arrange
    constituency_id = "NonexistentConstituency"
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = None
        
        # Act
        result = transaction_service.get_transaction_statistics(constituency_id)
        
        # Assert
        assert result == {}


def test_get_transaction(transaction_service, mock_db):
    """Test getting a transaction by ID."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_transaction = MagicMock()
        mock_get.return_value = mock_transaction
        
        # Act
        result = transaction_service.get_transaction(transaction_id)
        
        # Assert
        assert result == mock_transaction
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_get_transaction_not_found(transaction_service, mock_db):
    """Test getting a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_get.return_value = None
        
        # Act
        result = transaction_service.get_transaction(transaction_id)
        
        # Assert
        assert result is None
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_create_transaction(transaction_service, mock_db):
    """Test creating a transaction."""
    # Arrange
    transaction_data = MagicMock()
    # Ensure transaction_data.id is None to avoid duplicate check
    transaction_data.id = None
    
    with patch.object(transaction_service.validator, 'validate_transaction') as mock_validate:
        mock_validate.return_value = []  # No validation errors
        
        with patch('app.crud.transaction.transaction_crud.create') as mock_create:
            mock_transaction = MagicMock()
            mock_create.return_value = mock_transaction
            
            # Act
            result = transaction_service.create_transaction(transaction_data)
            
            # Assert
            assert result == mock_transaction
            mock_validate.assert_called_once_with(mock_db, transaction_data)
            mock_create.assert_called_once_with(db=mock_db, obj_in=transaction_data)


def test_create_transaction_validation_error(transaction_service, mock_db):
    """Test creating a transaction with validation errors."""
    # Arrange
    transaction_data = MagicMock()
    
    with patch.object(transaction_service.validator, 'validate_transaction') as mock_validate:
        mock_validate.return_value = ["Constituency not found"]  # Validation error
        
        # Act & Assert
        with pytest.raises(TransactionValidationError) as excinfo:
            transaction_service.create_transaction(transaction_data)
        
        assert "Transaction validation failed" in str(excinfo.value)
        mock_validate.assert_called_once_with(mock_db, transaction_data)


def test_update_transaction(transaction_service, mock_db):
    """Test updating a transaction."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    transaction_data = MagicMock()
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_transaction = MagicMock()
        mock_get.return_value = mock_transaction
        
        with patch('app.crud.transaction.transaction_crud.update') as mock_update:
            mock_updated_transaction = MagicMock()
            mock_update.return_value = mock_updated_transaction
            
            # Act
            result = transaction_service.update_transaction(transaction_id, transaction_data)
            
            # Assert
            assert result == mock_updated_transaction
            mock_get.assert_called_once_with(db=mock_db, id=transaction_id)
            mock_update.assert_called_once_with(db=mock_db, id=transaction_id, obj_in=transaction_data)


def test_update_transaction_not_found(transaction_service, mock_db):
    """Test updating a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    transaction_data = MagicMock()
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_get.return_value = None
        
        # Act
        result = transaction_service.update_transaction(transaction_id, transaction_data)
        
        # Assert
        assert result is None
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_delete_transaction(transaction_service, mock_db):
    """Test deleting a transaction."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_transaction = MagicMock()
        mock_get.return_value = mock_transaction
        
        with patch('app.crud.transaction.transaction_crud.remove') as mock_remove:
            # Act
            result = transaction_service.delete_transaction(transaction_id)
            
            # Assert
            assert result is True
            mock_get.assert_called_once_with(db=mock_db, id=transaction_id)
            mock_remove.assert_called_once_with(db=mock_db, id=transaction_id)


def test_delete_transaction_not_found(transaction_service, mock_db):
    """Test deleting a transaction that doesn't exist."""
    # Arrange
    transaction_id = "nonexistent_id"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_get.return_value = None
        
        # Act
        result = transaction_service.delete_transaction(transaction_id)
        
        # Assert
        assert result is False
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_get_transactions(transaction_service, mock_db):
    """Test getting transactions with filtering and pagination."""
    # Arrange
    with patch('app.crud.transaction.transaction_crud.get_transactions_with_filters') as mock_get_transactions:
        mock_transactions = [MagicMock(), MagicMock()]
        mock_get_transactions.return_value = (mock_transactions, 2)
        
        # Act
        transactions, total = transaction_service.get_transactions(
            constituency_id="test_constituency",
            transaction_type="blindSigIssue",
            start_time=datetime(2024, 9, 1),
            end_time=datetime(2024, 9, 30),
            status="processed",
            anomaly_detected=True,
            source="file_upload",
            file_id="test_file",
            page=2,
            limit=10,
            sort_by="timestamp",
            sort_order="asc"
        )
        
        # Assert
        assert transactions == mock_transactions
        assert total == 2
        mock_get_transactions.assert_called_once_with(
            db=mock_db,
            constituency_id="test_constituency",
            transaction_type="blindSigIssue",
            start_time=datetime(2024, 9, 1),
            end_time=datetime(2024, 9, 30),
            status="processed",
            anomaly_detected=True,
            source="file_upload",
            file_id="test_file",
            page=2,
            limit=10,
            sort_by="timestamp",
            sort_order="asc"
        )


def test_process_transaction_batch(transaction_service, mock_db):
    """Test processing a batch of transactions."""
    # Arrange
    transactions = [MagicMock(), MagicMock()]
    
    with patch.object(transaction_service.validator, 'validate_transaction_batch') as mock_validate:
        mock_validate.return_value = {}  # No validation errors
        
        with patch('app.crud.transaction.transaction_crud.create_batch') as mock_create_batch:
            mock_result = {
                "success": True,
                "processed": 2,
                "failed": 0,
                "errors": []
            }
            mock_create_batch.return_value = mock_result
            
            # Act
            result = transaction_service.process_transaction_batch(transactions)
            
            # Assert
            assert result == mock_result
            mock_validate.assert_called_once_with(mock_db, transactions)
            mock_create_batch.assert_called_once_with(db=mock_db, obj_in_list=transactions)


def test_process_transaction_batch_with_validation_errors(transaction_service, mock_db):
    """Test processing a batch of transactions with validation errors."""
    # Arrange
    transactions = [MagicMock(), MagicMock()]
    
    with patch.object(transaction_service.validator, 'validate_transaction_batch') as mock_validate:
        mock_validate.return_value = {1: ["Constituency not found"]}  # Validation error for second transaction
        
        with patch('app.crud.transaction.transaction_crud.create_batch') as mock_create_batch:
            mock_result = {
                "success": False,
                "processed": 1,
                "failed": 1,
                "errors": [{"index": 1, "error": "Database error"}]
            }
            mock_create_batch.return_value = mock_result
            
            # Act
            result = transaction_service.process_transaction_batch(transactions)
            
            # Assert
            assert result["success"] is False
            assert result["processed"] == 1
            assert result["failed"] == 1
            assert len(result["errors"]) == 1
            assert result["errors"][0]["index"] == 1
            assert result["errors"][0]["validation_errors"] == ["Constituency not found"]
            mock_validate.assert_called_once_with(mock_db, transactions)
            mock_create_batch.assert_called_once_with(db=mock_db, obj_in_list=transactions)


def test_get_transaction_statistics_error(transaction_service, mock_db):
    """Test error handling when getting transaction statistics."""
    # Arrange
    constituency_id = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.side_effect = Exception("Database error")
        
        # Act
        result = transaction_service.get_transaction_statistics(constituency_id)
        
        # Assert
        assert result == {}