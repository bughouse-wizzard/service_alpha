import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class MatchStatus(enum.Enum):
    MATCH = "MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"
    NOT_SPECIFIED = "NOT_SPECIFIED"


class SpecComparisonRow(Base):
    __tablename__ = "spec_comparison_row"

    # Primary key - using String for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # Foreign key to ContractResult - using String for SQLite compatibility
    contract_result_id = Column(
        String(36), 
        ForeignKey("contract_result.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Comparison fields
    target_value = Column(String(1000), nullable=False)
    actual_value = Column(String(1000), nullable=False)
    match_status = Column(Enum(MatchStatus), nullable=False, default=MatchStatus.NOT_SPECIFIED)
    
    # Additional comparison metadata
    parameter_name = Column(String(200), nullable=False)  # e.g., "price", "quantity", "delivery_date"
    parameter_unit = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)  # Confidence score for the match (0.0 to 1.0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship
    contract_result = relationship("ContractResult", back_populates="spec_comparisons")
    
    def __repr__(self):
        return f"<SpecComparisonRow(id={self.id}, parameter_name={self.parameter_name}, match_status={self.match_status})>"