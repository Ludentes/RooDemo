"""
Test script for the TransactionBatchProcessor.

This script tests the TransactionBatchProcessor by creating a batch request
and processing it.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.transaction_batch_processor import TransactionBatchProcessor
from app.models.schemas.transaction import TransactionCreate, TransactionBatchRequest
from app.models.schemas.constituency import ConstituencyCreate
from app.crud.constituency import constituency_crud
from datetime import datetime
from app.models.database import SessionLocal
import uuid

def test_batch_processor():
    """Test the TransactionBatchProcessor."""
    # Create a database session
    db = SessionLocal()
    
    try:
        # Create a test constituency
        constituency_id = str(uuid.uuid4())
        constituency = ConstituencyCreate(
            id=constituency_id,
            election_id="test-election-id",
            name="Test Constituency",
            region="test-region",
            type="urban",
            registered_voters=1000,
            status="active"
        )
        db_constituency = constituency_crud.create(db, obj_in=constituency)
        print(f"Created test constituency with ID: {constituency_id}")
        
        # Create a batch processor
        processor = TransactionBatchProcessor(db)
        
        # Create test transactions
        transaction1 = TransactionCreate(
            constituency_id=constituency_id,
            block_height=104,
            timestamp=datetime.utcnow(),
            type='blindSigIssue',
            raw_data={'key': 'operation', 'stringValue': 'blindSigIssue'},
            operation_data={'key': 'BLINDSIG_TEST1'},
            status='processed',
            source='batch'
        )
        
        transaction2 = TransactionCreate(
            constituency_id=constituency_id,
            block_height=105,
            timestamp=datetime.utcnow(),
            type='blindSigIssue',
            raw_data={'key': 'operation', 'stringValue': 'blindSigIssue'},
            operation_data={'key': 'BLINDSIG_TEST2'},
            status='processed',
            source='batch'
        )
        
        # Create a batch request
        batch_request = TransactionBatchRequest(transactions=[transaction1, transaction2])
        
        # Process the batch request
        try:
            result = processor.process_batch_request(batch_request)
            print(f'Batch processing result: {result}')
        except Exception as e:
            print(f'Error: {e}')
    finally:
        # Close the database session
        db.close()

if __name__ == '__main__':
    test_batch_processor()