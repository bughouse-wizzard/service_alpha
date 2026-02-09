import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ContractResult(Base):
    __tablename__ = "contract_results"
    __table_args__ = (
        Index('idx_contract_result_price', 'price'),
        Index('idx_contract_result_ai_score', 'ai_score'),
        Index('idx_contract_result_contract_date', 'contract_date'),
    )

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key to SearchRequest
    search_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("search_requests.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Contract details
    reestr_number = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    match_type = Column(String(50), nullable=True)  # e.g., "EXACT", "PARTIAL", "SIMILAR"
    ai_score = Column(Float, nullable=True)  # AI matching score from 0.0 to 1.0
    
    # Raw data from external sources
    raw_data_json = Column(JSON, nullable=True)
    
    # Additional contract metadata
    contract_date = Column(DateTime, nullable=True)
    supplier_name = Column(String(500), nullable=True)
    supplier_inn = Column(String(20), nullable=True)
    contract_status = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    search_request = relationship("SearchRequest", back_populates="contract_results")
    spec_comparisons = relationship("SpecComparisonRow", back_populates="contract_result", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ContractResult(id={self.id}, reestr_number={self.reestr_number}, price={self.price})>"