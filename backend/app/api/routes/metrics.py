"""
Metrics API routes for the Election Monitoring System.

This module provides API endpoints for accessing metrics data.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas.hourly_stats import HourlyStatsResponse, HourlyStatsList, ActivityTimeline
from app.services.hourly_stats_service import HourlyStatsService, get_hourly_stats_service
from app.services.constituency_metrics_service import ConstituencyMetricsService, get_constituency_metrics_service
from app.services.metrics_cache_service import MetricsCacheService, get_metrics_cache_service, cached

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)


# Dependency to get the metrics cache service
def get_cache() -> MetricsCacheService:
    """Get the metrics cache service."""
    cache = get_metrics_cache_service()
    return cache


@router.get("/hourly-stats/constituency/{constituency_id}")
async def get_hourly_stats_by_constituency(
    constituency_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get hourly stats for a constituency.
    
    Args:
        constituency_id: ID of the constituency
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        List of hourly stats
    """
    try:
        # Generate cache key
        cache_key = cache.get_hourly_stats_key(
            constituency_id=constituency_id,
            hour=start_time or datetime.utcnow()
        )
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        hourly_stats_service = get_hourly_stats_service(db)
        hourly_stats = hourly_stats_service.get_hourly_stats(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Convert to response model
        result = {
            "data": hourly_stats,
            "total": len(hourly_stats),
            "page": 1,
            "limit": len(hourly_stats)
        }
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=result,
            ttl=3600,  # 1 hour
            tags=[
                f"constituency:{constituency_id}",
                "hourly_stats"
            ]
        )
        
        return result
    
    except Exception as e:
        logger.exception(f"Error getting hourly stats for constituency {constituency_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting hourly stats: {str(e)}"
        )


@router.get("/hourly-stats/election/{election_id}")
async def get_hourly_stats_by_election(
    election_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get hourly stats for an election.
    
    Args:
        election_id: ID of the election
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        Dictionary mapping constituency IDs to lists of hourly stats
    """
    try:
        # Generate cache key
        cache_key = cache.get_election_metrics_key(
            election_id=election_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        hourly_stats_service = get_hourly_stats_service(db)
        hourly_stats = hourly_stats_service.get_hourly_stats_for_election(
            election_id=election_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=hourly_stats,
            ttl=3600,  # 1 hour
            tags=[
                f"election:{election_id}",
                "hourly_stats"
            ]
        )
        
        return hourly_stats
    
    except Exception as e:
        logger.exception(f"Error getting hourly stats for election {election_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting hourly stats: {str(e)}"
        )


@router.get("/constituency/{constituency_id}")
async def get_constituency_metrics(
    constituency_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get metrics for a constituency.
    
    Args:
        constituency_id: ID of the constituency
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        Dictionary of metrics
    """
    try:
        # Generate cache key
        cache_key = cache.get_constituency_metrics_key(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        constituency_metrics_service = get_constituency_metrics_service(db)
        metrics = constituency_metrics_service.calculate_metrics(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time,
            update_constituency=False
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=3600,  # 1 hour
            tags=[
                f"constituency:{constituency_id}",
                "constituency_metrics"
            ]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception(f"Error getting metrics for constituency {constituency_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/constituency/{constituency_id}/time-period")
async def get_constituency_metrics_by_time_period(
    constituency_id: str,
    period: str = "day",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get metrics for a constituency by time period.
    
    Args:
        constituency_id: ID of the constituency
        period: Time period to group by (hour, day, week, month)
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        Dictionary mapping time periods to metrics
    """
    try:
        # Generate cache key
        cache_key = f"constituency_metrics_by_period:{constituency_id}:{period}:{start_time}:{end_time}"
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        constituency_metrics_service = get_constituency_metrics_service(db)
        metrics = constituency_metrics_service.calculate_metrics_by_time_period(
            constituency_id=constituency_id,
            period=period,
            start_time=start_time,
            end_time=end_time
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=3600,  # 1 hour
            tags=[
                f"constituency:{constituency_id}",
                "constituency_metrics"
            ]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception(f"Error getting metrics for constituency {constituency_id} by time period")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/election/{election_id}")
async def get_election_metrics(
    election_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get metrics for an election.
    
    Args:
        election_id: ID of the election
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        Dictionary mapping constituency IDs to metrics
    """
    try:
        # Generate cache key
        cache_key = cache.get_election_metrics_key(
            election_id=election_id,
            start_time=start_time,
            end_time=end_time
        )
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        constituency_metrics_service = get_constituency_metrics_service(db)
        metrics = constituency_metrics_service.calculate_metrics_for_election(
            election_id=election_id,
            start_time=start_time,
            end_time=end_time,
            update_constituencies=False
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=3600,  # 1 hour
            tags=[
                f"election:{election_id}",
                "election_metrics"
            ]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception(f"Error getting metrics for election {election_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/election/{election_id}/constituencies")
async def get_election_constituency_metrics(
    election_id: str,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get metrics for all constituencies in an election.
    
    Args:
        election_id: ID of the election
        
    Returns:
        Dictionary mapping constituency IDs to metrics
    """
    try:
        # Generate cache key
        cache_key = f"election_constituency_metrics:{election_id}"
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        constituency_metrics_service = get_constituency_metrics_service(db)
        metrics = constituency_metrics_service.calculate_metrics_for_election(
            election_id=election_id,
            update_constituencies=False
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=3600,  # 1 hour
            tags=[
                f"election:{election_id}",
                "election_metrics"
            ]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception(f"Error getting constituency metrics for election {election_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/dashboard/summary")
async def get_dashboard_metrics_summary(
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get summary metrics for the dashboard.
    
    Returns:
        Dictionary of summary metrics
    """
    try:
        # Generate cache key
        cache_key = cache.get_dashboard_metrics_key(detailed=False)
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        from app.services.dashboard import DashboardService, get_dashboard_service
        dashboard_service = get_dashboard_service(db)
        metrics = dashboard_service.get_summary()
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=300,  # 5 minutes
            tags=["dashboard"]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception("Error getting dashboard summary metrics")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/dashboard/detailed")
async def get_dashboard_metrics_detailed(
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Get detailed metrics for the dashboard.
    
    Returns:
        Dictionary of detailed metrics
    """
    try:
        # Generate cache key
        cache_key = cache.get_dashboard_metrics_key(detailed=True)
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        from app.services.dashboard import DashboardService, get_dashboard_service
        dashboard_service = get_dashboard_service(db)
        metrics = dashboard_service.get_detailed_summary()
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=300,  # 5 minutes
            tags=["dashboard"]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception("Error getting detailed dashboard metrics")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metrics: {str(e)}"
        )


@router.get("/compare-constituencies")
async def compare_constituencies(
    constituency_ids: List[str] = Query(...),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Compare metrics for multiple constituencies.
    
    Args:
        constituency_ids: List of constituency IDs
        start_time: Optional start time of the range
        end_time: Optional end time of the range
        
    Returns:
        Dictionary mapping constituency IDs to metrics
    """
    try:
        # Generate cache key
        cache_key = f"compare_constituencies:{','.join(constituency_ids)}:{start_time}:{end_time}"
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Get from database
        constituency_metrics_service = get_constituency_metrics_service(db)
        metrics = constituency_metrics_service.compare_constituencies(
            constituency_ids=constituency_ids,
            start_time=start_time,
            end_time=end_time
        )
        
        # Cache the result
        cache.set(
            key=cache_key,
            value=metrics,
            ttl=3600,  # 1 hour
            tags=["constituency_metrics"]
        )
        
        return metrics
    
    except Exception as e:
        logger.exception(f"Error comparing constituencies {constituency_ids}")
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing constituencies: {str(e)}"
        )


@router.post("/invalidate-cache/constituency/{constituency_id}")
async def invalidate_constituency_cache(
    constituency_id: str,
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Invalidate all cache entries for a constituency.
    
    Args:
        constituency_id: ID of the constituency
        
    Returns:
        Number of entries invalidated
    """
    try:
        count = cache.invalidate_constituency_cache(constituency_id)
        return {"invalidated": count}
    
    except Exception as e:
        logger.exception(f"Error invalidating cache for constituency {constituency_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error invalidating cache: {str(e)}"
        )


@router.post("/invalidate-cache/election/{election_id}")
async def invalidate_election_cache(
    election_id: str,
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Invalidate all cache entries for an election.
    
    Args:
        election_id: ID of the election
        
    Returns:
        Number of entries invalidated
    """
    try:
        count = cache.invalidate_election_cache(election_id)
        return {"invalidated": count}
    
    except Exception as e:
        logger.exception(f"Error invalidating cache for election {election_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Error invalidating cache: {str(e)}"
        )


@router.post("/invalidate-cache/dashboard")
async def invalidate_dashboard_cache(
    cache: MetricsCacheService = Depends(get_cache)
):
    """
    Invalidate all dashboard cache entries.
    
    Returns:
        Number of entries invalidated
    """
    try:
        count = cache.invalidate_dashboard_cache()
        return {"invalidated": count}
    
    except Exception as e:
        logger.exception("Error invalidating dashboard cache")
        raise HTTPException(
            status_code=500,
            detail=f"Error invalidating cache: {str(e)}"
        )