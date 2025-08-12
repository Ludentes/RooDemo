"""
CRUD operations for the Election Monitoring System.

This module exports all CRUD operations for the application.
"""

from .base import BaseCRUD
from .election import election_crud
from .constituency import constituency_crud
from .transaction import transaction_crud
from .alert import alert_crud
from .hourly_stats import hourly_stats_crud
from .file_processing import file_processing_job_crud

__all__ = [
    "BaseCRUD",
    "election_crud",
    "constituency_crud",
    "transaction_crud",
    "alert_crud",
    "hourly_stats_crud",
    "file_processing_job_crud",
]