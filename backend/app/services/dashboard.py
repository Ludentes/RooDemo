from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.election import ElectionCRUD
from app.crud.constituency import ConstituencyCRUD
from app.crud.transaction import TransactionCRUD
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction
from app.services.transaction_query_service import TransactionQueryService

class DashboardService:
    """
    Service for dashboard-related operations.
    
    Provides methods to get summary statistics for the dashboard.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the dashboard service.
        
        Args:
            db: The database session
        """
        self.db = db
        self.election_crud = ElectionCRUD(Election)
        self.constituency_crud = ConstituencyCRUD(Constituency)
        self.transaction_crud = TransactionCRUD(Transaction)
        self.transaction_query_service = TransactionQueryService(db)
    
    async def get_summary(self):
        """
        Get essential summary statistics for the dashboard.
        
        Returns:
            Dict with core summary statistics:
            - Active elections count
            - Total constituencies count
            - Active constituencies count
            - Recent transactions count
            - Transaction statistics
        """
        # Get essential counts from core entities
        active_elections = self.election_crud.count(db=self.db, status="active")
        total_constituencies = self.constituency_crud.count(db=self.db)
        active_constituencies = self.constituency_crud.count(db=self.db, status="active")
        recent_transactions = self.transaction_crud.count_recent(db=self.db, hours=24)
        
        # Get transaction statistics
        transaction_stats = self.transaction_query_service.get_transaction_statistics()
        
        # Return enhanced dashboard data
        return {
            "active_elections": active_elections,
            "total_constituencies": total_constituencies,
            "active_constituencies": active_constituencies,
            "recent_transactions": recent_transactions,
            "transaction_stats": transaction_stats
        }
    
    async def get_detailed_summary(self):
        """
        Get detailed summary statistics for the dashboard.
        
        Returns:
            Dict with detailed summary statistics including:
            - Basic summary
            - Transaction statistics by type
            - Transaction statistics by status
            - Transaction statistics by source
            - Transaction rates
            - Anomaly statistics
        """
        # Get basic summary
        basic_summary = await self.get_summary()
        
        # Get detailed transaction statistics
        transaction_stats = self.transaction_query_service.get_transaction_statistics()
        
        # Get transaction counts by constituency
        constituencies = await self.constituency_crud.get_all(db=self.db)
        constituency_stats = {}
        
        for constituency in constituencies:
            constituency_id = constituency.id
            constituency_stats[constituency_id] = {
                "name": constituency.name,
                "stats": self.transaction_query_service.get_transaction_statistics(constituency_id)
            }
        
        # Return detailed dashboard data
        return {
            "summary": basic_summary,
            "transaction_stats": transaction_stats,
            "constituency_stats": constituency_stats
        }