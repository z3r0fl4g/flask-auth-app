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
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
        
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
