"""
Tests for the Election model.
"""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.models.election import Election


def test_election_creation(clean_db, sample_election_data):
    """
    Test creating an Election instance.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Query the election
    db_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    
    # Check that the election was created correctly
    assert db_election is not None
    assert db_election.id == sample_election_data["id"]
    assert db_election.name == sample_election_data["name"]
    assert db_election.country == sample_election_data["country"]
    assert db_election.status == sample_election_data["status"]
    assert db_election.type == sample_election_data["type"]
    assert db_election.description == sample_election_data["description"]
    assert db_election.timezone == sample_election_data["timezone"]


def test_election_relationships(clean_db, sample_election_data, sample_constituency_data):
    """
    Test Election relationships.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    from app.models.constituency import Constituency
    
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency for the election
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Query the election with constituencies
    db_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    
    # Check that the relationship works
    assert len(db_election.constituencies) == 1
    assert db_election.constituencies[0].id == sample_constituency_data["id"]
    assert db_election.constituencies[0].name == sample_constituency_data["name"]


def test_election_unique_id(clean_db, sample_election_data):
    """
    Test that Election IDs must be unique.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election1 = Election(**sample_election_data)
    clean_db.add(election1)
    clean_db.commit()
    
    # Try to create another election with the same ID
    election2 = Election(**sample_election_data)
    clean_db.add(election2)
    
    # This should raise an IntegrityError
    with pytest.raises(IntegrityError):
        clean_db.commit()
    
    # Rollback the transaction
    clean_db.rollback()


def test_election_required_fields(clean_db):
    """
    Test that required fields are enforced.
    
    Args:
        clean_db: SQLAlchemy session with clean database
    """
    # Try to create an election without required fields
    election = Election()
    clean_db.add(election)
    
    # This should raise an IntegrityError
    with pytest.raises(IntegrityError):
        clean_db.commit()
    
    # Rollback the transaction
    clean_db.rollback()


def test_election_default_values(clean_db):
    """
    Test that default values are set correctly.
    
    Args:
        clean_db: SQLAlchemy session with clean database
    """
    # Create an election with minimal fields
    election = Election(
        id="e67890",
        name="Test Election",
        country="Test Country",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow(),
    )
    clean_db.add(election)
    clean_db.commit()
    
    # Query the election
    db_election = clean_db.query(Election).filter(Election.id == "e67890").first()
    
    # Check default values
    assert db_election.status == "active"
    assert db_election.type == "general"
    assert db_election.created_at is not None
    assert db_election.updated_at is not None


def test_election_update(clean_db, sample_election_data):
    """
    Test updating an Election.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Update the election
    db_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    db_election.name = "Updated Election Name"
    db_election.status = "active"
    clean_db.commit()
    
    # Query the election again
    updated_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    
    # Check that the election was updated correctly
    assert updated_election.name == "Updated Election Name"
    assert updated_election.status == "active"


def test_election_delete(clean_db, sample_election_data):
    """
    Test deleting an Election.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Delete the election
    db_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    clean_db.delete(db_election)
    clean_db.commit()
    
    # Query the election again
    deleted_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    
    # Check that the election was deleted
    assert deleted_election is None


def test_election_cascade_delete(clean_db, sample_election_data, sample_constituency_data):
    """
    Test that deleting an Election cascades to related entities.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    from app.models.constituency import Constituency
    
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency for the election
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Delete the election
    db_election = clean_db.query(Election).filter(Election.id == sample_election_data["id"]).first()
    clean_db.delete(db_election)
    clean_db.commit()
    
    # Query the constituency
    deleted_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    
    # Check that the constituency was also deleted
    assert deleted_constituency is None