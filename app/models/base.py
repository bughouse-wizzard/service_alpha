"""
SQLAlchemy declarative base for database models.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Use a naming convention for constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    
    metadata = metadata
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"