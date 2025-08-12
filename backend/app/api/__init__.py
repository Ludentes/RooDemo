from fastapi import APIRouter

# Create main API router
api_router = APIRouter(prefix="/api")

# Use lazy imports to avoid circular dependencies
def setup_routes():
    # Import route modules
    from app.api.routes import health, constituencies, elections, dashboard, files
    
    # Include all route modules
    api_router.include_router(health.router)
    api_router.include_router(constituencies.router)
    api_router.include_router(elections.router)
    api_router.include_router(dashboard.router)
    api_router.include_router(files.router, prefix="/files", tags=["files"])

# Setup routes when this module is imported
setup_routes()