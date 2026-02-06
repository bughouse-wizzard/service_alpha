import enum
from sqlalchemy import Column, String, Integer, Enum, Float, ARRAY, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from .base import BaseModel

class SearchStatus(enum.Enum):
    """Status of search request"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SearchRequest(BaseModel):
    """Search request model"""
    __tablename__ = "search_requests"
    
    # Search parameters
    input_source = Column(String(255), nullable=False)
    ktru_code = Column(String(50), nullable=True)
    status = Column(Enum(SearchStatus), default=SearchStatus.PENDING, nullable=False)
    limit_contracts = Column(Integer, default=10, nullable=False)
    selected_contract_ids = Column(ARRAY(String(255)), nullable=True)
    nmc_value = Column(Float, nullable=True)
    
    # Additional search parameters
    search_query = Column(Text, nullable=True)
    region_filter = Column(String(100), nullable=True)
    date_from = Column(String(20), nullable=True)  # Format: YYYY-MM-DD
    date_to = Column(String(20), nullable=True)    # Format: YYYY-MM-DD
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    
    # Processing metadata
    total_contracts_found = Column(Integer, default=0, nullable=False)
    contracts_processed = Column(Integer, default=0, nullable=False)
    processing_started_at = Column(String(20), nullable=True)
    processing_completed_at = Column(String(20), nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    
    # AI/ML parameters
    ai_model_version = Column(String(50), nullable=True)
    confidence_threshold = Column(Float, default=0.7, nullable=False)
    
    # Relationships
    contract_results = relationship("ContractResult", back_populates="search_request", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SearchRequest(id={self.id}, status={self.status}, ktru_code={self.ktru_code})>"