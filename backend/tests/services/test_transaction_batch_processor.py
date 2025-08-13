"""
Tests for the TransactionBatchProcessor.

This module contains tests for the transaction batch processing service.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.services.transaction_batch_processor import TransactionBatchProcessor
from app.models.schemas.transaction import TransactionCreate, TransactionBatchRequest, TransactionBatchResponse
from app.api.errors.exceptions import BatchProcessingError


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def batch_processor(mock_db):
    """Create a TransactionBatchProcessor with a mock database session."""
    return TransactionBatchProcessor(db=mock_db)


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing."""
    return TransactionCreate(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        block_height=104,
        timestamp=datetime.fromisoformat("2024-09-06T08:30:28.819Z"),
        type="blindSigIssue",
        raw_data={"key": "operation", "stringValue": "blindSigIssue"},
        operation_data={"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
        status="processed",
        source="batch"
    )


@pytest.fixture
def sample_batch_request(sample_transaction):
    """Create a sample batch request for testing."""
    return TransactionBatchRequest(
        transactions=[sample_transaction, sample_transaction]
    )


def test_process_batch(batch_processor, sample_transaction, mock_db):
    """Test processing a batch of transactions."""
    # Arrange
    transactions = [sample_transaction, sample_transaction]
    
    with patch('app.services.transaction_validator.TransactionValidator.validate_transaction_batch') as mock_validate:
        mock_validate.return_value = {}  # No validation errors
        
        with patch('app.crud.transaction.transaction_crud.create_batch') as mock_create_batch:
            mock_create_batch.return_value = {
                "success": True,
                "processed": 2,
                "failed": 0,
                "errors": []
            }
            
            # Act
            result = batch_processor.process_batch(transactions)
            
            # Assert
            assert result["success"] is True
            assert result["processed"] == 2
            assert result["failed"] == 0
            assert result["errors"] == []
            mock_validate.assert_called_once_with(mock_db, transactions)
            mock_create_batch.assert_called_once_with(db=mock_db, obj_in_list=transactions)


def test_process_batch_with_validation_errors(batch_processor, sample_transaction, mock_db):
    """Test processing a batch of transactions with validation errors."""
    # Arrange
    transactions = [sample_transaction, sample_transaction]
    
    with patch('app.services.transaction_validator.TransactionValidator.validate_transaction_batch') as mock_validate:
        mock_validate.return_value = {1: ["Constituency not found"]}  # Validation error for second transaction
        
        with patch('app.crud.transaction.transaction_crud.create_batch') as mock_create_batch:
            mock_create_batch.return_value = {
                "success": False,
                "processed": 1,
                "failed": 1,
                "errors": [{"index": 1, "error": "Database error"}]
            }
            
            # Act
            result = batch_processor.process_batch(transactions)
            
            # Assert
            assert result["success"] is False
            assert result["processed"] == 1
            assert result["failed"] == 1
            assert len(result["errors"]) == 1
            assert result["errors"][0]["index"] == 1
            assert result["errors"][0]["error"] == "Database error"
            assert result["errors"][0]["validation_errors"] == ["Constituency not found"]
            mock_validate.assert_called_once_with(mock_db, transactions)
            mock_create_batch.assert_called_once_with(db=mock_db, obj_in_list=transactions)


def test_process_batch_with_database_error(batch_processor, sample_transaction, mock_db):
    """Test processing a batch of transactions with a database error."""
    # Arrange
    transactions = [sample_transaction, sample_transaction]
    
    with patch('app.services.transaction_validator.TransactionValidator.validate_transaction_batch') as mock_validate:
        mock_validate.return_value = {}  # No validation errors
        
        with patch('app.crud.transaction.transaction_crud.create_batch') as mock_create_batch:
            mock_create_batch.side_effect = Exception("Database error")
            
            # Act & Assert
            with pytest.raises(BatchProcessingError) as excinfo:
                batch_processor.process_batch(transactions)
            
            assert "Failed to process transaction batch" in str(excinfo.value)
            mock_validate.assert_called_once_with(mock_db, transactions)
            mock_create_batch.assert_called_once_with(db=mock_db, obj_in_list=transactions)
            mock_db.rollback.assert_called_once()


def test_split_into_batches(batch_processor, sample_transaction):
    """Test splitting transactions into batches."""
    # Arrange
    transactions = [sample_transaction] * 250  # 250 transactions
    batch_processor.batch_size = 100  # Set batch size to 100
    
    # Act
    batches = batch_processor.split_into_batches(transactions)
    
    # Assert
    assert len(batches) == 3
    assert len(batches[0]) == 100
    assert len(batches[1]) == 100
    assert len(batches[2]) == 50


def test_process_large_batch(batch_processor, sample_transaction, mock_db):
    """Test processing a large batch of transactions."""
    # Arrange
    transactions = [sample_transaction] * 3  # 3 transactions
    batch_processor.batch_size = 1  # Set batch size to 1 to force multiple batches
    
    with patch.object(batch_processor, 'process_batch') as mock_process_batch:
        mock_process_batch.side_effect = [
            {"success": True, "processed": 1, "failed": 0, "errors": []},
            {"success": True, "processed": 1, "failed": 0, "errors": []},
            {"success": True, "processed": 1, "failed": 0, "errors": []}
        ]
        
        # Act
        result = batch_processor.process_large_batch(transactions)
        
        # Assert
        assert result["success"] is True
        assert result["processed"] == 3
        assert result["failed"] == 0
        assert result["errors"] == []
        assert mock_process_batch.call_count == 3


def test_process_large_batch_with_errors(batch_processor, sample_transaction, mock_db):
    """Test processing a large batch of transactions with errors."""
    # Arrange
    transactions = [sample_transaction] * 3  # 3 transactions
    batch_processor.batch_size = 1  # Set batch size to 1 to force multiple batches
    
    with patch.object(batch_processor, 'process_batch') as mock_process_batch:
        mock_process_batch.side_effect = [
            {"success": True, "processed": 1, "failed": 0, "errors": []},
            {"success": False, "processed": 0, "failed": 1, "errors": [{"index": 0, "error": "Database error"}]},
            {"success": True, "processed": 1, "failed": 0, "errors": []}
        ]
        
        # Act
        result = batch_processor.process_large_batch(transactions)
        
        # Assert
        assert result["success"] is False
        assert result["processed"] == 2
        assert result["failed"] == 1
        assert len(result["errors"]) == 1
        assert result["errors"][0]["batch"] == 1
        assert result["errors"][0]["batch_index"] == 0
        assert result["errors"][0]["index"] == 1
        assert result["errors"][0]["error"] == "Database error"
        assert mock_process_batch.call_count == 3


def test_process_batch_request(batch_processor, sample_batch_request, mock_db):
    """Test processing a batch request."""
    # Arrange
    with patch.object(batch_processor, 'process_large_batch') as mock_process_large_batch:
        mock_process_large_batch.return_value = {
            "success": True,
            "processed": 2,
            "failed": 0,
            "errors": []
        }
        
        # Act
        result = batch_processor.process_batch_request(sample_batch_request)
        
        # Assert
        assert isinstance(result, TransactionBatchResponse)
        assert result.success is True
        assert result.processed == 2
        assert result.failed == 0
        assert result.errors == []
        mock_process_large_batch.assert_called_once_with(sample_batch_request.transactions)


def test_process_batch_request_with_error(batch_processor, sample_batch_request, mock_db):
    """Test processing a batch request with an error."""
    # Arrange
    with patch.object(batch_processor, 'process_large_batch') as mock_process_large_batch:
        mock_process_large_batch.side_effect = Exception("Unexpected error")
        
        # Act & Assert
        with pytest.raises(BatchProcessingError) as excinfo:
            batch_processor.process_batch_request(sample_batch_request)
        
        assert "Failed to process batch request" in str(excinfo.value)
        mock_process_large_batch.assert_called_once_with(sample_batch_request.transactions)