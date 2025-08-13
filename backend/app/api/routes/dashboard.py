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
        - Transaction statistics
    """
    return await service.get_summary()

@router.get("/detailed-summary")
async def get_detailed_dashboard_summary(
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get detailed summary statistics for the dashboard.
    
    Returns:
        dict: Detailed dashboard summary statistics including:
        - Basic summary
        - Transaction statistics by type
        - Transaction statistics by status
        - Transaction statistics by source
        - Transaction rates
        - Anomaly statistics
        - Constituency-specific transaction statistics
    """
    return await service.get_detailed_summary()

@router.get("/transaction-stats")
async def get_transaction_statistics(
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get transaction statistics for the dashboard.
    
    Returns:
        dict: Transaction statistics including:
        - Total transactions
        - Transactions by type
        - Transactions by status
        - Transactions by source
        - Transaction rates
        - Anomaly statistics
    """
    summary = await service.get_summary()
    return summary["transaction_stats"]