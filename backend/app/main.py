from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from fastapi.openapi.utils import get_openapi
from app.api import api_router, setup_routes
from app.api.errors.handlers import register_exception_handlers
from app.models.database import create_tables
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""    
    current_dir = os.getcwd()
    db_path = os.path.join(current_dir, "election_monitoring.db")
    logger.info(f"Current working directory: {current_dir}")
    logger.info(f"Database path: {db_path}")
    logger.info(f"Database exists before table creation: {os.path.exists(db_path)}")

    # Create tables
    try:
        create_tables()
        logger.info("Database tables created successfully")
        logger.info(f"Database exists after table creation: {os.path.exists(db_path)}")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    yield

app = FastAPI(
    title="Election Monitoring API",
    description="API for the Election Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

def custom_openapi():
    """
    Customize the OpenAPI schema with additional information.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Election Monitoring API",
        version="1.0.0",
        description="""
        # Election Monitoring System API
        
        This API provides endpoints for monitoring election data and detecting anomalies.
        
        ## Key Features
        
        * **Health Check**: Verify API and database availability
        * **Constituencies**: Access constituency data with filtering and pagination
        * **Elections**: Retrieve election information and upcoming elections
        * **Dashboard**: Get summary statistics for monitoring
        * **Files**: Process transaction files and update metrics
        * **Transactions**: Manage blockchain transactions with filtering, batch processing, and statistics
        * **Metrics**: Access detailed metrics for constituencies, elections, and dashboard
        
        ## Authentication
        
        Authentication will be added in a future update.
        """,
        routes=app.routes,
    )
    
    # Add contact information
    openapi_schema["info"]["contact"] = {
        "name": "Election Monitoring Team",
        "email": "support@electionmonitoring.example",
        "url": "https://electionmonitoring.example",
    }
    
    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "health",
            "description": "Health check endpoints to verify API availability",
        },
        {
            "name": "constituencies",
            "description": "Operations related to constituencies",
        },
        {
            "name": "elections",
            "description": "Operations related to elections",
        },
        {
            "name": "dashboard",
            "description": "Dashboard summary statistics",
        },
        {
            "name": "files",
            "description": "File processing operations for transaction data",
        },
        {
            "name": "transactions",
            "description": "Operations related to blockchain transactions",
        },
        {
            "name": "metrics",
            "description": "Metrics calculation and retrieval operations",
        },
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup API routes
setup_routes()

# Register API routes
app.include_router(api_router)

# Register exception handlers
register_exception_handlers(app)

# Create database tables on startup
# @app.on_event("startup")
# def startup_event():
#     """Create database tables on startup."""
#     # Log current directory and database file
#     current_dir = os.getcwd()
#     db_path = os.path.join(current_dir, "election_monitoring.db")
#     logger.info(f"Current working directory: {current_dir}")
#     logger.info(f"Database path: {db_path}")
#     logger.info(f"Database exists before table creation: {os.path.exists(db_path)}")
    
#     # Create tables
#     try:
#         create_tables()
#         logger.info("Database tables created successfully")
#         logger.info(f"Database exists after table creation: {os.path.exists(db_path)}")
#     except Exception as e:
#         logger.error(f"Error creating database tables: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())


    # Clean up the ML models and release the resources
    

@app.get("/")
async def root():
    """Root endpoint that redirects to API documentation."""
    return {
        "message": "Welcome to the Election Monitoring API",
        "documentation": "/docs"
    }