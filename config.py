"""
Configuration settings for Edu-Ride application
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///edu_ride.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SECRET_KEY = 'dev-key-for-development-only'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # SECRET_KEY should be set via environment variable in production

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
