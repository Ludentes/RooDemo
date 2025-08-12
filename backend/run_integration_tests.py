#!/usr/bin/env python3
"""
Integration test runner for the Election Monitoring API.

This script starts the FastAPI application with a test database
and runs integration tests against the running API.
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
    """Run the integration tests."""
    # Wait for the server to start
    time.sleep(2)
    
    # Run the tests
    result = pytest.main(["-xvs", "tests/api"])
    
    return result

async def setup_test_database():
    """Set up the test database with initial schema."""
    from app.models.database import engine, Base
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def main():
    """Main function to run the integration tests."""
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