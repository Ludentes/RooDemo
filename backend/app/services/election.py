from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.models.election import Election
from app.crud.election import ElectionCRUD
from app.api.errors.exceptions import NotFoundError

class ElectionService(BaseService[Election, ElectionCRUD]):
    """
    Service for election-related operations.
    
    Extends the BaseService with election-specific functionality.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the election service.
        
        Args:
            db: The database session
        """
        super().__init__(ElectionCRUD(Election), db)
    
    async def get_elections(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get elections with pagination and filtering.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            status: Filter by election status
            
        Returns:
            Tuple of (elections list, total count)
        """
        filters = {}
        if status is not None:
            filters["status"] = status
            
        elections, total = await self.get_multi(
            page=page,
            page_size=page_size,
            **filters
        )
        
        # Convert SQLAlchemy models to dictionaries
        election_dicts = []
        for election in elections:
            election_dict = {
                "id": election.id,
                "name": election.name,
                "country": election.country,
                "description": election.description,
                "status": election.status,
                "type": election.type,
                "timezone": election.timezone,
                "start_date": election.start_date,
                "end_date": election.end_date,
                "constituency_count": len(election.constituencies) if election.constituencies else 0,
                "created_at": election.created_at,
                "updated_at": election.updated_at
            }
            election_dicts.append(election_dict)
            
        return election_dicts, total
    
    async def get_election(self, election_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific election.
        
        Args:
            election_id: The ID of the election
            
        Returns:
            Election data with statistics or None if not found
        """
        election = await self.get(election_id)
        if not election:
            return None
            
        # Get statistics for the election
        # In a real implementation, this would fetch actual statistics
        # For now, we'll return placeholder data
        statistics = {
            "participation_rate": 0.68,
            "bulletins_issued": 340000,
            "votes_cast": 338000,
            "invalid_votes": 2000
        }
        
        # Get constituencies for the election
        constituencies = []
        if election.constituencies:
            for constituency in election.constituencies:
                constituency_dict = {
                    "id": constituency.id,
                    "name": constituency.name,
                    "code": constituency.code,
                    "registered_voters": constituency.registered_voters,
                    "status": constituency.status
                }
                constituencies.append(constituency_dict)
        
        # Convert SQLAlchemy model to dictionary with additional data
        election_dict = {
            "id": election.id,
            "name": election.name,
            "country": election.country,
            "description": election.description,
            "status": election.status,
            "type": election.type,
            "timezone": election.timezone,
            "start_date": election.start_date,
            "end_date": election.end_date,
            "registered_voters": sum(c.registered_voters for c in election.constituencies) if election.constituencies else 0,
            "constituencies": constituencies,
            "statistics": statistics,
            "created_at": election.created_at,
            "updated_at": election.updated_at
        }
        
        return election_dict
    
    async def get_upcoming_elections(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get upcoming elections (scheduled or upcoming status).
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (upcoming elections list, total count)
        """
        # Calculate skip value for pagination
        skip = (page - 1) * page_size
        
        # Get upcoming elections with pagination
        elections = self.crud.get_upcoming_elections(
            db=self.db,
            skip=skip,
            limit=page_size
        )
        
        # Get total count of upcoming elections
        total = self.crud.count_upcoming_elections(db=self.db)
        
        # Convert SQLAlchemy models to dictionaries
        election_dicts = []
        for election in elections:
            election_dict = {
                "id": election.id,
                "name": election.name,
                "country": election.country,
                "description": election.description,
                "status": election.status,
                "type": election.type,
                "timezone": election.timezone,
                "start_date": election.start_date,
                "end_date": election.end_date,
                "constituency_count": len(election.constituencies) if election.constituencies else 0,
                "created_at": election.created_at,
                "updated_at": election.updated_at
            }
            election_dicts.append(election_dict)
            
        return election_dicts, total