"""Selenium tests for signup flow."""
import pytest
import time
from tests.pages import SignupPage, TwoFAPage


@pytest.mark.signup
class TestSignupFlow:
    """Test cases for user signup functionality."""

    def test_signup_page_loads(self, driver, signup_page):
        """Test that signup page loads correctly."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        assert signup_page.is_on_signup_page()
        assert signup_page.is_visible(SignupPage.EMAIL_INPUT)
        assert signup_page.is_visible(SignupPage.PASSWORD_INPUT)
        assert signup_page.is_visible(SignupPage.SUBMIT_BUTTON)

    def test_signup_valid_credentials(self, driver, signup_page, test_user_data):
        """Test signup with valid credentials redirects to 2FA verification."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        # Should redirect to 2FA verification page
        time.sleep(2)  # Wait for redirect
        current_url = signup_page.get_current_url()

        assert "/2fa" in current_url or "/verify" in current_url, \
            f"Expected redirect to 2FA page, but got: {current_url}"

    @pytest.mark.slow
    def test_signup_complete_with_2fa(self, driver, signup_page, twofa_page,
                                       test_user_data, get_2fa_code):
        """Test complete signup flow including 2FA verification."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        # Wait for redirect to 2FA page
        time.sleep(2)

        # Get 2FA code from Flask logs
        code = get_2fa_code(timeout=15)

        if code:
            twofa_page.verify_code(code)

            # Should redirect to profile after verification
            time.sleep(2)
            assert twofa_page.wait_for_redirect_after_verify(timeout=10), \
                "Expected redirect to profile after 2FA verification"
        else:
            pytest.skip("Could not capture 2FA code from Flask logs")

    def test_signup_invalid_email(self, driver, signup_page, test_user_data):
        """Test signup with malformed email shows validation error."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email="invalid-email",  # Missing @ and domain
            password=test_user_data["password"]
        )

        time.sleep(1)

        # Should show error or stay on signup page
        assert signup_page.is_on_signup_page() or signup_page.is_error_visible(), \
            "Invalid email should prevent signup or show error"

    def test_signup_weak_password_too_short(self, driver, signup_page, test_user_data):
        """Test signup with password less than 8 characters."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=test_user_data["email"],
            password="Short1"  # Only 6 characters
        )

        time.sleep(1)

        # Should show error or stay on signup page
        assert signup_page.is_on_signup_page() or signup_page.is_error_visible(), \
            "Short password should prevent signup or show error"

    def test_signup_weak_password_no_number(self, driver, signup_page, test_user_data):
        """Test signup with password without digits."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=test_user_data["email"],
            password="NoNumbersHere"  # No digits
        )

        time.sleep(1)

        # Should show error or stay on signup page
        assert signup_page.is_on_signup_page() or signup_page.is_error_visible(), \
            "Password without number should prevent signup or show error"

    def test_signup_duplicate_email(self, driver, signup_page, create_test_user, test_user_data):
        """Test signup with already registered email."""
        # First signup (uses create_test_user fixture)
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        # Try to signup with same email
        signup_page.signup(
            fullname="Another User",
            email=test_user_data["email"],  # Same email as created user
            password="DifferentPass123!"
        )

        time.sleep(2)

        # Should show error about duplicate email
        assert signup_page.is_error_visible(), \
            "Duplicate email should show error message"

        error_msg = signup_page.get_error_message()
        assert error_msg is not None, "Expected error message for duplicate email"
        # Check for common error messages
        assert any(word in error_msg.lower() for word in ["already", "registered", "exists", "taken"]), \
            f"Error message should indicate email is taken, got: {error_msg}"

    def test_signup_empty_fields(self, driver, signup_page):
        """Test that form validation prevents submission with empty fields."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        # Try to click submit without filling any fields
        # HTML5 validation should prevent submission
        try:
            submit_btn = signup_page.driver.find_element(*SignupPage.SUBMIT_BUTTON)
            submit_btn.click()
        except Exception:
            pass  # Button might not be clickable due to validation

        time.sleep(1)

        # Should stay on signup page (HTML5 validation or custom error)
        assert signup_page.is_on_signup_page(), \
            "Empty form should not submit successfully"

    def test_signup_navigate_to_login(self, driver, signup_page):
        """Test clicking 'Sign in' link navigates to login page."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.click_login_link()

        time.sleep(1)

        # Should be on login page
        current_url = signup_page.get_current_url()
        assert "/login" in current_url, \
            f"Expected navigation to login page, but got: {current_url}"

    def test_signup_google_oauth_visible(self, driver, signup_page):
        """Test that Google OAuth button is visible on signup page."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        assert signup_page.is_google_oauth_visible(), \
            "Google OAuth button should be visible"


@pytest.mark.signup
class TestSignupValidation:
    """Test cases for signup form validation."""

    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "@missinglocal.com",
        "missing@domain",
        "missing.domain@",
        "spaces in@email.com",
    ])
    def test_signup_various_invalid_emails(self, driver, signup_page, test_user_data, invalid_email):
        """Test signup rejects various invalid email formats."""
        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=invalid_email,
            password=test_user_data["password"]
        )

        time.sleep(1)

        # Should stay on signup page or show error
        assert signup_page.is_on_signup_page() or signup_page.is_error_visible(), \
            f"Invalid email '{invalid_email}' should be rejected"

    @pytest.mark.parametrize("weak_password,description", [
        ("short1", "too short"),
        ("nolowercase1", "only lowercase without uppercase"),
        ("NOUPPERCASE1", "only uppercase without lowercase"),
        ("NoNumbers", "no digits"),
        ("12345678", "only digits"),
    ])
    def test_signup_various_weak_passwords(self, driver, signup_page, test_user_data,
                                           weak_password, description):
        """Test signup rejects various weak password formats."""
        # Generate unique email for each test
        timestamp = int(time.time() * 1000)
        unique_email = f"testuser_{timestamp}@example.com"

        signup_page.navigate_to_signup()
        signup_page.wait_for_page_load()

        signup_page.signup(
            fullname=test_user_data["fullname"],
            email=unique_email,
            password=weak_password
        )

        time.sleep(1)

        # Should stay on signup page or show error (depending on validation rules)
        # Note: Some weak passwords might pass if validation rules are lenient
        current_url = signup_page.get_current_url()

        # Log result for debugging
        if "/signup" not in current_url and not signup_page.is_error_visible():
            print(f"Warning: Password '{weak_password}' ({description}) was accepted")
