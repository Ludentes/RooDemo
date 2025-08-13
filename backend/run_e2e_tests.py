#!/usr/bin/env python3
"""
End-to-End test runner for the Election Monitoring API.

This script starts the FastAPI application with a test database
and runs E2E tests against the running API.
"""

import os
import sys
import subprocess
import time
import uvicorn
import asyncio
import pytest
from multiprocessing import Process

def run_api_server():
    """Run the FastAPI application in a separate process."""
    # Set environment variable to use test database
    os.environ["TESTING"] = "1"
    
    # Import and run the FastAPI application
    from app.main import app
    
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def run_tests():
    """Run the E2E tests."""
    # Wait for the server to start
    time.sleep(2)
    
    # Run the tests
    result = pytest.main(["-xvs", "tests/e2e"])
    
    return result

async def setup_test_database():
    """Set up the test database with initial schema and test data."""
    from app.models.database import engine, Base
    from app.models.election import Election
    from app.models.constituency import Constituency
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime, timedelta
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Add test data
    async with async_session() as session:
        # Add test election
        test_election = Election(
            id="e2e_test_election",
            name="E2E Test Election",
            country="Test Country",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=1),
            status="active",
            type="presidential",
            description="Election for E2E testing",
            timezone="UTC"
        )
        session.add(test_election)
        
        # Add test constituency
        test_constituency = Constituency(
            id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
            election_id="e2e_test_election",
            name="E2E Test Constituency",
            region="Test Region",
            type="district",
            status="active",
            registered_voters=1000,
            bulletins_issued=0,
            votes_cast=0,
            participation_rate=0.0,
            anomaly_score=0.0
        )
        session.add(test_constituency)
        
        await session.commit()

def main():
    """Main function to run the E2E tests."""
    # Set up the test database
    asyncio.run(setup_test_database())
    
    # Start the API server in a separate process
    server_process = Process(target=run_api_server)
    server_process.start()
    
    try:
        # Run the tests
        result = run_tests()
        
        # Exit with the test result
        sys.exit(result)
    finally:
        # Clean up the server process
        server_process.terminate()
        server_process.join()

if __name__ == "__main__":
    main()