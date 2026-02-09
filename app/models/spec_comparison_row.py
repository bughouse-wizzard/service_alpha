import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from app import db

class MatchStatus(Enum):
    MATCH = "MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"
    NOT_SPECIFIED = "NOT_SPECIFIED"

class SpecComparisonRow(db.Model):
    __tablename__ = 'spec_comparison_rows'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_result_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contract_results.id'), nullable=False, index=True)
    
    # Specification comparison fields
    parameter_name = db.Column(db.String(200), nullable=False)
    target_value = db.Column(db.Text, nullable=True)
    actual_value = db.Column(db.Text, nullable=True)
    match_status = db.Column(db.Enum(MatchStatus, name='match_status'), nullable=False, default=MatchStatus.NOT_SPECIFIED)
    
    # Additional metadata
    unit_of_measure = db.Column(db.String(50), nullable=True)
    importance_weight = db.Column(db.Numeric(5, 4), nullable=True)  # Weight from 0 to 1
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<SpecComparisonRow {self.parameter_name} - {self.match_status.value}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'contract_result_id': str(self.contract_result_id),
            'parameter_name': self.parameter_name,
            'target_value': self.target_value,
            'actual_value': self.actual_value,
            'match_status': self.match_status.value,
            'unit_of_measure': self.unit_of_measure,
            'importance_weight': float(self.importance_weight) if self.importance_weight else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }