"""
Orders API blueprint.
Fetches user's orders from our database.
"""
from flask import Blueprint, jsonify, g
from api.clerk_auth import clerk_auth_required
from events.models import Order

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['GET'])
@clerk_auth_required
def list_my_orders():
    """
    Get all orders for the current user.
    """
    try:
        orders = Order.query.filter_by(
            user_id=g.current_user.id
        ).order_by(Order.created_at.desc()).all()

        return jsonify({
            'success': True,
            'data': {
                'orders': [o.to_dict() for o in orders]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@orders_bp.route('/<order_number>', methods=['GET'])
@clerk_auth_required
def get_order(order_number):
    """
    Get a single order by order number.
    """
    try:
        order = Order.query.filter_by(order_number=order_number).first()

        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        # Verify ownership
        if order.user_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'order': order.to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
