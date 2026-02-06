"""
SearchRequest model for storing search requests and their status.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, Integer, Enum, DateTime, 
    Float, Text, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
import json

from .base import Base


class SearchStatus(PyEnum):
    """Enumeration for search request status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SearchRequest(Base):
    """
    Model representing a search request for contracts.
    
    Attributes:
        id: Unique identifier (UUID)
        input_source: Source of the input data (file, text, etc.)
        ktru_code: KTRU code for the search
        status: Current status of the search (enum)
        limit_contracts: Maximum number of contracts to return
        selected_contract_ids: Array of contract IDs that were selected
        nmc_value: NMC (Normalized Maximum Cost) value
        created_at: Timestamp when the request was created
        updated_at: Timestamp when the request was last updated
        completed_at: Timestamp when the request was completed
        error_message: Error message if the search failed
        metadata_json: Additional metadata in JSON format
        is_archived: Whether the search request is archived
    """
    
    __tablename__ = "search_requests"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    input_source = Column(String(255), nullable=False)
    ktru_code = Column(String(100), nullable=False)
    status = Column(
        Enum(SearchStatus, name="search_status_enum"),
        nullable=False,
        default=SearchStatus.PENDING
    )
    limit_contracts = Column(Integer, nullable=False, default=10)
    selected_contract_ids = Column(Text, nullable=True)  # Store as JSON string for SQLite
    nmc_value = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
    completed_at = Column(DateTime, nullable=True)
    
    # Additional fields
    error_message = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True, default="{}")  # Store as JSON string for SQLite
    is_archived = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    contract_results = relationship(
        "ContractResult", 
        back_populates="search_request",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<SearchRequest(id={self.id}, ktru_code={self.ktru_code}, status={self.status})>"