"""
Clerk authentication middleware for Flask.

Provides a decorator to verify Clerk JWT tokens and load the local user.
"""

import os
from functools import wraps
from flask import request, g, jsonify
import jwt
from jwt import PyJWKClient

from auth.models import User

# Clerk JWKS URL for verifying tokens
CLERK_JWKS_URL = "https://{}.clerk.accounts.dev/.well-known/jwks.json"


def get_clerk_jwks_client():
    """Get the JWKS client for Clerk token verification."""
    # Extract the Clerk instance ID from the publishable key or use environment variable
    clerk_publishable_key = os.getenv('VITE_CLERK_PUBLISHABLE_KEY', '')

    # Publishable key format: pk_test_xxx or pk_live_xxx
    # The frontend ID is in the key, but we need the instance ID from secret key
    # For now, we'll use the Clerk Backend SDK approach
    return None


def verify_clerk_token(token):
    """
    Verify a Clerk JWT token and return the payload.

    Args:
        token: The JWT token from the Authorization header

    Returns:
        dict: The decoded token payload, or None if invalid
    """
    try:
        # Clerk tokens are JWTs that can be verified with the secret key
        # or using JWKS endpoint. We'll use the secret key approach.
        clerk_secret = os.getenv('CLERK_SECRET_KEY', '')

        if not clerk_secret:
            print("CLERK_SECRET_KEY not configured")
            return None

        # Clerk uses RS256 algorithm with JWKS
        # We need to fetch the public key from Clerk's JWKS endpoint
        # The issuer is based on your Clerk instance

        # First, decode without verification to get the header
        unverified = jwt.decode(token, options={"verify_signature": False})
        issuer = unverified.get('iss', '')

        if not issuer:
            return None

        # Fetch JWKS from Clerk
        jwks_url = f"{issuer}/.well-known/jwks.json"
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Verify and decode the token
        # leeway allows for clock skew between servers (common in WSL/VMs)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=issuer,
            leeway=60,  # Allow 60 seconds of clock skew
            options={"verify_aud": False}  # Clerk doesn't always set audience
        )

        return payload

    except jwt.ExpiredSignatureError:
        print("Clerk token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid Clerk token: {e}")
        return None
    except Exception as e:
        print(f"Error verifying Clerk token: {e}")
        return None


def clerk_auth_required(f):
    """
    Decorator to require Clerk authentication for an endpoint.

    Verifies the JWT token from the Authorization header,
    looks up the local user by clerk_id, and sets g.current_user.

    Returns 401 if token is invalid or user not found.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'No authorization token provided',
                'error': 'UNAUTHORIZED'
            }), 401

        token = auth_header.replace('Bearer ', '')

        # Verify the token
        payload = verify_clerk_token(token)

        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token',
                'error': 'UNAUTHORIZED'
            }), 401

        # Get the Clerk user ID from the token (it's in the 'sub' claim)
        clerk_user_id = payload.get('sub')

        if not clerk_user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid token: no user ID',
                'error': 'UNAUTHORIZED'
            }), 401

        # Look up the local user
        user = User.get_by_clerk_id(clerk_user_id)

        if not user:
            # User exists in Clerk but not synced to local DB yet
            # This can happen if webhook hasn't fired yet
            return jsonify({
                'success': False,
                'message': 'User not found. Please wait for account sync.',
                'error': 'USER_NOT_SYNCED'
            }), 401

        # Set the current user on the request context
        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function


def clerk_auth_optional(f):
    """
    Decorator that attempts Clerk authentication but doesn't require it.

    If a valid token is provided, sets g.current_user.
    If no token or invalid token, g.current_user will be None.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.current_user = None

        auth_header = request.headers.get('Authorization', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
            payload = verify_clerk_token(token)

            if payload:
                clerk_user_id = payload.get('sub')
                if clerk_user_id:
                    g.current_user = User.get_by_clerk_id(clerk_user_id)

        return f(*args, **kwargs)

    return decorated_function
