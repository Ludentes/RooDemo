"""
Tests for the TransactionValidator.

This module contains tests for the transaction validation service.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.services.transaction_validator import TransactionValidator
from app.models.schemas.transaction import TransactionCreate
from app.api.errors.exceptions import TransactionValidationError


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def transaction_validator():
    """Create a TransactionValidator."""
    return TransactionValidator()


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
        source="api"
    )


def test_validate_transaction_valid(transaction_validator, sample_transaction, mock_db):
    """Test validating a valid transaction."""
    # Arrange
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = MagicMock()  # Constituency exists
        
        # Act
        errors = transaction_validator.validate_transaction(mock_db, sample_transaction)
        
        # Assert
        assert errors == []
        mock_get.assert_called_once_with(db=mock_db, id=sample_transaction.constituency_id)


def test_validate_transaction_invalid_constituency(transaction_validator, sample_transaction, mock_db):
    """Test validating a transaction with an invalid constituency."""
    # Arrange
    with patch('app.crud.constituency.constituency_crud.get') as mock_get:
        mock_get.return_value = None  # Constituency doesn't exist
        
        # Act
        errors = transaction_validator.validate_transaction(mock_db, sample_transaction)
        
        # Assert
        assert len(errors) == 1
        assert "Constituency not found" in errors[0]
        mock_get.assert_called_once_with(db=mock_db, id=sample_transaction.constituency_id)


def test_validate_transaction_invalid_type(transaction_validator, mock_db):
    """Test validating a transaction with an invalid type."""
    # Arrange
    invalid_transaction = TransactionCreate(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        block_height=104,
        timestamp=datetime.fromisoformat("2024-09-06T08:30:28.819Z"),
        type="invalid_type",  # Invalid type
        raw_data={"key": "operation", "stringValue": "invalid_type"},
        operation_data={"key": "INVALID_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
        status="processed",
        source="api"
    )
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        transaction_validator.validate_transaction(mock_db, invalid_transaction)
    
    assert "Type must be one of" in str(excinfo.value)


def test_validate_transaction_invalid_status(transaction_validator, mock_db):
    """Test validating a transaction with an invalid status."""
    # Arrange
    invalid_transaction = TransactionCreate(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        block_height=104,
        timestamp=datetime.fromisoformat("2024-09-06T08:30:28.819Z"),
        type="blindSigIssue",
        raw_data={"key": "operation", "stringValue": "blindSigIssue"},
        operation_data={"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
        status="invalid_status",  # Invalid status
        source="api"
    )
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        transaction_validator.validate_transaction(mock_db, invalid_transaction)
    
    assert "Status must be one of" in str(excinfo.value)


def test_validate_transaction_invalid_source(transaction_validator, mock_db):
    """Test validating a transaction with an invalid source."""
    # Arrange
    invalid_transaction = TransactionCreate(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        block_height=104,
        timestamp=datetime.fromisoformat("2024-09-06T08:30:28.819Z"),
        type="blindSigIssue",
        raw_data={"key": "operation", "stringValue": "blindSigIssue"},
        operation_data={"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"},
        status="processed",
        source="invalid_source"  # Invalid source
    )
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        transaction_validator.validate_transaction(mock_db, invalid_transaction)
    
    assert "Source must be one of" in str(excinfo.value)


def test_check_duplicate_exists(transaction_validator, mock_db):
    """Test checking for a duplicate transaction that exists."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_get.return_value = MagicMock()  # Transaction exists
        
        # Act
        result = transaction_validator.check_duplicate(mock_db, transaction_id)
        
        # Assert
        assert result is True
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_check_duplicate_not_exists(transaction_validator, mock_db):
    """Test checking for a duplicate transaction that doesn't exist."""
    # Arrange
    transaction_id = "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    
    with patch('app.crud.transaction.transaction_crud.get') as mock_get:
        mock_get.return_value = None  # Transaction doesn't exist
        
        # Act
        result = transaction_validator.check_duplicate(mock_db, transaction_id)
        
        # Assert
        assert result is False
        mock_get.assert_called_once_with(db=mock_db, id=transaction_id)


def test_validate_transaction_batch(transaction_validator, sample_transaction, mock_db):
    """Test validating a batch of transactions."""
    # Arrange
    transactions = [sample_transaction, sample_transaction]
    
    with patch.object(transaction_validator, 'validate_transaction') as mock_validate:
        mock_validate.return_value = []  # No errors
        
        # Act
        result = transaction_validator.validate_transaction_batch(mock_db, transactions)
        
        # Assert
        assert result == {}  # No errors
        assert mock_validate.call_count == 2


def test_validate_transaction_batch_with_errors(transaction_validator, sample_transaction, mock_db):
    """Test validating a batch of transactions with errors."""
    # Arrange
    transactions = [sample_transaction, sample_transaction]
    
    with patch.object(transaction_validator, 'validate_transaction') as mock_validate:
        mock_validate.side_effect = [
            [],  # No errors for first transaction
            ["Constituency not found"]  # Error for second transaction
        ]
        
        # Act
        result = transaction_validator.validate_transaction_batch(mock_db, transactions)
        
        # Assert
        assert len(result) == 1
        assert 1 in result  # Error for second transaction (index 1)
        assert result[1] == ["Constituency not found"]
        assert mock_validate.call_count == 2