from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.models.constituency import Constituency
from app.crud.constituency import ConstituencyCRUD
from app.api.errors.exceptions import NotFoundError

class ConstituencyService(BaseService[Constituency, ConstituencyCRUD]):
    """
    Service for constituency-related operations.
    
    Extends the BaseService with constituency-specific functionality.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the constituency service.
        
        Args:
            db: The database session
        """
        super().__init__(ConstituencyCRUD(Constituency), db)
    
    async def get_constituencies(
        self,
        page: int = 1,
        page_size: int = 10,
        election_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get constituencies with pagination and filtering.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            election_id: Filter by election ID
            status: Filter by constituency status
            
        Returns:
            Tuple of (constituencies list, total count)
        """
        filters = {}
        if election_id is not None:
            filters["election_id"] = election_id
        if status is not None:
            filters["status"] = status
            
        # Calculate skip value for pagination
        skip = (page - 1) * page_size
        
        # Get constituencies with pagination and filtering
        constituencies = self.crud.get_multi(
            db=self.db,
            skip=skip,
            limit=page_size,
            **filters
        )
        
        # Get total count
        total = self.crud.count(db=self.db)
        
        # Convert SQLAlchemy models to dictionaries
        constituency_dicts = []
        for constituency in constituencies:
            constituency_dict = {
                "id": constituency.id,
                "name": constituency.name,
                "election_id": constituency.election_id,
                "election_name": constituency.election.name if constituency.election else None,
                "region": constituency.region,
                "type": constituency.type,
                "registered_voters": constituency.registered_voters,
                "status": constituency.status,
                "last_update_time": constituency.last_update_time,
                "bulletins_issued": constituency.bulletins_issued,
                "votes_cast": constituency.votes_cast,
                "participation_rate": constituency.participation_rate,
                "anomaly_score": constituency.anomaly_score,
                "created_at": constituency.created_at,
                "updated_at": constituency.updated_at
            }
            constituency_dicts.append(constituency_dict)
            
        return constituency_dicts, total
    
    async def get_constituency(self, constituency_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific constituency.
        
        Args:
            constituency_id: The ID of the constituency
            
        Returns:
            Constituency data with statistics or None if not found
        """
        constituency = self.crud.get(db=self.db, id=constituency_id)
        if not constituency:
            return None
            
        # Get statistics for the constituency
        # In a real implementation, this would fetch actual statistics
        # For now, we'll return placeholder data
        statistics = {
            "participation_rate": 0.65,
            "bulletins_issued": 6500,
            "votes_cast": 6450,
            "invalid_votes": 50
        }
        
        # Convert SQLAlchemy model to dictionary with additional data
        constituency_dict = {
            "id": constituency.id,
            "name": constituency.name,
            "election_id": constituency.election_id,
            "election_name": constituency.election.name if constituency.election else None,
            "region": constituency.region,
            "type": constituency.type,
            "registered_voters": constituency.registered_voters,
            "status": constituency.status,
            "last_update_time": constituency.last_update_time,
            "bulletins_issued": constituency.bulletins_issued,
            "votes_cast": constituency.votes_cast,
            "participation_rate": constituency.participation_rate,
            "anomaly_score": constituency.anomaly_score,
            "statistics": statistics,
            "created_at": constituency.created_at,
            "updated_at": constituency.updated_at
        }
        
        return constituency_dict