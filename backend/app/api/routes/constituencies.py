from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.services.constituency import ConstituencyService
from app.api.dependencies import get_constituency_service
from app.models.schemas.constituency import ConstituencyResponse, ConstituencyList
from app.api.errors.exceptions import NotFoundError

router = APIRouter(prefix="/constituencies", tags=["constituencies"])

@router.get("", response_model=ConstituencyList)
async def list_constituencies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    election_id: Optional[int] = None,
    status: Optional[str] = None,
    service: ConstituencyService = Depends(get_constituency_service)
):
    """
    List constituencies with pagination and optional filtering.
    
    Parameters:
        page: Page number (1-indexed)
        page_size: Number of items per page
        election_id: Filter by election ID
        status: Filter by constituency status
        
    Returns:
        ConstituencyList: Paginated list of constituencies with metadata
    """
    constituencies, total = await service.get_constituencies(
        page=page,
        page_size=page_size,
        election_id=election_id,
        status=status
    )
    
    return {
        "data": constituencies,
        "total": total,
        "page": page,
        "limit": page_size
    }

@router.get("/{constituency_id}", response_model=ConstituencyResponse)
async def get_constituency(
    constituency_id: int,
    service: ConstituencyService = Depends(get_constituency_service)
):
    """
    Get detailed information about a specific constituency.
    
    Parameters:
        constituency_id: The ID of the constituency
        
    Returns:
        ConstituencyResponse: Detailed constituency information
        
    Raises:
        404: Constituency not found
    """
    constituency = await service.get_constituency(constituency_id)
    if not constituency:
        raise NotFoundError(f"Constituency with ID {constituency_id} not found")
    return constituency