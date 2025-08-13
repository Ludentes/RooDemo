from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException
from datetime import datetime

from app.services.transaction_service import TransactionService
from app.services.transaction_batch_processor import TransactionBatchProcessor
from app.services.transaction_query_service import TransactionQueryService
from app.api.dependencies import (
    get_transaction_service_instance,
    get_transaction_batch_processor_instance,
    get_transaction_query_service_instance
)
from app.models.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionList,
    TransactionBatchRequest,
    TransactionBatchResponse,
    TransactionQueryParams,
    TransactionStats
)
from app.api.errors.exceptions import (
    NotFoundError,
    TransactionValidationError,
    TransactionCreateError,
    TransactionUpdateError,
    TransactionDeleteError,
    BatchProcessingError
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionList)
async def list_transactions(
    constituency_id: Optional[str] = Query(None, description="Filter by constituency ID"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
    start_time: Optional[datetime] = Query(None, description="Filter by start time"),
    end_time: Optional[datetime] = Query(None, description="Filter by end time"),
    status: Optional[str] = Query(None, description="Filter by status"),
    anomaly_detected: Optional[bool] = Query(None, description="Filter by anomaly detection"),
    source: Optional[str] = Query(None, description="Filter by source"),
    file_id: Optional[str] = Query(None, description="Filter by file ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    sort_by: str = Query("timestamp", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc, desc)"),
    service: TransactionService = Depends(get_transaction_service_instance)
):
    """
    List transactions with filtering and pagination.
    
    Parameters:
        constituency_id: Filter by constituency ID
        transaction_type: Filter by transaction type
        start_time: Filter by start time
        end_time: Filter by end time
        status: Filter by status
        anomaly_detected: Filter by anomaly detection
        source: Filter by source
        file_id: Filter by file ID
        page: Page number
        limit: Items per page
        sort_by: Field to sort by
        sort_order: Sort order (asc, desc)
        
    Returns:
        TransactionList: Paginated list of transactions with metadata
    """
    transactions, total = service.get_transactions(
        constituency_id=constituency_id,
        transaction_type=transaction_type,
        start_time=start_time,
        end_time=end_time,
        status=status,
        anomaly_detected=anomaly_detected,
        source=source,
        file_id=file_id,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return {
        "data": transactions,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/statistics", response_model=TransactionStats)
async def get_statistics(
    constituency_id: Optional[str] = Query(None, description="Filter by constituency ID"),
    query_service: TransactionQueryService = Depends(get_transaction_query_service_instance)
):
    """
    Get transaction statistics.
    
    Parameters:
        constituency_id: Optional constituency ID to filter by
        
    Returns:
        TransactionStats: Transaction statistics
    """
    stats = query_service.get_transaction_statistics(constituency_id)
    return stats


@router.get("/search", response_model=TransactionList)
async def search_transactions(
    q: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    query_service: TransactionQueryService = Depends(get_transaction_query_service_instance)
):
    """
    Search for transactions.
    
    Parameters:
        q: Search term
        page: Page number
        limit: Items per page
        
    Returns:
        TransactionList: Paginated list of matching transactions
    """
    transactions, total = query_service.search_transactions(q, page, limit)
    
    return {
        "data": transactions,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str = Path(..., description="The ID of the transaction"),
    service: TransactionService = Depends(get_transaction_service_instance)
):
    """
    Get detailed information about a specific transaction.
    
    Parameters:
        transaction_id: The ID of the transaction
        
    Returns:
        TransactionResponse: Detailed transaction information
        
    Raises:
        404: Transaction not found
    """
    transaction = service.get_transaction(transaction_id)
    if not transaction:
        raise NotFoundError(f"Transaction with ID {transaction_id} not found")
    return transaction


@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service_instance)
):
    """
    Create a new transaction.
    
    Parameters:
        transaction: Transaction data
        
    Returns:
        TransactionResponse: Created transaction
        
    Raises:
        400: Validation error
        500: Creation error
    """
    try:
        created_transaction = service.create_transaction(transaction)
        return created_transaction
    except TransactionValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TransactionCreateError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str = Path(..., description="The ID of the transaction"),
    transaction: TransactionUpdate = None,
    service: TransactionService = Depends(get_transaction_service_instance)
):
    """
    Update a transaction.
    
    Parameters:
        transaction_id: The ID of the transaction
        transaction: Transaction data to update
        
    Returns:
        TransactionResponse: Updated transaction
        
    Raises:
        404: Transaction not found
        500: Update error
    """
    try:
        updated_transaction = service.update_transaction(transaction_id, transaction)
        if not updated_transaction:
            raise NotFoundError(f"Transaction with ID {transaction_id} not found")
        return updated_transaction
    except TransactionUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: str = Path(..., description="The ID of the transaction"),
    service: TransactionService = Depends(get_transaction_service_instance)
):
    """
    Delete a transaction.
    
    Parameters:
        transaction_id: The ID of the transaction
        
    Raises:
        404: Transaction not found
        500: Deletion error
    """
    try:
        deleted = service.delete_transaction(transaction_id)
        if not deleted:
            raise NotFoundError(f"Transaction with ID {transaction_id} not found")
    except TransactionDeleteError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=TransactionBatchResponse)
async def process_batch(
    batch_request: TransactionBatchRequest,
    processor: TransactionBatchProcessor = Depends(get_transaction_batch_processor_instance)
):
    """
    Process a batch of transactions.
    
    Parameters:
        batch_request: Batch request containing transactions
        
    Returns:
        TransactionBatchResponse: Batch processing results
        
    Raises:
        500: Batch processing error
    """
    try:
        response = processor.process_batch_request(batch_request)
        return response
    except BatchProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))

