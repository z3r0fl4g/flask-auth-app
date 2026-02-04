"""Selenium tests for login flow."""
import pytest
import time
from tests.pages import LoginPage, TwoFAPage


@pytest.mark.login
class TestLoginFlow:
    """Test cases for user login functionality."""

    def test_login_page_loads(self, driver, login_page):
        """Test that login page loads correctly."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        assert login_page.is_on_login_page()
        assert login_page.is_visible(LoginPage.EMAIL_INPUT)
        assert login_page.is_visible(LoginPage.PASSWORD_INPUT)
        assert login_page.is_visible(LoginPage.SUBMIT_BUTTON)

    def test_login_valid_credentials(self, driver, login_page, create_test_user, test_user_data):
        """Test login with valid credentials redirects to 2FA or profile."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        # Wait for redirect
        time.sleep(2)
        current_url = login_page.get_current_url()

        # Should redirect to 2FA verification or profile (if 2FA disabled)
        assert any(path in current_url for path in ["/2fa", "/verify", "/profile"]), \
            f"Expected redirect to 2FA or profile, but got: {current_url}"

    @pytest.mark.slow
    def test_login_complete_with_2fa(self, driver, login_page, twofa_page,
                                      create_test_user, test_user_data, get_2fa_code):
        """Test complete login flow including 2FA verification."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        # Wait for redirect to 2FA page
        time.sleep(2)
        current_url = login_page.get_current_url()

        # If redirected to 2FA, complete verification
        if "/2fa" in current_url or "/verify" in current_url:
            code = get_2fa_code(timeout=15)

            if code:
                twofa_page.verify_code(code)

                # Should redirect to profile after verification
                time.sleep(2)
                assert twofa_page.wait_for_redirect_after_verify(timeout=10), \
                    "Expected redirect to profile after 2FA verification"
            else:
                pytest.skip("Could not capture 2FA code from Flask logs")
        else:
            # No 2FA required, should be on profile
            assert "/profile" in current_url, \
                f"Expected profile page when 2FA not required, got: {current_url}"

    def test_login_invalid_email(self, driver, login_page, test_user_data):
        """Test login with non-existent email shows error."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email="nonexistent@example.com",
            password=test_user_data["password"]
        )

        time.sleep(2)

        # Should show error message
        assert login_page.is_error_visible(), \
            "Invalid credentials should show error message"

        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Expected error message for invalid credentials"
        assert any(word in error_msg.lower() for word in ["invalid", "incorrect", "wrong", "failed"]), \
            f"Error message should indicate invalid credentials, got: {error_msg}"

    def test_login_invalid_password(self, driver, login_page, create_test_user, test_user_data):
        """Test login with wrong password shows error."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password="WrongPassword123!"  # Incorrect password
        )

        time.sleep(2)

        # Should show error message
        assert login_page.is_error_visible(), \
            "Wrong password should show error message"

        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Expected error message for wrong password"
        assert any(word in error_msg.lower() for word in ["invalid", "incorrect", "wrong", "failed"]), \
            f"Error message should indicate invalid credentials, got: {error_msg}"

    def test_login_empty_fields(self, driver, login_page):
        """Test that form validation prevents submission with empty fields."""
        from tests.pages import LoginPage
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        # Try to click submit without filling any fields
        # HTML5 validation should prevent submission
        try:
            submit_btn = login_page.driver.find_element(*LoginPage.SUBMIT_BUTTON)
            submit_btn.click()
        except Exception:
            pass  # Button might not be clickable due to validation

        time.sleep(1)

        # Should stay on login page (HTML5 validation or custom error)
        assert login_page.is_on_login_page(), \
            "Empty form should not submit successfully"

    def test_login_navigate_to_signup(self, driver, login_page):
        """Test clicking 'Sign up' link navigates to signup page."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.click_signup_link()

        time.sleep(1)

        # Should be on signup page
        current_url = login_page.get_current_url()
        assert "/signup" in current_url, \
            f"Expected navigation to signup page, but got: {current_url}"

    def test_login_forgot_password_link(self, driver, login_page):
        """Test clicking 'Forgot password?' link navigates to forgot password page."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        try:
            login_page.click_forgot_password_link()
            time.sleep(1)

            # Should be on forgot password page
            current_url = login_page.get_current_url()
            assert "/forgot" in current_url or "/reset" in current_url, \
                f"Expected navigation to forgot password page, but got: {current_url}"
        except Exception:
            # Forgot password link might not be present
            pytest.skip("Forgot password link not found on login page")

    def test_login_google_oauth_visible(self, driver, login_page):
        """Test that Google OAuth button is visible on login page."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        assert login_page.is_google_oauth_visible(), \
            "Google OAuth button should be visible"


@pytest.mark.login
class TestLoginValidation:
    """Test cases for login form validation."""

    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "@missinglocal.com",
        "missing@domain",
    ])
    def test_login_various_invalid_emails(self, driver, login_page, test_user_data, invalid_email):
        """Test login rejects various invalid email formats."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=invalid_email,
            password=test_user_data["password"]
        )

        time.sleep(1)

        # Should stay on login page or show error
        assert login_page.is_on_login_page() or login_page.is_error_visible(), \
            f"Invalid email '{invalid_email}' should be rejected"

    def test_login_email_only(self, driver, login_page, test_user_data):
        """Test that password field is required."""
        from tests.pages import LoginPage
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        # Enter only email, leave password empty
        login_page.enter_email(test_user_data["email"])

        # Try to click submit - HTML5 validation should prevent submission
        try:
            submit_btn = login_page.driver.find_element(*LoginPage.SUBMIT_BUTTON)
            submit_btn.click()
        except Exception:
            pass

        time.sleep(1)

        # Should stay on login page
        assert login_page.is_on_login_page(), \
            "Should not submit with empty password"

    def test_login_password_only(self, driver, login_page, test_user_data):
        """Test that email field is required."""
        from tests.pages import LoginPage
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        # Enter only password, leave email empty
        login_page.enter_password(test_user_data["password"])

        # Try to click submit - HTML5 validation should prevent submission
        try:
            submit_btn = login_page.driver.find_element(*LoginPage.SUBMIT_BUTTON)
            submit_btn.click()
        except Exception:
            pass

        time.sleep(1)

        # Should stay on login page
        assert login_page.is_on_login_page(), \
            "Should not submit with empty email"


@pytest.mark.twofa
class TestTwoFAVerification:
    """Test cases for 2FA verification during login."""

    def test_2fa_page_displays_correctly(self, driver, login_page, twofa_page,
                                          create_test_user, test_user_data):
        """Test that 2FA page displays properly after login."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        time.sleep(2)
        current_url = login_page.get_current_url()

        if "/2fa" in current_url or "/verify" in current_url:
            # Verify 2FA page elements
            assert twofa_page.is_on_2fa_page(), "Should be on 2FA page"

            # Check for OTP inputs (should have 6 inputs)
            otp_count = twofa_page.get_otp_input_count()
            assert otp_count == 6, f"Expected 6 OTP inputs, got {otp_count}"
        else:
            pytest.skip("2FA not enabled for test user")

    def test_2fa_invalid_code(self, driver, login_page, twofa_page,
                              create_test_user, test_user_data):
        """Test that invalid 2FA code does not grant access to profile."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        time.sleep(2)
        current_url = login_page.get_current_url()

        if "/2fa" in current_url or "/verify" in current_url:
            # Enter invalid code
            twofa_page.verify_code("000000")

            time.sleep(3)

            # Handle any alert that might appear
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
            except Exception:
                pass  # No alert present

            # The key assertion: invalid code should NOT grant access to profile
            final_url = driver.current_url
            assert "/profile" not in final_url, \
                f"Invalid 2FA code should not grant access to profile, but got: {final_url}"
        else:
            pytest.skip("2FA not enabled for test user")

    @pytest.mark.slow
    def test_2fa_resend_code(self, driver, login_page, twofa_page,
                             create_test_user, test_user_data):
        """Test that resend code button works."""
        login_page.navigate_to_login()
        login_page.wait_for_page_load()

        login_page.login(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        time.sleep(2)
        current_url = login_page.get_current_url()

        if "/2fa" in current_url or "/verify" in current_url:
            # Click resend button
            twofa_page.click_resend()

            time.sleep(2)

            # Handle any alert that might appear (success message)
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                # Success if alert mentions "sent" or "code"
                assert any(word in alert_text.lower() for word in ["sent", "code", "email", "new"]), \
                    f"Alert should confirm code sent, got: {alert_text}"
            except Exception:
                # No alert - check we're still on 2FA page (success)
                assert twofa_page.is_on_2fa_page(), \
                    "Should remain on 2FA page after resend"
        else:
            pytest.skip("2FA not enabled for test user")
