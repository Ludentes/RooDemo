import time
import traceback
import os
import logging
from sqlalchemy import text
from app.models.database import engine, SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthService:
    """
    Service for checking the health of the API and its dependencies.
    """
    
    async def check_health(self):
        """
        Check the health of the system.
        
        Performs a basic database connection test and measures response time.
        
        Returns:
            Dict with basic health status information including:
            - API status
            - Database connection status
            - Response time
        """
        start_time = time.time()
        db_status = "ok"
        error_details = None
        
        try:
            # Log current directory and database file existence
            current_dir = os.getcwd()
            db_path = os.path.join(current_dir, "election_monitoring.db")
            db_exists = os.path.exists(db_path)
            logger.info(f"Current directory: {current_dir}")
            logger.info(f"Database path: {db_path}")
            logger.info(f"Database exists: {db_exists}")
            
            # Test database connection using synchronous API
            logger.info("Attempting database connection...")
            with SessionLocal() as session:
                # Use text() function to create a text SQL expression
                result = session.execute(text("SELECT 1")).fetchone()
                logger.info(f"Database query result: {result}")
                session.commit()
                logger.info("Database connection successful")
        except Exception as e:
            db_status = "error"
            error_details = str(e)
            logger.error(f"Database connection error: {error_details}")
            logger.error(traceback.format_exc())
            
        response = {
            "status": "healthy" if db_status == "ok" else "unhealthy",
            "database_connection": db_status,
            "response_time": f"{(time.time() - start_time) * 1000:.2f}ms"
        }
        
        # Add error details if there was an error
        if error_details:
            response["error_details"] = error_details
            
        return response