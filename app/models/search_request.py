import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app import db

class SearchStatus(Enum):
    RUNNING = "RUNNING"
    DONE = "DONE"
    STOPPED = "STOPPED"
    ERROR = "ERROR"

class SearchRequest(db.Model):
    __tablename__ = 'search_requests'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(db.Enum(SearchStatus, name='search_status'), nullable=False, default=SearchStatus.RUNNING, index=True)
    
    # Input fields
    object_name = db.Column(db.String(500), nullable=True)
    ktru = db.Column(db.String(100), nullable=True)
    okpd2 = db.Column(db.String(100), nullable=True)
    okved2 = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(200), nullable=True)
    price_min = db.Column(db.Numeric(15, 2), nullable=True)
    price_max = db.Column(db.Numeric(15, 2), nullable=True)
    date_from = db.Column(db.Date, nullable=True)
    date_to = db.Column(db.Date, nullable=True)
    
    # Computed fields
    nmc_value = db.Column(db.Numeric(15, 2), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    contract_results = db.relationship('ContractResult', backref='search_request', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SearchRequest {self.id} - {self.status.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'status': self.status.value,
            'object_name': self.object_name,
            'ktru': self.ktru,
            'okpd2': self.okpd2,
            'okved2': self.okved2,
            'region': self.region,
            'price_min': float(self.price_min) if self.price_min else None,
            'price_max': float(self.price_max) if self.price_max else None,
            'date_from': self.date_from.isoformat() if self.date_from else None,
            'date_to': self.date_to.isoformat() if self.date_to else None,
            'nmc_value': float(self.nmc_value) if self.nmc_value else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }