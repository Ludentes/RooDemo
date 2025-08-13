"""
File metadata for the Election Monitoring System.

This module provides a class for file metadata.
"""

from datetime import date
import re


class FileMetadata:
    """
    Class for file metadata.
    
    This class represents metadata extracted from a file name and path.
    
    Attributes:
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
        constituency_id: str, 
        date: date, 
        time_range: str,
        region_id: str = None,
        region_name: str = None,
        election_name: str = None,
        constituency_name: str = None
    ):
        """Initialize a FileMetadata instance."""
        # Validate constituency_id
        if not re.match(r'^[A-Za-z0-9]{32,}$', constituency_id):
            raise ValueError('Invalid constituency ID format')
        
        # Validate date
        if date > date.today():
            raise ValueError('Date cannot be in the future')
        
        # Validate time_range
        if not re.match(r'^[0-9]{4}-[0-9]{4}$', time_range):
            raise ValueError('Invalid time range format. Expected format: "HHMM-HHMM"')
        
        # Extract start and end times
        start_time, end_time = time_range.split('-')
        
        # Convert to integers for comparison
        start_hour = int(start_time[:2])
        start_minute = int(start_time[2:])
        end_hour = int(end_time[:2])
        end_minute = int(end_time[2:])
        
        # Validate hours and minutes
        if start_hour > 23 or start_minute > 59 or end_hour > 23 or end_minute > 59:
            raise ValueError('Invalid time values. Hours must be 0-23, minutes must be 0-59')
        
        # Ensure end time is after start time (unless it crosses midnight)
        start_total_minutes = start_hour * 60 + start_minute
        end_total_minutes = end_hour * 60 + end_minute
        
        if end_total_minutes <= start_total_minutes and end_total_minutes != 0:  # Allow 0000 as end time (midnight)
            raise ValueError('End time must be after start time')
        
        self.constituency_id = constituency_id
        self.date = date
        self.time_range = time_range
        self.region_id = region_id
        self.region_name = region_name
        self.election_name = election_name
        self.constituency_name = constituency_name
    
    def __repr__(self):
        """Return a string representation of the FileMetadata instance."""
        base_repr = (
            f"FileMetadata(constituency_id={self.constituency_id}, "
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