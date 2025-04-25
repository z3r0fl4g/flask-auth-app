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
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    fullname = db.Column(db.String(120))
    password = db.Column(db.String(128))
    provider = db.Column(db.String(20), default='local')
    provider_id = db.Column(db.String(120))
    
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
                provider_id=user_info.get('sub') or user_info.get('id')
            )
            db.session.add(user)
            db.session.commit()
            
        return user
