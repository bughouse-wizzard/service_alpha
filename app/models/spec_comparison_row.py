import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.db import db, SQLiteUUID


class MatchStatus(PyEnum):
    MATCH = "MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"
    NOT_SPECIFIED = "NOT_SPECIFIED"


class SpecComparisonRow(db.Model):
    __tablename__ = 'spec_comparison_rows'
    
    # Primary key
    id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to ContractResult
    contract_result_id = Column(SQLiteUUID(), ForeignKey('contract_results.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Comparison fields
    parameter_name = Column(String(255), nullable=False)
    target_value = Column(Text, nullable=False)
    actual_value = Column(Text, nullable=False)
    match_status = Column(Enum(MatchStatus, name='match_status_enum'), nullable=False, default=MatchStatus.NOT_SPECIFIED)
    
    # Additional metadata
    unit_of_measure = Column(String(50))
    importance_weight = Column(Float, default=1.0)
    confidence_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<SpecComparisonRow {self.id} - {self.parameter_name} - {self.match_status.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'contract_result_id': str(self.contract_result_id),
            'parameter_name': self.parameter_name,
            'target_value': self.target_value,
            'actual_value': self.actual_value,
            'match_status': self.match_status.value,
            'unit_of_measure': self.unit_of_measure,
            'importance_weight': self.importance_weight,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }