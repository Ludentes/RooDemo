"""
Schemas package for the Election Monitoring System.

This package exports all the Pydantic schemas for the application.
"""

from .base import (
    BaseSchema,
    IDSchema,
    TimestampSchema,
    ResponseBase,
    validate_status,
    validate_date_range,
    CreateBase,
    UpdateBase,
    ListBase,
)
from .election import (
    ElectionBase,
    ElectionCreate,
    ElectionUpdate,
    ElectionResponse,
    ElectionList,
)
from .constituency import (
    ConstituencyBase,
    ConstituencyCreate,
    ConstituencyUpdate,
    ConstituencyResponse,
    ConstituencyList,
    ConstituencyDetail,
)
from .transaction import (
    TransactionBase,
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionList,
    TransactionStats,
)
from .alert import (
    AlertBase,
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertList,
    AlertDetail,
    AddNoteRequest,
    UpdateStatusRequest,
)
from .hourly_stats import (
    HourlyStatsBase,
    HourlyStatsCreate,
    HourlyStatsUpdate,
    HourlyStatsResponse,
    HourlyStatsList,
    ActivityPoint,
    ActivityTimeline,
)
from .file_processing import (
    FileProcessingJobBase,
    FileProcessingJobCreate,
    FileProcessingJobUpdate,
    FileProcessingJobResponse,
    FileProcessingJobList,
    FileUploadResponse,
    FileStatusResponse,
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "IDSchema",
    "TimestampSchema",
    "ResponseBase",
    "validate_status",
    "validate_date_range",
    "CreateBase",
    "UpdateBase",
    "ListBase",
    
    # Election schemas
    "ElectionBase",
    "ElectionCreate",
    "ElectionUpdate",
    "ElectionResponse",
    "ElectionList",
    
    # Constituency schemas
    "ConstituencyBase",
    "ConstituencyCreate",
    "ConstituencyUpdate",
    "ConstituencyResponse",
    "ConstituencyList",
    "ConstituencyDetail",
    
    # Transaction schemas
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
    "TransactionList",
    "TransactionStats",
    
    # Alert schemas
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
    "AlertList",
    "AlertDetail",
    "AddNoteRequest",
    "UpdateStatusRequest",
    
    # HourlyStats schemas
    "HourlyStatsBase",
    "HourlyStatsCreate",
    "HourlyStatsUpdate",
    "HourlyStatsResponse",
    "HourlyStatsList",
    "ActivityPoint",
    "ActivityTimeline",
    
    # FileProcessingJob schemas
    "FileProcessingJobBase",
    "FileProcessingJobCreate",
    "FileProcessingJobUpdate",
    "FileProcessingJobResponse",
    "FileProcessingJobList",
    "FileUploadResponse",
    "FileStatusResponse",
]