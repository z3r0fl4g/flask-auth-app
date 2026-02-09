"""
Tickets API blueprint.
Fetches user's tickets from our database.
"""
from flask import Blueprint, jsonify, g
from api.clerk_auth import clerk_auth_required
from events.models import Ticket, Order

tickets_bp = Blueprint('tickets', __name__)


@tickets_bp.route('/', methods=['GET'])
@clerk_auth_required
def list_my_tickets():
    """
    Get all tickets for the current user.
    """
    try:
        # Get all orders for the current user
        orders = Order.query.filter_by(
            user_id=g.current_user.id,
            status='completed'
        ).all()

        # Debug: also check for pending orders
        all_orders = Order.query.filter_by(user_id=g.current_user.id).all()
        print(f"[TICKETS] User {g.current_user.id}: {len(all_orders)} total orders, {len(orders)} completed")
        for o in all_orders:
            print(f"  - Order {o.order_number}: status={o.status}, tickets={o.tickets.count()}")

        # Collect all tickets from these orders
        tickets = []
        for order in orders:
            for ticket in order.tickets:
                ticket_data = ticket.to_dict()
                ticket_data['event'] = order.event.to_dict() if order.event else None
                ticket_data['order_number'] = order.order_number
                tickets.append(ticket_data)

        return jsonify({
            'success': True,
            'data': {
                'tickets': tickets
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@tickets_bp.route('/<ticket_code>', methods=['GET'])
@clerk_auth_required
def get_ticket(ticket_code):
    """
    Get a single ticket by code.
    Used for displaying ticket details and QR code.
    """
    try:
        ticket = Ticket.query.filter_by(ticket_code=ticket_code).first()

        if not ticket:
            return jsonify({
                'success': False,
                'message': 'Ticket not found'
            }), 404

        # Verify the ticket belongs to the current user
        if ticket.order.user_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Ticket not found'
            }), 404

        ticket_data = ticket.to_dict()
        ticket_data['event'] = ticket.order.event.to_dict() if ticket.order.event else None
        ticket_data['order_number'] = ticket.order.order_number

        return jsonify({
            'success': True,
            'data': {
                'ticket': ticket_data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
