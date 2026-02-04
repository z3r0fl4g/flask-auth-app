"""
Application configuration module.
Provides environment-based configuration for development and production.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration with common settings."""

    # Flask core
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'd9e6c65c63c2b25041f511bd7ba8158ccb0baca7958b40013365dacf974f83fa')

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'tikepam_session:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@tikepam.com')

    # OAuth credentials
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    INSTAGRAM_CLIENT_ID = os.getenv('INSTAGRAM_CLIENT_ID')
    INSTAGRAM_CLIENT_SECRET = os.getenv('INSTAGRAM_CLIENT_SECRET')
    TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')

    # Twilio (for future SMS support)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

    # Frontend URL (for OAuth callbacks and CORS)
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

    # CORS origins
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:8080,http://localhost:3000').split(',')


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False

    # Database - PostgreSQL for development (fallback to SQLite for backward compatibility)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///auth.db'  # Fallback to SQLite if PostgreSQL not configured
    )

    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Rate limiting storage
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Session cookies (development - less strict)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_DOMAIN = None

    # Logging
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Database - PostgreSQL with connection pooling
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Validate required production settings (checked when config is loaded in app.py)
    @classmethod
    def validate(cls):
        """Validate required production environment variables."""
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable is required in production")
        if not os.getenv('REDIS_URL'):
            raise ValueError("REDIS_URL environment variable is required in production")

    # PostgreSQL connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,  # Verify connections before using
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    }

    # Redis
    REDIS_URL = os.getenv('REDIS_URL')

    # Rate limiting storage
    RATELIMIT_STORAGE_URL = REDIS_URL

    # Session cookies (production - strict security)
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'None'  # Allow cross-origin with HTTPS
    SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN')

    # Logging
    LOG_LEVEL = 'INFO'

    # Additional security headers
    PREFERRED_URL_SCHEME = 'https'


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = False
    TESTING = True

    # In-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Redis (can use fakeredis for testing)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Session cookies
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

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
