from fastapi import APIRouter

# Import route modules
from app.api.routes import health, constituencies, elections, dashboard

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all route modules
api_router.include_router(health.router)
api_router.include_router(constituencies.router)
api_router.include_router(elections.router)
api_router.include_router(dashboard.router)