"""
Tests for the Constituency model.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.constituency import Constituency
from app.models.election import Election


def test_constituency_creation(clean_db, sample_election_data, sample_constituency_data):
    """
    Test creating a Constituency instance.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election first
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Query the constituency
    db_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    
    # Check that the constituency was created correctly
    assert db_constituency is not None
    assert db_constituency.id == sample_constituency_data["id"]
    assert db_constituency.election_id == sample_constituency_data["election_id"]
    assert db_constituency.name == sample_constituency_data["name"]
    assert db_constituency.region == sample_constituency_data["region"]
    assert db_constituency.type == sample_constituency_data["type"]
    assert db_constituency.status == sample_constituency_data["status"]
    assert db_constituency.registered_voters == sample_constituency_data["registered_voters"]
    assert db_constituency.bulletins_issued == sample_constituency_data["bulletins_issued"]
    assert db_constituency.votes_cast == sample_constituency_data["votes_cast"]
    assert db_constituency.participation_rate == sample_constituency_data["participation_rate"]
    assert db_constituency.anomaly_score == sample_constituency_data["anomaly_score"]


def test_constituency_relationships(clean_db, sample_election_data, sample_constituency_data):
    """
    Test Constituency relationships.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Query the constituency with election
    db_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    
    # Check that the relationship works
    assert db_constituency.election is not None
    assert db_constituency.election.id == sample_election_data["id"]
    assert db_constituency.election.name == sample_election_data["name"]


def test_constituency_unique_id(clean_db, sample_election_data, sample_constituency_data):
    """
    Test that Constituency IDs must be unique.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
    constituency1 = Constituency(**sample_constituency_data)
    clean_db.add(constituency1)
    clean_db.commit()
    
    # Try to create another constituency with the same ID
    constituency2 = Constituency(**sample_constituency_data)
    clean_db.add(constituency2)
    
    # This should raise an IntegrityError
    with pytest.raises(IntegrityError):
        clean_db.commit()
    
    # Rollback the transaction
    clean_db.rollback()


def test_constituency_required_fields(clean_db, sample_election_data):
    """
    Test that required fields are enforced.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Try to create a constituency without required fields
    constituency = Constituency()
    clean_db.add(constituency)
    
    # This should raise an IntegrityError
    with pytest.raises(IntegrityError):
        clean_db.commit()
    
    # Rollback the transaction
    clean_db.rollback()


def test_constituency_foreign_key_constraint(clean_db, sample_constituency_data):
    """
    Test that the foreign key constraint is enforced.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_constituency_data: Sample constituency data
    """
    # Try to create a constituency without a valid election_id
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    
    # This should raise an IntegrityError
    with pytest.raises(IntegrityError):
        clean_db.commit()
    
    # Rollback the transaction
    clean_db.rollback()


def test_constituency_default_values(clean_db, sample_election_data):
    """
    Test that default values are set correctly.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency with minimal fields
    constituency = Constituency(
        id="c67890",
        election_id=sample_election_data["id"],
        name="Test Constituency",
        region="Test Region",
    )
    clean_db.add(constituency)
    clean_db.commit()
    
    # Query the constituency
    db_constituency = clean_db.query(Constituency).filter(Constituency.id == "c67890").first()
    
    # Check default values
    assert db_constituency.type == "district"
    assert db_constituency.status == "inactive"
    assert db_constituency.registered_voters == 0
    assert db_constituency.bulletins_issued == 0
    assert db_constituency.votes_cast == 0
    assert db_constituency.participation_rate == 0.0
    assert db_constituency.anomaly_score == 0.0
    assert db_constituency.created_at is not None
    assert db_constituency.updated_at is not None


def test_constituency_update(clean_db, sample_election_data, sample_constituency_data):
    """
    Test updating a Constituency.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Update the constituency
    db_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    db_constituency.name = "Updated Constituency Name"
    db_constituency.status = "active"
    db_constituency.registered_voters = 30000000
    db_constituency.bulletins_issued = 20000000
    db_constituency.votes_cast = 18000000
    db_constituency.participation_rate = 0.6
    clean_db.commit()
    
    # Query the constituency again
    updated_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    
    # Check that the constituency was updated correctly
    assert updated_constituency.name == "Updated Constituency Name"
    assert updated_constituency.status == "active"
    assert updated_constituency.registered_voters == 30000000
    assert updated_constituency.bulletins_issued == 20000000
    assert updated_constituency.votes_cast == 18000000
    assert updated_constituency.participation_rate == 0.6


def test_constituency_delete(clean_db, sample_election_data, sample_constituency_data):
    """
    Test deleting a Constituency.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
    constituency = Constituency(**sample_constituency_data)
    clean_db.add(constituency)
    clean_db.commit()
    
    # Delete the constituency
    db_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    clean_db.delete(db_constituency)
    clean_db.commit()
    
    # Query the constituency again
    deleted_constituency = clean_db.query(Constituency).filter(
        Constituency.id == sample_constituency_data["id"]
    ).first()
    
    # Check that the constituency was deleted
    assert deleted_constituency is None


def test_constituency_cascade_delete_from_election(clean_db, sample_election_data, sample_constituency_data):
    """
    Test that deleting an Election cascades to Constituencies.
    
    Args:
        clean_db: SQLAlchemy session with clean database
        sample_election_data: Sample election data
        sample_constituency_data: Sample constituency data
    """
    # Create an election
    election = Election(**sample_election_data)
    clean_db.add(election)
    clean_db.commit()
    
    # Create a constituency
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