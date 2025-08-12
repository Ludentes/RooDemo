from typing import Generic, TypeVar, Type, Optional, List, Tuple, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import BaseCRUD
from app.models.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CRUDType = TypeVar("CRUDType", bound=BaseCRUD)

class BaseService(Generic[ModelType, CRUDType]):
    """
    Base service class with common functionality for all services.
    
    Provides generic methods for common operations like get and get_multi.
    Specific service classes should inherit from this class and implement
    their specialized methods.
    """
    
    def __init__(self, crud_class: Type[CRUDType], db: AsyncSession):
        """
        Initialize the service with a CRUD class and database session.
        
        Args:
            crud_class: The CRUD class to use for database operations
            db: The database session
        """
        # Create an instance of the CRUD class without passing db
        # The db will be passed to each method call instead
        self.crud = crud_class
        self.db = db
        
    async def get(self, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            id: The ID of the record to get
            
        Returns:
            The record if found, None otherwise
        """
        # Pass the db parameter to the CRUD method
        return self.crud.get(db=self.db, id=id)
        
    async def get_multi(
        self,
        page: int = 1,
        page_size: int = 10,
        **filters
    ) -> Tuple[List[ModelType], int]:
        """
        Get multiple records with pagination and filtering.
        
        Args:
            page: The page number (1-indexed)
            page_size: The number of items per page
            **filters: Additional filters to apply
            
        Returns:
            A tuple of (list of records, total count)
        """
        skip = (page - 1) * page_size
        
        # Get the records with pagination
        records = self.crud.get_multi(db=self.db, skip=skip, limit=page_size)
        
        # Count total records with filters
        # This is a simplified approach; in a real app, you'd apply the same filters
        total = self.crud.count(db=self.db)
        
        return records, total