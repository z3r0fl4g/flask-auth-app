"""
Check-in API blueprint.
Validates and marks tickets as used at the event.
"""
from flask import Blueprint, jsonify, request, g
from datetime import datetime
from api.clerk_auth import clerk_auth_required
from events.models import Ticket
from auth import db

checkin_bp = Blueprint('checkin', __name__)


@checkin_bp.route('/validate/<ticket_code>', methods=['GET'])
@clerk_auth_required
def validate_ticket(ticket_code):
    """
    Validate a ticket without marking it as used.
    Used to check ticket status before check-in.
    """
    try:
        ticket = Ticket.query.filter_by(ticket_code=ticket_code).first()

        if not ticket:
            return jsonify({
                'valid': False,
                'message': 'Ticket not found'
            }), 404

        # Check if user is the event organizer
        if ticket.order.event.organizer_id != g.current_user.id:
            return jsonify({
                'valid': False,
                'message': 'Not authorized to check in for this event'
            }), 403

        if ticket.status == 'used':
            return jsonify({
                'valid': False,
                'message': 'Ticket already checked in',
                'checked_in_at': ticket.checked_in_at.isoformat() if ticket.checked_in_at else None
            })

        if ticket.status == 'cancelled':
            return jsonify({
                'valid': False,
                'message': 'Ticket has been cancelled'
            })

        if ticket.order.status != 'completed':
            return jsonify({
                'valid': False,
                'message': 'Payment not completed'
            })

        return jsonify({
            'valid': True,
            'ticket': {
                'ticket_code': ticket.ticket_code,
                'tier': ticket.tier.name,
                'attendee': ticket.order.user.fullname or ticket.order.user.email,
                'event': ticket.order.event.title
            }
        })

    except Exception as e:
        return jsonify({
            'valid': False,
            'message': str(e)
        }), 500


@checkin_bp.route('/', methods=['POST'])
@clerk_auth_required
def checkin_ticket():
    """
    Mark a ticket as used (check-in).

    Request body:
        {
            "ticket_code": "TIK-XXXXXXXXXX"
        }
    """
    try:
        data = request.json
        ticket_code = data.get('ticket_code')

        if not ticket_code:
            return jsonify({
                'valid': False,
                'message': 'ticket_code is required'
            }), 400

        ticket = Ticket.query.filter_by(ticket_code=ticket_code).first()

        if not ticket:
            return jsonify({
                'valid': False,
                'message': 'Ticket not found'
            }), 404

        # Check if user is the event organizer
        if ticket.order.event.organizer_id != g.current_user.id:
            return jsonify({
                'valid': False,
                'message': 'Not authorized to check in for this event'
            }), 403

        if ticket.status == 'used':
            return jsonify({
                'valid': False,
                'message': 'Ticket already checked in',
                'checked_in_at': ticket.checked_in_at.isoformat() if ticket.checked_in_at else None
            }), 400

        if ticket.status == 'cancelled':
            return jsonify({
                'valid': False,
                'message': 'Ticket has been cancelled'
            }), 400

        if ticket.order.status != 'completed':
            return jsonify({
                'valid': False,
                'message': 'Payment not completed'
            }), 400

        # Mark as used
        ticket.status = 'used'
        ticket.checked_in_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'valid': True,
            'message': 'Check-in successful',
            'ticket': {
                'ticket_code': ticket.ticket_code,
                'tier': ticket.tier.name,
                'attendee': ticket.order.user.fullname or ticket.order.user.email,
                'event': ticket.order.event.title,
                'checked_in_at': ticket.checked_in_at.isoformat()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'valid': False,
            'message': str(e)
        }), 500
