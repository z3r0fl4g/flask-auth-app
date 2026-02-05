"""
Authentication API endpoints.

Provides endpoints for getting current user information.
Authentication is handled by Clerk (JWT tokens).
"""

from flask import Blueprint, g

from .clerk_auth import clerk_auth_required, clerk_auth_optional
from .responses import success_response, error_response

api_auth_bp = Blueprint('api_auth', __name__)


@api_auth_bp.route('/me', methods=['GET'])
@clerk_auth_required
def get_current_user():
    """
    GET /api/auth/me

    Returns the current authenticated user's profile.
    Requires a valid Clerk JWT token in the Authorization header.

    Returns:
        JSON: User profile data
    """
    user = g.current_user

    return success_response(
        data={
            'user': user.to_dict()
        }
    )


@api_auth_bp.route('/session', methods=['GET'])
@clerk_auth_optional
def check_session():
    """
    GET /api/auth/session

    Check if the current request has a valid session.
    Returns user data if authenticated, null otherwise.

    Returns:
        JSON: Authentication status and user data if authenticated
    """
    if g.current_user:
        return success_response(
            data={
                'authenticated': True,
                'user': g.current_user.to_dict()
            }
        )

    return success_response(
        data={
            'authenticated': False,
            'user': None
        }
    )
