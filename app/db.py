from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import String, Text, TypeDecorator
import uuid
import json

db = SQLAlchemy()

# SQLite compatibility layer
class SQLiteJSON(TypeDecorator):
    """JSON type for SQLite that stores as TEXT and loads as dict/list"""
    impl = Text
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

class SQLiteUUID(TypeDecorator):
    """UUID type for SQLite that stores as TEXT and loads as UUID"""
    impl = String(36)
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == 'postgresql':
            return value
        else:
            return str(value) if isinstance(value, uuid.UUID) else value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if dialect.name == 'postgresql':
            return value
        else:
            return uuid.UUID(value) if value else None

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
    
    return db