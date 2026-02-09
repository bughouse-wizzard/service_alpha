import uuid
import json
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from app import db

class MatchType(Enum):
    EXACT = "EXACT"
    PARTIAL = "PARTIAL"
    SIMILAR = "SIMILAR"
    NO_MATCH = "NO_MATCH"

class ContractResult(db.Model):
    __tablename__ = 'contract_results'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id = db.Column(UUID(as_uuid=True), db.ForeignKey('search_requests.id'), nullable=False, index=True)
    
    # Basic contract information
    reestr_number = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    match_type = db.Column(db.Enum(MatchType, name='match_type'), nullable=False)
    ai_score = db.Column(db.Numeric(5, 4), nullable=True)  # Score from 0 to 1
    
    # Raw data from external sources
    raw_data_json = db.Column(JSON, nullable=True)
    
    # Additional metadata
    supplier_name = db.Column(db.String(500), nullable=True)
    contract_date = db.Column(db.Date, nullable=True)
    delivery_date = db.Column(db.Date, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    spec_comparisons = db.relationship('SpecComparisonRow', backref='contract_result', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ContractResult {self.reestr_number} - {self.match_type.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'search_id': str(self.search_id),
            'reestr_number': self.reestr_number,
            'price': float(self.price) if self.price else None,
            'match_type': self.match_type.value,
            'ai_score': float(self.ai_score) if self.ai_score else None,
            'supplier_name': self.supplier_name,
            'contract_date': self.contract_date.isoformat() if self.contract_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'raw_data_json': self.raw_data_json,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }