import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, Float, Text, Index
from sqlalchemy.sql import func
from app.db import db, SQLiteUUID


class SearchStatus(PyEnum):
    RUNNING = "RUNNING"
    DONE = "DONE"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class SearchRequest(db.Model):
    __tablename__ = 'search_requests'
    __table_args__ = (
        Index('idx_search_requests_status', 'status'),
        Index('idx_search_requests_created_at', 'created_at'),
    )
    
    # Primary key
    id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    
    # Status field with ENUM
    status = Column(Enum(SearchStatus, name='search_status_enum'), nullable=False, default=SearchStatus.RUNNING)
    
    # Input fields
    object_name = Column(String(255), nullable=False)
    ktru = Column(String(255))
    okpd2 = Column(String(255))
    okved2 = Column(String(255))
    region = Column(String(255))
    customer_name = Column(String(255))
    customer_inn = Column(String(20))
    price_from = Column(Float)
    price_to = Column(Float)
    publication_date_from = Column(DateTime)
    publication_date_to = Column(DateTime)
    additional_filters = Column(Text)
    
    # Computed fields
    nmc_value = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    contract_results = db.relationship('ContractResult', backref='search_request', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SearchRequest {self.id} - {self.object_name} - {self.status.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'status': self.status.value,
            'object_name': self.object_name,
            'ktru': self.ktru,
            'okpd2': self.okpd2,
            'okved2': self.okved2,
            'region': self.region,
            'customer_name': self.customer_name,
            'customer_inn': self.customer_inn,
            'price_from': self.price_from,
            'price_to': self.price_to,
            'publication_date_from': self.publication_date_from.isoformat() if self.publication_date_from else None,
            'publication_date_to': self.publication_date_to.isoformat() if self.publication_date_to else None,
            'additional_filters': self.additional_filters,
            'nmc_value': self.nmc_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }