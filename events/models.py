"""
Event ticketing models for Tikepam.

Defines the core data models:
- Event: Event details (title, date, venue, organizer)
- TicketTier: Ticket types with pricing and availability
- Order: Purchase records with Stripe integration
- Ticket: Individual tickets with check-in tracking
"""

from auth import db
from datetime import datetime
import uuid


def generate_slug(title):
    """Generate URL-friendly slug from title."""
    from slugify import slugify
    base = slugify(title)
    return f"{base}-{uuid.uuid4().hex[:6]}"


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(250), unique=True, nullable=False)

    # Basic info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))

    # Date/time
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)

    # Location
    venue_name = db.Column(db.String(200))
    venue_address = db.Column(db.String(500))
    city = db.Column(db.String(100), default='Port-au-Prince')
    is_online = db.Column(db.Boolean, default=False)
    online_url = db.Column(db.String(500))

    # Media
    cover_image = db.Column(db.String(500))

    # Organizer
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organizer = db.relationship('User', backref='organized_events')

    # Status
    status = db.Column(db.String(20), default='draft')  # draft, published, cancelled
    is_featured = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ticket_tiers = db.relationship('TicketTier', backref='event', lazy='dynamic',
                                   cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'venue_name': self.venue_name,
            'venue_address': self.venue_address,
            'city': self.city,
            'is_online': self.is_online,
            'online_url': self.online_url,
            'cover_image': self.cover_image,
            'status': self.status,
            'is_featured': self.is_featured,
            'organizer': {
                'id': self.organizer.id,
                'fullname': self.organizer.fullname
            } if self.organizer else None,
            'ticket_tiers': [t.to_dict() for t in self.ticket_tiers]
        }


class TicketTier(db.Model):
    __tablename__ = 'ticket_tiers'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)  # cents

    quantity_total = db.Column(db.Integer, nullable=False)
    quantity_sold = db.Column(db.Integer, default=0)

    max_per_order = db.Column(db.Integer, default=10)

    @property
    def quantity_available(self):
        return self.quantity_total - self.quantity_sold

    @property
    def is_sold_out(self):
        return self.quantity_available <= 0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'price_display': f"${self.price / 100:.2f}",
            'quantity_available': self.quantity_available,
            'is_sold_out': self.is_sold_out,
            'max_per_order': self.max_per_order
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='orders')

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship('Event', backref='orders')

    # Pricing (cents)
    subtotal = db.Column(db.Integer, nullable=False)
    fees = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, nullable=False)

    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled, refunded

    # Stripe
    stripe_session_id = db.Column(db.String(100))
    stripe_payment_intent_id = db.Column(db.String(100))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    tickets = db.relationship('Ticket', backref='order', lazy='dynamic',
                              cascade='all, delete-orphan')

    @staticmethod
    def generate_order_number():
        return f"TK-{uuid.uuid4().hex[:8].upper()}"

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'event': self.event.to_dict() if self.event else None,
            'subtotal': self.subtotal,
            'fees': self.fees,
            'total': self.total,
            'total_display': f"${self.total / 100:.2f}",
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'tickets': [t.to_dict() for t in self.tickets]
        }


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String(20), unique=True, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    tier_id = db.Column(db.Integer, db.ForeignKey('ticket_tiers.id'), nullable=False)
    tier = db.relationship('TicketTier')

    # Status
    status = db.Column(db.String(20), default='valid')  # valid, used, cancelled
    checked_in_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_ticket_code():
        return f"TIK-{uuid.uuid4().hex[:10].upper()}"

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_code': self.ticket_code,
            'tier': self.tier.to_dict() if self.tier else None,
            'status': self.status,
            'checked_in_at': self.checked_in_at.isoformat() if self.checked_in_at else None,
            'qr_data': self.ticket_code  # Frontend generates QR from this
        }
