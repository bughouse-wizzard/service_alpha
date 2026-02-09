import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, Float, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db, SQLiteUUID, SQLiteJSON


class MatchType(PyEnum):
    EXACT = "EXACT"
    PARTIAL = "PARTIAL"
    SIMILAR = "SIMILAR"
    NO_MATCH = "NO_MATCH"


class ContractResult(db.Model):
    __tablename__ = 'contract_results'
    __table_args__ = (
        Index('idx_contract_results_search_id', 'search_id'),
        Index('idx_contract_results_reestr_number', 'reestr_number'),
        Index('idx_contract_results_search_reestr', 'search_id', 'reestr_number'),
    )
    
    # Primary key
    id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to SearchRequest
    search_id = Column(SQLiteUUID(), ForeignKey('search_requests.id', ondelete='CASCADE'), nullable=False)
    
    # Contract identification
    reestr_number = Column(String(100), nullable=False)
    
    # Contract details
    price = Column(Float, nullable=False)
    match_type = Column(Enum(MatchType, name='match_type_enum'), nullable=False)
    ai_score = Column(Float, nullable=False)
    
    # Raw data storage
    raw_data_json = Column(SQLiteJSON(), nullable=False)
    
    # Additional metadata
    contract_date = Column(DateTime)
    supplier_name = Column(String(255))
    supplier_inn = Column(String(20))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    spec_comparison_rows = relationship('SpecComparisonRow', backref='contract_result', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ContractResult {self.id} - {self.reestr_number} - {self.match_type.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'search_id': str(self.search_id),
            'reestr_number': self.reestr_number,
            'price': self.price,
            'match_type': self.match_type.value,
            'ai_score': self.ai_score,
            'raw_data_json': self.raw_data_json,
            'contract_date': self.contract_date.isoformat() if self.contract_date else None,
            'supplier_name': self.supplier_name,
            'supplier_inn': self.supplier_inn,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }