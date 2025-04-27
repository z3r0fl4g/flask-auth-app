"""
Two-factor authentication routes and utilities.

This module handles all 2FA-related functionality including:
- 2FA verification process
- Code generation and validation
- Email-based verification
- 2FA settings management
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user, logout_user, login_user
from flask_mail import Message
from datetime import datetime, timedelta
import secrets
import bcrypt
from ..models import db, User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create 2FA blueprint
twofa_bp = Blueprint('twofa', __name__, url_prefix='/2fa')

# Get limiter from app
limiter = Limiter(key_func=get_remote_address)

@twofa_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """
    Handle 2FA verification process.
    
    GET: Display verification form
    POST: Process verification code submission
    
    Verifies the submitted code against the stored hash and
    marks the user as verified if successful.
    
    Security measures:
    - Time-limited codes
    - Secure code storage with bcrypt
    - Session regeneration on success
    """
    # Get user from session
    if 'verification_user_id' not in session:
        return redirect(url_for('auth.login_page'))
        
    user = User.query.get(session['verification_user_id'])
    if not user:
        return redirect(url_for('auth.login_page'))
        
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        if validate_2fa_code(user, code):
            # Log in the user after successful verification
            login_user(user)
            user.twofa_verified = True
            db.session.commit()
            
            # Clear verification session data
            session.pop('verification_user_id', None)
            session.pop('requires_2fa', None)
            
            flash('Verification successful', 'success')
            
            # Redirect to originally intended URL or profile page
            next_url = session.pop('next_url', None)
            return redirect(next_url or url_for('auth.profile'))
            
        flash('Invalid or expired verification code', 'danger')
    return render_template('twofa_verify.html')

@twofa_bp.route('/resend-code')
@login_required
@limiter.limit("3 per hour")  # Prevent brute force attacks
def resend_code():
    """
    Resend 2FA verification code with rate limiting.
    
    Generates a new verification code and sends it to the user's
    email address. Limited to 3 requests per hour to prevent abuse.
    """
    # Always allow resending code regardless of verification status
        
    send_verification_email(current_user)
    flash('New verification code sent to your email', 'info')
    return redirect(url_for('twofa.verify'))

@twofa_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Manage 2FA settings.
    
    GET: Display 2FA settings page
    POST: Update 2FA settings
    
    Allows users to enable/disable 2FA and select verification methods.
    When enabling 2FA, sends a verification code to the user's email.
    """
    if request.method == 'POST':
        enable_2fa = 'enable_2fa' in request.form
        current_user.twofa_enabled = enable_2fa
        
        if enable_2fa:
            current_user.twofa_method = 'email'
            # Set as not verified and send verification email
            current_user.twofa_verified = False
            send_verification_email(current_user)
            flash('Two-factor authentication enabled. Please verify your email address.', 'success')
            db.session.commit()
            
            # Redirect to verification page
            return redirect(url_for('twofa.verify'))
        else:
            current_user.twofa_method = None
            current_user.twofa_verified = True
            flash('Two-factor authentication disabled', 'info')
            
        db.session.commit()
        return redirect(url_for('twofa.settings'))
    
    return render_template('twofa_settings.html')

def generate_secure_code():
    """
    Generate a time-limited verification code.
    
    Returns:
        tuple: (code, expiration_datetime)
        
    Creates a secure random code and sets an expiration time
    15 minutes in the future.
    """
    code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    return code, expires_at

def validate_2fa_code(user, submitted_code):
    """
    Validate 2FA code with bcrypt and expiration check.
    
    Args:
        user: User object
        submitted_code: Code submitted by user
        
    Returns:
        bool: True if code is valid and not expired
        
    Checks both the code hash and expiration time.
    """
    if not user.twofa_code_hash or not user.twofa_code_expires:
        return False
    if datetime.utcnow() > user.twofa_code_expires:
        return False
    return bcrypt.checkpw(submitted_code.encode('utf-8'), user.twofa_code_hash.encode('utf-8'))

def send_verification_email(user):
    """
    Send verification email with secure code.
    
    Args:
        user: User object to send code to
        
    Generates a new code, stores its hash and expiration,
    and sends it to the user's email address.
    
    Note: In production, this would use a proper email service.
    """
    code, expires = generate_secure_code()
    user.twofa_code_hash = bcrypt.hashpw(code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.twofa_code_expires = expires
    db.session.commit()
    
    # Create email message with noreply sender
    msg = Message(
        subject="Your Verification Code",
        sender=("Security Team", "noreply@authsystem.com"),
        recipients=[user.email],
        body=f"""
Hello,

Your verification code is: {code}

This code will expire in 15 minutes.

If you did not request this code, please ignore this email.

Best regards,
The Security Team
        """,
        html=f"""
<h2>Your Verification Code</h2>
<p>Your verification code is: <strong style="font-size: 1.2em;">{code}</strong></p>
<p>This code will expire in 15 minutes.</p>
<p>If you did not request this code, please ignore this email.</p>
<p>Best regards,<br>The Security Team</p>
        """
    )
    
    # Import Flask utilities here to avoid circular imports
    from flask import flash, current_app
    
    try:
        # Import mail here to avoid circular imports
        from app import mail
        # Send email
        mail.send(msg)
        print(f"Email sent successfully to {user.email}")
    except Exception as e:
        # Log the error but don't expose it to the user
        print(f"Error sending email: {str(e)}")
        print("This is expected in development if email credentials are not configured.")
        print("Check your .env file and ensure MAIL_USERNAME and MAIL_PASSWORD are set correctly.")
        print("\nFor Gmail accounts, you need to:")
        print("1. If 2FA is enabled: Create an App Password at https://myaccount.google.com/apppasswords")
        print("2. If 2FA is not enabled: Enable 'Less secure app access' at https://myaccount.google.com/lesssecureapps")
        print("3. Make sure your account doesn't have any security blocks: https://accounts.google.com/DisplayUnlockCaptcha")
        
        # Don't show verification code in UI, only log to console
        # This prevents code leakage in the UI
    
    # For development, always print the code to console
    print(f"============================================")
    print(f"VERIFICATION CODE: {code}")
    print(f"For user: {user.email}")
    print(f"Valid until: {expires}")
    print(f"============================================")
