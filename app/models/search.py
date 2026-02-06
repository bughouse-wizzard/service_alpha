from sqlalchemy import Column, String, Integer, Enum, DateTime, Text, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from app.models.base import Base, generate_uuid


class SearchStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SearchRequest(Base):
    __tablename__ = 'search_requests'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    input_source = Column(String(255), nullable=False)
    ktru_code = Column(String(50), nullable=False)
    status = Column(Enum(SearchStatus), default=SearchStatus.PENDING, nullable=False)
    limit_contracts = Column(Integer, default=10)
    selected_contract_ids = Column(ARRAY(String), nullable=True)
    nmc_value = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional fields that might be needed based on requirements
    search_query = Column(Text, nullable=True)
    search_parameters = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<SearchRequest(id={self.id}, ktru_code={self.ktru_code}, status={self.status})>"