"""
Test script for the FileService.

This script tests the basic functionality of the FileService class.
"""

import os
import sys
import tempfile
from datetime import date
from pathlib import Path

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, backend_dir)

# Now import the modules

from app.services.file_service import FileService

def main():
    """Run tests for the FileService."""
    # Create a FileService instance
    service = FileService()
    
    
    print("Testing FileService...")
    
    try:
        # Test extracting metadata from a filename
        print("\nTesting metadata extraction:")
        filename = "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"
        metadata = service.extract_metadata_from_filename(filename)
        print(f"Metadata extraction successful:")
        print(f"  constituency_id: {metadata.constituency_id}")
        print(f"  date: {metadata.date}")
        print(f"  time_range: {metadata.time_range}")
        
        # Test parsing JSON-like structure
        print("\nTesting JSON parsing:")
        data_str = '{"key": "operation", "stringValue": "blindSigIssue"},{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"}'
        result = service._parse_json_like_structure(data_str)
        print(f"JSON parsing successful: {result}")
        
        # Test extracting transactions from CSV
        print("\nTesting transaction extraction:")
        csv_content = """65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;104;1662453028819;1662453028819;1662453028819;1662453028819;{"key": "operation", "stringValue": "blindSigIssue"};{"key": "BLINDSIG_65dbpXPGsbH3UsuYfvshDQsC9AcHTQx3emmKWbZKYQQS"};1;1
7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr;AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM;1;105;1662453128819;1662453128819;1662453128819;1662453128819;{"key": "operation", "stringValue": "vote"};{"key": "VOTE_7JKyZBUQRCvwbk8APzKHEGFmQXC9ZxFJxmJHkd6ec5Vr"};1;1"""
        transactions = service.extract_transactions_from_csv(csv_content, metadata)
        print(f"Transaction extraction successful:")
        print(f"  Number of transactions: {len(transactions)}")
        print(f"  First transaction ID: {transactions[0].transaction_id}")
        print(f"  First transaction type: {transactions[0].type}")
        
        # Test processing a file
        print("\nTesting file processing:")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file.write(csv_content.encode('utf-8'))
            temp_path = temp_file.name
        
        # Create a new file with the correct name
        new_path = os.path.join(os.path.dirname(temp_path), filename)
        os.rename(temp_path, new_path)
        
        try:
            result, transactions = service.process_file(Path(new_path))
            print(f"File processing successful:")
            print(f"  Filename: {result.filename}")
            print(f"  Transactions processed: {result.transactions_processed}")
            print(f"  Constituency ID: {result.constituency_id}")
        finally:
            # Clean up
            if os.path.exists(new_path):
                os.unlink(new_path)
        
        print("\nAll tests passed!")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)