"""
FileProcessingJob CRUD operations for the Election Monitoring System.

This module provides CRUD operations for the FileProcessingJob model.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from .base import BaseCRUD
from app.models.file_processing import FileProcessingJob
from app.models.schemas.file_processing import FileProcessingJobCreate, FileProcessingJobUpdate


class FileProcessingJobCRUD(BaseCRUD[FileProcessingJob, FileProcessingJobCreate, FileProcessingJobUpdate]):
    """
    CRUD operations for FileProcessingJob model.
    
    This class provides CRUD operations specific to the FileProcessingJob model.
    """
    
    def get_by_election(self, db: Session, *, election_id: str) -> List[FileProcessingJob]:
        """
        Get file processing jobs by election ID.
        
        Args:
            db: Database session
            election_id: ID of the election to get jobs for
            
        Returns:
            List of file processing jobs for the election
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.election_id == election_id).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[FileProcessingJob]:
        """
        Get file processing jobs by status.
        
        Args:
            db: Database session
            status: Status of jobs to get
            
        Returns:
            List of file processing jobs with the specified status
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.status == status).all()
    
    def get_by_file_type(self, db: Session, *, file_type: str) -> List[FileProcessingJob]:
        """
        Get file processing jobs by file type.
        
        Args:
            db: Database session
            file_type: Type of files to get jobs for
            
        Returns:
            List of file processing jobs for the specified file type
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.file_type == file_type).all()
    
    def get_by_time_range(
        self, db: Session, *, start_time: datetime, end_time: datetime
    ) -> List[FileProcessingJob]:
        """
        Get file processing jobs within a time range.
        
        Args:
            db: Database session
            start_time: Start time of the range
            end_time: End time of the range
            
        Returns:
            List of file processing jobs within the time range
        """
        return db.query(FileProcessingJob).filter(
            FileProcessingJob.created_at >= start_time,
            FileProcessingJob.created_at <= end_time
        ).all()
    
    def get_latest(self, db: Session, *, limit: int = 10) -> List[FileProcessingJob]:
        """
        Get the latest file processing jobs.
        
        Args:
            db: Database session
            limit: Maximum number of jobs to return
            
        Returns:
            List of the latest file processing jobs
        """
        return db.query(FileProcessingJob).order_by(desc(FileProcessingJob.created_at)).limit(limit).all()
    
    def get_pending_jobs(self, db: Session) -> List[FileProcessingJob]:
        """
        Get all pending file processing jobs.
        
        Args:
            db: Database session
            
        Returns:
            List of pending file processing jobs
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.status == "pending").all()
    
    def get_processing_jobs(self, db: Session) -> List[FileProcessingJob]:
        """
        Get all processing file processing jobs.
        
        Args:
            db: Database session
            
        Returns:
            List of processing file processing jobs
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.status == "processing").all()
    
    def get_completed_jobs(self, db: Session) -> List[FileProcessingJob]:
        """
        Get all completed file processing jobs.
        
        Args:
            db: Database session
            
        Returns:
            List of completed file processing jobs
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.status == "completed").all()
    
    def get_failed_jobs(self, db: Session) -> List[FileProcessingJob]:
        """
        Get all failed file processing jobs.
        
        Args:
            db: Database session
            
        Returns:
            List of failed file processing jobs
        """
        return db.query(FileProcessingJob).filter(FileProcessingJob.status == "failed").all()
    
    def update_status(
        self, db: Session, *, id: str, status: str, error_message: Optional[str] = None
    ) -> FileProcessingJob:
        """
        Update file processing job status.
        
        Args:
            db: Database session
            id: ID of the job to update
            status: New status
            error_message: Error message if the job failed
            
        Returns:
            The updated file processing job
        """
        job = self.get(db, id)
        if job:
            job.status = status
            if status == "processing":
                job.started_at = datetime.utcnow()
            elif status == "completed":
                job.completed_at = datetime.utcnow()
            elif status == "failed" and error_message:
                job.error_message = error_message
                job.completed_at = datetime.utcnow()
            
            db.add(job)
            db.commit()
            db.refresh(job)
        return job
    
    def update_progress(
        self, db: Session, *, id: str, progress: float, message: Optional[str] = None
    ) -> FileProcessingJob:
        """
        Update file processing job progress.
        
        Args:
            db: Database session
            id: ID of the job to update
            progress: Progress percentage (0-100)
            message: Progress message
            
        Returns:
            The updated file processing job
        """
        job = self.get(db, id)
        if job:
            job.progress = progress
            if message:
                job.progress_message = message
            job.updated_at = datetime.utcnow()
            db.add(job)
            db.commit()
            db.refresh(job)
        return job
    
    def update_result(
        self, db: Session, *, id: str, result: Dict[str, Any]
    ) -> FileProcessingJob:
        """
        Update file processing job result.
        
        Args:
            db: Database session
            id: ID of the job to update
            result: Job result data
            
        Returns:
            The updated file processing job
        """
        job = self.get(db, id)
        if job:
            job.result = result
            job.updated_at = datetime.utcnow()
            db.add(job)
            db.commit()
            db.refresh(job)
        return job
    
    def get_job_counts_by_status(self, db: Session) -> Dict[str, int]:
        """
        Get job counts by status.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of job counts by status
        """
        result = db.query(
            FileProcessingJob.status, func.count(FileProcessingJob.id)
        ).group_by(FileProcessingJob.status).all()
        
        return {status: count for status, count in result}
    
    def get_job_counts_by_file_type(self, db: Session) -> Dict[str, int]:
        """
        Get job counts by file type.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of job counts by file type
        """
        result = db.query(
            FileProcessingJob.file_type, func.count(FileProcessingJob.id)
        ).group_by(FileProcessingJob.file_type).all()
        
        return {file_type: count for file_type, count in result}
    
    def get_average_processing_time(self, db: Session) -> Dict[str, float]:
        """
        Get average processing time by file type.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of average processing times by file type
        """
        # Calculate average time difference between started_at and completed_at
        result = db.query(
            FileProcessingJob.file_type,
            func.avg(
                func.extract('epoch', FileProcessingJob.completed_at) - 
                func.extract('epoch', FileProcessingJob.started_at)
            ).label('avg_time')
        ).filter(
            FileProcessingJob.status == "completed",
            FileProcessingJob.started_at.isnot(None),
            FileProcessingJob.completed_at.isnot(None)
        ).group_by(FileProcessingJob.file_type).all()
        
        return {file_type: float(avg_time) for file_type, avg_time in result}


# Create an instance of FileProcessingJobCRUD
file_processing_job_crud = FileProcessingJobCRUD(FileProcessingJob)