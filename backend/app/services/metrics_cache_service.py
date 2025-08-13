"""
Metrics Cache Service for the Election Monitoring System.

This module provides services for caching metrics data.
"""

import logging
import time
import json
import hashlib
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from functools import wraps
import threading
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheEntry:
    """
    Represents a cached entry.
    
    Attributes:
        key (str): Cache key
        value (Any): Cached value
        expiry (float): Expiry time as Unix timestamp
        tags (List[str]): Tags for cache invalidation
    """
    
    def __init__(
        self, 
        key: str, 
        value: Any, 
        expiry: float,
        tags: List[str] = None
    ):
        """
        Initialize a new cache entry.
        
        Args:
            key: Cache key
            value: Cached value
            expiry: Expiry time as Unix timestamp
            tags: Tags for cache invalidation
        """
        self.key = key
        self.value = value
        self.expiry = expiry
        self.tags = tags or []
    
    def is_expired(self) -> bool:
        """
        Check if the cache entry is expired.
        
        Returns:
            True if the entry is expired, False otherwise
        """
        return time.time() > self.expiry


class InMemoryCache:
    """
    In-memory cache implementation.
    """
    
    def __init__(self):
        """
        Initialize a new in-memory cache.
        """
        self.cache = {}
        self.tag_index = {}
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self.lock:
            entry = self.cache.get(key)
            
            if entry is None:
                return None
            
            if entry.is_expired():
                self._remove_entry(entry)
                return None
            
            return entry.value
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: int = 3600,
        tags: List[str] = None
    ) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            tags: Tags for cache invalidation
        """
        with self.lock:
            expiry = time.time() + ttl
            entry = CacheEntry(key, value, expiry, tags)
            
            # Remove old entry if it exists
            old_entry = self.cache.get(key)
            if old_entry:
                self._remove_entry(old_entry)
            
            # Add new entry
            self.cache[key] = entry
            
            # Update tag index
            if tags:
                for tag in tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = set()
                    self.tag_index[tag].add(key)
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        with self.lock:
            entry = self.cache.get(key)
            
            if entry is None:
                return False
            
            self._remove_entry(entry)
            return True
    
    def invalidate_tag(self, tag: str) -> int:
        """
        Invalidate all entries with a specific tag.
        
        Args:
            tag: Tag to invalidate
            
        Returns:
            Number of entries invalidated
        """
        with self.lock:
            keys = self.tag_index.get(tag, set())
            count = 0
            
            for key in list(keys):
                if self.delete(key):
                    count += 1
            
            return count
    
    def _remove_entry(self, entry: CacheEntry) -> None:
        """
        Remove a cache entry and update the tag index.
        
        Args:
            entry: Cache entry to remove
        """
        # Remove from cache
        self.cache.pop(entry.key, None)
        
        # Remove from tag index
        for tag in entry.tags:
            if tag in self.tag_index:
                self.tag_index[tag].discard(entry.key)
                if not self.tag_index[tag]:
                    self.tag_index.pop(tag)
    
    def clear(self) -> int:
        """
        Clear the entire cache.
        
        Returns:
            Number of entries cleared
        """
        with self.lock:
            count = len(self.cache)
            self.cache = {}
            self.tag_index = {}
            return count
    
    def cleanup(self) -> int:
        """
        Remove all expired entries from the cache.
        
        Returns:
            Number of entries removed
        """
        with self.lock:
            count = 0
            now = time.time()
            
            for key, entry in list(self.cache.items()):
                if entry.expiry <= now:
                    self._remove_entry(entry)
                    count += 1
            
            return count


class MetricsCacheService:
    """
    Service for caching metrics data.
    
    This service provides methods for caching and retrieving metrics data.
    """
    
    def __init__(self, cache_backend=None):
        """
        Initialize the service with a cache backend.
        
        Args:
            cache_backend: Cache backend to use (defaults to InMemoryCache)
        """
        self.cache = cache_backend or InMemoryCache()
        self.cleanup_interval = 300  # 5 minutes
        self.running = False
        self.cleanup_thread = None
    
    def start(self):
        """
        Start the metrics cache service.
        """
        if self.running:
            logger.warning("Metrics cache service is already running")
            return
        
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()
        
        logger.info("Metrics cache service started")
    
    def stop(self):
        """
        Stop the metrics cache service.
        """
        if not self.running:
            logger.warning("Metrics cache service is not running")
            return
        
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5.0)
        
        logger.info("Metrics cache service stopped")
    
    def _cleanup_loop(self):
        """
        Main cleanup loop for removing expired entries.
        """
        while self.running:
            try:
                # Sleep first to avoid immediate cleanup on startup
                time.sleep(self.cleanup_interval)
                
                # Cleanup expired entries
                count = self.cache.cleanup()
                if count > 0:
                    logger.info(f"Cleaned up {count} expired cache entries")
            
            except Exception as e:
                logger.error(f"Error in metrics cache cleanup loop: {str(e)}")
                logger.error(traceback.format_exc())
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        return self.cache.get(key)
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: int = 3600,
        tags: List[str] = None
    ) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            tags: Tags for cache invalidation
        """
        self.cache.set(key, value, ttl, tags)
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        return self.cache.delete(key)
    
    def invalidate_tag(self, tag: str) -> int:
        """
        Invalidate all entries with a specific tag.
        
        Args:
            tag: Tag to invalidate
            
        Returns:
            Number of entries invalidated
        """
        return self.cache.invalidate_tag(tag)
    
    def clear(self) -> int:
        """
        Clear the entire cache.
        
        Returns:
            Number of entries cleared
        """
        return self.cache.clear()
    
    def get_hourly_stats_key(
        self, 
        constituency_id: str, 
        hour: datetime
    ) -> str:
        """
        Generate a cache key for hourly stats.
        
        Args:
            constituency_id: ID of the constituency
            hour: Hour timestamp
            
        Returns:
            Cache key
        """
        hour_str = hour.strftime("%Y-%m-%d-%H")
        return f"hourly_stats:{constituency_id}:{hour_str}"
    
    def get_constituency_metrics_key(
        self, 
        constituency_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> str:
        """
        Generate a cache key for constituency metrics.
        
        Args:
            constituency_id: ID of the constituency
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            Cache key
        """
        start_str = start_time.strftime("%Y-%m-%d-%H") if start_time else "none"
        end_str = end_time.strftime("%Y-%m-%d-%H") if end_time else "none"
        return f"constituency_metrics:{constituency_id}:{start_str}:{end_str}"
    
    def get_election_metrics_key(
        self, 
        election_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None
    ) -> str:
        """
        Generate a cache key for election metrics.
        
        Args:
            election_id: ID of the election
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            
        Returns:
            Cache key
        """
        start_str = start_time.strftime("%Y-%m-%d-%H") if start_time else "none"
        end_str = end_time.strftime("%Y-%m-%d-%H") if end_time else "none"
        return f"election_metrics:{election_id}:{start_str}:{end_str}"
    
    def get_dashboard_metrics_key(
        self, 
        detailed: bool = False
    ) -> str:
        """
        Generate a cache key for dashboard metrics.
        
        Args:
            detailed: Whether to get detailed metrics
            
        Returns:
            Cache key
        """
        return f"dashboard_metrics:{'detailed' if detailed else 'summary'}"
    
    def invalidate_constituency_cache(self, constituency_id: str) -> int:
        """
        Invalidate all cache entries for a constituency.
        
        Args:
            constituency_id: ID of the constituency
            
        Returns:
            Number of entries invalidated
        """
        return self.invalidate_tag(f"constituency:{constituency_id}")
    
    def invalidate_election_cache(self, election_id: str) -> int:
        """
        Invalidate all cache entries for an election.
        
        Args:
            election_id: ID of the election
            
        Returns:
            Number of entries invalidated
        """
        return self.invalidate_tag(f"election:{election_id}")
    
    def invalidate_dashboard_cache(self) -> int:
        """
        Invalidate all dashboard cache entries.
        
        Returns:
            Number of entries invalidated
        """
        return self.invalidate_tag("dashboard")


def cached(
    ttl: int = 3600,
    key_fn: Optional[Callable] = None,
    tags_fn: Optional[Callable] = None
):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds
        key_fn: Function to generate cache key from function arguments
        tags_fn: Function to generate tags from function arguments
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get the cache service
            if hasattr(self, 'cache'):
                cache = self.cache
            else:
                # No cache service available, just call the function
                return func(self, *args, **kwargs)
            
            # Generate cache key
            if key_fn:
                key = key_fn(self, *args, **kwargs)
            else:
                # Default key generation
                arg_str = ':'.join(str(arg) for arg in args)
                kwarg_str = ':'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                key = f"{func.__module__}:{func.__name__}:{arg_str}:{kwarg_str}"
                key = hashlib.md5(key.encode()).hexdigest()
            
            # Try to get from cache
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Call the function
            result = func(self, *args, **kwargs)
            
            # Generate tags
            if tags_fn:
                tags = tags_fn(self, *args, **kwargs)
            else:
                tags = []
            
            # Cache the result
            cache.set(key, result, ttl, tags)
            
            return result
        return wrapper
    return decorator


# Create a function to get the service
def get_metrics_cache_service() -> MetricsCacheService:
    """
    Get an instance of the MetricsCacheService.
    
    Returns:
        MetricsCacheService instance
    """
    return MetricsCacheService()