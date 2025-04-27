"""
Run database migrations to update the schema.

This script applies all pending Alembic migrations to bring
the database schema up to date with the current models.
"""

from app import app
from flask_migrate import upgrade

def run_migrations():
    """
    Run all pending database migrations.
    
    Uses Flask-Migrate's upgrade command to apply all migrations
    that haven't been applied yet.
    """
    with app.app_context():
        # Run migrations
        upgrade()
        print("Migrations applied successfully!")

if __name__ == '__main__':
    run_migrations()
