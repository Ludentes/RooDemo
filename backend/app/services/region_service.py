"""
Region service for the Election Monitoring System.

This module provides services for creating, updating, and retrieving regions.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.region import Region
from app.models.schemas.region import RegionCreate, RegionUpdate
from app.crud import region as region_crud


class RegionService:
    """
    Service for region operations.
    
    This class provides methods for creating, updating, and retrieving regions.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_region(self, region_id: str) -> Optional[Region]:
        """
        Get a region by ID.
        
        Args:
            region_id: Region ID
            
        Returns:
            Region if found, None otherwise
        """
        return region_crud.get(self.db, region_id)
    
    def get_region_by_name(self, name: str) -> Optional[Region]:
        """
        Get a region by name.
        
        Args:
            name: Region name
            
        Returns:
            Region if found, None otherwise
        """
        return region_crud.get_by_name(self.db, name)
    
    def get_all_regions(self, skip: int = 0, limit: int = 100) -> List[Region]:
        """
        Get all regions.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of regions
        """
        return region_crud.get_all(self.db, skip, limit)
    
    def create_region(self, region: RegionCreate) -> Region:
        """
        Create a new region.
        
        Args:
            region: Region data
            
        Returns:
            Created region
        """
        return region_crud.create(self.db, region)
    
    def update_region(self, region_id: str, region: RegionUpdate) -> Optional[Region]:
        """
        Update an existing region.
        
        Args:
            region_id: Region ID
            region: Updated region data
            
        Returns:
            Updated region if found, None otherwise
        """
        return region_crud.update(self.db, region_id, region)
    
    def delete_region(self, region_id: str) -> Optional[Region]:
        """
        Delete a region.
        
        Args:
            region_id: Region ID
            
        Returns:
            Deleted region if found, None otherwise
        """
        return region_crud.delete(self.db, region_id)
    
    def create_or_update_region(self, region_id: str, region_name: str, country: str = "Russia") -> Region:
        """
        Create a new region or update an existing one.
        
        Args:
            region_id: Region ID
            region_name: Region name
            country: Country name (default: "Russia")
            
        Returns:
            Created or updated region
        """
        return region_crud.create_or_update(self.db, region_id, region_name, country)
    
    def extract_region_from_path(self, path_part: str) -> tuple:
        """
        Extract region ID and name from a path part.
        
        Args:
            path_part: Path part containing region information (e.g., "90 - Пермский край")
            
        Returns:
            Tuple of (region_id, region_name)
            
        Raises:
            ValueError: If the path part does not contain valid region information
        """
        import re
        
        # Expected format: "[RegionID] - [RegionName]"
        # Example: "90 - Пермский край"
        match = re.match(r"(\d+)\s*-\s*(.*)", path_part)
        if not match:
            raise ValueError(f"Invalid region format: {path_part}")
        
        region_id = match.group(1)
        region_name = match.group(2)
        
        return region_id, region_name