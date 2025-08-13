"""
Tests for the Region schema.

This module contains tests for the Region schema.
"""

import pytest
from pydantic import ValidationError

from app.models.schemas.region import RegionBase, RegionCreate, RegionUpdate, Region


def test_region_base_schema():
    """Test the RegionBase schema."""
    # Arrange & Act
    region = RegionBase(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"


def test_region_base_schema_default_country():
    """Test the RegionBase schema with default country."""
    # Arrange & Act
    region = RegionBase(
        id="90",
        name="Пермский край"
    )
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"  # Default value


def test_region_base_schema_required_fields():
    """Test that id and name are required for RegionBase."""
    # Act & Assert
    with pytest.raises(ValidationError):
        RegionBase(name="Пермский край")  # Missing id
    
    with pytest.raises(ValidationError):
        RegionBase(id="90")  # Missing name


def test_region_create_schema():
    """Test the RegionCreate schema."""
    # Arrange & Act
    region = RegionCreate(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"


def test_region_update_schema():
    """Test the RegionUpdate schema."""
    # Arrange & Act
    region = RegionUpdate(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"


def test_region_response_schema():
    """Test the Region response schema."""
    # Arrange & Act
    region = Region(
        id="90",
        name="Пермский край",
        country="Russia"
    )
    
    # Assert
    assert region.id == "90"
    assert region.name == "Пермский край"
    assert region.country == "Russia"


def test_region_schema_example():
    """Test that the Region schema has an example."""
    # Arrange & Act
    example = Region.Config.schema_extra["example"]
    
    # Assert
    assert example["id"] == "90"
    assert example["name"] == "Пермский край"
    assert example["country"] == "Russia"