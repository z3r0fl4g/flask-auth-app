"""Login page object for Selenium tests."""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page at /login."""

    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".bg-rose-50, .bg-red-50")
    GOOGLE_OAUTH_LINK = (By.CSS_SELECTOR, "a[href*='google']")
    SIGNUP_LINK = (By.CSS_SELECTOR, "a[href='/signup']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/forgot-password']")

    def __init__(self, driver, base_url="http://localhost:5173"):
        super().__init__(driver, base_url)

    def navigate_to_login(self):
        """Navigate to the login page."""
        return self.navigate("/login")

    def enter_email(self, email):
        """Enter email in the email field."""
        return self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Enter password in the password field."""
        return self.type_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the submit/login button."""
        return self.click(self.SUBMIT_BUTTON)

    def login(self, email, password):
        """Complete login flow with email and password."""
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

    def click_signup_link(self):
        """Click the signup link."""
        return self.click(self.SIGNUP_LINK)

    def click_forgot_password_link(self):
        """Click the forgot password link."""
        return self.click(self.FORGOT_PASSWORD_LINK)

    def click_google_oauth(self):
        """Click the Google OAuth button."""
        return self.click(self.GOOGLE_OAUTH_LINK)

    def is_google_oauth_visible(self):
        """Check if Google OAuth button is visible."""
        return self.is_visible(self.GOOGLE_OAUTH_LINK)

    def is_on_login_page(self):
        """Check if currently on the login page."""
        return "/login" in self.get_current_url()
