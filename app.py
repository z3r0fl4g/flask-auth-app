"""
Main Flask application configuration and routes.

This module serves as the entry point for the Flask web application.
It handles:
- Application initialization and configuration
- Environment variable loading
- Blueprint registration for auth and OAuth routes
- Core application routes
- Error handling
- Development utilities

The application uses:
- Flask for web framework
- SQLAlchemy for database ORM
- Flask-Login for authentication
- OAuthLib for third-party authentication
- dotenv for environment management
"""

from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from auth.routes.oauth import oauth_bp, init_oauth
from auth.routes.auth import auth_bp
from auth.routes.twofa import twofa_bp
from auth.routes.docs import docs_bp
from auth import init_auth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='auth/templates')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise ValueError("No FLASK_SECRET_KEY set in environment variables")

# Load OAuth provider credentials
app.config.update(
    GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID'),
    GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET'),
    GITHUB_CLIENT_ID=os.getenv('GITHUB_CLIENT_ID'),
    GITHUB_CLIENT_SECRET=os.getenv('GITHUB_CLIENT_SECRET'),
    INSTAGRAM_CLIENT_ID=os.getenv('INSTAGRAM_CLIENT_ID'),
    INSTAGRAM_CLIENT_SECRET=os.getenv('INSTAGRAM_CLIENT_SECRET'),
    TWITTER_CLIENT_ID=os.getenv('TWITTER_CLIENT_ID'),
    TWITTER_CLIENT_SECRET=os.getenv('TWITTER_CLIENT_SECRET')
)

# Configure email settings
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', 'yes', '1'),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')
)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Auth and Database
init_auth(app)

# Initialize OAuth
init_oauth(app)

# Register blueprints
app.register_blueprint(oauth_bp, url_prefix='/auth')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(twofa_bp, url_prefix='/auth/2fa')
app.register_blueprint(docs_bp, url_prefix='/docs')

@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors by rendering a custom 404 page.
    
    Args:
        e: The error object
        
    Returns:
        Response: Rendered 404.html template with 404 status code
    """
    return render_template('404.html'), 404

@app.route('/')
def index():
    """
    Render the main application index page.
    
    Returns:
        Response: Rendered index.html template with base layout
    """
    return render_template('index.html')

@app.route('/create_test_user')
def create_test_user():
    """
    Development endpoint to create a test user.
    
    Creates a user with:
    - Username: testuser
    - Password: test123
    
    Returns:
        str: Confirmation message about user creation
    
    Note:
        Only for development use - remove in production
    """
    from auth.models import User
    from auth import db
    from flask import current_app
    
    with current_app.app_context():
        test_username = "testuser"
        test_password = "test123"
        
        # Check if user already exists
        user = User.query.filter_by(username=test_username).first()
        if user:
            return f"User already exists: {test_username}/{test_password}"
            
        # Create new user
        user = User(
            username=test_username,
            password=test_password
        )
        db.session.add(user)
        db.session.commit()
        
        return f"Test user created: {test_username}/{test_password}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
