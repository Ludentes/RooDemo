"""
Database configuration and base models for the Election Monitoring System.

This module provides the SQLAlchemy Base class, database connection,
session management, and common model mixins.
"""

import os
import logging
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from typing import Generator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the backend directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
db_path = os.path.join(backend_dir, "election_monitoring.db")
logger.info(f"Using database path: {db_path}")

# Database URL with absolute path
DATABASE_URL = f"sqlite:///{db_path}"
logger.info(f"Database URL: {DATABASE_URL}")

# Create engine with SQLite-specific arguments
# In production, this would be replaced with PostgreSQL connection
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite-specific
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for all models
Base = declarative_base()

# Common mixins for models
class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class UUIDMixin:
    """Mixin to add UUID primary key to models."""
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))


# Database dependency for FastAPI
def get_db() -> Generator:
    """
    Get a database session.
    
    Yields:
        Session: A SQLAlchemy session
        
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create all tables
def create_tables() -> None:
    """
    Create all tables in the database.
    
    This function should be called when the application starts.
    """
    try:
        # Ensure the directory exists
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            logger.info(f"Creating database directory: {db_dir}")
            os.makedirs(db_dir, exist_ok=True)
        
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Verify database file exists
        if os.path.exists(db_path):
            logger.info(f"Database file created at: {db_path}")
        else:
            logger.warning(f"Database file not found at: {db_path}")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise