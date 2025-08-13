"""
Tests for the RegionService.

This module contains tests for the region service.
"""

import pytest
from unittest.mock import MagicMock, patch

from app.services.region_service import RegionService
from app.models.region import Region
from app.models.schemas.region import RegionCreate, RegionUpdate


def test_get_region(db_session):
    """Test getting a region by ID."""
    # Arrange
    region = Region(id="90", name="Пермский край", country="Russia")
    db_session.add(region)
    db_session.commit()
    
    service = RegionService(db_session)
    
    # Act
    result = service.get_region("90")
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Пермский край"
    assert result.country == "Russia"


def test_get_region_not_found(db_session):
    """Test getting a non-existent region."""
    # Arrange
    service = RegionService(db_session)
    
    # Act
    result = service.get_region("nonexistent")
    
    # Assert
    assert result is None


def test_get_region_by_name(db_session):
    """Test getting a region by name."""
    # Arrange
    region = Region(id="90", name="Пермский край", country="Russia")
    db_session.add(region)
    db_session.commit()
    
    service = RegionService(db_session)
    
    # Act
    result = service.get_region_by_name("Пермский край")
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Пермский край"
    assert result.country == "Russia"


def test_get_all_regions(db_session):
    """Test getting all regions."""
    # Arrange
    region1 = Region(id="90", name="Пермский край", country="Russia")
    region2 = Region(id="77", name="Москва", country="Russia")
    db_session.add(region1)
    db_session.add(region2)
    db_session.commit()
    
    service = RegionService(db_session)
    
    # Act
    results = service.get_all_regions()
    
    # Assert
    assert len(results) == 2
    assert any(r.id == "90" and r.name == "Пермский край" for r in results)
    assert any(r.id == "77" and r.name == "Москва" for r in results)


def test_create_region(db_session):
    """Test creating a new region."""
    # Arrange
    service = RegionService(db_session)
    region_data = RegionCreate(id="90", name="Пермский край", country="Russia")
    
    # Act
    result = service.create_region(region_data)
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Пермский край"
    assert result.country == "Russia"
    
    # Verify it's in the database
    db_region = db_session.query(Region).filter(Region.id == "90").first()
    assert db_region is not None
    assert db_region.name == "Пермский край"


def test_update_region(db_session):
    """Test updating an existing region."""
    # Arrange
    region = Region(id="90", name="Пермский край", country="Russia")
    db_session.add(region)
    db_session.commit()
    
    service = RegionService(db_session)
    update_data = RegionUpdate(id="90", name="Updated Region", country="Russia")
    
    # Act
    result = service.update_region("90", update_data)
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Updated Region"
    assert result.country == "Russia"
    
    # Verify it's updated in the database
    db_region = db_session.query(Region).filter(Region.id == "90").first()
    assert db_region is not None
    assert db_region.name == "Updated Region"


def test_update_region_not_found(db_session):
    """Test updating a non-existent region."""
    # Arrange
    service = RegionService(db_session)
    update_data = RegionUpdate(id="nonexistent", name="Updated Region", country="Russia")
    
    # Act
    result = service.update_region("nonexistent", update_data)
    
    # Assert
    assert result is None


def test_delete_region(db_session):
    """Test deleting a region."""
    # Arrange
    region = Region(id="90", name="Пермский край", country="Russia")
    db_session.add(region)
    db_session.commit()
    
    service = RegionService(db_session)
    
    # Act
    result = service.delete_region("90")
    
    # Assert
    assert result is not None
    assert result.id == "90"
    
    # Verify it's deleted from the database
    db_region = db_session.query(Region).filter(Region.id == "90").first()
    assert db_region is None


def test_delete_region_not_found(db_session):
    """Test deleting a non-existent region."""
    # Arrange
    service = RegionService(db_session)
    
    # Act
    result = service.delete_region("nonexistent")
    
    # Assert
    assert result is None


def test_create_or_update_region_create(db_session):
    """Test create_or_update_region when the region doesn't exist."""
    # Arrange
    service = RegionService(db_session)
    
    # Act
    result = service.create_or_update_region("90", "Пермский край", "Russia")
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Пермский край"
    assert result.country == "Russia"
    
    # Verify it's in the database
    db_region = db_session.query(Region).filter(Region.id == "90").first()
    assert db_region is not None
    assert db_region.name == "Пермский край"


def test_create_or_update_region_update(db_session):
    """Test create_or_update_region when the region exists."""
    # Arrange
    region = Region(id="90", name="Пермский край", country="Russia")
    db_session.add(region)
    db_session.commit()
    
    service = RegionService(db_session)
    
    # Act
    result = service.create_or_update_region("90", "Updated Region", "Russia")
    
    # Assert
    assert result is not None
    assert result.id == "90"
    assert result.name == "Updated Region"
    assert result.country == "Russia"
    
    # Verify it's updated in the database
    db_region = db_session.query(Region).filter(Region.id == "90").first()
    assert db_region is not None
    assert db_region.name == "Updated Region"


def test_extract_region_from_path():
    """Test extracting region ID and name from a path part."""
    # Arrange
    service = RegionService(MagicMock())
    path_part = "90 - Пермский край"
    
    # Act
    region_id, region_name = service.extract_region_from_path(path_part)
    
    # Assert
    assert region_id == "90"
    assert region_name == "Пермский край"


def test_extract_region_from_path_with_spaces():
    """Test extracting region ID and name from a path part with extra spaces."""
    # Arrange
    service = RegionService(MagicMock())
    path_part = "90  -  Пермский край"
    
    # Act
    region_id, region_name = service.extract_region_from_path(path_part)
    
    # Assert
    assert region_id == "90"
    assert region_name == "Пермский край"


def test_extract_region_from_path_invalid_format():
    """Test extracting region from an invalid path part."""
    # Arrange
    service = RegionService(MagicMock())
    path_part = "Invalid Format"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid region format"):
        service.extract_region_from_path(path_part)