"""Signup page object for Selenium tests."""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class SignupPage(BasePage):
    """Page object for the signup page at /signup."""

    # Locators
    FULLNAME_INPUT = (By.CSS_SELECTOR, "#fullname")
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".bg-rose-50, .bg-red-50")
    GOOGLE_OAUTH_LINK = (By.CSS_SELECTOR, "a[href*='google']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    PASSWORD_REQUIREMENTS = (By.CSS_SELECTOR, ".text-xs.text-muted, .text-xs.text-gray-500")

    def __init__(self, driver, base_url="http://localhost:5173"):
        super().__init__(driver, base_url)

    def navigate_to_signup(self):
        """Navigate to the signup page."""
        return self.navigate("/signup")

    def enter_fullname(self, fullname):
        """Enter full name in the fullname field."""
        return self.type_text(self.FULLNAME_INPUT, fullname)

    def enter_email(self, email):
        """Enter email in the email field."""
        return self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Enter password in the password field."""
        return self.type_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the submit/signup button."""
        return self.click(self.SUBMIT_BUTTON)

    def signup(self, fullname, email, password):
        """Complete signup flow with fullname, email, and password."""
        self.enter_fullname(fullname)
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_error_message(self):
        """Get the error message text if visible."""
        try:
            return self.get_text(self.ERROR_MESSAGE, timeout=3)
        except Exception:
            return None

    def is_error_visible(self):
        """Check if error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE)

    def click_login_link(self):
        """Click the login link."""
        return self.click(self.LOGIN_LINK)

    def click_google_oauth(self):
        """Click the Google OAuth button."""
        return self.click(self.GOOGLE_OAUTH_LINK)

    def is_google_oauth_visible(self):
        """Check if Google OAuth button is visible."""
        return self.is_visible(self.GOOGLE_OAUTH_LINK)

    def is_on_signup_page(self):
        """Check if currently on the signup page."""
        return "/signup" in self.get_current_url()

    def get_password_requirements_text(self):
        """Get password requirements help text if visible."""
        try:
            return self.get_text(self.PASSWORD_REQUIREMENTS, timeout=2)
        except Exception:
            return None
