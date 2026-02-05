"""
User model representing application users.

Handles Clerk-authenticated users with:
- Core user attributes (email, fullname)
- Clerk ID for auth sync
- Profile picture
"""

from . import db


class User(db.Model):
    """
    User database model synced from Clerk via webhooks.

    Attributes:
        id (int): Primary key
        clerk_id (str): Unique Clerk user ID (from webhook)
        email (str): Unique email address
        fullname (str): User's full name
        profile_pic (str): URL to user's profile picture
        created_at (datetime): When the user was created
        updated_at (datetime): When the user was last updated
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    clerk_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120))
    profile_pic = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def get_by_clerk_id(clerk_id):
        """Find user by Clerk ID."""
        return User.query.filter_by(clerk_id=clerk_id).first()

    @staticmethod
    def get_or_create_from_clerk(clerk_user_data):
        """
        Find or create user based on Clerk webhook data.

        Args:
            clerk_user_data (dict): User data from Clerk webhook

        Returns:
            User: Existing or newly created user instance
        """
        clerk_id = clerk_user_data.get('id')
        user = User.query.filter_by(clerk_id=clerk_id).first()

        if not user:
            # Extract email from Clerk's email_addresses array
            email_addresses = clerk_user_data.get('email_addresses', [])
            primary_email = next(
                (e['email_address'] for e in email_addresses if e.get('id') == clerk_user_data.get('primary_email_address_id')),
                email_addresses[0]['email_address'] if email_addresses else None
            )

            user = User(
                clerk_id=clerk_id,
                email=primary_email,
                fullname=f"{clerk_user_data.get('first_name', '')} {clerk_user_data.get('last_name', '')}".strip(),
                profile_pic=clerk_user_data.get('image_url')
            )
            db.session.add(user)
            db.session.commit()

        return user

    def update_from_clerk(self, clerk_user_data):
        """
        Update user fields from Clerk webhook data.

        Args:
            clerk_user_data (dict): User data from Clerk webhook
        """
        email_addresses = clerk_user_data.get('email_addresses', [])
        primary_email = next(
            (e['email_address'] for e in email_addresses if e.get('id') == clerk_user_data.get('primary_email_address_id')),
            email_addresses[0]['email_address'] if email_addresses else self.email
        )

        self.email = primary_email
        self.fullname = f"{clerk_user_data.get('first_name', '')} {clerk_user_data.get('last_name', '')}".strip()
        self.profile_pic = clerk_user_data.get('image_url')
        db.session.commit()

    def to_dict(self):
        """Return user as dictionary for API responses."""
        return {
            'id': self.id,
            'clerk_id': self.clerk_id,
            'email': self.email,
            'fullname': self.fullname,
            'profile_pic': self.profile_pic
        }
