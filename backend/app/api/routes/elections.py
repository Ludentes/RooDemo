from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.services.election import ElectionService
from app.api.dependencies import get_election_service
from app.models.schemas.election import ElectionResponse, ElectionList
from app.api.errors.exceptions import NotFoundError

router = APIRouter(prefix="/elections", tags=["elections"])

@router.get("", response_model=ElectionList)
async def list_elections(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    service: ElectionService = Depends(get_election_service)
):
    """
    List elections with pagination and optional filtering.
    
    Parameters:
        page: Page number (1-indexed)
        page_size: Number of items per page
        status: Filter by election status
        
    Returns:
        ElectionList: Paginated list of elections with metadata
    """
    elections, total = await service.get_elections(
        page=page,
        page_size=page_size,
        status=status
    )
    
    return {
        "data": elections,
        "total": total,
        "page": page,
        "limit": page_size
    }

@router.get("/upcoming", response_model=ElectionList)
async def get_upcoming_elections(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: ElectionService = Depends(get_election_service)
):
    """
    List upcoming elections (scheduled or upcoming status).
    
    Parameters:
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        ElectionList: Paginated list of upcoming elections with metadata
    """
    elections, total = await service.get_upcoming_elections(
        page=page,
        page_size=page_size
    )
    
    return {
        "data": elections,
        "total": total,
        "page": page,
        "limit": page_size
    }

@router.get("/{election_id}", response_model=ElectionResponse)
async def get_election(
    election_id: int,
    service: ElectionService = Depends(get_election_service)
):
    """
    Get detailed information about a specific election.
    
    Parameters:
        election_id: The ID of the election
        
    Returns:
        ElectionResponse: Detailed election information
        
    Raises:
        404: Election not found
    """
    election = await service.get_election(election_id)
    if not election:
        raise NotFoundError(f"Election with ID {election_id} not found")
    return election