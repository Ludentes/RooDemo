"""
Base CRUD operations for the Election Monitoring System.

This module provides a generic CRUD class for database operations.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.database import Base

# Define generic types for SQLAlchemy models and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations.
    
    This class provides generic CRUD operations that can be used with any model.
    
    Attributes:
        model: The SQLAlchemy model class
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize with SQLAlchemy model class.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: Database session
            id: ID of the record to get
            
        Returns:
            The record if found, None otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Data to create the record with
            
        Returns:
            The created record
        """
        # Convert Pydantic model to dict while preserving datetime objects
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record.
        
        Args:
            db: Database session
            db_obj: Record to update
            obj_in: Data to update the record with
            
        Returns:
            The updated record
        """
        # Get current data as dict
        obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Convert Pydantic model to dict while preserving datetime objects
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: Any) -> ModelType:
        """
        Delete a record.
        
        Args:
            db: Database session
            id: ID of the record to delete
            
        Returns:
            The deleted record
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    # Alias for delete method
    remove = delete
    
    def count(self, db: Session) -> int:
        """
        Count the number of records.
        
        Args:
            db: Database session
            
        Returns:
            The number of records
        """
        return db.query(self.model).count()
    
    def exists(self, db: Session, id: Any) -> bool:
        """
        Check if a record exists.
        
        Args:
            db: Database session
            id: ID of the record to check
            
        Returns:
            True if the record exists, False otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first() is not None