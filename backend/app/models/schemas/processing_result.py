"""
Processing result classes for the Election Monitoring System.

This module provides classes for file processing results.
"""

from datetime import date


class ProcessingResult:
    """
    Class for file processing result.
    
    This class represents the result of processing a single file.
    
    Attributes:
        filename (str): Name of the processed file
        transactions_processed (int): Number of transactions processed
        constituency_id (str): ID of the constituency (smart contract address)
        date (date): Date of the data
        time_range (str): Time range of the data (e.g., "0800-0900")
        region_id (str, optional): ID of the region (e.g., "90")
        region_name (str, optional): Name of the region (e.g., "Пермский край")
        election_name (str, optional): Name of the election (e.g., "Выборы депутатов Думы Красновишерского городского округа")
        constituency_name (str, optional): Name of the constituency (e.g., "Округ №1_3")
    """
    
    def __init__(
        self,
        filename: str,
        transactions_processed: int,
        constituency_id: str,
        date: date,
        time_range: str,
        region_id: str = None,
        region_name: str = None,
        election_name: str = None,
        constituency_name: str = None
    ):
        """Initialize a ProcessingResult instance."""
        self.filename = filename
        self.transactions_processed = transactions_processed
        self.constituency_id = constituency_id
        self.date = date
        self.time_range = time_range
        self.region_id = region_id
        self.region_name = region_name
        self.election_name = election_name
        self.constituency_name = constituency_name
    
    def __repr__(self):
        """Return a string representation of the ProcessingResult instance."""
        base_repr = (
            f"ProcessingResult(filename={self.filename}, "
            f"transactions_processed={self.transactions_processed}, "
            f"constituency_id={self.constituency_id}, "
            f"date={self.date}, "
            f"time_range={self.time_range}"
        )
        
        # Add optional fields if they exist
        if self.region_id:
            base_repr += f", region_id={self.region_id}"
        if self.region_name:
            base_repr += f", region_name={self.region_name}"
        if self.election_name:
            base_repr += f", election_name={self.election_name}"
        if self.constituency_name:
            base_repr += f", constituency_name={self.constituency_name}"
        
        return base_repr + ")"


class DirectoryProcessingResult:
    """
    Class for directory processing result.
    
    This class represents the result of processing a directory of files.
    
    Attributes:
        files_processed (int): Number of files processed
        transactions_processed (int): Total number of transactions processed
        constituency_id (str): ID of the constituency (smart contract address)
        region_id (str, optional): ID of the region (e.g., "90")
        region_name (str, optional): Name of the region (e.g., "Пермский край")
        election_name (str, optional): Name of the election (e.g., "Выборы депутатов Думы Красновишерского городского округа")
        constituency_name (str, optional): Name of the constituency (e.g., "Округ №1_3")
    """
    
    def __init__(
        self,
        files_processed: int,
        transactions_processed: int,
        constituency_id: str,
        region_id: str = None,
        region_name: str = None,
        election_name: str = None,
        constituency_name: str = None
    ):
        """Initialize a DirectoryProcessingResult instance."""
        self.files_processed = files_processed
        self.transactions_processed = transactions_processed
        self.constituency_id = constituency_id
        self.region_id = region_id
        self.region_name = region_name
        self.election_name = election_name
        self.constituency_name = constituency_name
    
    def __repr__(self):
        """Return a string representation of the DirectoryProcessingResult instance."""
        base_repr = (
            f"DirectoryProcessingResult(files_processed={self.files_processed}, "
            f"transactions_processed={self.transactions_processed}, "
            f"constituency_id={self.constituency_id}"
        )
        
        # Add optional fields if they exist
        if self.region_id:
            base_repr += f", region_id={self.region_id}"
        if self.region_name:
            base_repr += f", region_name={self.region_name}"
        if self.election_name:
            base_repr += f", election_name={self.election_name}"
        if self.constituency_name:
            base_repr += f", constituency_name={self.constituency_name}"
        
        return base_repr + ")"


class TransactionData:
    """
    Class for transaction data.
    
    This class represents the data extracted from a transaction in a CSV file.
    
    Attributes:
        transaction_id (str): ID of the transaction
        constituency_id (str): ID of the constituency (smart contract address)
        block_height (int): Blockchain block height
        timestamp (str): Transaction timestamp
        type (str): Transaction type ('blindSigIssue' or 'vote')
        raw_data (dict): Raw transaction data
        operation_data (dict): Processed operation data
    """
    
    def __init__(
        self,
        transaction_id: str,
        constituency_id: str,
        block_height: int,
        timestamp: str,
        type: str,
        raw_data: dict,
        operation_data: dict
    ):
        """Initialize a TransactionData instance."""
        self.transaction_id = transaction_id
        self.constituency_id = constituency_id
        self.block_height = block_height
        self.timestamp = timestamp
        self.type = type
        self.raw_data = raw_data
        self.operation_data = operation_data
    
    def __repr__(self):
        """Return a string representation of the TransactionData instance."""
        return (
            f"TransactionData(transaction_id={self.transaction_id}, "
            f"constituency_id={self.constituency_id}, "
            f"block_height={self.block_height}, "
            f"timestamp={self.timestamp}, "
            f"type={self.type})"
        )