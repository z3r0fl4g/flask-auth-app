"""API-based tests for authentication flows (no browser required)."""
import pytest
import requests
import time


BASE_URL = "http://localhost:5001"


@pytest.fixture
def session():
    """Create a requests session that maintains cookies."""
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture
def unique_email():
    """Generate unique test email."""
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}@example.com"


class TestSignupAPI:
    """Test signup via API."""

    def test_signup_valid_credentials(self, session, unique_email):
        """Test signup with valid credentials."""
        response = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "TestPass123!",
            "fullname": "Test User"
        })

        assert response.status_code in [200, 201], f"Signup failed: {response.text}"
        data = response.json()
        assert data.get("success") is True
        assert data.get("data", {}).get("requires_2fa") is True
        print(f"✓ Signup successful for {unique_email}")
        print(f"  Requires 2FA: {data.get('data', {}).get('requires_2fa')}")

    def test_signup_invalid_email(self, session):
        """Test signup with invalid email format."""
        response = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": "invalid-email",
            "password": "TestPass123!",
            "fullname": "Test User"
        })

        assert response.status_code == 422, f"Expected 422 for invalid email, got {response.status_code}"
        print("✓ Invalid email correctly rejected")

    def test_signup_weak_password(self, session, unique_email):
        """Test signup with weak password."""
        response = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "weak",
            "fullname": "Test User"
        })

        assert response.status_code == 422, f"Expected 422 for weak password, got {response.status_code}"
        print("✓ Weak password correctly rejected")

    def test_signup_duplicate_email(self, session, unique_email):
        """Test signup with duplicate email."""
        # First signup
        response1 = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "TestPass123!",
            "fullname": "Test User"
        })
        assert response1.status_code in [200, 201]

        # Second signup with same email
        response2 = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "TestPass123!",
            "fullname": "Another User"
        })

        assert response2.status_code == 409, f"Expected 409 for duplicate email, got {response2.status_code}"
        print("✓ Duplicate email correctly rejected")


class TestLoginAPI:
    """Test login via API."""

    @pytest.fixture
    def created_user(self, session, unique_email):
        """Create a test user for login tests."""
        response = session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "TestPass123!",
            "fullname": "Test User"
        })
        assert response.status_code in [200, 201]
        return {"email": unique_email, "password": "TestPass123!"}

    def test_login_valid_credentials(self, session, created_user):
        """Test login with valid credentials."""
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": created_user["email"],
            "password": created_user["password"]
        })

        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert data.get("success") is True
        print(f"✓ Login successful for {created_user['email']}")
        print(f"  Requires 2FA: {data.get('data', {}).get('requires_2fa')}")

    def test_login_invalid_email(self, session):
        """Test login with non-existent email."""
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "TestPass123!"
        })

        assert response.status_code == 401, f"Expected 401 for invalid email, got {response.status_code}"
        print("✓ Invalid email correctly rejected")

    def test_login_wrong_password(self, session, created_user):
        """Test login with wrong password."""
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": created_user["email"],
            "password": "WrongPassword123!"
        })

        assert response.status_code == 401, f"Expected 401 for wrong password, got {response.status_code}"
        print("✓ Wrong password correctly rejected")

    def test_session_check_unauthenticated(self, session):
        """Test session check when not logged in."""
        response = session.get(f"{BASE_URL}/api/auth/session")

        assert response.status_code == 200
        data = response.json()
        assert data.get("data", {}).get("authenticated") is False
        print("✓ Session correctly shows unauthenticated")


class Test2FAAPI:
    """Test 2FA verification via API."""

    @pytest.fixture
    def user_awaiting_2fa(self, session, unique_email):
        """Create user and initiate login to trigger 2FA."""
        # Signup
        session.post(f"{BASE_URL}/api/auth/signup", json={
            "email": unique_email,
            "password": "TestPass123!",
            "fullname": "Test User"
        })
        return {"email": unique_email, "password": "TestPass123!", "session": session}

    def test_2fa_invalid_code(self, user_awaiting_2fa):
        """Test 2FA with invalid code."""
        session = user_awaiting_2fa["session"]

        response = session.post(f"{BASE_URL}/api/2fa/verify", json={
            "code": "000000"
        })

        assert response.status_code == 401, f"Expected 401 for invalid code, got {response.status_code}"
        print("✓ Invalid 2FA code correctly rejected")

    def test_2fa_resend(self, user_awaiting_2fa):
        """Test 2FA code resend."""
        session = user_awaiting_2fa["session"]

        response = session.post(f"{BASE_URL}/api/2fa/resend")

        # Should succeed or show rate limit
        assert response.status_code in [200, 429], f"Unexpected status: {response.status_code}"
        if response.status_code == 200:
            print("✓ 2FA code resend successful")
        else:
            print("✓ 2FA code resend rate limited (expected behavior)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
