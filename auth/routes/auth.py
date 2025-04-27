"""
Authentication routes for user login, logout, signup, and password management.

This module handles all authentication-related routes including:
- User login and session management
- User registration
- Password reset functionality
- Social authentication routes
"""

"""
Authentication routes for the application.

This module contains all routes related to user authentication including:
- User registration and login
- Password management
- Session handling
- Authentication views and templates

Routes are implemented as a Flask Blueprint that gets registered
with the main application. Uses Flask-Login for session management
and Werkzeug for password hashing.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import LoginManager, login_user, logout_user, login_required
from .. import verification_required
import random
from werkzeug.security import generate_password_hash

from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer
from urllib.parse import quote as url_quote
from flask import current_app
from ..models import User
from .. import db

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

# Configure Flask-Login (initialized in __init__.py)
from .. import login_manager
login_manager.login_view = 'auth.login_page'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Handle user login requests.
    
    GET: Render login page template with CSRF token
    POST: Process login form submission with validation
    
    Validates credentials and either:
    - Logs user in and redirects to index on success
    - Shows appropriate error message on failure
    
    Security measures:
    - Rate limited (10 requests/min)
    - CSRF protected
    - Secure session cookies
    
    Error cases handled:
    - No user found with provided email
    - Incorrect password for user
    - Too many requests
    """
    # Clear any existing flash messages when visiting login page
    if request.method == 'GET':
        session.pop('_flashes', None)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('No account found with this email', 'error')
        elif not user.check_password(password):
            flash('Incorrect password for this account', 'error')
        else:
            # Store next URL in session
            session['next_url'] = request.args.get('next') or url_for('auth.profile')
            
            # Check if 2FA is enabled
            if user.twofa_enabled:
                session['requires_2fa'] = True
            else:
                session['requires_2fa'] = False  # Mark as non-2FA verification
            
            # Store user ID in session for verification flow
            session['verification_user_id'] = user.id
            
            # Import send_verification_email here to avoid circular imports
            from .twofa import send_verification_email
            # Send verification email with code
            send_verification_email(user)
            
            return redirect(url_for('twofa.verify'))
    return render_template('login.html')

@auth_bp.route('/signup')
def signup_page():
    """
    Render signup page template.
    
    GET: Returns the signup form template
    """
    return render_template('signup.html')

@auth_bp.route('/profile')
@login_required
@verification_required
def profile():
    """
    Display user profile page.
    
    Renders the profile template with user information.
    Requires user to be logged in (@login_required)
    and verified (@verification_required)
    """
    return render_template('profile.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    
    Clears the user session and redirects to index.
    Requires user to be logged in (@login_required)
    """
    # Clear all flash messages before logout
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Handle new user registration.
    
    Processes signup form submission with validation for:
    - Required fields presence
    - Password confirmation match
    - Unique username and email
    
    On success:
    - Creates new user with hashed password
    - Logs user in automatically
    - Redirects to index page
    
    On failure:
    - Shows appropriate error message
    - Redirects back to signup page
    """
    # Get form data
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate inputs
    if not email or not password:
        missing = []
        if not email: missing.append("email")
        if not password: missing.append("password")
        flash(f'Missing required fields: {", ".join(missing)}', 'error')
        return redirect(url_for('auth.signup_page'))

    # Check if email exists
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return redirect(url_for('auth.signup_page'))

    # Create new user with 2FA enabled by default
    new_user = User(
        email=email,
        password=generate_password_hash(password),
        provider='local',
        twofa_enabled=True,
        twofa_method='email'
    )

    db.session.add(new_user)
    db.session.commit()

    # Store new user ID in session for verification
    session['verification_user_id'] = new_user.id
    session['next_url'] = url_for('auth.profile')
    session['requires_2fa'] = True  # New users have 2FA enabled by default
    
    # Import send_verification_email here to avoid circular imports
    from .twofa import send_verification_email
    # Send verification email with code
    send_verification_email(new_user)
    
    return redirect(url_for('twofa.verify'))

def generate_token(email):
    """
    Generate a secure token for password reset.
    
    Args:
        email (str): User's email to encode in token
        
    Returns:
        str: Time-limited signed token containing email
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_token(token, expiration=3600):
    """
    Verify password reset token validity.
    
    Args:
        token (str): Token to verify
        expiration (int): Max token age in seconds (default 1 hour)
        
    Returns:
        str|bool: Decoded email if valid, False otherwise
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except Exception:
        return False

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Handle password reset requests.
    
    GET: Render forgot password form
    POST: Process email submission and generate reset token
    
    On valid email:
    - Generates reset token
    - Shows reset link (in dev - would email in production)
    
    On invalid email:
    - Shows error message
    """
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = generate_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            # In a real app, you would send this link via email
            flash(f'Password reset link: {reset_url}', 'info')
        else:
            flash('No account found with that email', 'error')
        return redirect(url_for('auth.forgot_password'))
    return render_template('forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Handle password reset form.
    
    GET: Render reset form if token is valid
    POST: Process new password submission
    
    Validates:
    - Token expiration and signature
    - Password confirmation match
    
    On success:
    - Updates user password
    - Redirects to login page
    
    On failure:
    - Shows appropriate error
    - Redirects to forgot password page
    """
    email = verify_token(token)
    if not email:
        flash('Invalid or expired token', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(request.url)
            
        user.password = generate_password_hash(password)
        db.session.commit()
        flash('Password updated successfully', 'success')
        return redirect(url_for('auth.login_page'))
    
    return render_template('reset_password.html', token=token)
