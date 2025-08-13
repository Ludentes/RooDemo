"""
Recreate database script for the Election Monitoring System.

This script recreates the database schema using SQLAlchemy's create_all() method.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.database import SessionLocal, engine, Base, db_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database(delete_file=False):
    """
    Recreate the database schema.
    
    Args:
        delete_file: If True, delete the database file completely before recreating
    """
    logger.info("Starting database recreation...")
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        
        # Optionally delete the database file
        if delete_file and os.path.exists(db_path):
            os.remove(db_path)
            logger.info(f"Database file deleted: {db_path}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        
        logger.info("Database recreation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error recreating database: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Recreate the Election Monitoring database")
    parser.add_argument("--delete-file", action="store_true", help="Delete the database file completely")
    args = parser.parse_args()
    
    recreate_database(delete_file=args.delete_file)