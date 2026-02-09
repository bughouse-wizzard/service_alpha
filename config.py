import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///service_alpha.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 't')
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'