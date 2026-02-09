"""
Checkout API blueprint.
Handles Stripe checkout session creation for ticket purchases.
Creates Order and Tickets in our database before redirecting to Stripe.
"""
import os
from flask import Blueprint, jsonify, request, g
import stripe

from api.clerk_auth import clerk_auth_required
from events.models import Event, TicketTier, Order, Ticket
from auth import db

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/create-session', methods=['POST'])
@clerk_auth_required
def create_checkout_session():
    """
    Create a Stripe Checkout Session for ticket purchase.

    Request body:
        {
            "event_id": 1,
            "items": [
                {
                    "tier_id": 1,
                    "quantity": 2
                }
            ]
        }

    Flow:
    1. Validate ticket availability
    2. Reserve tickets (update quantity_sold)
    3. Create pending Order + Tickets in DB
    4. Create Stripe Checkout Session
    5. Return session URL for redirect
    """
    try:
        data = request.json

        event_id = data.get('event_id')
        items = data.get('items', [])

        if not event_id or not items:
            return jsonify({
                'success': False,
                'message': 'event_id and items are required'
            }), 400

        # Fetch the event
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404

        if event.status != 'published':
            return jsonify({
                'success': False,
                'message': 'Event is not available for purchase'
            }), 400

        # Validate and reserve tickets
        line_items = []
        order_items = []  # For creating tickets later
        subtotal = 0

        for item in items:
            tier_id = item.get('tier_id')
            quantity = item.get('quantity', 1)

            tier = TicketTier.query.get(tier_id)
            if not tier or tier.event_id != event.id:
                return jsonify({
                    'success': False,
                    'message': f'Invalid ticket tier: {tier_id}'
                }), 400

            if tier.quantity_available < quantity:
                return jsonify({
                    'success': False,
                    'message': f'Not enough tickets available for {tier.name}. Only {tier.quantity_available} left.'
                }), 400

            if quantity > tier.max_per_order:
                return jsonify({
                    'success': False,
                    'message': f'Maximum {tier.max_per_order} tickets per order for {tier.name}'
                }), 400

            # Reserve tickets
            tier.quantity_sold += quantity
            subtotal += tier.price * quantity

            # Build Stripe line item
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"{event.title} - {tier.name}",
                    },
                    'unit_amount': tier.price,
                },
                'quantity': quantity
            })

            order_items.append({
                'tier_id': tier_id,
                'tier': tier,
                'quantity': quantity
            })

        # Create the order
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=g.current_user.id,
            event_id=event.id,
            subtotal=subtotal,
            fees=0,
            total=subtotal,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create tickets
        for item in order_items:
            for _ in range(item['quantity']):
                ticket = Ticket(
                    ticket_code=Ticket.generate_ticket_code(),
                    order_id=order.id,
                    tier_id=item['tier_id'],
                    status='valid'
                )
                db.session.add(ticket)

        # Create Stripe Checkout Session
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f"{frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{frontend_url}/events/{event.slug}",
            customer_email=g.current_user.email,
            metadata={
                'order_id': str(order.id),
                'order_number': order.order_number
            }
        )

        # Save Stripe session ID to order
        order.stripe_session_id = session.id
        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'session_id': session.id,
                'url': session.url,
                'order_number': order.order_number
            }
        })

    except stripe.error.StripeError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Payment error: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@checkout_bp.route('/session/<session_id>', methods=['GET'])
@clerk_auth_required
def get_checkout_session(session_id):
    """
    Get details of a checkout session.
    Used to verify payment status on success page.
    Also acts as a webhook fallback — if Stripe reports the session
    as complete but the webhook hasn't fired yet, update the order here.
    """
    try:
        # First check our database
        order = Order.query.filter_by(stripe_session_id=session_id).first()

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

        # Get Stripe session status
        session = stripe.checkout.Session.retrieve(session_id)

        print(f"[CHECKOUT] Order {order.order_number}: DB status={order.status}, Stripe status={session.status}, payment_status={session.payment_status}")

        # Webhook fallback: if Stripe says complete but order is still pending, update it
        if order.status == 'pending' and session.status == 'complete':
            from datetime import datetime
            order.status = 'completed'
            order.completed_at = datetime.utcnow()
            if session.payment_intent:
                order.stripe_payment_intent_id = session.payment_intent
            db.session.commit()
            print(f"[CHECKOUT] Order {order.order_number} updated to completed (webhook fallback)")

        return jsonify({
            'success': True,
            'data': {
                'order': order.to_dict(),
                'payment_status': session.payment_status,
                'session_status': session.status
            }
        })

    except stripe.error.StripeError as e:
        return jsonify({
            'success': False,
            'message': f'Payment error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@checkout_bp.route('/cancel/<order_number>', methods=['POST'])
@clerk_auth_required
def cancel_pending_order(order_number):
    """
    Cancel a pending order (if payment was abandoned).
    Releases the reserved tickets.
    """
    try:
        order = Order.query.filter_by(order_number=order_number).first()

        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        if order.user_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        if order.status != 'pending':
            return jsonify({
                'success': False,
                'message': 'Only pending orders can be cancelled'
            }), 400

        # Release tickets
        for ticket in order.tickets:
            ticket.tier.quantity_sold -= 1
            ticket.status = 'cancelled'

        order.status = 'cancelled'
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order cancelled'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
