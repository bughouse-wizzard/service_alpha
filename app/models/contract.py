"""
ContractResult and SpecComparisonRow models for storing contract search results.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, Integer, Enum, DateTime, 
    Float, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
import json

from .base import Base


class MatchType(PyEnum):
    """Enumeration for contract match types."""
    EXACT = "exact"
    PARTIAL = "partial"
    SIMILAR = "similar"
    NO_MATCH = "no_match"


class MatchStatus(PyEnum):
    """Enumeration for specification comparison match status."""
    MATCH = "match"
    PARTIAL_MATCH = "partial_match"
    NO_MATCH = "no_match"
    NOT_APPLICABLE = "not_applicable"


class ContractResult(Base):
    """
    Model representing a contract search result.
    
    Attributes:
        id: Unique identifier
        search_id: Foreign key to SearchRequest
        reestr_number: Registry number of the contract
        match_type: Type of match (enum)
        ai_score: AI matching score (0-100)
        raw_data_json: Raw contract data in JSON format
        created_at: Timestamp when the result was created
        updated_at: Timestamp when the result was last updated
        is_selected: Whether this contract was selected by the user
        selection_rank: Ranking position when selected
        notes: Additional notes about the contract
    """
    
    __tablename__ = "contract_results"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    search_id = Column(
        String(36), 
        ForeignKey("search_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reestr_number = Column(String(100), nullable=False, index=True)
    match_type = Column(
        Enum(MatchType, name="match_type_enum"),
        nullable=False,
        default=MatchType.PARTIAL
    )
    ai_score = Column(Float, nullable=False, default=0.0)
    raw_data_json = Column(Text, nullable=False, default="{}")  # Store as JSON string for SQLite
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
    
    # Selection information
    is_selected = Column(Boolean, default=False, nullable=False)
    selection_rank = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    search_request = relationship("SearchRequest", back_populates="contract_results")
    spec_comparisons = relationship(
        "SpecComparisonRow", 
        back_populates="contract_result",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<ContractResult(id={self.id}, reestr_number={self.reestr_number}, match_type={self.match_type})>"


class SpecComparisonRow(Base):
    """
    Model representing a specification comparison row for a contract.
    
    Attributes:
        id: Unique identifier
        contract_result_id: Foreign key to ContractResult
        name: Name of the specification parameter
        target_value: Target/expected value
        actual_value: Actual value from the contract
        match_status: Status of the match (enum)
        created_at: Timestamp when the comparison was created
        updated_at: Timestamp when the comparison was last updated
        confidence_score: Confidence score for this comparison (0-100)
        notes: Additional notes about the comparison
    """
    
    __tablename__ = "spec_comparison_rows"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_result_id = Column(
        String(36), 
        ForeignKey("contract_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(255), nullable=False)
    target_value = Column(Text, nullable=True)
    actual_value = Column(Text, nullable=True)
    match_status = Column(
        Enum(MatchStatus, name="match_status_enum"),
        nullable=False,
        default=MatchStatus.NOT_APPLICABLE
    )
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
    
    # Additional fields
    confidence_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    contract_result = relationship("ContractResult", back_populates="spec_comparisons")
    
    def __repr__(self):
        return f"<SpecComparisonRow(id={self.id}, name={self.name}, match_status={self.match_status})>"