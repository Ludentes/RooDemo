"""
CRUD operations for regions.

This module provides functions for creating, reading, updating, and deleting regions.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.region import Region
from app.models.schemas.region import RegionCreate, RegionUpdate


def get(db: Session, id: str) -> Optional[Region]:
    """
    Get a region by ID.
    
    Args:
        db: Database session
        id: Region ID
        
    Returns:
        Region if found, None otherwise
    """
    return db.query(Region).filter(Region.id == id).first()


def get_by_name(db: Session, name: str) -> Optional[Region]:
    """
    Get a region by name.
    
    Args:
        db: Database session
        name: Region name
        
    Returns:
        Region if found, None otherwise
    """
    return db.query(Region).filter(Region.name == name).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Region]:
    """
    Get all regions.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of regions
    """
    return db.query(Region).offset(skip).limit(limit).all()


def create(db: Session, region: RegionCreate) -> Region:
    """
    Create a new region.
    
    Args:
        db: Database session
        region: Region data
        
    Returns:
        Created region
    """
    db_region = Region(
        id=region.id,
        name=region.name,
        country=region.country
    )
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region


def update(db: Session, id: str, region: RegionUpdate) -> Optional[Region]:
    """
    Update a region.
    
    Args:
        db: Database session
        id: Region ID
        region: Updated region data
        
    Returns:
        Updated region if found, None otherwise
    """
    db_region = get(db, id)
    if db_region:
        update_data = region.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_region, key, value)
        db.commit()
        db.refresh(db_region)
    return db_region


def delete(db: Session, id: str) -> Optional[Region]:
    """
    Delete a region.
    
    Args:
        db: Database session
        id: Region ID
        
    Returns:
        Deleted region if found, None otherwise
    """
    db_region = get(db, id)
    if db_region:
        db.delete(db_region)
        db.commit()
    return db_region


def create_or_update(db: Session, id: str, name: str, country: str = "Russia") -> Region:
    """
    Create a new region or update an existing one.
    
    Args:
        db: Database session
        id: Region ID
        name: Region name
        country: Country name (default: "Russia")
        
    Returns:
        Created or updated region
    """
    db_region = get(db, id)
    if db_region:
        db_region.name = name
        db_region.country = country
        db.commit()
        db.refresh(db_region)
        return db_region
    else:
        return create(db, RegionCreate(id=id, name=name, country=country))