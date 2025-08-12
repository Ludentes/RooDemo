from fastapi import APIRouter, Depends
from app.services.dashboard import DashboardService
from app.api.dependencies import get_dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
async def get_dashboard_summary(
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get summary statistics for the dashboard.
    
    Returns:
        dict: Dashboard summary statistics including:
        - Active elections count
        - Total constituencies count
        - Active constituencies count
        - Recent transactions count
    """
    return await service.get_summary()