"""
Create 5 additional sample events for testing.
"""
from app import app, db
from auth.models import User
from events.models import Event, TicketTier, generate_slug
from datetime import datetime, timedelta

with app.app_context():
    # Get the test user
    test_user = User.query.filter_by(email='tikepam-test@mailinator.com').first()

    if not test_user:
        print("✗ Test user not found. Please create a user first.")
        exit(1)

    events_data = [
        {
            'title': 'Kompa Night at SOBs',
            'description': '''Get ready for the hottest Kompa night in NYC!

🎵 Live Performances by:
- T-Vice
- Carimi
- Harmonik

🍹 Premium Open Bar (9PM - 11PM)
🎉 DJ Ritchy spinning all your favorites
📸 Photo booth & professional photography

This is THE event of the month - don't miss out!

Dress Code: Upscale casual / Club attire''',
            'category': 'nightlife',
            'start_date': datetime.utcnow() + timedelta(days=7),
            'end_date': datetime.utcnow() + timedelta(days=7, hours=5),
            'venue_name': 'SOBs (Sounds of Brazil)',
            'venue_address': '204 Varick St, New York, NY 10014',
            'city': 'New York',
            'is_online': False,
            'cover_image': None,
            'is_featured': True,
            'tiers': [
                {'name': 'Early Bird', 'description': 'Limited time offer! Save $10', 'price': 3000, 'quantity': 50, 'max': 4},
                {'name': 'General Admission', 'description': 'Standard entry', 'price': 4000, 'quantity': 200, 'max': 6},
                {'name': 'VIP Table (4 people)', 'description': 'Reserved table, bottle service included', 'price': 25000, 'quantity': 10, 'max': 1},
            ]
        },
        {
            'title': 'Miami Kite Festival & Haitian Food Fair',
            'description': '''Family-friendly celebration of Haitian culture and cuisine!

🪁 Traditional Kite Flying Competition
🍽️ 20+ Haitian Food Vendors
🎪 Kids Zone with games and activities
🎨 Haitian arts & crafts market
🎵 Live Rasin music performances

Bring the whole family for a day of fun, food, and culture!

Free parking available.''',
            'category': 'festival',
            'start_date': datetime.utcnow() + timedelta(days=21),
            'end_date': datetime.utcnow() + timedelta(days=21, hours=8),
            'venue_name': 'Bayfront Park',
            'venue_address': '301 Biscayne Blvd, Miami, FL 33132',
            'city': 'Miami',
            'is_online': False,
            'cover_image': None,
            'is_featured': False,
            'tiers': [
                {'name': 'Kids (under 12)', 'description': 'Children admission', 'price': 500, 'quantity': 300, 'max': 5},
                {'name': 'Adult', 'description': 'General admission', 'price': 1000, 'quantity': 500, 'max': 10},
                {'name': 'Family Pass (2 adults + 3 kids)', 'description': 'Best value for families', 'price': 3000, 'quantity': 100, 'max': 2},
            ]
        },
        {
            'title': 'Haitian Creole Language Workshop',
            'description': '''Learn Haitian Creole in this interactive 4-week virtual course!

📚 What You'll Learn:
- Basic conversational phrases
- Proper pronunciation & accent
- Grammar fundamentals
- Cultural context & expressions

👨‍🏫 Taught by native speakers
💻 Live Zoom sessions every Saturday
📖 Course materials included
🎓 Certificate upon completion

Perfect for beginners or those wanting to reconnect with their roots!

Classes run for 4 consecutive Saturdays (2 hours each session)''',
            'category': 'community',
            'start_date': datetime.utcnow() + timedelta(days=10),
            'end_date': datetime.utcnow() + timedelta(days=31, hours=2),
            'venue_name': 'Online Event',
            'venue_address': '',
            'city': 'Online',
            'is_online': True,
            'online_url': 'https://zoom.us/j/haitian-creole-workshop',
            'cover_image': None,
            'is_featured': False,
            'tiers': [
                {'name': 'Standard Registration', 'description': '4-week course access', 'price': 7500, 'quantity': 50, 'max': 3},
                {'name': 'Premium (with materials)', 'description': 'Course + physical workbook shipped', 'price': 10000, 'quantity': 30, 'max': 2},
            ]
        },
        {
            'title': 'Griot & Pikliz Cook-Off Competition',
            'description': '''Calling all Haitian chefs! Compete for the title of Best Griot & Pikliz!

🏆 Grand Prize: $1,000 + Trophy
🍖 Categories:
   - Best Griot (fried pork)
   - Best Pikliz (spicy slaw)
   - People's Choice Award

👨‍🍳 Professional chef judges
🎤 Live DJ & MC
🍻 Cash bar
📺 Event will be livestreamed

Competitors: Register as "Competitor Entry"
Spectators: Come taste and vote!

Limited competitor slots - register early!''',
            'category': 'food',
            'start_date': datetime.utcnow() + timedelta(days=28),
            'end_date': datetime.utcnow() + timedelta(days=28, hours=6),
            'venue_name': 'Little Haiti Cultural Complex',
            'venue_address': '212-260 NE 59th Terrace, Miami, FL 33137',
            'city': 'Miami',
            'is_online': False,
            'cover_image': None,
            'is_featured': True,
            'tiers': [
                {'name': 'Spectator Ticket', 'description': 'Watch, taste, and vote', 'price': 2000, 'quantity': 200, 'max': 5},
                {'name': 'Competitor Entry', 'description': 'Enter the competition', 'price': 5000, 'quantity': 20, 'max': 1},
                {'name': 'VIP Judge Table', 'description': 'Reserved seating with judges', 'price': 7500, 'quantity': 10, 'max': 2},
            ]
        },
        {
            'title': 'Art & Soul: Haitian Painting Exhibition',
            'description': '''Experience the vibrant world of Haitian art!

🎨 Featured Artists:
- Works from the famous St. Soleil school
- Contemporary Haitian painters
- Emerging local artists

🖼️ 50+ Original Paintings on Display
🍷 Wine & Cheese Reception (Opening Night)
🎵 Live acoustic guitar performances
💬 Artist Q&A sessions
🛒 Artwork available for purchase

This exhibition celebrates the rich artistic heritage of Haiti through color, story, and tradition.

Opening night features artist meet & greet!''',
            'category': 'art',
            'start_date': datetime.utcnow() + timedelta(days=18),
            'end_date': datetime.utcnow() + timedelta(days=18, hours=4),
            'venue_name': 'Brooklyn Museum - Community Gallery',
            'venue_address': '200 Eastern Parkway, Brooklyn, NY 11238',
            'city': 'Brooklyn',
            'is_online': False,
            'cover_image': None,
            'is_featured': False,
            'tiers': [
                {'name': 'General Admission', 'description': 'Exhibition access', 'price': 1500, 'quantity': 150, 'max': 4},
                {'name': 'Opening Night Reception', 'description': 'Wine, cheese, artist meet & greet', 'price': 3500, 'quantity': 50, 'max': 2},
            ]
        }
    ]

    created_events = []

    for event_data in events_data:
        tiers_data = event_data.pop('tiers')

        event = Event(
            slug=generate_slug(event_data['title']),
            organizer_id=test_user.id,
            status='published',
            **event_data
        )

        db.session.add(event)
        db.session.flush()

        # Create ticket tiers
        for tier_data in tiers_data:
            tier = TicketTier(
                event_id=event.id,
                name=tier_data['name'],
                description=tier_data['description'],
                price=tier_data['price'],
                quantity_total=tier_data['quantity'],
                max_per_order=tier_data['max']
            )
            db.session.add(tier)

        created_events.append(event)

    db.session.commit()

    print(f"\n✓ {len(created_events)} events created successfully!\n")

    for event in created_events:
        print(f"📅 {event.title}")
        print(f"   Category: {event.category.title()}")
        print(f"   Date: {event.start_date.strftime('%B %d, %Y')}")
        print(f"   Location: {event.city}")
        print(f"   Tickets: {event.ticket_tiers.count()} tiers")
        print(f"   URL: http://localhost:5173/events/{event.slug}")
        print()

    print(f"Total events in database: {Event.query.filter_by(status='published').count()}")
    print(f"\nView all events at: http://localhost:5173/events")
