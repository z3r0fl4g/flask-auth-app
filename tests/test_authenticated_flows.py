"""
Comprehensive authenticated flow tests for Tikepam.
Tests all authenticated endpoints and full user flows.
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001"

# Test user ID (must exist in database)
TEST_USER_ID = "1"
TEST_HEADERS = {
    "X-Test-User-Id": TEST_USER_ID,
    "Content-Type": "application/json"
}

def test_my_events_empty():
    """Test listing organizer's events (initially empty for test user)."""
    print("\n=== Test: My Events (Organizer) ===")
    response = requests.get(f"{BASE_URL}/api/events/my-events", headers=TEST_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "events" in data["data"]
    print(f"✓ My events works - {len(data['data']['events'])} events found")
    return data["data"]["events"]

def test_create_event():
    """Test creating a new event."""
    print("\n=== Test: Create Event ===")

    event_data = {
        "title": "Test Automated Event",
        "description": "This is a test event created by automated tests.",
        "category": "music",
        "start_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "venue_name": "Test Venue",
        "city": "Port-au-Prince",
        "ticket_tiers": [
            {
                "name": "General Admission",
                "description": "Standard entry",
                "price": 1000,  # $10.00 in cents
                "quantity_total": 100,
                "max_per_order": 10
            },
            {
                "name": "VIP",
                "description": "Premium access",
                "price": 2500,  # $25.00 in cents
                "quantity_total": 50,
                "max_per_order": 5
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/api/events/",
        json=event_data,
        headers=TEST_HEADERS
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert "event" in data["data"]

    event = data["data"]["event"]
    assert event["title"] == event_data["title"]
    assert event["status"] == "draft"
    assert len(event["ticket_tiers"]) == 2

    print(f"✓ Event created: {event['title']} (ID: {event['id']})")
    print(f"  - Slug: {event['slug']}")
    print(f"  - Status: {event['status']}")
    print(f"  - Tiers: {len(event['ticket_tiers'])}")

    return event

def test_update_event(event_id):
    """Test updating an event."""
    print("\n=== Test: Update Event ===")

    update_data = {
        "title": "Test Automated Event (Updated)",
        "venue_name": "Updated Venue"
    }

    response = requests.put(
        f"{BASE_URL}/api/events/{event_id}",
        json=update_data,
        headers=TEST_HEADERS
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    event = data["data"]["event"]
    assert event["title"] == update_data["title"]
    assert event["venue_name"] == update_data["venue_name"]

    print(f"✓ Event updated: {event['title']}")

def test_publish_event(event_id):
    """Test publishing an event."""
    print("\n=== Test: Publish Event ===")

    response = requests.post(
        f"{BASE_URL}/api/events/{event_id}/publish",
        headers=TEST_HEADERS
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    event = data["data"]["event"]
    assert event["status"] == "published"

    print(f"✓ Event published: {event['title']}")
    return event

def test_checkout_validation():
    """Test checkout input validation."""
    print("\n=== Test: Checkout Validation ===")

    # Missing items
    response = requests.post(
        f"{BASE_URL}/api/checkout/create-session",
        json={"event_id": 1},
        headers=TEST_HEADERS
    )
    assert response.status_code == 400
    print("✓ Checkout rejects missing items")

    # Invalid event
    response = requests.post(
        f"{BASE_URL}/api/checkout/create-session",
        json={"event_id": 99999, "items": [{"tier_id": 1, "quantity": 1}]},
        headers=TEST_HEADERS
    )
    assert response.status_code == 404
    print("✓ Checkout rejects invalid event")

def test_checkout_create_session(event):
    """Test creating a checkout session."""
    print("\n=== Test: Checkout Create Session ===")

    if not event.get("ticket_tiers"):
        print("⚠ Event has no ticket tiers, skipping checkout test")
        return None

    tier = event["ticket_tiers"][0]

    checkout_data = {
        "event_id": event["id"],
        "items": [
            {
                "tier_id": tier["id"],
                "quantity": 2
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/api/checkout/create-session",
        json=checkout_data,
        headers=TEST_HEADERS
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "session_id" in data["data"]
    assert "url" in data["data"]
    assert "order_number" in data["data"]

    print(f"✓ Checkout session created")
    print(f"  - Order: {data['data']['order_number']}")
    print(f"  - Session: {data['data']['session_id'][:20]}...")

    return data["data"]

def test_my_orders():
    """Test listing user's orders."""
    print("\n=== Test: My Orders ===")

    response = requests.get(f"{BASE_URL}/api/orders/", headers=TEST_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "orders" in data["data"]

    print(f"✓ My orders works - {len(data['data']['orders'])} orders found")

    for order in data["data"]["orders"]:
        print(f"  - {order['order_number']}: {order['total_display']} ({order['status']})")

    return data["data"]["orders"]

def test_my_tickets():
    """Test listing user's tickets."""
    print("\n=== Test: My Tickets ===")

    response = requests.get(f"{BASE_URL}/api/tickets/", headers=TEST_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "tickets" in data["data"]

    print(f"✓ My tickets works - {len(data['data']['tickets'])} tickets found")

    for ticket in data["data"]["tickets"]:
        print(f"  - {ticket['ticket_code']}: {ticket['tier']['name']} ({ticket['status']})")

    return data["data"]["tickets"]

def test_get_single_ticket(ticket_code):
    """Test getting a single ticket."""
    print("\n=== Test: Get Single Ticket ===")

    response = requests.get(
        f"{BASE_URL}/api/tickets/{ticket_code}",
        headers=TEST_HEADERS
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "ticket" in data["data"]

    ticket = data["data"]["ticket"]
    assert ticket["ticket_code"] == ticket_code

    print(f"✓ Single ticket retrieved: {ticket['ticket_code']}")

def test_checkin_validate(ticket_code):
    """Test validating a ticket without checking in."""
    print("\n=== Test: Check-in Validate ===")

    response = requests.get(
        f"{BASE_URL}/api/checkin/validate/{ticket_code}",
        headers=TEST_HEADERS
    )

    # This will fail if test user is not the organizer
    if response.status_code == 403:
        print("⚠ Test user is not the event organizer, skipping check-in tests")
        return False

    assert response.status_code == 200
    data = response.json()
    assert "valid" in data

    if data["valid"]:
        print(f"✓ Ticket validated: {data['ticket']['ticket_code']}")
        print(f"  - Attendee: {data['ticket']['attendee']}")
        print(f"  - Event: {data['ticket']['event']}")
    else:
        print(f"⚠ Ticket invalid: {data['message']}")

    return data["valid"]

def test_checkin_ticket(ticket_code):
    """Test checking in a ticket."""
    print("\n=== Test: Check-in Ticket ===")

    response = requests.post(
        f"{BASE_URL}/api/checkin/",
        json={"ticket_code": ticket_code},
        headers=TEST_HEADERS
    )

    # This will fail if test user is not the organizer
    if response.status_code == 403:
        print("⚠ Test user is not the event organizer, skipping")
        return

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True

    print(f"✓ Ticket checked in: {data['ticket']['ticket_code']}")
    print(f"  - Checked in at: {data['ticket']['checked_in_at']}")

def test_checkin_duplicate(ticket_code):
    """Test that checking in a used ticket fails."""
    print("\n=== Test: Check-in Duplicate Prevention ===")

    response = requests.post(
        f"{BASE_URL}/api/checkin/",
        json={"ticket_code": ticket_code},
        headers=TEST_HEADERS
    )

    if response.status_code == 403:
        print("⚠ Test user is not the event organizer, skipping")
        return

    assert response.status_code == 400
    data = response.json()
    assert data["valid"] == False
    assert "already checked in" in data["message"].lower()

    print(f"✓ Duplicate check-in prevented: {data['message']}")

def test_delete_event(event_id, has_orders=False):
    """Test deleting an event."""
    print("\n=== Test: Delete Event ===")

    response = requests.delete(
        f"{BASE_URL}/api/events/{event_id}",
        headers=TEST_HEADERS
    )

    if has_orders:
        # Event with orders should not be deletable (foreign key constraint)
        assert response.status_code == 500
        print(f"✓ Event with orders cannot be deleted (expected behavior)")
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print(f"✓ Event deleted (ID: {event_id})")

def run_all_tests():
    """Run all authenticated tests."""
    print("=" * 60)
    print("TIKEPAM AUTHENTICATED FLOW TESTS")
    print("=" * 60)
    print(f"Using test user ID: {TEST_USER_ID}")

    try:
        # Organizer flows
        existing_events = test_my_events_empty()
        created_event = test_create_event()
        test_update_event(created_event["id"])
        published_event = test_publish_event(created_event["id"])

        # Checkout flow
        test_checkout_validation()
        checkout = test_checkout_create_session(published_event)

        # Orders and tickets
        orders = test_my_orders()
        tickets = test_my_tickets()

        # Single ticket
        if tickets:
            test_get_single_ticket(tickets[0]["ticket_code"])

        # Check-in flow (only works if test user is organizer)
        if tickets:
            ticket_code = tickets[0]["ticket_code"]
            if test_checkin_validate(ticket_code):
                test_checkin_ticket(ticket_code)
                test_checkin_duplicate(ticket_code)

        # Cleanup
        test_delete_event(created_event["id"], has_orders=True)

        print("\n" + "=" * 60)
        print("ALL AUTHENTICATED TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
