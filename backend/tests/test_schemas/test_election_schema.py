"""
Tests for the Election Pydantic schemas.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.schemas.election import (
    ElectionBase,
    ElectionCreate,
    ElectionUpdate,
    ElectionInDB,
    ElectionResponse,
)


def test_election_base_schema():
    """
    Test the ElectionBase schema.
    """
    # Valid data
    valid_data = {
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": "2024-11-05T00:00:00",
        "end_date": "2024-11-05T23:59:59",
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
    }
    
    # Create schema instance
    election = ElectionBase(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.name == valid_data["name"]
    assert election.country == valid_data["country"]
    assert isinstance(election.start_date, datetime)
    assert isinstance(election.end_date, datetime)
    assert election.status == valid_data["status"]
    assert election.type == valid_data["type"]
    assert election.description == valid_data["description"]
    assert election.timezone == valid_data["timezone"]


def test_election_base_schema_validation():
    """
    Test validation in the ElectionBase schema.
    """
    # Invalid status
    with pytest.raises(ValidationError):
        ElectionBase(
            name="Test Election",
            country="Test Country",
            start_date="2024-11-05T00:00:00",
            end_date="2024-11-05T23:59:59",
            status="invalid_status",  # Invalid status
            type="presidential",
            description="Test Description",
            timezone="America/New_York",
        )
    
    # Invalid type
    with pytest.raises(ValidationError):
        ElectionBase(
            name="Test Election",
            country="Test Country",
            start_date="2024-11-05T00:00:00",
            end_date="2024-11-05T23:59:59",
            status="scheduled",
            type="invalid_type",  # Invalid type
            description="Test Description",
            timezone="America/New_York",
        )
    
    # Invalid timezone
    with pytest.raises(ValidationError):
        ElectionBase(
            name="Test Election",
            country="Test Country",
            start_date="2024-11-05T00:00:00",
            end_date="2024-11-05T23:59:59",
            status="scheduled",
            type="presidential",
            description="Test Description",
            timezone="Invalid/Timezone",  # Invalid timezone
        )
    
    # End date before start date
    with pytest.raises(ValidationError):
        ElectionBase(
            name="Test Election",
            country="Test Country",
            start_date="2024-11-05T00:00:00",
            end_date="2024-11-04T23:59:59",  # End date before start date
            status="scheduled",
            type="presidential",
            description="Test Description",
            timezone="America/New_York",
        )


def test_election_create_schema():
    """
    Test the ElectionCreate schema.
    """
    # Valid data
    valid_data = {
        "id": "e12345",
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": "2024-11-05T00:00:00",
        "end_date": "2024-11-05T23:59:59",
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
    }
    
    # Create schema instance
    election = ElectionCreate(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.id == valid_data["id"]
    assert election.name == valid_data["name"]
    assert election.country == valid_data["country"]
    assert isinstance(election.start_date, datetime)
    assert isinstance(election.end_date, datetime)
    assert election.status == valid_data["status"]
    assert election.type == valid_data["type"]
    assert election.description == valid_data["description"]
    assert election.timezone == valid_data["timezone"]


def test_election_create_schema_validation():
    """
    Test validation in the ElectionCreate schema.
    """
    # Invalid ID format
    with pytest.raises(ValidationError):
        ElectionCreate(
            id="invalid-id",  # Invalid ID format
            name="Test Election",
            country="Test Country",
            start_date="2024-11-05T00:00:00",
            end_date="2024-11-05T23:59:59",
            status="scheduled",
            type="presidential",
            description="Test Description",
            timezone="America/New_York",
        )


def test_election_update_schema():
    """
    Test the ElectionUpdate schema.
    """
    # Valid data with some fields
    valid_data = {
        "name": "Updated Election Name",
        "status": "active",
    }
    
    # Create schema instance
    election = ElectionUpdate(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.name == valid_data["name"]
    assert election.status == valid_data["status"]
    
    # Check that other fields are None
    assert election.country is None
    assert election.start_date is None
    assert election.end_date is None
    assert election.type is None
    assert election.description is None
    assert election.timezone is None


def test_election_update_schema_validation():
    """
    Test validation in the ElectionUpdate schema.
    """
    # Invalid status
    with pytest.raises(ValidationError):
        ElectionUpdate(
            status="invalid_status",  # Invalid status
        )
    
    # Invalid type
    with pytest.raises(ValidationError):
        ElectionUpdate(
            type="invalid_type",  # Invalid type
        )
    
    # Invalid timezone
    with pytest.raises(ValidationError):
        ElectionUpdate(
            timezone="Invalid/Timezone",  # Invalid timezone
        )


def test_election_in_db_schema():
    """
    Test the ElectionInDB schema.
    """
    # Valid data
    valid_data = {
        "id": "e12345",
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": "2024-11-05T00:00:00",
        "end_date": "2024-11-05T23:59:59",
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
        "created_at": "2024-08-01T12:00:00",
        "updated_at": "2024-08-01T12:00:00",
    }
    
    # Create schema instance
    election = ElectionInDB(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.id == valid_data["id"]
    assert election.name == valid_data["name"]
    assert election.country == valid_data["country"]
    assert isinstance(election.start_date, datetime)
    assert isinstance(election.end_date, datetime)
    assert election.status == valid_data["status"]
    assert election.type == valid_data["type"]
    assert election.description == valid_data["description"]
    assert election.timezone == valid_data["timezone"]
    assert isinstance(election.created_at, datetime)
    assert isinstance(election.updated_at, datetime)


def test_election_response_schema():
    """
    Test the ElectionResponse schema.
    """
    # Valid data
    valid_data = {
        "id": "e12345",
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": "2024-11-05T00:00:00",
        "end_date": "2024-11-05T23:59:59",
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
        "created_at": "2024-08-01T12:00:00",
        "updated_at": "2024-08-01T12:00:00",
        "constituencies": [],
    }
    
    # Create schema instance
    election = ElectionResponse(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.id == valid_data["id"]
    assert election.name == valid_data["name"]
    assert election.country == valid_data["country"]
    assert isinstance(election.start_date, datetime)
    assert isinstance(election.end_date, datetime)
    assert election.status == valid_data["status"]
    assert election.type == valid_data["type"]
    assert election.description == valid_data["description"]
    assert election.timezone == valid_data["timezone"]
    assert isinstance(election.created_at, datetime)
    assert isinstance(election.updated_at, datetime)
    assert election.constituencies == []


def test_election_response_schema_with_constituencies():
    """
    Test the ElectionResponse schema with constituencies.
    """
    # Valid data with constituencies
    valid_data = {
        "id": "e12345",
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": "2024-11-05T00:00:00",
        "end_date": "2024-11-05T23:59:59",
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
        "created_at": "2024-08-01T12:00:00",
        "updated_at": "2024-08-01T12:00:00",
        "constituencies": [
            {
                "id": "c12345",
                "election_id": "e12345",
                "name": "California",
                "region": "West",
                "type": "state",
                "status": "active",
                "registered_voters": 25000000,
                "bulletins_issued": 0,
                "votes_cast": 0,
                "participation_rate": 0.0,
                "anomaly_score": 0.0,
                "created_at": "2024-08-01T12:00:00",
                "updated_at": "2024-08-01T12:00:00",
            }
        ],
    }
    
    # Create schema instance
    election = ElectionResponse(**valid_data)
    
    # Check that the data was parsed correctly
    assert election.id == valid_data["id"]
    assert len(election.constituencies) == 1
    assert election.constituencies[0].id == valid_data["constituencies"][0]["id"]
    assert election.constituencies[0].name == valid_data["constituencies"][0]["name"]