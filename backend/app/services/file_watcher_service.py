"""
File watcher service for the Election Monitoring System.

This module provides a service for watching directories for new files
and processing them automatically.
"""

import os
import time
import logging
from pathlib import Path
from typing import Dict, Optional, List
from threading import Thread, Event
from sqlalchemy.orm import Session

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from app.services.file_service import FileService
from app.services.transaction_service import TransactionService
from app.services.transaction_batch_processor import TransactionBatchProcessor
from app.services.transaction_validator import TransactionValidator
from app.services.region_service import RegionService
from app.models.schemas.transaction import TransactionCreate
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)


class FileEventHandler(FileSystemEventHandler):
    """
    Handler for file system events.
    
    This class handles file system events, such as file creation,
    and processes new files automatically.
    """
    
    def __init__(self, db: Session, recursive: bool = True, patterns: List[str] = None):
        """
        Initialize the handler with a database session.
        
        Args:
            db: Database session
            recursive: Whether to watch subdirectories
            patterns: List of file patterns to watch (e.g., ["*.csv"])
        """
        self.db = db
        self.recursive = recursive
        self.patterns = patterns or ["*.csv"]
        self.file_service = FileService()
        self.transaction_service = TransactionService(db)
        self.batch_processor = TransactionBatchProcessor(db)
        self.validator = TransactionValidator()
        self.region_service = RegionService(db)
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        # Check if the file matches any of the patterns
        file_path = Path(event.src_path)
        if not any(file_path.match(pattern) for pattern in self.patterns):
            return
        
        logger.info(f"New file detected: {file_path}")
        
        try:
            # Wait a short time to ensure the file is fully written
            time.sleep(1)
            
            # Process the file
            result, transactions = self.file_service.process_file(file_path)
            logger.info(f"Processed {len(transactions)} transactions from {file_path}")
            
            # Create or update region if region information is available
            if result.region_id and result.region_name:
                self.region_service.create_or_update_region(result.region_id, result.region_name)
            
            # Convert TransactionData objects to TransactionCreate objects
            transaction_creates = []
            for transaction in transactions:
                transaction_create = TransactionCreate(
                    constituency_id=transaction.constituency_id,
                    block_height=transaction.block_height,
                    timestamp=datetime.fromisoformat(transaction.timestamp),
                    type=transaction.type,
                    raw_data=transaction.raw_data,
                    operation_data=transaction.operation_data,
                    status="processed",
                    source="file_watcher",
                    file_id=str(file_path)
                )
                transaction_creates.append(transaction_create)
            
            # Process transactions in batch
            batch_result = self.batch_processor.process_large_batch(transaction_creates)
            logger.info(f"Batch processing result: {batch_result}")
            
            # Update constituency metrics
            if result.constituency_id:
                self.transaction_service.update_constituency_metrics(result.constituency_id)
                logger.info(f"Updated metrics for constituency: {result.constituency_id}")
        except Exception as e:
            logger.exception(f"Error processing file {file_path}: {e}")


class FileWatcherService:
    """
    Service for watching directories for new files.
    
    This class provides methods for starting and stopping file watchers.
    """
    
    # Dictionary to store instances of FileWatcherService
    _instances: Dict[str, 'FileWatcherService'] = {}
    
    @classmethod
    def get_instance(cls, directory_path: str, db: Session) -> 'FileWatcherService':
        """
        Get or create a FileWatcherService instance for a directory.
        
        Args:
            directory_path: Path to the directory to watch
            db: Database session
            
        Returns:
            FileWatcherService instance
        """
        if directory_path not in cls._instances:
            cls._instances[directory_path] = cls(directory_path, db)
        return cls._instances[directory_path]
    
    @classmethod
    def stop_all(cls):
        """
        Stop all file watchers.
        """
        # Make a copy of the instances to avoid modifying the dictionary during iteration
        instances = list(cls._instances.values())
        for instance in instances:
            instance.stop()
        # Clear any remaining instances (should be empty already)
        cls._instances.clear()
    
    @classmethod
    def get_watching_directories(cls) -> List[str]:
        """
        Get a list of directories being watched.
        
        Returns:
            List of directory paths
        """
        return list(cls._instances.keys())
    
    def __init__(self, directory_path: str, db: Session):
        """
        Initialize the service with a directory path and database session.
        
        Args:
            directory_path: Path to the directory to watch
            db: Database session
        """
        self.directory_path = directory_path
        self.db = db
        self.observer = None
        self.stop_event = Event()
        self.thread = None
        self.is_watching = False
    
    def start(self, recursive: bool = True, patterns: List[str] = None):
        """
        Start watching the directory.
        
        Args:
            recursive: Whether to watch subdirectories
            patterns: List of file patterns to watch (e.g., ["*.csv"])
            
        Raises:
            Exception: If starting the watcher fails
        """
        if self.is_watching:
            logger.warning(f"Watcher for {self.directory_path} already running")
            return
        
        try:
            # Create event handler
            event_handler = FileEventHandler(self.db, recursive, patterns)
            
            # Create observer
            self.observer = Observer()
            self.observer.schedule(event_handler, self.directory_path, recursive=recursive)
            
            # Start observer in a separate thread
            self.stop_event.clear()
            self.thread = Thread(target=self._run_observer)
            self.thread.daemon = True
            self.thread.start()
            
            self.is_watching = True
            logger.info(f"Started watching directory: {self.directory_path}")
        except Exception as e:
            logger.exception(f"Error starting file watcher: {e}")
            raise
    
    def _run_observer(self):
        """
        Run the observer in a separate thread.
        """
        self.observer.start()
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except Exception as e:
            logger.exception(f"Error in file watcher thread: {e}")
        finally:
            self.observer.stop()
            self.observer.join()
    
    def stop(self):
        """
        Stop watching the directory.
        
        Raises:
            Exception: If stopping the watcher fails
        """
        if not self.is_watching:
            logger.warning(f"No watcher running for {self.directory_path}")
            return
        
        try:
            self.stop_event.set()
            if self.thread:
                self.thread.join(timeout=5)
            self.observer = None
            self.thread = None
            self.is_watching = False
            
            # Remove from instances
            if self.directory_path in self._instances:
                del self._instances[self.directory_path]
            
            logger.info(f"Stopped watching directory: {self.directory_path}")
        except Exception as e:
            logger.exception(f"Error stopping file watcher: {e}")
            raise
    
    def is_running(self) -> bool:
        """
        Check if the watcher is running.
        
        Returns:
            True if the watcher is running, False otherwise
        """
        return self.is_watching