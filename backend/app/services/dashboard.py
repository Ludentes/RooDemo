from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.election import ElectionCRUD
from app.crud.constituency import ConstituencyCRUD
from app.crud.transaction import TransactionCRUD
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction

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
    
    async def get_summary(self):
        """
        Get essential summary statistics for the dashboard.
        
        Returns:
            Dict with core summary statistics:
            - Active elections count
            - Total constituencies count
            - Active constituencies count
            - Recent transactions count
        """
        # Get essential counts from core entities
        active_elections = self.election_crud.count(db=self.db, status="active")
        total_constituencies = self.constituency_crud.count(db=self.db)
        active_constituencies = self.constituency_crud.count(db=self.db, status="active")
        recent_transactions = self.transaction_crud.count_recent(db=self.db, hours=24)
        
        # Return simplified dashboard data
        return {
            "active_elections": active_elections,
            "total_constituencies": total_constituencies,
            "active_constituencies": active_constituencies,
            "recent_transactions": recent_transactions
        }