from flask import Blueprint, request, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash

from auth.models import User, db
from auth.routes.auth import (
    normalize_email, is_valid_email, is_secure_password,
    generate_token, verify_token
)
from .responses import success_response, error_response, validation_error
from .decorators import api_login_required

api_auth_bp = Blueprint('api_auth', __name__)

@api_auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    POST /api/auth/signup
    Body: {"email": "user@example.com", "password": "Pass123", "fullname": "John Doe"}
    Returns: {success: true, data: {user}, requires_2fa: bool}
    """
    data = request.get_json()

    # Validate input
    email = normalize_email(data.get('email', ''))
    password = data.get('password', '')
    fullname = data.get('fullname', '')

    if not is_valid_email(email):
        return error_response('Invalid email address', status=422)

    if not is_secure_password(password):
        return error_response(
            'Password must be at least 8 characters with letter and number',
            status=422
        )

    # Check if user exists
    if User.query.filter_by(email=email).first():
        return error_response('Email already registered', status=409)

    # Create user
    user = User(
        email=email,
        password=generate_password_hash(password),
        fullname=fullname,
        provider='local',
        twofa_enabled=True,  # Enable by default
        twofa_method='email'
    )
    db.session.add(user)
    db.session.commit()

    # Set up 2FA verification
    session['verification_user_id'] = user.id
    session['requires_2fa'] = True

    # Send verification email (reuse existing function)
    from auth.routes.twofa import send_verification_email
    send_verification_email(user)

    return success_response(
        data={'requires_2fa': True, 'email': user.email},
        message='Account created. Check email for verification code.',
        status=201
    )

@api_auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /api/auth/login
    Body: {"email": "user@example.com", "password": "Pass123"}
    Returns: {success: true, data: {user}, requires_2fa: bool}
    """
    data = request.get_json()

    email = normalize_email(data.get('email', ''))
    password = data.get('password', '')

    # Validate
    if not is_valid_email(email) or not is_secure_password(password):
        return error_response('Invalid credentials', status=401)

    # Find user
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return error_response('Invalid credentials', status=401)

    # Check if 2FA required
    if user.twofa_enabled:
        session['verification_user_id'] = user.id
        session['requires_2fa'] = True

        # Send verification code
        from auth.routes.twofa import send_verification_email
        send_verification_email(user)

        return success_response(
            data={'requires_2fa': True, 'email': user.email},
            message='Verification code sent to your email'
        )

    # No 2FA - log in directly
    login_user(user)
    user.twofa_verified = True
    db.session.commit()

    return success_response(
        data={
            'requires_2fa': False,
            'user': {
                'id': user.id,
                'email': user.email,
                'fullname': user.fullname,
                'provider': user.provider,
                'twofa_enabled': user.twofa_enabled
            }
        },
        message='Login successful'
    )

@api_auth_bp.route('/logout', methods=['POST'])
@api_login_required
def logout():
    """POST /api/auth/logout"""
    logout_user()
    session.clear()
    return success_response(message='Logged out successfully')

@api_auth_bp.route('/session', methods=['GET'])
def check_session():
    """
    GET /api/auth/session
    Returns current user if authenticated, null otherwise
    """
    if current_user.is_authenticated:
        return success_response(
            data={
                'authenticated': True,
                'user': {
                    'id': current_user.id,
                    'email': current_user.email,
                    'fullname': current_user.fullname,
                    'provider': current_user.provider,
                    'profile_pic': current_user.profile_pic,
                    'twofa_enabled': current_user.twofa_enabled,
                    'twofa_verified': current_user.twofa_verified
                }
            }
        )
    return success_response(data={'authenticated': False})

@api_auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    POST /api/auth/forgot-password
    Body: {"email": "user@example.com"}
    """
    data = request.get_json()
    email = normalize_email(data.get('email', ''))

    if not is_valid_email(email):
        return error_response('Invalid email address', status=422)

    user = User.query.filter_by(email=email).first()

    # Security: Always return success even if user doesn't exist
    if user:
        token = generate_token(email)
        # TODO: Send password reset email (implement in Phase 5)
        # For now, log token to console
        print(f"Password reset token for {email}: {token}")

    return success_response(
        message='If an account exists, a password reset link has been sent'
    )

@api_auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    POST /api/auth/reset-password
    Body: {"token": "xyz", "password": "NewPass123"}
    """
    data = request.get_json()
    token = data.get('token', '')
    password = data.get('password', '')

    # Verify token
    email = verify_token(token)
    if not email:
        return error_response('Invalid or expired reset link', status=400)

    # Validate password
    if not is_secure_password(password):
        return error_response(
            'Password must be at least 8 characters with letter and number',
            status=422
        )

    # Update password
    user = User.query.filter_by(email=email).first()
    if not user:
        return error_response('User not found', status=404)

    user.password = generate_password_hash(password)
    db.session.commit()

    return success_response(message='Password reset successful')
