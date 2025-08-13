"""
Tests for the Region model.

This module contains tests for the Region model.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.region import Region


def test_region_creation(db_session):
    """Test creating a Region instance."""
    # Arrange
    region = Region(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Act
    db_session.add(region)
    db_session.commit()
    db_session.refresh(region)
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"


def test_region_string_representation():
    """Test the string representation of a Region instance."""
    # Arrange
    region = Region(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Act
    region_str = str(region)
    
    # Assert
    assert "Region" in region_str
    assert "id=90" in region_str
    assert "name=Пермский край" in region_str
    assert "country=Russia" in region_str


def test_region_unique_id_constraint(db_session):
    """Test that Region ID must be unique."""
    # Arrange
    region1 = Region(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    db_session.add(region1)
    db_session.commit()
    
    # Act & Assert
    region2 = Region(
        id="90",  # Same ID as region1
        name="Another Region",
        country="Russia"
    )
    db_session.add(region2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback to clean up the session
    db_session.rollback()


def test_region_required_fields(db_session):
    """Test that name is required for Region."""
    # Arrange
    region = Region(
        id="90",
        # name is missing
        country="Russia"
    )
    
    # Act & Assert
    db_session.add(region)
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback to clean up the session
    db_session.rollback()