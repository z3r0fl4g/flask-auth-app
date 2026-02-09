"""
Create a sample published event with tickets for testing checkout flow.
"""
from app import app, db
from auth.models import User
from events.models import Event, TicketTier, generate_slug
from datetime import datetime, timedelta

with app.app_context():
    # Get the test user (or create if doesn't exist)
    test_user = User.query.filter_by(email='tikepam-test@mailinator.com').first()

    if not test_user:
        print("✗ Test user not found. Please create a user first.")
        exit(1)

    # Create a sample event
    event_date = datetime.utcnow() + timedelta(days=14)  # 2 weeks from now

    event = Event(
        slug=generate_slug("Haitian Independence Day Celebration 2026"),
        title="Haitian Independence Day Celebration 2026",
        description="""Join us for an unforgettable celebration of Haitian Independence Day!

🎉 Live Kompa & Rasin Music
🍽️ Authentic Haitian Cuisine
🎨 Art Exhibition & Cultural Performances
🎤 Guest Speakers on Haitian History

This year marks a special celebration of our heritage and culture. Come together with the community for an evening of music, food, and celebration!

Dress Code: Haitian flag colors welcome!""",
        category="culture",
        start_date=event_date,
        end_date=event_date + timedelta(hours=6),
        venue_name="Brooklyn Center for the Arts",
        venue_address="123 Flatbush Avenue, Brooklyn, NY 11217",
        city="Brooklyn",
        is_online=False,
        organizer_id=test_user.id,
        status='published',  # Published so it's visible
        is_featured=True
    )

    db.session.add(event)
    db.session.flush()  # Get event ID

    # Create ticket tiers
    tiers = [
        {
            'name': 'General Admission',
            'description': 'Standard entry to the event. Includes access to all performances and exhibitions.',
            'price': 2500,  # $25.00
            'quantity_total': 150,
            'max_per_order': 5
        },
        {
            'name': 'VIP Pass',
            'description': 'Premium experience with reserved seating, complimentary drinks, and meet & greet with artists.',
            'price': 5000,  # $50.00
            'quantity_total': 50,
            'max_per_order': 3
        },
        {
            'name': 'Student Ticket',
            'description': 'Discounted rate for students with valid ID. Same access as General Admission.',
            'price': 1500,  # $15.00
            'quantity_total': 100,
            'max_per_order': 2
        }
    ]

    for tier_data in tiers:
        tier = TicketTier(
            event_id=event.id,
            **tier_data
        )
        db.session.add(tier)

    db.session.commit()

    print(f"""
✓ Sample event created successfully!

Event: {event.title}
Slug: {event.slug}
Date: {event.start_date.strftime('%B %d, %Y at %I:%M %p')}
Status: {event.status}
Tickets: {len(tiers)} tiers created

View event at: http://localhost:5173/events/{event.slug}

Ticket Tiers:
""")

    for tier in event.ticket_tiers:
        print(f"  - {tier.name}: ${tier.price / 100:.2f} ({tier.quantity_total} available)")

    print(f"\nOrganizer: {test_user.fullname or test_user.email}")
