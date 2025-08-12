from fastapi import APIRouter, Depends
from app.services.health import HealthService
from app.api.dependencies import get_health_service

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", summary="Check API health")
async def health_check(health_service: HealthService = Depends(get_health_service)):
    """
    Check the health of the API and its dependencies.
    
    Returns:
        dict: Health status information including database connection status
    """
    return await health_service.check_health()