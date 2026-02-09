"""
Application configuration module.
Provides environment-based configuration for development and production.
"""
import os


class Config:
    """Base configuration with common settings."""

    # Flask core
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'd9e6c65c63c2b25041f511bd7ba8158ccb0baca7958b40013365dacf974f83fa')

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clerk authentication
    CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
    CLERK_WEBHOOK_SECRET = os.getenv('CLERK_WEBHOOK_SECRET')

    # Email configuration (for transactional emails, not auth)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@tikepam.com')

    # Frontend URL (for CORS)
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

    # CORS origins
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:8080,http://localhost:3000').split(',')


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False

    # Email - Log to console in development (no SMTP needed)
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', 'False').lower() == 'true'

    # Database - Supabase PostgreSQL (or local SQLite fallback)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///auth.db'  # Fallback to SQLite if Supabase not configured
    )

    # Logging
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Database - Supabase PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Validate required production settings
    @classmethod
    def validate(cls):
        """Validate required production environment variables."""
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable is required in production")
        if not os.getenv('CLERK_SECRET_KEY'):
            raise ValueError("CLERK_SECRET_KEY environment variable is required in production")

    # PostgreSQL connection pooling for Supabase
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    }

    # Logging
    LOG_LEVEL = 'INFO'

    # Security
    PREFERRED_URL_SCHEME = 'https'


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = False
    TESTING = True

    # In-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Logging
    LOG_LEVEL = 'ERROR'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    return config.get(env, config['default'])
