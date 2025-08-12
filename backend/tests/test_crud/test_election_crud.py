"""
Tests for the Election CRUD operations.
"""

import pytest
from datetime import datetime

from app.models.election import Election
from app.models.schemas.election import ElectionCreate, ElectionUpdate
from app.crud.election import election_crud


def test_create_election(clean_db, sample_election_data):
    """
    Test creating an election using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election = election_crud.create(clean_db, obj_in=election_in)
    
    # Check that the election was created correctly
    assert election.id == sample_election_data["id"]
    assert election.name == sample_election_data["name"]
    assert election.country == sample_election_data["country"]
    assert election.status == sample_election_data["status"]
    assert election.type == sample_election_data["type"]
    assert election.description == sample_election_data["description"]
    assert election.timezone == sample_election_data["timezone"]
    assert election.created_at is not None
    assert election.updated_at is not None


def test_get_election(clean_db, sample_election_data):
    """
    Test getting an election using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Get election
    election = election_crud.get(clean_db, id=sample_election_data["id"])
    
    # Check that the election was retrieved correctly
    assert election is not None
    assert election.id == sample_election_data["id"]
    assert election.name == sample_election_data["name"]


def test_get_election_not_found(clean_db):
    """
    Test getting a non-existent election using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
    """
    # Get non-existent election
    election = election_crud.get(clean_db, id="non-existent-id")
    
    # Check that the election was not found
    assert election is None


def test_get_elections(clean_db, sample_election_data):
    """
    Test getting all elections using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Create another election
    another_election_data = sample_election_data.copy()
    another_election_data["id"] = "e67890"
    another_election_data["name"] = "Another Election"
    another_election_in = ElectionCreate(**another_election_data)
    election_crud.create(clean_db, obj_in=another_election_in)
    
    # Get all elections
    elections = election_crud.get_multi(clean_db)
    
    # Check that both elections were retrieved
    assert len(elections) == 2
    assert any(e.id == sample_election_data["id"] for e in elections)
    assert any(e.id == "e67890" for e in elections)


def test_update_election(clean_db, sample_election_data):
    """
    Test updating an election using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Update data
    update_data = {
        "name": "Updated Election Name",
        "status": "active",
    }
    election_update = ElectionUpdate(**update_data)
    
    # Update election
    updated_election = election_crud.update(
        clean_db, db_obj=election_crud.get(clean_db, id=sample_election_data["id"]), obj_in=election_update
    )
    
    # Check that the election was updated correctly
    assert updated_election.name == update_data["name"]
    assert updated_election.status == update_data["status"]
    assert updated_election.country == sample_election_data["country"]  # Unchanged field


def test_delete_election(clean_db, sample_election_data):
    """
    Test deleting an election using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Delete election
    deleted_election = election_crud.remove(clean_db, id=sample_election_data["id"])
    
    # Check that the election was deleted
    assert deleted_election.id == sample_election_data["id"]
    
    # Try to get the deleted election
    election = election_crud.get(clean_db, id=sample_election_data["id"])
    assert election is None


def test_get_by_status(clean_db, sample_election_data):
    """
    Test getting elections by status using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Create another election with different status
    another_election_data = sample_election_data.copy()
    another_election_data["id"] = "e67890"
    another_election_data["name"] = "Another Election"
    another_election_data["status"] = "active"
    another_election_in = ElectionCreate(**another_election_data)
    election_crud.create(clean_db, obj_in=another_election_in)
    
    # Get elections by status
    scheduled_elections = election_crud.get_by_status(clean_db, status="scheduled")
    active_elections = election_crud.get_by_status(clean_db, status="active")
    
    # Check that the elections were retrieved correctly
    assert len(scheduled_elections) == 1
    assert scheduled_elections[0].id == sample_election_data["id"]
    
    assert len(active_elections) == 1
    assert active_elections[0].id == "e67890"


def test_get_by_country(clean_db, sample_election_data):
    """
    Test getting elections by country using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Create another election with different country
    another_election_data = sample_election_data.copy()
    another_election_data["id"] = "e67890"
    another_election_data["name"] = "Another Election"
    another_election_data["country"] = "Canada"
    another_election_in = ElectionCreate(**another_election_data)
    election_crud.create(clean_db, obj_in=another_election_in)
    
    # Get elections by country
    us_elections = election_crud.get_by_country(clean_db, country="United States")
    canada_elections = election_crud.get_by_country(clean_db, country="Canada")
    
    # Check that the elections were retrieved correctly
    assert len(us_elections) == 1
    assert us_elections[0].id == sample_election_data["id"]
    
    assert len(canada_elections) == 1
    assert canada_elections[0].id == "e67890"


def test_get_by_type(clean_db, sample_election_data):
    """
    Test getting elections by type using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Create another election with different type
    another_election_data = sample_election_data.copy()
    another_election_data["id"] = "e67890"
    another_election_data["name"] = "Another Election"
    another_election_data["type"] = "parliamentary"
    another_election_in = ElectionCreate(**another_election_data)
    election_crud.create(clean_db, obj_in=another_election_in)
    
    # Get elections by type
    presidential_elections = election_crud.get_by_type(clean_db, type="presidential")
    parliamentary_elections = election_crud.get_by_type(clean_db, type="parliamentary")
    
    # Check that the elections were retrieved correctly
    assert len(presidential_elections) == 1
    assert presidential_elections[0].id == sample_election_data["id"]
    
    assert len(parliamentary_elections) == 1
    assert parliamentary_elections[0].id == "e67890"


def test_get_active_elections(clean_db, sample_election_data):
    """
    Test getting active elections using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema with scheduled status
    election_in = ElectionCreate(**sample_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Create another election with active status
    another_election_data = sample_election_data.copy()
    another_election_data["id"] = "e67890"
    another_election_data["name"] = "Another Election"
    another_election_data["status"] = "active"
    another_election_in = ElectionCreate(**another_election_data)
    election_crud.create(clean_db, obj_in=another_election_in)
    
    # Get active elections
    active_elections = election_crud.get_active_elections(clean_db)
    
    # Check that only the active election was retrieved
    assert len(active_elections) == 1
    assert active_elections[0].id == "e67890"


def test_get_upcoming_elections(clean_db, sample_election_data):
    """
    Test getting upcoming elections using the CRUD operations.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create election schema with future start date
    future_election_data = sample_election_data.copy()
    future_election_data["start_date"] = datetime.utcnow()
    future_election_data["end_date"] = datetime.utcnow()
    election_in = ElectionCreate(**future_election_data)
    
    # Create election
    election_crud.create(clean_db, obj_in=election_in)
    
    # Get upcoming elections
    upcoming_elections = election_crud.get_upcoming_elections(clean_db)
    
    # Check that the upcoming election was retrieved
    assert len(upcoming_elections) == 1
    assert upcoming_elections[0].id == sample_election_data["id"]