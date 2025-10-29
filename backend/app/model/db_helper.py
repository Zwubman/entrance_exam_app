from sqlalchemy import Boolean, Column, DateTime, func, UUID, String
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.ext.declarative import declarative_base
import uuid


Base = declarative_base()

@declarative_mixin
class DBHelper:
    id = Column(
        String(36),  # Store UUID as string
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Primary key identifier"
    )
    
    is_deleted = Column(
        Boolean,
        nullable=False,
        default=0,  # MySQL requires 0/1 instead of 'false'
        comment="Soft delete flag"
    )    
    
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when record was soft deleted"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when record was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when record was last updated"
    )
        
    @declared_attr
    def __tablename__(cls):
        """Auto-generate table name from class name"""
        return cls.__name__.lower() + 's'
    
    def soft_delete(self):
        """Helper method for soft deletion"""
        self.is_deleted = True
        self.deleted_at = func.now()