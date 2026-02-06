import enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from .base import BaseModel

class MatchType(enum.Enum):
    """Type of match between search and contract"""
    EXACT = "exact"
    PARTIAL = "partial"
    SIMILAR = "similar"
    NO_MATCH = "no_match"

class MatchStatus(enum.Enum):
    """Status of specification comparison"""
    MATCH = "match"
    MISMATCH = "mismatch"
    PARTIAL = "partial"
    UNKNOWN = "unknown"

class ContractResult(BaseModel):
    """Contract result model"""
    __tablename__ = "contract_results"
    
    # Foreign key to search request
    search_id = Column(UUID(as_uuid=True), ForeignKey("search_requests.id"), nullable=False, index=True)
    
    # Contract identification
    reestr_number = Column(String(100), nullable=False, index=True)
    contract_number = Column(String(100), nullable=True)
    contract_date = Column(String(20), nullable=True)  # Format: YYYY-MM-DD
    
    # Match information
    match_type = Column(Enum(MatchType), nullable=False)
    ai_score = Column(Float, nullable=False)
    confidence_level = Column(Float, nullable=True)
    
    # Contract details
    supplier_name = Column(String(255), nullable=True)
    supplier_inn = Column(String(20), nullable=True)
    customer_name = Column(String(255), nullable=True)
    customer_inn = Column(String(20), nullable=True)
    contract_price = Column(Float, nullable=True)
    currency = Column(String(10), nullable=True, default="RUB")
    
    # Additional metadata
    source_system = Column(String(100), nullable=True)
    source_url = Column(Text, nullable=True)
    scraped_at = Column(String(20), nullable=True)
    
    # Raw data storage
    raw_data_json = Column(JSONB, nullable=True)
    
    # Processing flags
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_notes = Column(Text, nullable=True)
    
    # Relationships
    search_request = relationship("SearchRequest", back_populates="contract_results")
    spec_comparisons = relationship("SpecComparisonRow", back_populates="contract_result", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ContractResult(id={self.id}, reestr_number={self.reestr_number}, match_type={self.match_type}, ai_score={self.ai_score})>"

class SpecComparisonRow(BaseModel):
    """Specification comparison row model"""
    __tablename__ = "spec_comparison_rows"
    
    # Foreign key to contract result
    contract_result_id = Column(UUID(as_uuid=True), ForeignKey("contract_results.id"), nullable=False, index=True)
    
    # Comparison data
    name = Column(String(255), nullable=False)
    target_value = Column(Text, nullable=True)
    actual_value = Column(Text, nullable=True)
    match_status = Column(Enum(MatchStatus), nullable=False)
    
    # Additional comparison metrics
    similarity_score = Column(Float, nullable=True)
    comparison_notes = Column(Text, nullable=True)
    
    # Relationships
    contract_result = relationship("ContractResult", back_populates="spec_comparisons")
    
    def __repr__(self):
        return f"<SpecComparisonRow(id={self.id}, name={self.name}, match_status={self.match_status})>"