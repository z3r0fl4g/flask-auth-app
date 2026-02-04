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
- SQLAlchemy for database ORM with PostgreSQL
- Redis for sessions and caching
- Flask-Login for authentication
- OAuthLib for third-party authentication
- Celery for background tasks
"""

from flask import Flask, render_template, jsonify
from flask_mail import Mail
from jinja2 import ChoiceLoader, FileSystemLoader
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

# Import configuration
from config import get_config

# Import blueprints
from auth.routes.oauth import oauth_bp, init_oauth
from auth.routes.auth import auth_bp
from auth.routes.twofa import twofa_bp
from auth.routes.docs import docs_bp

# Import initialization functions
from auth import init_auth
from extensions import init_extensions
from cors_config import init_cors

# Create Flask app
app = Flask(__name__, template_folder='auth/templates')

# Load configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
config_class = get_config(env)
app.config.from_object(config_class)

app.logger.info(f"Starting Flask application in {env} mode")

# Extend template search path to include global templates directory
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('templates'),
    app.jinja_loader,
])

# Initialize CORS (must be done early)
init_cors(app)

# Initialize extensions (Redis, Session, Rate Limiter)
init_extensions(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Auth and Database
init_auth(app)

# Initialize OAuth
init_oauth(app)

# Register existing blueprints (template-based routes)
app.register_blueprint(oauth_bp, url_prefix='/auth')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(twofa_bp, url_prefix='/auth/2fa')
app.register_blueprint(docs_bp, url_prefix='/docs')

# Register API blueprints for Vue.js frontend
from api.auth import api_auth_bp
from api.twofa import api_twofa_bp

app.register_blueprint(api_auth_bp, url_prefix='/api/auth')
app.register_blueprint(api_twofa_bp, url_prefix='/api/2fa')

app.logger.info("API blueprints registered for Vue.js frontend")

# TODO: Register additional API blueprints (Phase 5)
# from api.user import api_user_bp
# app.register_blueprint(api_user_bp, url_prefix='/api/user')


# ============================================
# ERROR HANDLERS
# ============================================

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


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handle 500 errors with JSON response for API or HTML for web.

    Args:
        e: The error object

    Returns:
        Response: JSON or HTML error response
    """
    app.logger.error(f"Internal server error: {e}")

    # Check if it's an API request
    from flask import request
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e) if app.debug else 'An unexpected error occurred'
        }), 500

    return render_template('404.html'), 500  # You can create a 500.html template


# ============================================
# CORE ROUTES
# ============================================

@app.route('/')
def index():
    """
    Render the main application index page.

    Returns:
        Response: Rendered index.html template with base layout
    """
    return render_template('index.html')


# ============================================
# DEVELOPMENT UTILITIES
# ============================================

@app.route('/create_test_user')
def create_test_user():
    """
    Development endpoint to create a test user.

    Creates a user with:
    - Email: testuser@example.com
    - Password: test123

    Returns:
        str: Confirmation message about user creation

    Note:
        Only for development use - should be removed or protected in production
    """
    # Only allow in development mode
    if app.config.get('ENV') == 'production' or app.config.get('FLASK_ENV') == 'production':
        return "This endpoint is disabled in production", 403

    from auth.models import User
    from auth import db
    from werkzeug.security import generate_password_hash

    test_username = "testuser"
    test_email = "testuser@example.com"
    test_password = "test123"

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == test_username) | (User.email == test_email)
    ).first()
    if existing_user:
        return f"User already exists: {test_email}/{test_password}"

    # Create new user with hashed password
    user = User(
        username=test_username,
        email=test_email,
        password=generate_password_hash(test_password),
        provider='local',
        twofa_enabled=False,
        twofa_verified=True  # Skip 2FA for test user
    )
    db.session.add(user)
    db.session.commit()

    return f"Test user created: {test_email}/{test_password}"


# ============================================
# LEGACY API ENDPOINT (To be migrated to api/user.py)
# ============================================

@app.route('/api/appointments/book', methods=['POST'])
# Rate limiter will be initialized from extensions
def book_appointment():
    """
    API endpoint to book an appointment for the current user.

    Returns:
        JSON: Success message or error details

    Note:
        Requires user authentication
        This is a placeholder - will be migrated to proper API structure
    """
    from flask_login import current_user
    from extensions import limiter
    from datetime import datetime, timedelta

    # Apply rate limiting
    @limiter.limit("5 per minute")
    def _book():
        # Check if user is authenticated
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': 'Please log in to book an appointment'
            }), 401

        try:
            # Generate a mock appointment time (next available slot)
            appointment_time = datetime.now() + timedelta(days=1)
            appointment_time_str = appointment_time.strftime('%Y-%m-%d at %I:%M %p')

            # In a real application, you would:
            # 1. Check availability in the database
            # 2. Create an appointment record
            # 3. Send confirmation email (via Celery)
            # 4. Add to calendar

            return jsonify({
                'success': True,
                'message': f'Appointment booked successfully for {appointment_time_str}',
                'data': {
                    'appointment_time': appointment_time.isoformat(),
                    'confirmation_id': f'APPT-{datetime.now().strftime("%Y%m%d%H%M%S")}'
                }
            }), 200

        except Exception as e:
            app.logger.error(f"Error booking appointment: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': 'Failed to book appointment. Please try again later.'
            }), 500

    return _book()


# ============================================
# APPLICATION ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Development server
    # In production, use Gunicorn: gunicorn -c gunicorn.conf.py app:app
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001))
    )
