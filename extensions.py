"""Shared Flask extension instances."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Rate limiter with in-memory storage (no Redis needed)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def init_extensions(app):
    """
    Initialize Flask extensions with app context.

    Args:
        app: Flask application instance
    """
    limiter.init_app(app)
    app.logger.info("Rate limiter initialized with in-memory storage")

    return app
