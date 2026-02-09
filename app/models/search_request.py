import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, Float, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class SearchStatus(enum.Enum):
    RUNNING = "RUNNING"
    DONE = "DONE"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class SearchRequest(Base):
    __tablename__ = "search_request"
    __table_args__ = (
        Index('idx_search_request_status_created', 'status', 'created_at'),
        Index('idx_search_request_object_name', 'object_name'),
    )

    # Primary key - using String for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # Status field with ENUM
    status = Column(Enum(SearchStatus), nullable=False, default=SearchStatus.RUNNING)
    
    # Input fields
    object_name = Column(String(500), nullable=False)
    ktru = Column(String(100), nullable=True)
    okpd2 = Column(String(100), nullable=True)
    okved2 = Column(String(100), nullable=True)
    region = Column(String(200), nullable=True)
    customer_name = Column(String(500), nullable=True)
    customer_inn = Column(String(20), nullable=True)
    price_from = Column(Float, nullable=True)
    price_to = Column(Float, nullable=True)
    date_from = Column(DateTime, nullable=True)
    date_to = Column(DateTime, nullable=True)
    
    # Computed fields
    nmc_value = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    search_parameters = Column(JSON, nullable=True)  # Store additional search parameters as JSON
    error_message = Column(String(1000), nullable=True)
    
    # Relationships
    contract_results = relationship("ContractResult", back_populates="search_request", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SearchRequest(id={self.id}, status={self.status}, object_name={self.object_name})>"