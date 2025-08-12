"""
Tests for the FileService.

This module contains tests for the file processing service.
"""

import pytest
import tempfile
import os
from pathlib import Path
from datetime import date

from app.services.file_service import FileService
from app.models.schemas.file_metadata import FileMetadata
from app.api.errors.exceptions import MetadataExtractionError, TransactionExtractionError


def test_extract_metadata_from_filename():
    """Test extracting metadata from a valid filename."""
    # Arrange
    service = FileService()
    filename = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
    
    # Act
    metadata = service.extract_metadata_from_filename(filename)
    
    # Assert
    assert metadata.constituency_id == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    assert metadata.date == date(2024, 9, 6)
    assert metadata.time_range == "0800-0900"


def test_extract_metadata_from_invalid_filename():
    """Test extracting metadata from an invalid filename."""
    # Arrange
    service = FileService()
    filename = "invalid_filename.csv"
    
    # Act & Assert
    with pytest.raises(MetadataExtractionError):
        service.extract_metadata_from_filename(filename)


def test_parse_json_like_structure():
    """Test parsing JSON-like structure."""
    # Arrange
    service = FileService()
    data_str = '{"key": "operation", "stringValue": "blindSigIssue"},{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"}'
    
    # Act
    result = service._parse_json_like_structure(data_str)
    
    # Assert
    assert len(result) == 2
    assert result[0]["key"] == "operation"
    assert result[0]["stringValue"] == "blindSigIssue"
    assert result[1]["key"] == "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"


def test_parse_empty_json_like_structure():
    """Test parsing empty JSON-like structure."""
    # Arrange
    service = FileService()
    data_str = ""
    
    # Act
    result = service._parse_json_like_structure(data_str)
    
    # Assert
    assert result == []


def test_extract_transactions_from_csv():
    """Test extracting transactions from CSV content."""
    # Arrange
    service = FileService()
    metadata = FileMetadata(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        date=date(2024, 9, 6),
        time_range="0800-0900"
    )
    
    csv_content = """65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;104;1662453028819;1662453028819;1662453028819;1662453028819;{"key": "operation", "stringValue": "blindSigIssue"};{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"};1;1
7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;105;1662453128819;1662453128819;1662453128819;1662453128819;{"key": "operation", "stringValue": "vote"};{"key": "VOTE_7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr"};1;1"""
    
    # Act
    transactions = service.extract_transactions_from_csv(csv_content, metadata)
    
    # Assert
    assert len(transactions) == 2
    assert transactions[0].transaction_id == "65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"
    assert transactions[0].constituency_id == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    assert transactions[0].block_height == 104
    assert transactions[0].type == "blindSigIssue"
    
    assert transactions[1].transaction_id == "7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr"
    assert transactions[1].type == "vote"


def test_extract_transactions_from_invalid_csv():
    """Test extracting transactions from invalid CSV content."""
    # Arrange
    service = FileService()
    metadata = FileMetadata(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        date=date(2024, 9, 6),
        time_range="0800-0900"
    )
    
    csv_content = "invalid,csv,content"
    
    # Act & Assert
    with pytest.raises(TransactionExtractionError):
        service.extract_transactions_from_csv(csv_content, metadata)


def test_process_file():
    """Test processing a file."""
    # Arrange
    service = FileService()
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
        filename = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
        temp_path = Path(temp_file.name)
        # Rename the temp file to match our expected format
        temp_file.write(b"""65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;104;1662453028819;1662453028819;1662453028819;1662453028819;{"key": "operation", "stringValue": "blindSigIssue"};{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"};1;1
7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;105;1662453128819;1662453128819;1662453128819;1662453128819;{"key": "operation", "stringValue": "vote"};{"key": "VOTE_7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr"};1;1""")
    
    try:
        # Create a new file with the correct name
        new_path = temp_path.parent / filename
        os.rename(temp_path, new_path)
        
        # Act
        result, transactions = service.process_file(new_path)
        
        # Assert
        assert result.filename == filename
        assert result.transactions_processed == 2
        assert result.constituency_id == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
        assert result.date == date(2024, 9, 6)
        assert result.time_range == "0800-0900"
        
        assert len(transactions) == 2
        assert transactions[0].type == "blindSigIssue"
        assert transactions[1].type == "vote"
    finally:
        # Clean up
        if os.path.exists(new_path):
            os.unlink(new_path)


def test_process_directory():
    """Test processing a directory."""
    # Arrange
    service = FileService()
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary CSV file in the directory
        file_path = Path(temp_dir) / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
        with open(file_path, 'w') as f:
            f.write("""65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;104;1662453028819;1662453028819;1662453028819;1662453028819;{"key": "operation", "stringValue": "blindSigIssue"};{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"};1;1
7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;105;1662453128819;1662453128819;1662453128819;1662453128819;{"key": "operation", "stringValue": "vote"};{"key": "VOTE_7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr"};1;1""")
        
        # Act
        result, transactions = service.process_directory(temp_dir)
        
        # Assert
        assert result.files_processed == 1
        assert result.transactions_processed == 2
        assert result.constituency_id == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
        
        assert len(transactions) == 2
        assert transactions[0].type == "blindSigIssue"
        assert transactions[1].type == "vote"