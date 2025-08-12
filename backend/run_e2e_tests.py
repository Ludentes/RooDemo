#!/usr/bin/env python3
"""
End-to-end test runner for the File Processing System.

This script runs the end-to-end tests for the File Processing System, which test
the complete flow from file upload API to database storage and metrics updates.

Usage:
    python run_e2e_tests.py
"""

import os
import sys
import subprocess
import time
import uvicorn
import asyncio
import pytest
from multiprocessing import Process

# Set environment variable to use test database
os.environ["TESTING"] = "1"

# Set the database URL environment variable
test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path}"

def run_api_server():
    """Run the FastAPI application in a separate process."""
    # Import and run the FastAPI application
    from app.main import app
    
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def run_tests():
    """Run the end-to-end tests."""
    # Wait for the server to start
    time.sleep(2)
    
    # Run the tests with the integration mark
    result = pytest.main(["-xvs", "tests/api/test_files.py", "-m", "integration"])
    
    return result

def setup_test_database():
    """Set up the test database with initial schema."""
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.models.database import Base
    
    # Get the test database path from the environment variable
    test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
    
    # Remove the test database if it exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        
    print(f"Using database path: {test_db_path}")
    
    # Create the test database
    test_engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}
    )
    
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Override the get_db dependency
    from app.api.dependencies import get_db
    
    # Create a new get_db function that uses the test database
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Replace the get_db dependency with our test version
    import app.api.dependencies
    app.api.dependencies.get_db = override_get_db

def create_test_data():
    """Create test data in the database."""
    print("Creating test data...")
    
    # Import necessary modules
    from app.models.election import Election
    from app.models.constituency import Constituency
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os
    from datetime import datetime, timedelta
    
    # Get the path to the test database
    test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
    
    # Create a database engine
    engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}
    )
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create a test election
        election = Election(
            id="e12345",
            name="Test Election",
            country="Test Country",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=1),
            status="active",
            type="test",
            description="Test Election Description",
            timezone="UTC"
        )
        session.add(election)
        session.commit()
        
        # Create a test constituency
        constituency = Constituency(
            id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
            election_id="e12345",
            name="Test Constituency",
            region="Test Region",
            type="test",
            status="active",
            registered_voters=1000,
            bulletins_issued=0,
            votes_cast=0,
            participation_rate=0.0,
            anomaly_score=0.0
        )
        session.add(constituency)
        session.commit()
        
        print("Test data created successfully")
    except Exception as e:
        print(f"Error creating test data: {e}")
        session.rollback()
    finally:
        session.close()

def verify_test_data():
    """Verify that the test data was created successfully."""
    print("Verifying test data...")
    
    # Import necessary modules
    from app.models.election import Election
    from app.models.constituency import Constituency
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os
    
    # Get the path to the test database
    test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
    
    # Create a database engine
    engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}
    )
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if the election exists
        election = session.query(Election).filter_by(id="e12345").first()
        if not election:
            print("ERROR: Test election not found in database!")
            sys.exit(1)
        
        # Check if the constituency exists
        constituency = session.query(Constituency).filter_by(
            id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
        ).first()
        if not constituency:
            print("ERROR: Test constituency not found in database!")
            sys.exit(1)
        
        print("Test data verified successfully")
    except Exception as e:
        print(f"Error verifying test data: {e}")
        sys.exit(1)
    finally:
        session.close()

def main():
    """Main function to run the end-to-end tests."""
    print("Setting up test database...")
    # Set up the test database
    setup_test_database()
    
    # Create test data
    create_test_data()
    
    # Verify that the test data was created successfully
    verify_test_data()
    
    print("Starting API server...")
    # Start the API server in a separate process
    server_process = Process(target=run_api_server)
    server_process.start()
    
    try:
        print("Running end-to-end tests...")
        # Run the tests
        result = run_tests()
        
        # Exit with the test result
        sys.exit(result)
    finally:
        print("Cleaning up...")
        # Clean up the server process
        server_process.terminate()
        
        # Comment out the database removal to keep it for inspection
        # test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
        # if os.path.exists(test_db_path):
        #     os.remove(test_db_path)
        print("Database file kept at: /home/newub/w/electmoni/backend/test.db")
        server_process.join()

if __name__ == "__main__":
    main()