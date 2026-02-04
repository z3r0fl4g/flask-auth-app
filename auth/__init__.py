from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from functools import wraps
from flask import redirect, url_for
import ssl

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure SSL context using standard library
ssl_context = ssl.create_default_context()

# Custom decorator to require verification
def verification_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.twofa_verified:
            return redirect(url_for('twofa.verify'))
        return f(*args, **kwargs)
    return decorated_function

def init_auth(app):
    """
    Initialize authentication system with database and login manager.

    Database configuration is now handled in config.py and loaded in app.py.
    This allows for environment-based configuration (dev/prod).
    """
    # Initialize database with app
    # Note: SQLALCHEMY_DATABASE_URI and other DB settings come from config
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_page'  # Redirect to login page if not authenticated

    # Initialize migrations
    migrate.init_app(app, db)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))

    app.logger.info(f"Auth system initialized with database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')[:50]}...")
