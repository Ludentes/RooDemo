#!/usr/bin/env python3
"""
Script to process a CSV file using the File Processing System.

This script demonstrates how to use the File Processing System to process a CSV file
and store the transactions in the database.

Usage:
    python process_file.py <file_path>
"""

import os
import sys
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.database import SessionLocal
from app.services.file_service import FileService
from app.services.transaction_service import TransactionService


def process_file(file_path: str) -> None:
    """
    Process a CSV file and store the transactions in the database.
    
    Args:
        file_path: Path to the CSV file
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Create services
        file_service = FileService()
        transaction_service = TransactionService(db)
        
        # Process file
        print(f"Processing file: {file_path}")
        result, transactions = file_service.process_file(Path(file_path))
        
        # Print result
        print(f"File processed successfully:")
        print(f"  Filename: {result.filename}")
        print(f"  Constituency ID: {result.constituency_id}")
        print(f"  Date: {result.date}")
        print(f"  Time Range: {result.time_range}")
        print(f"  Transactions extracted: {len(transactions)}")
        
        # Count transactions by type
        transaction_types = {}
        for transaction in transactions:
            transaction_types[transaction.type] = transaction_types.get(transaction.type, 0) + 1
        
        print("Transaction types:")
        for transaction_type, count in transaction_types.items():
            print(f"  {transaction_type}: {count}")
        
        # Save transactions to database
        print("Saving transactions to database...")
        saved_count = transaction_service.save_transactions(transactions)
        print(f"Saved {saved_count} transactions to database")
        
        # Update constituency metrics
        print(f"Updating constituency metrics for {result.constituency_id}...")
        transaction_service.update_constituency_metrics(result.constituency_id)
        print("Constituency metrics updated successfully")
        
        # Get transaction statistics
        print("Getting transaction statistics...")
        statistics = transaction_service.get_transaction_statistics(result.constituency_id)
        
        print("Transaction statistics:")
        print(f"  Total transactions: {statistics['total_transactions']}")
        print(f"  Bulletins issued: {statistics['bulletins_issued']}")
        print(f"  Votes cast: {statistics['votes_cast']}")
        print(f"  Participation rate: {statistics['participation_rate']:.2f}%")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def process_directory(directory_path: str) -> None:
    """
    Process all CSV files in a directory.
    
    Args:
        directory_path: Path to the directory
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Create services
        file_service = FileService()
        transaction_service = TransactionService(db)
        
        # Process directory
        print(f"Processing directory: {directory_path}")
        result, transactions = file_service.process_directory(directory_path)
        
        # Print result
        print(f"Directory processed successfully:")
        print(f"  Files processed: {result.files_processed}")
        print(f"  Constituency ID: {result.constituency_id}")
        print(f"  Transactions extracted: {len(transactions)}")
        
        # Count transactions by type
        transaction_types = {}
        for transaction in transactions:
            transaction_types[transaction.type] = transaction_types.get(transaction.type, 0) + 1
        
        print("Transaction types:")
        for transaction_type, count in transaction_types.items():
            print(f"  {transaction_type}: {count}")
        
        # Save transactions to database
        print("Saving transactions to database...")
        saved_count = transaction_service.save_transactions(transactions)
        print(f"Saved {saved_count} transactions to database")
        
        # Update constituency metrics
        if result.constituency_id:
            print(f"Updating constituency metrics for {result.constituency_id}...")
            transaction_service.update_constituency_metrics(result.constituency_id)
            print("Constituency metrics updated successfully")
        
    except Exception as e:
        print(f"Error processing directory: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python process_file.py <file_path>")
        print("  python process_file.py --directory <directory_path>")
        sys.exit(1)
    
    if sys.argv[1] == "--directory":
        if len(sys.argv) < 3:
            print("Usage: python process_file.py --directory <directory_path>")
            sys.exit(1)
        
        directory_path = sys.argv[2]
        process_directory(directory_path)
    else:
        file_path = sys.argv[1]
        process_file(file_path)


if __name__ == "__main__":
    main()