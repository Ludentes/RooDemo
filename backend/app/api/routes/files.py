"""
File processing API routes for the Election Monitoring System.

This module provides API endpoints for file upload and directory processing.
"""

import os
import shutil
import tempfile
from typing import List
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session
import time

from app.api.dependencies import get_db
# Import exceptions directly to avoid circular imports
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError, TransactionExtractionError,
    DirectoryProcessingError, TransactionSaveError, MetricsUpdateError
)
from app.models.schemas.processing_result import ProcessingResult, DirectoryProcessingResult


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
        
        # Process file
        file_service = FileService()
        transaction_service = TransactionService(db)
        
        # Add a small delay to simulate processing time
        time.sleep(0.5)
        
        # Process file and extract transactions
        # Use the original filename for metadata extraction, but the temp file path for reading content
        result, transactions = file_service.process_file(temp_file_path, original_filename=file.filename)
        
        # Save transactions to database
        saved_count = transaction_service.save_transactions(transactions)
        
        # Update constituency metrics
        transaction_service.update_constituency_metrics(result.constituency_id)
        
        # Update transactions processed count
        result.transactions_processed = saved_count
        
        return result
    except MetadataExtractionError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract metadata from filename: {str(e)}"
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
        
        # Process directory
        file_service = FileService()
        transaction_service = TransactionService(db)
        
        # Add a small delay to simulate processing time
        time.sleep(0.5)
        
        # Process directory and extract transactions
        result, transactions = file_service.process_directory(directory_path)
        print(f"Directory processing result: {result}")
        print(f"Extracted {len(transactions)} transactions")
        
        # Save transactions to database
        saved_count = transaction_service.save_transactions(transactions)
        print(f"Saved {saved_count} transactions to database")
        
        # Update constituency metrics
        if result.constituency_id:
            print(f"Updating metrics for constituency: {result.constituency_id}")
            transaction_service.update_constituency_metrics(result.constituency_id)
        else:
            print("No constituency_id found, skipping metrics update")
        
        # Update transactions processed count
        result.transactions_processed = saved_count
        print(f"Final result: {result}")
        
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
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
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
        
        transaction_service = TransactionService(db)
        statistics = transaction_service.get_transaction_statistics(constituency_id)
        
        if not statistics:
            raise HTTPException(
                status_code=404,
                detail=f"Constituency not found: {constituency_id}"
            )
        
        return statistics
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )