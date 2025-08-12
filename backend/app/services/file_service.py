"""
File service for the Election Monitoring System.

This module provides services for file processing, including metadata extraction
and transaction extraction from CSV files.
"""

import os
import re
import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date

from app.models.schemas.file_metadata import FileMetadata
from app.models.schemas.processing_result import ProcessingResult, DirectoryProcessingResult, TransactionData
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError,
    TransactionExtractionError, DirectoryProcessingError
)


class FileService:
    """
    Service for file processing.
    
    This class provides methods for processing files, extracting metadata,
    and extracting transactions from CSV files.
    """
    
    def extract_metadata_from_filename(self, filename: str) -> FileMetadata:
        """
        Extract metadata from a file name.
        
        Args:
            filename: The name of the file
            
        Returns:
            Extracted metadata (constituency_id, date, time_range)
            
        Raises:
            MetadataExtractionError: If metadata cannot be extracted
        """
        try:
            # Expected format: [SmartContractID]_[Date]_[TimeRange].csv
            # Example: AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
            
            # Remove file extension and path
            filename = Path(filename).stem
            
            # Split by underscore
            parts = filename.split('_')
            if len(parts) != 3:
                raise ValueError(f"Invalid filename format: {filename}")
            
            constituency_id = parts[0]
            date_str = parts[1]
            time_range = parts[2]
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            return FileMetadata(
                constituency_id=constituency_id,
                date=date_obj,
                time_range=time_range
            )
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from filename: {e}")
    
    def extract_transactions_from_csv(self, file_content: str, metadata: FileMetadata) -> List[TransactionData]:
        """
        Extract transactions from CSV content.
        
        Args:
            file_content: Content of the CSV file
            metadata: Metadata extracted from filename
            
        Returns:
            List of extracted transactions
            
        Raises:
            TransactionExtractionError: If extraction fails
        """
        try:
            transactions = []
            
            # Parse CSV content
            csv_reader = csv.reader(file_content.splitlines(), delimiter=';')
            
            for row in csv_reader:
                if len(row) < 12:
                    continue  # Skip invalid rows
                
                transaction_id = row[0]
                block_height = int(row[3])
                timestamp_ms = int(row[4])
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000).isoformat()
                
                # Parse operation data (JSON-like structure)
                operation_data_str = row[8]
                operation_data = self._parse_json_like_structure(operation_data_str)
                
                # Determine transaction type
                transaction_type = None
                for item in operation_data:
                    if isinstance(item, dict) and item.get('key') == 'operation' and item.get('stringValue'):
                        transaction_type = item.get('stringValue')
                        break
                
                if not transaction_type:
                    continue  # Skip transactions without a type
                
                # Parse operation-specific data
                specific_data_str = row[9]
                specific_data = self._parse_json_like_structure(specific_data_str)
                
                # Convert lists to dictionaries for raw_data and operation_data
                raw_data_dict = {}
                for item in operation_data:
                    if isinstance(item, dict) and 'key' in item:
                        raw_data_dict[item['key']] = item
                
                operation_data_dict = {}
                for item in specific_data:
                    if isinstance(item, dict) and 'key' in item:
                        operation_data_dict[item['key']] = item
                
                transaction = TransactionData(
                    transaction_id=transaction_id,
                    constituency_id=metadata.constituency_id,
                    block_height=block_height,
                    timestamp=timestamp,
                    type=transaction_type,
                    raw_data=raw_data_dict,
                    operation_data=operation_data_dict
                )
                
                transactions.append(transaction)
            
            # Raise an error if no valid transactions were found
            if not transactions:
                raise ValueError("No valid transactions found in the CSV file")
            
            return transactions
        except Exception as e:
            raise TransactionExtractionError(f"Failed to extract transactions from CSV: {e}")
    
    def _parse_json_like_structure(self, data_str: str) -> List[Dict[str, Any]]:
        """
        Parse a JSON-like structure from a string.
        
        Args:
            data_str: String containing JSON-like structure
            
        Returns:
            Parsed data as a list of dictionaries
            
        Raises:
            ValueError: If parsing fails
        """
        try:
            # Handle empty strings
            if not data_str or data_str.strip() == '':
                return []
            
            # Remove square brackets at the beginning and end
            if data_str.startswith('[') and data_str.endswith(']'):
                data_str = data_str[1:-1]
            
            # Split by commas, but not within JSON objects
            items = []
            current_item = ""
            brace_count = 0
            
            for char in data_str:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                
                if char == ',' and brace_count == 0:
                    if current_item:
                        items.append(current_item.strip())
                        current_item = ""
                else:
                    current_item += char
            
            if current_item:
                items.append(current_item.strip())
            
            # Parse each item as JSON
            result = []
            for item in items:
                try:
                    result.append(json.loads(item))
                except json.JSONDecodeError:
                    # Skip items that can't be parsed as JSON
                    pass
            
            return result
        except Exception as e:
            raise ValueError(f"Failed to parse JSON-like structure: {e}")
    
    def process_file(self, file_path: Path, original_filename: str = None) -> ProcessingResult:
        """
        Process a CSV file and extract transactions.
        
        Args:
            file_path: Path to the file
            original_filename: Original filename to use for metadata extraction (optional)
            
        Returns:
            ProcessingResult with statistics
            
        Raises:
            FileProcessingError: If processing fails
        """
        try:
            # Extract metadata from filename
            filename_for_metadata = original_filename if original_filename else file_path.name
            metadata = self.extract_metadata_from_filename(filename_for_metadata)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract transactions
            transactions = self.extract_transactions_from_csv(content, metadata)
            
            # Create processing result
            result = ProcessingResult(
                filename=original_filename if original_filename else file_path.name,
                transactions_processed=len(transactions),
                constituency_id=metadata.constituency_id,
                date=metadata.date,
                time_range=metadata.time_range
            )
            
            return result, transactions
        except Exception as e:
            raise FileProcessingError(f"Failed to process file {file_path}: {e}")
    
    def process_directory(self, directory_path: str) -> Tuple[DirectoryProcessingResult, List[TransactionData]]:
        """
        Process all CSV files in a directory.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            DirectoryProcessingResult with statistics and list of all transactions
            
        Raises:
            DirectoryProcessingError: If processing fails
        """
        try:
            directory = Path(directory_path)
            print(f"Processing directory: {directory}")
            if not directory.exists() or not directory.is_dir():
                raise DirectoryProcessingError(f"Directory not found: {directory_path}")
            
            # Find all CSV files in the directory
            csv_files = list(directory.glob('**/*.csv'))
            print(f"Found {len(csv_files)} CSV files: {csv_files}")
            if not csv_files:
                raise DirectoryProcessingError(f"No CSV files found in directory: {directory_path}")
            
            # Process each file
            total_transactions_processed = 0
            all_transactions = []
            constituency_id = None
            
            for file_path in csv_files:
                try:
                    print(f"Processing file: {file_path}")
                    result, transactions = self.process_file(file_path)
                    print(f"Processed {result.transactions_processed} transactions from {file_path}")
                    total_transactions_processed += result.transactions_processed
                    all_transactions.extend(transactions)
                    
                    # Set constituency_id from the first file
                    if constituency_id is None:
                        constituency_id = result.constituency_id
                except Exception as e:
                    # Log error but continue processing other files
                    print(f"Error processing file {file_path}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Create directory processing result
            result = DirectoryProcessingResult(
                files_processed=len(csv_files),
                transactions_processed=total_transactions_processed,
                constituency_id=constituency_id or ""  # Fallback if no files were processed successfully
            )
            
            return result, all_transactions
        except Exception as e:
            raise DirectoryProcessingError(f"Failed to process directory {directory_path}: {e}")


# Simple minitest to check if the basic functionality works
if __name__ == "__main__":
    import tempfile
    import os
    import sys
    from datetime import date
    from pathlib import Path
    
    # Fix import paths when running directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.abspath(os.path.join(current_dir, '../../'))
    sys.path.insert(0, backend_dir)
    
    # Now import the modules
    from app.models.schemas.file_metadata import FileMetadata
    from app.models.schemas.processing_result import TransactionData
    
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
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()