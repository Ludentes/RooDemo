"""
Clear script for the Election Monitoring System.

This script removes all data from the database and optionally deletes the database file.
"""

import os
import sys
import logging
import argparse

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.database import SessionLocal, engine, Base, db_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_database(delete_file=False):
    """
    Clear all data from the database.
    
    Args:
        delete_file: If True, delete the database file completely
    """
    logger.info("Starting database clearing...")
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        
        # Optionally delete the database file
        if delete_file and os.path.exists(db_path):
            os.remove(db_path)
            logger.info(f"Database file deleted: {db_path}")
        
        logger.info("Database clearing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clear the Election Monitoring database")
    parser.add_argument("--delete-file", action="store_true", help="Delete the database file completely")
    args = parser.parse_args()
    
    clear_database(delete_file=args.delete_file)