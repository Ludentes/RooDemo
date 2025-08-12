from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db
from app.services.health import HealthService
from app.services.constituency import ConstituencyService
from app.services.election import ElectionService
from app.services.dashboard import DashboardService

async def get_health_service() -> HealthService:
    """Dependency for health service"""
    return HealthService()

async def get_constituency_service(db: AsyncSession = Depends(get_db)) -> ConstituencyService:
    """Dependency for constituency service"""
    return ConstituencyService(db)

async def get_election_service(db: AsyncSession = Depends(get_db)) -> ElectionService:
    """Dependency for election service"""
    return ElectionService(db)

async def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    """Dependency for dashboard service"""
    return DashboardService(db)