"""
User model representing application users.

Handles both local and OAuth authentication with:
- Core user attributes (username, email, password)
- OAuth provider integration fields
- Password hashing and verification
- User creation/lookup methods
"""

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    """
    User database model with authentication capabilities.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username
        email (str): Unique email address
        fullname (str): User's full name
        password (str): Hashed password (empty for OAuth users)
        provider (str): Auth provider ('local' or OAuth service name)
        provider_id (str): Unique ID from OAuth provider
        profile_pic (str): URL to user's profile picture
        twofa_enabled (bool): Whether 2FA is enabled for this user
        twofa_method (str): 2FA method (email, app, etc.)
        twofa_secret (str): Secret key for 2FA (for authenticator apps)
        twofa_code_hash (str): Hash of current verification code
        twofa_code_expires (datetime): Expiration time of verification code
        twofa_verified (bool): Whether user has completed 2FA verification
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    fullname = db.Column(db.String(120))
    password = db.Column(db.String(128))
    provider = db.Column(db.String(20), default='local')
    provider_id = db.Column(db.String(120))
    profile_pic = db.Column(db.String(500), nullable=True)  # URL to profile picture
    
    # Two-factor authentication fields
    twofa_enabled = db.Column(db.Boolean, default=False)
    twofa_method = db.Column(db.String(10), nullable=True)
    twofa_secret = db.Column(db.String(128), nullable=True)
    twofa_code_hash = db.Column(db.String(128), nullable=True)
    twofa_code_expires = db.Column(db.DateTime, nullable=True)
    twofa_verified = db.Column(db.Boolean, default=True)  # Default True for backward compatibility
    
    def check_password(self, password):
        """
        Verify password against stored hash.
        
        Args:
            password (str): Plaintext password to verify
            
        Returns:
            bool: True if password matches hash, False otherwise
            
        Note:
            For OAuth users (empty password), always returns False
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    @staticmethod
    def get_or_create(provider, user_info):
        """
        Find or create user based on OAuth provider data.
        
        Args:
            provider (str): OAuth provider name (e.g. 'google')
            user_info (dict): User data from OAuth provider
            
        Returns:
            User: Existing or newly created user instance
            
        Handles:
            - User lookup by provider ID
            - New user creation with OAuth data
            - Automatic commit of new users
        """
        # Check if user exists
        user = User.query.filter_by(
            provider=provider,
            provider_id=user_info.get('sub') or user_info.get('id')
        ).first()
        
        if not user:
            # Create new user
            user = User(
                username=user_info.get('email'),  # Use email as username for OAuth users
                email=user_info.get('email'),
                fullname=user_info.get('name'),
                password='',  # OAuth users don't need password
                provider=provider,
                provider_id=user_info.get('sub') or user_info.get('id'),
                twofa_verified=True  # New OAuth users don't need 2FA verification initially
            )
            
            # Add profile picture if available
            if user_info.get('picture'):
                user.profile_pic = user_info.get('picture')
                
            db.session.add(user)
            db.session.commit()
            
        return user
