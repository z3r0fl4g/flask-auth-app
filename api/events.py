"""
Events API blueprint.
CRUD operations for events in our database.
"""
from flask import Blueprint, jsonify, request, g
from api.clerk_auth import clerk_auth_required
from events.models import Event, TicketTier, generate_slug
from auth import db
from datetime import datetime

events_bp = Blueprint('events', __name__)


@events_bp.route('/', methods=['GET'])
def list_events():
    """
    List all published events.

    Query params:
        category: Filter by category
        city: Filter by city
        featured: Show only featured events
        limit: Maximum number of events (default: 50)
    """
    try:
        query = Event.query.filter_by(status='published')

        # Apply filters
        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)

        city = request.args.get('city')
        if city:
            query = query.filter_by(city=city)

        featured = request.args.get('featured')
        if featured == 'true':
            query = query.filter_by(is_featured=True)

        # Order by start date (upcoming first)
        query = query.filter(Event.start_date >= datetime.utcnow())
        query = query.order_by(Event.start_date.asc())

        # Apply limit
        limit = request.args.get('limit', 50, type=int)
        events = query.limit(limit).all()

        return jsonify({
            'success': True,
            'data': {
                'events': [e.to_dict() for e in events]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/<slug>', methods=['GET'])
def get_event(slug):
    """
    Get a single event by slug with its ticket tiers.
    """
    try:
        event = Event.query.filter_by(slug=slug).first()

        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'event': event.to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/', methods=['POST'])
@clerk_auth_required
def create_event():
    """
    Create a new event.
    """
    try:
        data = request.json

        # Validate required fields
        if not data.get('title'):
            return jsonify({
                'success': False,
                'message': 'Title is required'
            }), 400

        if not data.get('start_date'):
            return jsonify({
                'success': False,
                'message': 'Start date is required'
            }), 400

        # Parse dates
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = None
        if data.get('end_date'):
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))

        # Create event
        event = Event(
            slug=generate_slug(data['title']),
            title=data['title'],
            description=data.get('description'),
            category=data.get('category'),
            start_date=start_date,
            end_date=end_date,
            venue_name=data.get('venue_name'),
            venue_address=data.get('venue_address'),
            city=data.get('city', 'Port-au-Prince'),
            is_online=data.get('is_online', False),
            online_url=data.get('online_url'),
            cover_image=data.get('cover_image'),
            organizer_id=g.current_user.id,
            status='draft'
        )

        db.session.add(event)
        db.session.flush()  # Get the event ID

        # Create ticket tiers
        for tier_data in data.get('ticket_tiers', []):
            tier = TicketTier(
                event_id=event.id,
                name=tier_data['name'],
                description=tier_data.get('description'),
                price=tier_data['price'],  # cents
                quantity_total=tier_data['quantity_total'],
                max_per_order=tier_data.get('max_per_order', 10)
            )
            db.session.add(tier)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'event': event.to_dict()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/<int:event_id>', methods=['PUT'])
@clerk_auth_required
def update_event(event_id):
    """
    Update an existing event (owner only).
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404

        # Check ownership
        if event.organizer_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403

        data = request.json

        # Update fields
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'category' in data:
            event.category = data['category']
        if 'start_date' in data:
            event.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        if 'end_date' in data:
            event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data['end_date'] else None
        if 'venue_name' in data:
            event.venue_name = data['venue_name']
        if 'venue_address' in data:
            event.venue_address = data['venue_address']
        if 'city' in data:
            event.city = data['city']
        if 'is_online' in data:
            event.is_online = data['is_online']
        if 'online_url' in data:
            event.online_url = data['online_url']
        if 'cover_image' in data:
            event.cover_image = data['cover_image']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'event': event.to_dict()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/<int:event_id>', methods=['DELETE'])
@clerk_auth_required
def delete_event(event_id):
    """
    Delete an event (owner only).
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404

        # Check ownership
        if event.organizer_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403

        db.session.delete(event)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Event deleted'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/<int:event_id>/publish', methods=['POST'])
@clerk_auth_required
def publish_event(event_id):
    """
    Publish an event (owner only).
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404

        # Check ownership
        if event.organizer_id != g.current_user.id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403

        # Validate event has ticket tiers
        if event.ticket_tiers.count() == 0:
            return jsonify({
                'success': False,
                'message': 'Event must have at least one ticket tier'
            }), 400

        event.status = 'published'
        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'event': event.to_dict()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@events_bp.route('/my-events', methods=['GET'])
@clerk_auth_required
def my_events():
    """
    List events created by the current user.
    """
    try:
        events = Event.query.filter_by(
            organizer_id=g.current_user.id
        ).order_by(Event.created_at.desc()).all()

        return jsonify({
            'success': True,
            'data': {
                'events': [e.to_dict() for e in events]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
