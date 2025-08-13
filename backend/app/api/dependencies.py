from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db
from app.services.health import HealthService
from app.services.constituency import ConstituencyService
from app.services.election import ElectionService
from app.services.dashboard import DashboardService
from app.services import (
    get_transaction_service,
    get_transaction_validator,
    get_transaction_batch_processor,
    get_transaction_query_service
)

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

async def get_transaction_service_instance(db: AsyncSession = Depends(get_db)):
    """Dependency for transaction service"""
    TransactionService = get_transaction_service()
    return TransactionService(db)

async def get_transaction_validator_instance():
    """Dependency for transaction validator"""
    TransactionValidator = get_transaction_validator()
    return TransactionValidator()

async def get_transaction_batch_processor_instance(db: AsyncSession = Depends(get_db)):
    """Dependency for transaction batch processor"""
    TransactionBatchProcessor = get_transaction_batch_processor()
    return TransactionBatchProcessor(db)

async def get_transaction_query_service_instance(db: AsyncSession = Depends(get_db)):
    """Dependency for transaction query service"""
    TransactionQueryService = get_transaction_query_service()
    return TransactionQueryService(db)