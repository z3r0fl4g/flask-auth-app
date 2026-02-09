"""
Webhook endpoints for external service integrations.

Handles Clerk webhooks for user synchronization.
Handles Stripe webhooks for payment confirmation and ticket issuance.
"""

import os
import json
from flask import Blueprint, request, jsonify
from svix.webhooks import Webhook, WebhookVerificationError
import stripe

from auth.models import User
from auth import db
from events.models import Order, Ticket
from datetime import datetime

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

webhook_bp = Blueprint('webhooks', __name__)


@webhook_bp.route('/clerk', methods=['POST'])
def clerk_webhook():
    """
    Handle Clerk webhook events for user synchronization.

    Events handled:
    - user.created: Create a new local user
    - user.updated: Update local user fields
    - user.deleted: Remove local user

    Returns:
        JSON response with success status
    """
    # Get the webhook secret
    webhook_secret = os.getenv('CLERK_WEBHOOK_SECRET', '')

    if not webhook_secret:
        print("WARNING: CLERK_WEBHOOK_SECRET not configured")
        return jsonify({'success': False, 'message': 'Webhook not configured'}), 500

    # Get the headers for verification
    svix_id = request.headers.get('svix-id')
    svix_timestamp = request.headers.get('svix-timestamp')
    svix_signature = request.headers.get('svix-signature')

    if not all([svix_id, svix_timestamp, svix_signature]):
        return jsonify({'success': False, 'message': 'Missing webhook headers'}), 400

    # Get the raw body
    payload = request.get_data(as_text=True)

    # Verify the webhook signature
    try:
        wh = Webhook(webhook_secret)
        event = wh.verify(payload, {
            'svix-id': svix_id,
            'svix-timestamp': svix_timestamp,
            'svix-signature': svix_signature
        })
    except WebhookVerificationError as e:
        print(f"Webhook verification failed: {e}")
        return jsonify({'success': False, 'message': 'Invalid webhook signature'}), 400

    # Process the event
    event_type = event.get('type')
    data = event.get('data', {})

    print(f"Received Clerk webhook: {event_type}")

    try:
        if event_type == 'user.created':
            handle_user_created(data)
        elif event_type == 'user.updated':
            handle_user_updated(data)
        elif event_type == 'user.deleted':
            handle_user_deleted(data)
        else:
            print(f"Unhandled webhook event type: {event_type}")

        return jsonify({'success': True, 'message': f'Handled {event_type}'})

    except Exception as e:
        print(f"Error handling webhook {event_type}: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


def handle_user_created(data):
    """
    Handle user.created webhook event.

    Creates a new user in the local database.

    Args:
        data: User data from Clerk webhook
    """
    clerk_id = data.get('id')

    # Check if user already exists (idempotency)
    existing = User.query.filter_by(clerk_id=clerk_id).first()
    if existing:
        print(f"User {clerk_id} already exists, skipping creation")
        return

    # Extract primary email
    email_addresses = data.get('email_addresses', [])
    primary_email_id = data.get('primary_email_address_id')
    primary_email = next(
        (e['email_address'] for e in email_addresses if e.get('id') == primary_email_id),
        email_addresses[0]['email_address'] if email_addresses else None
    )

    if not primary_email:
        print(f"No email found for user {clerk_id}")
        return

    # Create the user
    user = User(
        clerk_id=clerk_id,
        email=primary_email,
        fullname=f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
        profile_pic=data.get('image_url')
    )

    db.session.add(user)
    db.session.commit()

    print(f"Created user: {user.email} (clerk_id: {clerk_id})")


def handle_user_updated(data):
    """
    Handle user.updated webhook event.

    Updates an existing user in the local database.

    Args:
        data: User data from Clerk webhook
    """
    clerk_id = data.get('id')

    user = User.query.filter_by(clerk_id=clerk_id).first()
    if not user:
        # User doesn't exist locally, create them
        print(f"User {clerk_id} not found locally, creating")
        handle_user_created(data)
        return

    # Extract primary email
    email_addresses = data.get('email_addresses', [])
    primary_email_id = data.get('primary_email_address_id')
    primary_email = next(
        (e['email_address'] for e in email_addresses if e.get('id') == primary_email_id),
        email_addresses[0]['email_address'] if email_addresses else user.email
    )

    # Update fields
    user.email = primary_email
    user.fullname = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
    user.profile_pic = data.get('image_url')

    db.session.commit()

    print(f"Updated user: {user.email} (clerk_id: {clerk_id})")


def handle_user_deleted(data):
    """
    Handle user.deleted webhook event.

    Removes a user from the local database.

    Args:
        data: User data from Clerk webhook
    """
    clerk_id = data.get('id')

    user = User.query.filter_by(clerk_id=clerk_id).first()
    if not user:
        print(f"User {clerk_id} not found locally, nothing to delete")
        return

    email = user.email
    db.session.delete(user)
    db.session.commit()

    print(f"Deleted user: {email} (clerk_id: {clerk_id})")


# ==================== Stripe Webhooks ====================

@webhook_bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    """
    Handle Stripe webhook events for payment confirmation.

    Events handled:
    - checkout.session.completed: Issue tickets via Ticket Tailor

    Returns:
        JSON response with success status
    """
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')

    # If no webhook secret configured, accept the event (dev mode)
    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            print(f"Invalid Stripe payload: {e}")
            return jsonify({'error': 'Invalid payload'}), 400
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid Stripe signature: {e}")
            return jsonify({'error': 'Invalid signature'}), 400
    else:
        # Dev mode: parse without verification
        event = json.loads(payload)
        print("WARNING: Stripe webhook signature not verified (no secret configured)")

    event_type = event.get('type') if isinstance(event, dict) else event['type']
    print(f"Received Stripe webhook: {event_type}")

    try:
        if event_type == 'checkout.session.completed':
            session = event['data']['object']
            handle_checkout_completed(session)

        return jsonify({'received': True})

    except Exception as e:
        print(f"Error handling Stripe webhook {event_type}: {e}")
        return jsonify({'error': str(e)}), 500


def handle_checkout_completed(session):
    """
    Handle checkout.session.completed event.

    Marks the order as completed after successful payment.

    Args:
        session: Stripe Checkout Session object
    """
    session_id = session.get('id')
    payment_intent_id = session.get('payment_intent')

    if not session_id:
        print("Missing session ID in webhook")
        return

    # Find the order by Stripe session ID
    order = Order.query.filter_by(stripe_session_id=session_id).first()

    if not order:
        print(f"Order not found for session: {session_id}")
        return

    if order.status == 'completed':
        print(f"Order {order.order_number} already completed, skipping")
        return

    # Update order status
    order.status = 'completed'
    order.completed_at = datetime.utcnow()
    if payment_intent_id:
        order.stripe_payment_intent_id = payment_intent_id

    db.session.commit()

    print(f"Order {order.order_number} completed - {order.tickets.count()} tickets issued")

    # Send confirmation email with tickets
    try:
        from services.email import send_order_confirmation
        tickets_list = list(order.tickets.all())
        send_order_confirmation(order, tickets_list)
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
