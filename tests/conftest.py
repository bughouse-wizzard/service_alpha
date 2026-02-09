import pytest
from app import create_app, db
from app.models import SearchRequest, ContractResult, SpecComparisonRow
from config import TestConfig

@pytest.fixture(scope='module')
def test_app():
    """Create a Flask app for testing."""
    app = create_app(TestConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_db(test_app):
    """Create a test database."""
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def session(test_db):
    """Create a new database session for a test."""
    connection = test_db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = test_db._make_scoped_session(options=options)
    
    test_db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()