from fastapi import APIRouter

# Create main API router
api_router = APIRouter(prefix="/api")

# Define setup_routes function but don't call it immediately
def setup_routes():
    # Import route modules
    from app.api.routes import health, constituencies, elections, dashboard, files, transactions, metrics
    
    # Include all route modules
    api_router.include_router(health.router)
    api_router.include_router(constituencies.router)
    api_router.include_router(elections.router)
    api_router.include_router(dashboard.router)
    api_router.include_router(files.router, prefix="/files", tags=["files"])
    api_router.include_router(transactions.router)
    api_router.include_router(metrics.router)

# Don't setup routes immediately to avoid circular imports
# Routes will be set up when the application starts in main.py