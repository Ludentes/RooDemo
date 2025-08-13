"""
File processing API routes for the Election Monitoring System.

This module provides API endpoints for file upload and directory processing.
"""

import os
import shutil
import tempfile
import logging
from typing import List, Dict
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session
import datetime
import time

from app.api.dependencies import get_db
# Import exceptions directly to avoid circular imports
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError, TransactionExtractionError,
    DirectoryProcessingError, TransactionSaveError, MetricsUpdateError
)
from app.models.schemas.processing_result import ProcessingResult, DirectoryProcessingResult

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=None)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a transaction file for processing.
    
    Args:
        file: The file to upload
        db: Database session
        
    Returns:
        Processing result with statistics
    """
    # Check file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Expected CSV file."
        )
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    temp_file_path = Path(temp_file.name)
    
    try:
        # Save uploaded file to temporary location
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        
        # Import services here to avoid circular imports
        from app.services.file_service import FileService
        from app.services.transaction_service import TransactionService
        from app.services.transaction_batch_processor import TransactionBatchProcessor
        from app.services.transaction_validator import TransactionValidator
        from app.services.region_service import RegionService
        from app.models.schemas.transaction import TransactionCreate
        
        # Process file
        file_service = FileService()
        transaction_service = TransactionService(db)
        batch_processor = TransactionBatchProcessor(db)
        validator = TransactionValidator()
        region_service = RegionService(db)
        
        # Process file and extract transactions
        # Use the original filename for metadata extraction, but the temp file path for reading content
        result, transactions = file_service.process_file(temp_file_path, original_filename=file.filename)
        
        # Create or update region if region information is available
        if result.region_id and result.region_name:
            region_service.create_or_update_region(result.region_id, result.region_name)
        
        # Convert TransactionData objects to TransactionCreate objects
        transaction_creates = []
        for transaction in transactions:
            transaction_create = TransactionCreate(
                constituency_id=transaction.constituency_id,
                block_height=transaction.block_height,
                timestamp=datetime.datetime.fromisoformat(transaction.timestamp),
                type=transaction.type,
                raw_data=transaction.raw_data,
                operation_data=transaction.operation_data,
                status="processed",
                source="file_upload",
                file_id=file.filename
            )
            transaction_creates.append(transaction_create)
        
        # Process transactions in batch
        batch_result = batch_processor.process_large_batch(transaction_creates)
        
        # Update constituency metrics
        transaction_service.update_constituency_metrics(result.constituency_id)
        
        # Update transactions processed count
        result.transactions_processed = batch_result["processed"]
        
        return result
    except MetadataExtractionError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract metadata from file: {str(e)}"
        )
    except TransactionExtractionError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract transactions from file: {str(e)}"
        )
    except TransactionSaveError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save transactions: {str(e)}"
        )
    except MetricsUpdateError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update constituency metrics: {str(e)}"
        )
    except FileProcessingError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )
    except Exception as e:
        logger.exception("Unexpected error during file upload")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path.exists():
            os.unlink(temp_file_path)


@router.post("/process-directory", response_model=None)
async def process_directory(
    directory_path: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Process all files in a directory.
    
    Args:
        directory_path: Path to the directory
        db: Database session
        
    Returns:
        Processing result with statistics
    """
    try:
        # Import services here to avoid circular imports
        from app.services.file_service import FileService
        from app.services.transaction_service import TransactionService
        from app.services.transaction_batch_processor import TransactionBatchProcessor
        from app.services.transaction_validator import TransactionValidator
        from app.services.region_service import RegionService
        from app.models.schemas.transaction import TransactionCreate
        from datetime import datetime
        
        # Process directory
        file_service = FileService()
        transaction_service = TransactionService(db)
        batch_processor = TransactionBatchProcessor(db)
        validator = TransactionValidator()
        region_service = RegionService(db)
        
        # Process directory and extract transactions
        result, transactions = file_service.process_directory(directory_path)
        logger.info(f"Directory processing result: {result}")
        logger.info(f"Extracted {len(transactions)} transactions")
        
        # Create or update region if region information is available
        if result.region_id and result.region_name:
            region_service.create_or_update_region(result.region_id, result.region_name)
        
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
                source="file_upload",
                file_id=f"dir:{directory_path}"
            )
            transaction_creates.append(transaction_create)
        
        # Process transactions in batch
        batch_result = batch_processor.process_large_batch(transaction_creates)
        logger.info(f"Batch processing result: {batch_result}")
        
        # Update constituency metrics
        if result.constituency_id:
            logger.info(f"Updating metrics for constituency: {result.constituency_id}")
            transaction_service.update_constituency_metrics(result.constituency_id)
        else:
            logger.warning("No constituency_id found, skipping metrics update")
        
        # Update transactions processed count
        result.transactions_processed = batch_result["processed"]
        logger.info(f"Final result: {result}")
        
        return result
    except DirectoryProcessingError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process directory: {str(e)}"
        )
    except TransactionSaveError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save transactions: {str(e)}"
        )
    except MetricsUpdateError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update constituency metrics: {str(e)}"
        )
    except Exception as e:
        logger.exception("Unexpected error during directory processing")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/watch-directory")
async def watch_directory(
    directory_path: str = Form(...),
    recursive: bool = Form(True),
    patterns: List[str] = Form(["*.csv"]),
    db: Session = Depends(get_db)
):
    """
    Start watching a directory for new files.
    
    Args:
        directory_path: Path to the directory to watch
        recursive: Whether to watch subdirectories
        patterns: List of file patterns to watch (e.g., ["*.csv"])
        db: Database session
        
    Returns:
        Success message
    """
    try:
        # Import service here to avoid circular imports
        from app.services.file_watcher_service import FileWatcherService
        
        # Check if directory exists
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            raise HTTPException(
                status_code=400,
                detail=f"Directory not found: {directory_path}"
            )
        
        # Get or create file watcher
        watcher = FileWatcherService.get_instance(directory_path, db)
        
        # Start watching
        watcher.start(recursive=recursive, patterns=patterns)
        
        return {
            "message": f"Started watching directory: {directory_path}",
            "recursive": recursive,
            "patterns": patterns
        }
    except Exception as e:
        logger.exception(f"Error starting file watcher for {directory_path}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start watching directory: {str(e)}"
        )


@router.post("/stop-watching")
async def stop_watching(
    directory_path: str = Form(None)
):
    """
    Stop watching a directory or all directories.
    
    Args:
        directory_path: Path to the directory to stop watching (optional)
        
    Returns:
        Success message
    """
    try:
        # Import service here to avoid circular imports
        from app.services.file_watcher_service import FileWatcherService
        
        if directory_path:
            # Get file watcher
            watcher = FileWatcherService.get_instance(directory_path, None)
            
            # Stop watching
            watcher.stop()
            
            return {
                "message": f"Stopped watching directory: {directory_path}"
            }
        else:
            # Stop all watchers
            FileWatcherService.stop_all()
            
            return {
                "message": "Stopped watching all directories"
            }
    except Exception as e:
        logger.exception(f"Error stopping file watcher for {directory_path or 'all directories'}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop watching directory: {str(e)}"
        )


@router.get("/watching-directories")
async def get_watching_directories():
    """
    Get a list of directories being watched.
    
    Returns:
        List of directory paths
    """
    try:
        # Import service here to avoid circular imports
        from app.services.file_watcher_service import FileWatcherService
        
        # Get watching directories
        directories = FileWatcherService.get_watching_directories()
        
        return {
            "directories": directories,
            "count": len(directories)
        }
    except Exception as e:
        logger.exception("Error getting watching directories")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get watching directories: {str(e)}"
        )


@router.get("/statistics/{constituency_id}")
async def get_transaction_statistics(
    constituency_id: str,
    db: Session = Depends(get_db)
):
    """
    Get transaction statistics for a constituency.
    
    Args:
        constituency_id: ID of the constituency
        db: Database session
        
    Returns:
        Transaction statistics
    """
    try:
        # Import service here to avoid circular imports
        from app.services.transaction_service import TransactionService
        from app.services.transaction_query_service import TransactionQueryService
        
        transaction_service = TransactionService(db)
        query_service = TransactionQueryService(db)
        
        # Get statistics from both services
        basic_stats = transaction_service.get_transaction_statistics(constituency_id)
        advanced_stats = query_service.get_transaction_statistics(constituency_id)
        
        # Combine statistics
        statistics = {**basic_stats, **advanced_stats}
        
        if not statistics:
            raise HTTPException(
                status_code=404,
                detail=f"Constituency not found: {constituency_id}"
            )
        
        return statistics
    except Exception as e:
        logger.exception(f"Error getting statistics for constituency {constituency_id}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )