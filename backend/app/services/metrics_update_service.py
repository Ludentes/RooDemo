"""
Metrics Update Service for the Election Monitoring System.

This module provides services for automatically updating metrics.
"""

import logging
import asyncio
import time
from typing import Dict, List, Optional, Any, Callable, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import threading
from queue import Queue, PriorityQueue
import traceback

from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction
from app.services.hourly_stats_service import HourlyStatsService
from app.services.constituency_metrics_service import ConstituencyMetricsService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdateTask:
    """
    Represents a metrics update task.
    
    Attributes:
        task_id (str): Unique identifier for the task
        priority (int): Priority of the task (lower is higher priority)
        task_type (str): Type of the task (hourly_stats, constituency_metrics)
        params (Dict): Parameters for the task
        created_at (datetime): When the task was created
        attempts (int): Number of attempts made to process the task
        max_attempts (int): Maximum number of attempts before giving up
        last_error (str): Last error message if the task failed
    """
    
    def __init__(
        self, 
        task_id: str, 
        priority: int, 
        task_type: str, 
        params: Dict[str, Any],
        max_attempts: int = 3
    ):
        """
        Initialize a new update task.
        
        Args:
            task_id: Unique identifier for the task
            priority: Priority of the task (lower is higher priority)
            task_type: Type of the task (hourly_stats, constituency_metrics)
            params: Parameters for the task
            max_attempts: Maximum number of attempts before giving up
        """
        self.task_id = task_id
        self.priority = priority
        self.task_type = task_type
        self.params = params
        self.created_at = datetime.utcnow()
        self.attempts = 0
        self.max_attempts = max_attempts
        self.last_error = None
    
    def __lt__(self, other):
        """
        Compare tasks by priority for the priority queue.
        
        Args:
            other: Another UpdateTask
            
        Returns:
            True if this task has higher priority than the other
        """
        return self.priority < other.priority


class MetricsUpdateService:
    """
    Service for automatically updating metrics.
    
    This service provides methods for scheduling and processing metrics updates.
    """
    
    def __init__(self, db_factory: Callable[[], Session]):
        """
        Initialize the service with a database session factory.
        
        Args:
            db_factory: Function that returns a new database session
        """
        self.db_factory = db_factory
        self.task_queue = PriorityQueue()
        self.running = False
        self.worker_thread = None
        self.scheduled_tasks = {}  # Map of task_id to scheduled task info
    
    def start(self):
        """
        Start the metrics update service.
        """
        if self.running:
            logger.warning("Metrics update service is already running")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        logger.info("Metrics update service started")
    
    def stop(self):
        """
        Stop the metrics update service.
        """
        if not self.running:
            logger.warning("Metrics update service is not running")
            return
        
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        
        logger.info("Metrics update service stopped")
    
    def _worker_loop(self):
        """
        Main worker loop for processing tasks.
        """
        while self.running:
            try:
                # Get the next task from the queue with a timeout
                try:
                    task = self.task_queue.get(timeout=1.0)
                except Exception:
                    # No task available, continue the loop
                    continue
                
                # Process the task
                success = self._process_task(task)
                
                # If the task failed and hasn't reached max attempts, requeue it
                if not success and task.attempts < task.max_attempts:
                    # Increase priority (higher number = lower priority)
                    task.priority += 1
                    # Add a delay before retrying
                    time.sleep(1.0)
                    self.task_queue.put(task)
                
                # Mark the task as done
                self.task_queue.task_done()
            
            except Exception as e:
                logger.error(f"Error in metrics update worker loop: {str(e)}")
                logger.error(traceback.format_exc())
                # Sleep to avoid tight loop in case of persistent errors
                time.sleep(1.0)
    
    def _process_task(self, task: UpdateTask) -> bool:
        """
        Process a metrics update task.
        
        Args:
            task: The task to process
            
        Returns:
            True if the task was processed successfully, False otherwise
        """
        task.attempts += 1
        
        try:
            # Get a new database session
            db = self.db_factory()
            
            # Process the task based on its type
            if task.task_type == "hourly_stats":
                self._process_hourly_stats_task(db, task)
            elif task.task_type == "constituency_metrics":
                self._process_constituency_metrics_task(db, task)
            else:
                logger.error(f"Unknown task type: {task.task_type}")
                task.last_error = f"Unknown task type: {task.task_type}"
                return False
            
            # Close the database session
            db.close()
            
            return True
        
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {str(e)}")
            logger.error(traceback.format_exc())
            task.last_error = str(e)
            
            # Close the database session if it exists
            if 'db' in locals():
                db.close()
            
            return False
    
    def _process_hourly_stats_task(self, db: Session, task: UpdateTask):
        """
        Process a hourly stats update task.
        
        Args:
            db: Database session
            task: The task to process
        """
        # Extract parameters
        constituency_id = task.params.get("constituency_id")
        hour = task.params.get("hour")
        force_recalculate = task.params.get("force_recalculate", False)
        
        if not constituency_id or not hour:
            raise ValueError("Missing required parameters: constituency_id, hour")
        
        # Convert hour string to datetime if needed
        if isinstance(hour, str):
            hour = datetime.fromisoformat(hour)
        
        # Create the service and aggregate hourly stats
        hourly_stats_service = HourlyStatsService(db)
        hourly_stats_service.aggregate_hourly_stats(
            constituency_id=constituency_id,
            hour=hour,
            force_recalculate=force_recalculate
        )
        
        logger.info(f"Updated hourly stats for constituency {constituency_id}, hour {hour}")
    
    def _process_constituency_metrics_task(self, db: Session, task: UpdateTask):
        """
        Process a constituency metrics update task.
        
        Args:
            db: Database session
            task: The task to process
        """
        # Extract parameters
        constituency_id = task.params.get("constituency_id")
        start_time = task.params.get("start_time")
        end_time = task.params.get("end_time")
        update_constituency = task.params.get("update_constituency", True)
        
        if not constituency_id:
            raise ValueError("Missing required parameter: constituency_id")
        
        # Convert time strings to datetime if needed
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)
        
        # Create the service and calculate metrics
        constituency_metrics_service = ConstituencyMetricsService(db)
        constituency_metrics_service.calculate_metrics(
            constituency_id=constituency_id,
            start_time=start_time,
            end_time=end_time,
            update_constituency=update_constituency
        )
        
        logger.info(f"Updated metrics for constituency {constituency_id}")
    
    def schedule_hourly_stats_update(
        self, 
        constituency_id: str, 
        hour: datetime,
        priority: int = 10,
        force_recalculate: bool = False
    ) -> str:
        """
        Schedule an hourly stats update.
        
        Args:
            constituency_id: ID of the constituency
            hour: Hour to update stats for
            priority: Priority of the task (lower is higher priority)
            force_recalculate: If True, recalculate even if stats already exist
            
        Returns:
            Task ID
        """
        # Create a unique task ID
        task_id = f"hourly_stats_{constituency_id}_{hour.isoformat()}"
        
        # Create the task
        task = UpdateTask(
            task_id=task_id,
            priority=priority,
            task_type="hourly_stats",
            params={
                "constituency_id": constituency_id,
                "hour": hour,
                "force_recalculate": force_recalculate
            }
        )
        
        # Add the task to the queue
        self.task_queue.put(task)
        
        logger.info(f"Scheduled hourly stats update for constituency {constituency_id}, hour {hour}")
        return task_id
    
    def schedule_constituency_metrics_update(
        self, 
        constituency_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        priority: int = 20,
        update_constituency: bool = True
    ) -> str:
        """
        Schedule a constituency metrics update.
        
        Args:
            constituency_id: ID of the constituency
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            priority: Priority of the task (lower is higher priority)
            update_constituency: If True, update the constituency with calculated metrics
            
        Returns:
            Task ID
        """
        # Create a unique task ID
        task_id = f"constituency_metrics_{constituency_id}_{datetime.utcnow().isoformat()}"
        
        # Create the task
        task = UpdateTask(
            task_id=task_id,
            priority=priority,
            task_type="constituency_metrics",
            params={
                "constituency_id": constituency_id,
                "start_time": start_time,
                "end_time": end_time,
                "update_constituency": update_constituency
            }
        )
        
        # Add the task to the queue
        self.task_queue.put(task)
        
        logger.info(f"Scheduled constituency metrics update for constituency {constituency_id}")
        return task_id
    
    def schedule_election_metrics_update(
        self, 
        election_id: str, 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        priority: int = 30,
        update_constituencies: bool = True
    ) -> List[str]:
        """
        Schedule metrics updates for all constituencies in an election.
        
        Args:
            election_id: ID of the election
            start_time: Optional start time of the range
            end_time: Optional end time of the range
            priority: Priority of the task (lower is higher priority)
            update_constituencies: If True, update constituencies with calculated metrics
            
        Returns:
            List of task IDs
        """
        # Get a new database session
        db = self.db_factory()
        
        try:
            # Get all constituencies for this election
            constituencies = db.query(Constituency).filter(
                Constituency.election_id == election_id
            ).all()
            
            # Schedule updates for each constituency
            task_ids = []
            for constituency in constituencies:
                task_id = self.schedule_constituency_metrics_update(
                    constituency_id=constituency.id,
                    start_time=start_time,
                    end_time=end_time,
                    priority=priority,
                    update_constituency=update_constituencies
                )
                task_ids.append(task_id)
            
            logger.info(f"Scheduled metrics updates for {len(task_ids)} constituencies in election {election_id}")
            return task_ids
        
        finally:
            # Close the database session
            db.close()
    
    def schedule_transaction_triggered_update(
        self, 
        transaction: Transaction,
        priority: int = 5
    ) -> List[str]:
        """
        Schedule updates triggered by a new transaction.
        
        Args:
            transaction: The new transaction
            priority: Priority of the task (lower is higher priority)
            
        Returns:
            List of task IDs
        """
        task_ids = []
        
        # Round the transaction timestamp to the nearest hour
        hour = datetime(
            transaction.timestamp.year,
            transaction.timestamp.month,
            transaction.timestamp.day,
            transaction.timestamp.hour
        )
        
        # Schedule hourly stats update
        hourly_stats_task_id = self.schedule_hourly_stats_update(
            constituency_id=transaction.constituency_id,
            hour=hour,
            priority=priority
        )
        task_ids.append(hourly_stats_task_id)
        
        # Schedule constituency metrics update
        metrics_task_id = self.schedule_constituency_metrics_update(
            constituency_id=transaction.constituency_id,
            priority=priority + 10
        )
        task_ids.append(metrics_task_id)
        
        logger.info(f"Scheduled transaction-triggered updates for constituency {transaction.constituency_id}")
        return task_ids
    
    def schedule_periodic_updates(
        self, 
        interval_seconds: int = 3600,
        priority: int = 50
    ):
        """
        Schedule periodic updates for all active elections.
        
        Args:
            interval_seconds: Interval between updates in seconds
            priority: Priority of the task (lower is higher priority)
        """
        def _periodic_update():
            while self.running:
                try:
                    # Get a new database session
                    db = self.db_factory()
                    
                    # Get all active elections
                    active_elections = db.query(Election).filter(
                        Election.status == "ACTIVE"
                    ).all()
                    
                    # Schedule updates for each active election
                    for election in active_elections:
                        self.schedule_election_metrics_update(
                            election_id=election.id,
                            priority=priority
                        )
                    
                    logger.info(f"Scheduled periodic updates for {len(active_elections)} active elections")
                
                except Exception as e:
                    logger.error(f"Error in periodic update: {str(e)}")
                    logger.error(traceback.format_exc())
                
                finally:
                    # Close the database session if it exists
                    if 'db' in locals():
                        db.close()
                    
                    # Sleep until the next update
                    time.sleep(interval_seconds)
        
        # Start the periodic update thread
        periodic_thread = threading.Thread(target=_periodic_update)
        periodic_thread.daemon = True
        periodic_thread.start()
        
        logger.info(f"Started periodic updates with interval {interval_seconds} seconds")


# Create a function to get the service
def get_metrics_update_service(db_factory: Callable[[], Session]) -> MetricsUpdateService:
    """
    Get an instance of the MetricsUpdateService.
    
    Args:
        db_factory: Function that returns a new database session
        
    Returns:
        MetricsUpdateService instance
    """
    return MetricsUpdateService(db_factory)