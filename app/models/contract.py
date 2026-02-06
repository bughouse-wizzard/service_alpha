from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base, generate_uuid


class MatchType(enum.Enum):
    EXACT = "exact"
    PARTIAL = "partial"
    FUZZY = "fuzzy"
    NO_MATCH = "no_match"


class MatchStatus(enum.Enum):
    MATCH = "match"
    PARTIAL_MATCH = "partial_match"
    NO_MATCH = "no_match"
    NOT_APPLICABLE = "not_applicable"


class ContractResult(Base):
    __tablename__ = 'contract_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    search_id = Column(UUID(as_uuid=True), ForeignKey('search_requests.id'), nullable=False)
    reestr_number = Column(String(100), nullable=False)
    match_type = Column(Enum(MatchType), nullable=False)
    ai_score = Column(Float, nullable=True)
    raw_data_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional fields
    contract_name = Column(String(500), nullable=True)
    supplier_name = Column(String(500), nullable=True)
    contract_price = Column(Float, nullable=True)
    contract_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    search_request = relationship("SearchRequest", backref="contract_results")
    spec_comparisons = relationship("SpecComparisonRow", backref="contract_result", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ContractResult(id={self.id}, reestr_number={self.reestr_number}, match_type={self.match_type})>"


class SpecComparisonRow(Base):
    __tablename__ = 'spec_comparison_rows'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    contract_result_id = Column(UUID(as_uuid=True), ForeignKey('contract_results.id'), nullable=False)
    name = Column(String(255), nullable=False)
    target_value = Column(Text, nullable=True)
    actual_value = Column(Text, nullable=True)
    match_status = Column(Enum(MatchStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional fields
    comparison_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<SpecComparisonRow(id={self.id}, name={self.name}, match_status={self.match_status})>"