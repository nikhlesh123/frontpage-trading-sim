import os
from datetime import timedelta

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///trading_sim.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # AngelOne API Configuration
    # IMPORTANT: Users must obtain their own API credentials from AngelOne
    # These are placeholder values and will not work without proper authentication
    ANGELONE_API_KEY = os.environ.get('ANGELONE_API_KEY') or 'YOUR_API_KEY_HERE'  # User must provide
    ANGELONE_CLIENT_CODE = os.environ.get('ANGELONE_CLIENT_CODE') or 'YOUR_CLIENT_CODE_HERE'  # User must provide
    ANGELONE_PASSWORD = os.environ.get('ANGELONE_PASSWORD') or 'YOUR_PASSWORD_HERE'  # User must provide
    ANGELONE_TOTP = os.environ.get('ANGELONE_TOTP') or 'YOUR_TOTP_SECRET_HERE'  # User must provide
    
    # Redis Configuration for Celery
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
