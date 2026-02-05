"""
Authentication module initialization.

Database and migration setup for the auth system.
Authentication is now handled by Clerk (JWT-based).
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_auth(app):
    """
    Initialize database for the application.

    Database configuration is handled in config.py and loaded in app.py.
    Authentication is handled by Clerk - no Flask-Login needed.
    """
    # Initialize database with app
    db.init_app(app)

    # Initialize migrations
    migrate.init_app(app, db)

    # Import models to register them with SQLAlchemy
    from .models import User  # noqa: F401

    app.logger.info(f"Database initialized: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')[:50]}...")
