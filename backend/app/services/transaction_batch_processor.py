"""
Transaction batch processor for the Election Monitoring System.

This module provides batch processing services for transaction data.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from app.models.schemas.transaction import TransactionCreate, TransactionBatchRequest, TransactionBatchResponse
from app.crud.transaction import transaction_crud
from app.api.errors.exceptions import BatchProcessingError

# Set up logging
logger = logging.getLogger(__name__)


class TransactionBatchProcessor:
    """
    Batch processor for transaction data.
    
    This class provides methods for processing transaction data in batches.
    """
    
    def __init__(self, db: Session, batch_size: int = 100):
        """
        Initialize the batch processor.
        
        Args:
            db: Database session
            batch_size: Size of each batch
        """
        self.db = db
        self.batch_size = batch_size
        # Lazy import to avoid circular dependencies
        from app.services.transaction_validator import TransactionValidator
        self.validator = TransactionValidator()
    
    def process_batch(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a batch of transactions.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Validate transactions
            validation_results = self.validator.validate_transaction_batch(self.db, transactions)
            
            # Create batch
            result = transaction_crud.create_batch(db=self.db, obj_in_list=transactions)
            
            # Add validation errors to result
            for index, errors in validation_results.items():
                if index < len(result["errors"]):
                    result["errors"][index]["validation_errors"] = errors
                else:
                    result["errors"].append({
                        "index": index,
                        "validation_errors": errors
                    })
            
            logger.info(f"Processed {result['processed']} transactions in batch (failed: {result['failed']})")
            return result
        except Exception as e:
            logger.exception("Failed to process transaction batch")
            self.db.rollback()
            raise BatchProcessingError(f"Failed to process transaction batch: {e}")
    
    def split_into_batches(self, transactions: List[TransactionCreate]) -> List[List[TransactionCreate]]:
        """
        Split transactions into batches.
        
        Args:
            transactions: List of transactions to split
            
        Returns:
            List of transaction batches
        """
        return [
            transactions[i:i + self.batch_size]
            for i in range(0, len(transactions), self.batch_size)
        ]
    
    def process_large_batch(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a large batch of transactions by splitting it into smaller batches.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Split into batches
            batches = self.split_into_batches(transactions)
            logger.info(f"Split {len(transactions)} transactions into {len(batches)} batches")
            
            # Process each batch
            results = []
            for i, batch in enumerate(batches):
                logger.info(f"Processing batch {i+1}/{len(batches)} with {len(batch)} transactions")
                result = self.process_batch(batch)
                results.append(result)
            
            # Combine results
            combined_result = {
                "success": all(r["success"] for r in results),
                "processed": sum(r["processed"] for r in results),
                "failed": sum(r["failed"] for r in results),
                "errors": []
            }
            
            # Combine errors
            for i, result in enumerate(results):
                for error in result["errors"]:
                    # Adjust index to account for batching
                    error["batch"] = i
                    error["batch_index"] = error["index"]
                    error["index"] = i * self.batch_size + error["index"]
                    combined_result["errors"].append(error)
            
            logger.info(f"Processed {combined_result['processed']} transactions in large batch (failed: {combined_result['failed']})")
            return combined_result
        except Exception as e:
            logger.exception("Failed to process large transaction batch")
            self.db.rollback()
            raise BatchProcessingError(f"Failed to process large transaction batch: {e}")
    
    async def process_batch_async(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a batch of transactions asynchronously.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Run in thread pool to avoid blocking
            with ThreadPoolExecutor() as executor:
                result = await asyncio.get_event_loop().run_in_executor(
                    executor, self.process_batch, transactions
                )
            return result
        except Exception as e:
            logger.exception("Failed to process transaction batch asynchronously")
            raise BatchProcessingError(f"Failed to process transaction batch asynchronously: {e}")
    
    async def process_large_batch_async(self, transactions: List[TransactionCreate]) -> Dict[str, Any]:
        """
        Process a large batch of transactions asynchronously.
        
        Args:
            transactions: List of transactions to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Split into batches
            batches = self.split_into_batches(transactions)
            logger.info(f"Split {len(transactions)} transactions into {len(batches)} batches for async processing")
            
            # Process each batch asynchronously
            tasks = [self.process_batch_async(batch) for batch in batches]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Batch {i} failed: {result}")
                    results[i] = {
                        "success": False,
                        "processed": 0,
                        "failed": len(batches[i]),
                        "errors": [{
                            "batch": i,
                            "error": str(result)
                        }]
                    }
            
            # Combine results
            combined_result = {
                "success": all(r["success"] for r in results),
                "processed": sum(r["processed"] for r in results),
                "failed": sum(r["failed"] for r in results),
                "errors": []
            }
            
            # Combine errors
            for i, result in enumerate(results):
                for error in result.get("errors", []):
                    # Adjust index to account for batching
                    error["batch"] = i
                    if "index" in error:
                        error["batch_index"] = error["index"]
                        error["index"] = i * self.batch_size + error["index"]
                    combined_result["errors"].append(error)
            
            logger.info(f"Processed {combined_result['processed']} transactions in async large batch (failed: {combined_result['failed']})")
            return combined_result
        except Exception as e:
            logger.exception("Failed to process large transaction batch asynchronously")
            raise BatchProcessingError(f"Failed to process large transaction batch asynchronously: {e}")
    
    def process_batch_request(self, batch_request: TransactionBatchRequest) -> TransactionBatchResponse:
        """
        Process a batch request.
        
        Args:
            batch_request: Batch request to process
            
        Returns:
            Batch response
            
        Raises:
            BatchProcessingError: If processing fails
        """
        try:
            # Process batch
            result = self.process_large_batch(batch_request.transactions)
            
            # Convert to response
            response = TransactionBatchResponse(
                success=result["success"],
                processed=result["processed"],
                failed=result["failed"],
                errors=result["errors"]
            )
            
            return response
        except Exception as e:
            logger.exception("Failed to process batch request")
            raise BatchProcessingError(f"Failed to process batch request: {e}")