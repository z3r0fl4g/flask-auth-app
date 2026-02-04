"""Shared Flask extension instances."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from redis import Redis

# Redis client (initialized in app.py after config is loaded)
redis_client = None

# Session management with Redis
session = Session()

# Rate limiter (will be configured with Redis in app.py)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=None  # Set in app.py after config load
)


def init_redis(app):
    """
    Initialize Redis client from app configuration.

    Args:
        app: Flask application instance

    Returns:
        Redis client instance
    """
    global redis_client

    redis_url = app.config.get('REDIS_URL')

    if redis_url:
        try:
            redis_client = Redis.from_url(
                redis_url,
                decode_responses=False,  # Keep binary mode for session data
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            redis_client.ping()
            app.logger.info(f"Redis connected: {redis_url}")
        except Exception as e:
            app.logger.error(f"Redis connection failed: {e}")
            redis_client = None
    else:
        app.logger.warning("REDIS_URL not configured - some features will be limited")
        redis_client = None

    return redis_client


def init_extensions(app):
    """
    Initialize all Flask extensions with app context.

    Args:
        app: Flask application instance
    """
    # Initialize Redis
    init_redis(app)

    # Configure Flask-Session with Redis
    if redis_client:
        app.config['SESSION_REDIS'] = redis_client
        session.init_app(app)
        app.logger.info("Flask-Session initialized with Redis")

    # Configure rate limiter with Redis storage
    if redis_client:
        limiter.storage_uri = app.config.get('RATELIMIT_STORAGE_URL')

    limiter.init_app(app)
    app.logger.info("Rate limiter initialized")

    return app
