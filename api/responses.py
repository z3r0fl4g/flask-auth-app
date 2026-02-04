from flask import jsonify

def success_response(data=None, message=None, status=200):
    """Standardized success response"""
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status

def error_response(message, errors=None, status=400):
    """Standardized error response"""
    response = {'success': False, 'message': message}
    if errors:
        response['errors'] = errors
    return jsonify(response), status

def validation_error(errors, status=422):
    """Validation error response"""
    return jsonify({
        'success': False,
        'message': 'Validation failed',
        'errors': errors
    }), status
