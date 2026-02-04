from flask import Blueprint, request, session
from flask_login import login_user, current_user

from auth.models import User, db
from auth.routes.twofa import validate_2fa_code, send_verification_email
from .responses import success_response, error_response
from .decorators import api_login_required
from extensions import limiter

api_twofa_bp = Blueprint('api_twofa', __name__)

@api_twofa_bp.route('/verify', methods=['POST'])
def verify():
    """
    POST /api/2fa/verify
    Body: {"code": "123456"}
    """
    if 'verification_user_id' not in session:
        return error_response('No verification in progress', status=400)

    user = User.query.get(session['verification_user_id'])
    if not user:
        return error_response('User not found', status=404)

    code = request.get_json().get('code', '').strip()

    if not validate_2fa_code(user, code):
        return error_response('Invalid or expired code', status=401)

    # Success - log in user
    login_user(user)
    user.twofa_verified = True
    db.session.commit()

    # Clear session data
    session.pop('verification_user_id', None)
    session.pop('requires_2fa', None)

    return success_response(
        data={
            'user': {
                'id': user.id,
                'email': user.email,
                'fullname': user.fullname,
                'provider': user.provider,
                'twofa_enabled': user.twofa_enabled
            }
        },
        message='Verification successful'
    )

@api_twofa_bp.route('/resend', methods=['POST'])
@limiter.limit("3 per hour")
def resend():
    """POST /api/2fa/resend - Rate limited to 3 per hour"""
    user_id = session.get('verification_user_id')
    if not user_id:
        return error_response('No verification in progress', status=400)

    user = User.query.get(user_id)
    if not user:
        return error_response('User not found', status=404)

    send_verification_email(user)

    return success_response(message='New code sent to your email')

@api_twofa_bp.route('/settings', methods=['GET', 'POST'])
@api_login_required
def settings():
    """
    GET /api/2fa/settings - Get current 2FA settings
    POST /api/2fa/settings - Update 2FA settings
    Body: {"enabled": true/false}
    """
    if request.method == 'GET':
        return success_response(data={
            'twofa_enabled': current_user.twofa_enabled,
            'twofa_method': current_user.twofa_method
        })

    # POST - Update settings
    data = request.get_json()
    enable_2fa = data.get('enabled', False)

    current_user.twofa_enabled = enable_2fa

    if enable_2fa:
        current_user.twofa_method = 'email'
        current_user.twofa_verified = False
        send_verification_email(current_user)

        session['verification_user_id'] = current_user.id
        session['requires_2fa'] = True

        db.session.commit()

        return success_response(
            data={'requires_verification': True},
            message='2FA enabled. Check your email for verification code.'
        )
    else:
        current_user.twofa_method = None
        current_user.twofa_verified = True
        db.session.commit()

        return success_response(
            data={'requires_verification': False},
            message='2FA disabled'
        )
