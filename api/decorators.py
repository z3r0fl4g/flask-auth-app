from functools import wraps
from flask import jsonify
from flask_login import current_user

def api_login_required(f):
    """API version of login_required - returns JSON instead of redirect"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': 'Authentication required',
                'error': 'UNAUTHORIZED'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def api_verification_required(f):
    """API version of verification_required for 2FA"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': 'Authentication required',
                'error': 'UNAUTHORIZED'
            }), 401
        if not current_user.twofa_verified:
            return jsonify({
                'success': False,
                'message': '2FA verification required',
                'error': 'VERIFICATION_REQUIRED'
            }), 403
        return f(*args, **kwargs)
    return decorated_function
