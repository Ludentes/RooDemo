"""
Tests for the FileWatcherService.

This module contains tests for the file watcher service.
"""

import os
import time
import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.services.file_watcher_service import FileWatcherService, FileEventHandler
from app.models.schemas.processing_result import ProcessingResult


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_file_event_handler_init():
    """Test initializing a FileEventHandler."""
    # Arrange
    db_mock = MagicMock()
    
    # Act
    handler = FileEventHandler(db_mock)
    
    # Assert
    assert handler.db == db_mock
    assert handler.recursive is True
    assert handler.patterns == ["*.csv"]
    assert handler.file_service is not None
    assert handler.transaction_service is not None
    assert handler.region_service is not None


def test_file_event_handler_on_created_directory_event():
    """Test that directory events are ignored."""
    # Arrange
    db_mock = MagicMock()
    handler = FileEventHandler(db_mock)
    
    event_mock = MagicMock()
    event_mock.is_directory = True
    
    # Act
    result = handler.on_created(event_mock)
    
    # Assert
    assert result is None  # Should return early


def test_file_event_handler_on_created_non_matching_file():
    """Test that non-matching files are ignored."""
    # Arrange
    db_mock = MagicMock()
    handler = FileEventHandler(db_mock)
    
    event_mock = MagicMock()
    event_mock.is_directory = False
    event_mock.src_path = "/path/to/file.txt"  # Not a CSV file
    
    # Act
    result = handler.on_created(event_mock)
    
    # Assert
    assert result is None  # Should return early


@patch('app.services.file_service.FileService.process_file')
@patch('app.services.transaction_service.TransactionService.save_transactions')
@patch('app.services.transaction_service.TransactionService.update_constituency_metrics')
@patch('app.services.region_service.RegionService.create_or_update_region')
def test_file_event_handler_on_created_matching_file(
    mock_create_or_update_region,
    mock_update_metrics,
    mock_save_transactions,
    mock_process_file,
    temp_dir
):
    """Test handling a matching file creation event."""
    # Arrange
    db_mock = MagicMock()
    handler = FileEventHandler(db_mock)
    
    # Create a test file
    file_path = Path(temp_dir) / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
    with open(file_path, 'w') as f:
        f.write("test content")
    
    event_mock = MagicMock()
    event_mock.is_directory = False
    event_mock.src_path = str(file_path)
    
    # Mock process_file return value
    result_mock = MagicMock()
    result_mock.region_id = "90"
    result_mock.region_name = "Пермский край"
    result_mock.constituency_id = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    transactions_mock = [MagicMock(), MagicMock()]
    mock_process_file.return_value = (result_mock, transactions_mock)
    
    mock_save_transactions.return_value = 2
    
    # Act
    with patch('time.sleep'):  # Mock sleep to speed up test
        handler.on_created(event_mock)
    
    # Assert
    mock_process_file.assert_called_once_with(file_path)
    mock_create_or_update_region.assert_called_once_with("90", "Пермский край")
    mock_save_transactions.assert_called_once_with(transactions_mock)
    mock_update_metrics.assert_called_once_with("AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM")


@patch('app.services.file_service.FileService.process_file')
def test_file_event_handler_on_created_error_handling(mock_process_file, temp_dir):
    """Test error handling in on_created method."""
    # Arrange
    db_mock = MagicMock()
    handler = FileEventHandler(db_mock)
    
    # Create a test file
    file_path = Path(temp_dir) / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
    with open(file_path, 'w') as f:
        f.write("test content")
    
    event_mock = MagicMock()
    event_mock.is_directory = False
    event_mock.src_path = str(file_path)
    
    # Mock process_file to raise an exception
    mock_process_file.side_effect = Exception("Test error")
    
    # Act
    with patch('time.sleep'):  # Mock sleep to speed up test
        handler.on_created(event_mock)
    
    # Assert
    mock_process_file.assert_called_once_with(file_path)
    # No exception should be raised, it should be caught and logged


def test_file_watcher_service_get_instance():
    """Test getting a FileWatcherService instance."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    # Act
    watcher1 = FileWatcherService.get_instance(directory_path, db_mock)
    watcher2 = FileWatcherService.get_instance(directory_path, db_mock)
    
    # Assert
    assert watcher1 is watcher2  # Should return the same instance
    assert watcher1.directory_path == directory_path
    assert watcher1.db == db_mock
    
    # Clean up
    FileWatcherService.stop_all()


def test_file_watcher_service_get_watching_directories():
    """Test getting a list of watching directories."""
    # Arrange
    db_mock = MagicMock()
    directory_path1 = "/path/to/directory1"
    directory_path2 = "/path/to/directory2"
    
    # Act
    FileWatcherService.get_instance(directory_path1, db_mock)
    FileWatcherService.get_instance(directory_path2, db_mock)
    directories = FileWatcherService.get_watching_directories()
    
    # Assert
    assert len(directories) == 2
    assert directory_path1 in directories
    assert directory_path2 in directories
    
    # Clean up
    FileWatcherService.stop_all()


@patch('app.services.file_watcher_service.Observer')
def test_file_watcher_service_start(mock_observer_class):
    """Test starting a file watcher."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer
    
    watcher = FileWatcherService(directory_path, db_mock)
    
    # Act
    watcher.start()
    
    # Assert
    assert watcher.is_watching is True
    mock_observer.schedule.assert_called_once()
    mock_observer.start.assert_called_once()
    
    # Clean up
    watcher.stop()


@patch('app.services.file_watcher_service.Observer')
def test_file_watcher_service_start_already_running(mock_observer_class):
    """Test starting a file watcher that's already running."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer
    
    watcher = FileWatcherService(directory_path, db_mock)
    watcher.is_watching = True
    
    # Act
    watcher.start()
    
    # Assert
    mock_observer.schedule.assert_not_called()
    mock_observer.start.assert_not_called()
    
    # Clean up
    watcher.is_watching = False


@patch('app.services.file_watcher_service.Observer')
def test_file_watcher_service_stop(mock_observer_class):
    """Test stopping a file watcher."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer
    
    watcher = FileWatcherService(directory_path, db_mock)
    watcher.start()
    
    # Act
    watcher.stop()
    
    # Assert
    assert watcher.is_watching is False
    assert watcher.observer is None
    assert watcher.thread is None


def test_file_watcher_service_stop_not_running():
    """Test stopping a file watcher that's not running."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    watcher = FileWatcherService(directory_path, db_mock)
    
    # Act
    watcher.stop()
    
    # Assert
    assert watcher.is_watching is False


def test_file_watcher_service_is_running():
    """Test checking if a file watcher is running."""
    # Arrange
    db_mock = MagicMock()
    directory_path = "/path/to/directory"
    
    watcher = FileWatcherService(directory_path, db_mock)
    
    # Act & Assert
    assert watcher.is_running() is False
    
    watcher.is_watching = True
    assert watcher.is_running() is True
    
    # Clean up
    watcher.is_watching = False


@patch('app.services.file_watcher_service.Observer')
def test_file_watcher_service_stop_all(mock_observer_class):
    """Test stopping all file watchers."""
    # Arrange
    db_mock = MagicMock()
    directory_path1 = "/path/to/directory1"
    directory_path2 = "/path/to/directory2"
    
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer
    
    watcher1 = FileWatcherService.get_instance(directory_path1, db_mock)
    watcher2 = FileWatcherService.get_instance(directory_path2, db_mock)
    
    watcher1.start()
    watcher2.start()
    
    # Act
    FileWatcherService.stop_all()
    
    # Assert
    assert len(FileWatcherService._instances) == 0
    assert watcher1.is_watching is False
    assert watcher2.is_watching is False