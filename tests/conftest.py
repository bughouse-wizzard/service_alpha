import pytest
import os
import tempfile
from flask import Flask
from app.db import db, init_db
from config import Config


@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Create test config
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
    
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    
    # Initialize database
    with app.app_context():
        init_db(app)
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def database(app):
    """Provide database session"""
    with app.app_context():
        yield db