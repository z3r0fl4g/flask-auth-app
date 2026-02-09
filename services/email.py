"""
Email service for sending ticket confirmations and notifications.
"""
from flask_mail import Message
from flask import current_app
import os


def send_order_confirmation(order, tickets):
    """
    Send order confirmation email with tickets.

    Args:
        order: Order object
        tickets: List of Ticket objects
    """
    if not order.user or not order.user.email:
        print(f"Cannot send email - no email address for order {order.order_number}")
        return False

    try:
        # Build ticket list for email
        ticket_list = []
        for ticket in tickets:
            ticket_list.append({
                'code': ticket.ticket_code,
                'tier': ticket.tier.name if ticket.tier else 'General',
                'price': f"${ticket.tier.price / 100:.2f}" if ticket.tier else '$0.00'
            })

        # Email subject
        subject = f"Your tickets for {order.event.title}"

        # Email body (HTML)
        html_body = render_template_string(ORDER_CONFIRMATION_TEMPLATE,
            user_name=order.user.fullname or order.user.email.split('@')[0],
            order_number=order.order_number,
            event_title=order.event.title,
            event_date=order.event.start_date.strftime('%B %d, %Y at %I:%M %p') if order.event.start_date else 'TBD',
            venue_name=order.event.venue_name or 'Online Event',
            venue_address=order.event.venue_address or order.event.online_url or '',
            tickets=ticket_list,
            total=f"${order.total / 100:.2f}",
            frontend_url=os.getenv('FRONTEND_URL', 'http://localhost:5173')
        )

        # Email body (plain text fallback)
        text_body = f"""
Hi {order.user.fullname or 'there'},

Your order #{order.order_number} is confirmed!

Event: {order.event.title}
Date: {order.event.start_date.strftime('%B %d, %Y at %I:%M %p') if order.event.start_date else 'TBD'}
Venue: {order.event.venue_name or 'Online Event'}

Your Tickets:
{chr(10).join(f"- {t['tier']}: {t['code']}" for t in ticket_list)}

Total: ${order.total / 100:.2f}

View your tickets: {os.getenv('FRONTEND_URL', 'http://localhost:5173')}/my-tickets

See you at the event!

— Tikepam Team
        """

        # Create and send email
        msg = Message(
            subject=subject,
            recipients=[order.user.email],
            body=text_body,
            html=html_body,
            sender=os.getenv('MAIL_DEFAULT_SENDER', 'noreply@tikepam.com')
        )

        # Get mail instance from current app
        from app import mail
        mail.send(msg)
        print(f"✓ Order confirmation email sent to {order.user.email}")
        return True

    except Exception as e:
        print(f"✗ Failed to send order confirmation email: {e}")
        return False


# HTML email template
ORDER_CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: white; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }
        .event-details { background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .ticket { background: white; border: 2px solid #7c3aed; border-radius: 8px; padding: 15px; margin: 10px 0; }
        .ticket-code { font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #7c3aed; }
        .button { display: inline-block; background: #7c3aed; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Order Confirmed!</h1>
        </div>

        <div class="content">
            <p>Hi {{ user_name }},</p>

            <p>Your order <strong>#{{ order_number }}</strong> is confirmed! Get ready for an amazing experience.</p>

            <div class="event-details">
                <h2 style="margin-top: 0;">{{ event_title }}</h2>
                <p><strong>📅 Date:</strong> {{ event_date }}</p>
                <p><strong>📍 Venue:</strong> {{ venue_name }}</p>
                {% if venue_address %}
                <p style="color: #6b7280;">{{ venue_address }}</p>
                {% endif %}
            </div>

            <h3>Your Tickets</h3>
            {% for ticket in tickets %}
            <div class="ticket">
                <div><strong>{{ ticket.tier }}</strong> - {{ ticket.price }}</div>
                <div class="ticket-code">{{ ticket.code }}</div>
            </div>
            {% endfor %}

            <p><strong>Total Paid:</strong> {{ total }}</p>

            <p style="text-align: center;">
                <a href="{{ frontend_url }}/my-tickets" class="button">View My Tickets</a>
            </p>

            <p style="color: #6b7280; font-size: 14px;">
                💡 <strong>Tip:</strong> Show the QR code on your ticket at the door for quick entry.
            </p>
        </div>

        <div class="footer">
            <p>Tikepam - Real Haitian Events</p>
            <p>Questions? Reply to this email or visit our website.</p>
        </div>
    </div>
</body>
</html>
"""
