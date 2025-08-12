"""
Pytest configuration for the Election Monitoring System.

This module provides fixtures for testing the application.
"""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from datetime import datetime

from app.models.database import Base
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.models.hourly_stats import HourlyStats
from app.models.file_processing import FileProcessingJob


@pytest.fixture(scope="session")
def engine():
    """
    Create a SQLAlchemy engine for testing.
    
    This fixture creates an in-memory SQLite database for testing.
    
    Returns:
        SQLAlchemy engine
    """
    # Use in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Enable foreign key constraints in SQLite
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Create a SQLAlchemy session for testing.
    
    This fixture creates a new session for each test function.
    
    Args:
        engine: SQLAlchemy engine
        
    Returns:
        SQLAlchemy session
    """
    # Create a new session for each test
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def clean_db(db_session):
    """
    Clean the database before each test.
    
    This fixture deletes all data from the database before each test.
    
    Args:
        db_session: SQLAlchemy session
        
    Returns:
        SQLAlchemy session
    """
    # Delete all data from all tables
    db_session.query(FileProcessingJob).delete()
    db_session.query(HourlyStats).delete()
    db_session.query(Alert).delete()
    db_session.query(Transaction).delete()
    db_session.query(Constituency).delete()
    db_session.query(Election).delete()
    db_session.commit()
    
    return db_session


def parse_datetime(datetime_str):
    """
    Parse a datetime string into a datetime object.
    
    Args:
        datetime_str: Datetime string in ISO format
        
    Returns:
        Datetime object
    """
    if isinstance(datetime_str, str):
        return datetime.fromisoformat(datetime_str)
    return datetime_str


@pytest.fixture
def sample_election_data():
    """
    Provide sample election data for testing.
    
    Returns:
        Dictionary with sample election data
    """
    data = {
        "id": "e12345",
        "name": "Presidential Election 2024",
        "country": "United States",
        "start_date": parse_datetime("2024-11-05T00:00:00"),
        "end_date": parse_datetime("2024-11-05T23:59:59"),
        "status": "scheduled",
        "type": "presidential",
        "description": "2024 United States Presidential Election",
        "timezone": "America/New_York",
    }
    return data


@pytest.fixture
def sample_constituency_data():
    """
    Provide sample constituency data for testing.
    
    Returns:
        Dictionary with sample constituency data
    """
    return {
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
    }


@pytest.fixture
def sample_transaction_data():
    """
    Provide sample transaction data for testing.
    
    Returns:
        Dictionary with sample transaction data
    """
    return {
        "id": "t12345",
        "election_id": "e12345",
        "constituency_id": "c12345",
        "type": "vote_count",
        "status": "processed",
        "source": "polling_station",
        "data": {"votes": 100, "station_id": "ps123"},
        "timestamp": parse_datetime("2024-11-05T12:00:00"),
        "anomaly_detected": False,
        "anomaly_reason": None,
    }


@pytest.fixture
def sample_alert_data():
    """
    Provide sample alert data for testing.
    
    Returns:
        Dictionary with sample alert data
    """
    return {
        "id": "a12345",
        "election_id": "e12345",
        "constituency_id": "c12345",
        "type": "anomaly",
        "severity": "medium",
        "status": "active",
        "message": "Unusual voting pattern detected",
        "timestamp": parse_datetime("2024-11-05T14:30:00"),
        "data": {"votes_per_minute": 200, "expected": 50},
        "comments": ["Investigating", "Checking with polling station"],
        "resolution_notes": None,
        "resolved_at": None,
    }


@pytest.fixture
def sample_hourly_stats_data():
    """
    Provide sample hourly stats data for testing.
    
    Returns:
        Dictionary with sample hourly stats data
    """
    return {
        "id": "h12345",
        "election_id": "e12345",
        "constituency_id": "c12345",
        "hour": 12,
        "timestamp": parse_datetime("2024-11-05T12:00:00"),
        "transaction_count": 150,
        "votes_count": 5000,
        "bulletins_issued": 5500,
        "participation_rate": 0.22,
        "anomaly_count": 2,
    }


@pytest.fixture
def sample_file_processing_job_data():
    """
    Provide sample file processing job data for testing.
    
    Returns:
        Dictionary with sample file processing job data
    """
    return {
        "id": "f12345",
        "election_id": "e12345",
        "file_name": "results.csv",
        "file_type": "csv",
        "file_size": 1024,
        "status": "pending",
        "progress": 0.0,
        "progress_message": "Waiting to start",
        "error_message": None,
        "created_at": parse_datetime("2024-11-05T10:00:00"),
        "started_at": None,
        "completed_at": None,
        "result": None,
    }