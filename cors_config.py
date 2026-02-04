"""
CORS (Cross-Origin Resource Sharing) configuration.
Enables Vue.js frontend to communicate with Flask API.
"""
from flask_cors import CORS


def init_cors(app):
    """
    Configure CORS for the Flask application.

    Allows cross-origin requests from Vue.js frontend with credentials (cookies).
    In development, allows multiple localhost ports for different dev servers.
    In production, restricts to specific frontend domain.
    """
    allowed_origins = app.config.get('CORS_ORIGINS', [
        'http://localhost:5173',  # Vite default port
        'http://localhost:8080',  # Vue CLI default port
        'http://localhost:3000',  # Alternative dev port
    ])

    # In production, use only the configured frontend URL
    if app.config.get('ENV') == 'production' or app.config.get('FLASK_ENV') == 'production':
        frontend_url = app.config.get('FRONTEND_URL')
        if frontend_url:
            allowed_origins = [frontend_url]

    CORS(
        app,
        origins=allowed_origins,
        supports_credentials=True,  # Allow cookies/sessions
        allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
        expose_headers=['Content-Type', 'Authorization'],
        max_age=3600  # Cache preflight requests for 1 hour
    )

    app.logger.info(f"CORS initialized with origins: {allowed_origins}")

    return app
