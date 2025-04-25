"""
Database initialization script

Handles:
- Database schema creation
- Schema reset (drop & recreate)
- Should be run during initial setup or when schema changes
"""

from app import app
from auth.models import db

def initialize_database():
    """
    Initialize the database by dropping and recreating all tables.
    
    WARNING: This will delete all existing data!
    Should only be used during development or initial setup.
    
    Usage:
    - Called directly when script is run
    - Can be imported and called from other modules
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    """Entry point for direct script execution"""
    initialize_database()
