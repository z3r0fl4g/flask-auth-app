"""
Comprehensive API flow tests for Tikepam.
Tests all major endpoints and flows.
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001"

def test_events_list():
    """Test listing events."""
    print("\n=== Test: Events List ===")
    response = requests.get(f"{BASE_URL}/api/events/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "events" in data["data"]
    print(f"✓ Events list works - {len(data['data']['events'])} events found")
    return data["data"]["events"]

def test_events_filter_category():
    """Test filtering events by category."""
    print("\n=== Test: Events Filter by Category ===")
    response = requests.get(f"{BASE_URL}/api/events/?category=music")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    for event in data["data"]["events"]:
        assert event["category"] == "music"
    print(f"✓ Category filter works - {len(data['data']['events'])} music events")

def test_events_filter_featured():
    """Test filtering featured events."""
    print("\n=== Test: Events Filter by Featured ===")
    response = requests.get(f"{BASE_URL}/api/events/?featured=true")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    for event in data["data"]["events"]:
        assert event["is_featured"] == True
    print(f"✓ Featured filter works - {len(data['data']['events'])} featured events")

def test_single_event(events):
    """Test getting a single event."""
    print("\n=== Test: Single Event ===")
    if not events:
        print("⚠ No events to test")
        return None

    slug = events[0]["slug"]
    response = requests.get(f"{BASE_URL}/api/events/{slug}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "event" in data["data"]
    event = data["data"]["event"]
    assert event["slug"] == slug
    assert "ticket_tiers" in event
    print(f"✓ Single event works - '{event['title']}' with {len(event['ticket_tiers'])} ticket tiers")
    return event

def test_event_not_found():
    """Test getting a non-existent event."""
    print("\n=== Test: Event Not Found ===")
    response = requests.get(f"{BASE_URL}/api/events/non-existent-event-xyz")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] == False
    print("✓ 404 for non-existent event works")

def test_auth_session_unauthenticated():
    """Test auth session without login."""
    print("\n=== Test: Auth Session (Unauthenticated) ===")
    response = requests.get(f"{BASE_URL}/api/auth/session")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["data"]["authenticated"] == False
    print("✓ Auth session returns unauthenticated correctly")

def test_protected_endpoint_without_auth():
    """Test that protected endpoints require auth."""
    print("\n=== Test: Protected Endpoints Require Auth ===")

    # Test my-events
    response = requests.get(f"{BASE_URL}/api/events/my-events")
    assert response.status_code == 401
    print("✓ /api/events/my-events requires auth")

    # Test create event
    response = requests.post(f"{BASE_URL}/api/events/", json={"title": "Test"})
    assert response.status_code == 401
    print("✓ POST /api/events/ requires auth")

    # Test tickets
    response = requests.get(f"{BASE_URL}/api/tickets/")
    assert response.status_code == 401
    print("✓ /api/tickets/ requires auth")

    # Test checkout
    response = requests.post(f"{BASE_URL}/api/checkout/create-session", json={})
    assert response.status_code == 401
    print("✓ /api/checkout/create-session requires auth")

    # Test orders
    response = requests.get(f"{BASE_URL}/api/orders/")
    assert response.status_code == 401
    print("✓ /api/orders/ requires auth")

    # Test checkin
    response = requests.post(f"{BASE_URL}/api/checkin/", json={})
    assert response.status_code == 401
    print("✓ /api/checkin/ requires auth")

def test_checkout_validation():
    """Test checkout validates input."""
    print("\n=== Test: Checkout Input Validation ===")
    # This would need auth, but we can verify the endpoint exists
    response = requests.post(
        f"{BASE_URL}/api/checkout/create-session",
        json={"event_id": 1, "items": []}
    )
    # Should be 401 (auth required) not 404 (not found)
    assert response.status_code == 401
    print("✓ Checkout endpoint exists and requires auth")

def test_stripe_webhook_endpoint():
    """Test Stripe webhook endpoint exists."""
    print("\n=== Test: Stripe Webhook Endpoint ===")
    # Webhook accepts in dev mode (no signature verification)
    response = requests.post(
        f"{BASE_URL}/api/webhooks/stripe",
        data="{}",
        headers={"Content-Type": "application/json"}
    )
    # In dev mode (no secret), it returns 200
    # In prod mode (with secret), it returns 400 (bad signature)
    assert response.status_code in [200, 400]
    print("✓ Stripe webhook endpoint exists")

def test_clerk_webhook_endpoint():
    """Test Clerk webhook endpoint exists."""
    print("\n=== Test: Clerk Webhook Endpoint ===")
    response = requests.post(
        f"{BASE_URL}/api/webhooks/clerk",
        json={},
        headers={"Content-Type": "application/json"}
    )
    # Should return error (missing svix headers) not 404
    assert response.status_code in [400, 401, 500]
    print("✓ Clerk webhook endpoint exists")

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("TIKEPAM API FLOW TESTS")
    print("=" * 60)

    try:
        # Public endpoints
        events = test_events_list()
        test_events_filter_category()
        test_events_filter_featured()
        test_single_event(events)
        test_event_not_found()

        # Auth tests
        test_auth_session_unauthenticated()
        test_protected_endpoint_without_auth()

        # Validation tests
        test_checkout_validation()
        test_stripe_webhook_endpoint()
        test_clerk_webhook_endpoint()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
