"""
File service for the Election Monitoring System.

This module provides services for file processing, including metadata extraction
and transaction extraction from CSV files.
"""

import os
import re
import csv
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date

from app.models.schemas.file_metadata import FileMetadata
from app.models.schemas.processing_result import ProcessingResult, DirectoryProcessingResult, TransactionData
from app.api.errors.exceptions import (
    FileProcessingError, MetadataExtractionError,
    TransactionExtractionError, DirectoryProcessingError
)

# Set up logging
logger = logging.getLogger(__name__)


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
            FileMetadata object with extracted metadata
            
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
            
            # Create and return a FileMetadata object
            return FileMetadata(
                constituency_id=constituency_id,
                date=date_obj,
                time_range=time_range
            )
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from filename: {e}")
    
    def extract_metadata_from_path(self, file_path: Path) -> Dict[str, str]:
        """
        Extract metadata from a file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with extracted metadata (region_id, region_name, election_name, constituency_name, constituency_id)
            
        Raises:
            MetadataExtractionError: If metadata cannot be extracted
        """
        try:
            # Convert to absolute path to ensure we have the full path
            abs_path = file_path.absolute()
            
            # Get parts of the path
            parts = abs_path.parts
            
            # Look for a directory with the pattern "XX - Region Name" in the path
            region_index = -1
            for i, part in enumerate(parts):
                if re.match(r"\d+\s*-\s*.*", part):
                    region_index = i
                    break
            
            if region_index == -1 or region_index + 3 >= len(parts):
                raise ValueError(f"Could not find region directory in path: {file_path}")
            
            # Extract region information
            region_part = parts[region_index]
            region_match = re.match(r"(\d+)\s*-\s*(.*)", region_part)
            if not region_match:
                raise ValueError(f"Invalid region format: {region_part}")
            
            region_id = region_match.group(1)
            region_name = region_match.group(2)
            
            # Extract election name
            election_name = parts[region_index + 1]
            
            # Extract constituency name
            constituency_name = parts[region_index + 2]
            
            # Extract constituency ID (smart contract ID)
            constituency_id = parts[region_index + 3]
            
            return {
                "region_id": region_id,
                "region_name": region_name,
                "election_name": election_name,
                "constituency_name": constituency_name,
                "constituency_id": constituency_id
            }
        except Exception as e:
            raise MetadataExtractionError(f"Failed to extract metadata from path: {e}")
    
    def extract_transactions_from_csv(self, file_content: str, metadata: FileMetadata) -> List[TransactionData]:
        """
        Extract transactions from CSV content.
        
        Args:
            file_content: Content of the CSV file
            metadata: Metadata extracted from filename and path
            
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
    
    def process_file(self, file_path: Path, original_filename: str = None) -> Tuple[ProcessingResult, List[TransactionData]]:
        """
        Process a CSV file and extract transactions with enhanced metadata.
        
        Args:
            file_path: Path to the file
            original_filename: Original filename to use for metadata extraction (optional)
            
        Returns:
            ProcessingResult with statistics and list of transactions
            
        Raises:
            FileProcessingError: If processing fails
        """
        try:
            # Extract metadata from filename
            filename_for_metadata = original_filename if original_filename else file_path.name
            filename_metadata = self.extract_metadata_from_filename(filename_for_metadata)
            
            # Extract metadata from path
            try:
                path_metadata = self.extract_metadata_from_path(file_path)
                
                # Verify that constituency_id from filename matches constituency_id from path
                if filename_metadata.constituency_id != path_metadata["constituency_id"]:
                    logger.warning(
                        f"Constituency ID mismatch: {filename_metadata.constituency_id} (filename) "
                        f"vs {path_metadata['constituency_id']} (path)"
                    )
            except MetadataExtractionError as e:
                logger.warning(f"Failed to extract metadata from path: {e}")
                path_metadata = {
                    "region_id": None,
                    "region_name": None,
                    "election_name": None,
                    "constituency_name": None,
                    "constituency_id": filename_metadata.constituency_id
                }
            
            # Update FileMetadata object with path metadata
            filename_metadata.region_id = path_metadata["region_id"]
            filename_metadata.region_name = path_metadata["region_name"]
            filename_metadata.election_name = path_metadata["election_name"]
            filename_metadata.constituency_name = path_metadata["constituency_name"]
            
            # Use the updated metadata
            metadata = filename_metadata
            
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
                time_range=metadata.time_range,
                region_id=metadata.region_id,
                region_name=metadata.region_name,
                election_name=metadata.election_name,
                constituency_name=metadata.constituency_name
            )
            
            return result, transactions
        except Exception as e:
            raise FileProcessingError(f"Failed to process file {file_path}: {e}")
    
    def process_directory(self, directory_path: str) -> Tuple[DirectoryProcessingResult, List[TransactionData]]:
        """
        Process all CSV files in a directory with enhanced metadata extraction.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            DirectoryProcessingResult with statistics and list of all transactions
            
        Raises:
            DirectoryProcessingError: If processing fails
        """
        try:
            directory = Path(directory_path)
            logger.info(f"Processing directory: {directory}")
            if not directory.exists() or not directory.is_dir():
                raise DirectoryProcessingError(f"Directory not found: {directory_path}")
            
            # Find all CSV files in the directory
            csv_files = list(directory.glob('**/*.csv'))
            logger.info(f"Found {len(csv_files)} CSV files")
            if not csv_files:
                raise DirectoryProcessingError(f"No CSV files found in directory: {directory_path}")
            
            # Process each file
            total_transactions_processed = 0
            all_transactions = []
            
            # Variables to store common metadata
            region_id = None
            region_name = None
            election_name = None
            constituency_name = None
            constituency_id = None
            
            for file_path in csv_files:
                try:
                    logger.info(f"Processing file: {file_path}")
                    result, transactions = self.process_file(file_path)
                    logger.info(f"Processed {result.transactions_processed} transactions from {file_path}")
                    total_transactions_processed += result.transactions_processed
                    all_transactions.extend(transactions)
                    
                    # Set metadata from the first successful file
                    if constituency_id is None:
                        constituency_id = result.constituency_id
                        region_id = result.region_id
                        region_name = result.region_name
                        election_name = result.election_name
                        constituency_name = result.constituency_name
                except Exception as e:
                    # Log error but continue processing other files
                    logger.error(f"Error processing file {file_path}: {e}")
            
            # Create directory processing result
            result = DirectoryProcessingResult(
                files_processed=len(csv_files),
                transactions_processed=total_transactions_processed,
                constituency_id=constituency_id or "",  # Fallback if no files were processed successfully
                region_id=region_id,
                region_name=region_name,
                election_name=election_name,
                constituency_name=constituency_name
            )
            
            return result, all_transactions
        except Exception as e:
            raise DirectoryProcessingError(f"Failed to process directory {directory_path}: {e}")