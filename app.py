"""
Main Flask application configuration and routes.

This module serves as the entry point for the Flask web application.
It handles:
- Application initialization and configuration
- Environment variable loading
- Blueprint registration
- Core application routes
- Error handling

The application uses:
- Flask for web framework
- SQLAlchemy for database ORM with Supabase (PostgreSQL)
- Clerk for authentication (JWT-based)
"""

from flask import Flask, render_template, jsonify, g
from flask_mail import Mail
from jinja2 import ChoiceLoader, FileSystemLoader
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

# Import configuration
from config import get_config

# Import initialization functions
from auth import init_auth, db
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

# Initialize extensions (Rate Limiter)
init_extensions(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Database
init_auth(app)

# Import models so SQLAlchemy registers them before create_all
from events.models import Event, TicketTier, Order, Ticket

# Auto-create tables on startup (safe to run multiple times - uses CREATE IF NOT EXISTS)
with app.app_context():
    db.create_all()
    app.logger.info("Database tables created/verified")

# Register API blueprints
from api.auth import api_auth_bp
from api.webhooks import webhook_bp
from api.events import events_bp
from api.checkout import checkout_bp
from api.tickets import tickets_bp
from api.orders import orders_bp
from api.checkin import checkin_bp

app.register_blueprint(api_auth_bp, url_prefix='/api/auth')
app.register_blueprint(webhook_bp, url_prefix='/api/webhooks')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(checkout_bp, url_prefix='/api/checkout')
app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(checkin_bp, url_prefix='/api/checkin')

# Register docs blueprint (for legacy Jinja templates)
from auth.routes.docs import docs_bp
app.register_blueprint(docs_bp, url_prefix='/docs')

app.logger.info("API blueprints registered")


# Context processor for legacy Jinja templates (replaces Flask-Login's current_user)
class AnonymousUser:
    is_authenticated = False
    email = None
    fullname = None
    profile_pic = None

@app.context_processor
def inject_current_user():
    """Provide current_user for legacy Jinja templates."""
    return {'current_user': AnonymousUser()}


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with JSON response."""
    return jsonify({
        'success': False,
        'message': 'Not found',
        'error': 'NOT_FOUND'
    }), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors with JSON response."""
    app.logger.error(f"Internal server error: {e}")
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'error': str(e) if app.debug else 'An unexpected error occurred'
    }), 500


# ============================================
# CORE ROUTES
# ============================================

@app.route('/')
def index():
    """API server index - frontend is served by Vite."""
    return jsonify({
        'success': True,
        'message': 'Tikepam API Server',
        'version': '2.0',
        'frontend': 'http://localhost:5173',
        'endpoints': {
            'auth': '/api/auth',
            'events': '/api/events',
            'checkout': '/api/checkout',
            'orders': '/api/orders',
            'tickets': '/api/tickets',
            'checkin': '/api/checkin',
            'webhooks': '/api/webhooks'
        }
    })


# ============================================
# DATABASE INITIALIZATION
# ============================================

@app.route('/init-db')
def init_database():
    """
    Development endpoint to initialize/migrate database tables.

    Creates all tables defined in SQLAlchemy models.
    Use this after connecting to a new Supabase instance.
    """
    if app.config.get('ENV') == 'production' or app.config.get('FLASK_ENV') == 'production':
        return jsonify({'success': False, 'message': 'Disabled in production'}), 403

    try:
        db.create_all()
        return jsonify({
            'success': True,
            'message': 'Database tables created successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating tables: {str(e)}'
        }), 500


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
