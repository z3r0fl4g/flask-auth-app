"""2FA verification page object for Selenium tests."""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class TwoFAPage(BasePage):
    """Page object for the 2FA verification page at /2fa/verify."""

    # Locators - OTP inputs (6 individual digit inputs)
    OTP_INPUTS = (By.CSS_SELECTOR, "input[maxlength='1']")
    OTP_INPUT_1 = (By.CSS_SELECTOR, "input[maxlength='1']:nth-of-type(1)")
    VERIFY_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], button:contains('Verify')")
    RESEND_BUTTON = (By.CSS_SELECTOR, "button:contains('Resend'), .btn-secondary")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".bg-rose-50, .bg-red-50")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".bg-green-50")
    EXPIRY_MESSAGE = (By.CSS_SELECTOR, ".text-xs.text-muted, .text-muted")

    def __init__(self, driver, base_url="http://localhost:5173"):
        super().__init__(driver, base_url)

    def navigate_to_verify(self):
        """Navigate to the 2FA verification page."""
        return self.navigate("/2fa/verify")

    def enter_code(self, code):
        """Enter the 6-digit verification code.

        Args:
            code: 6-digit string code
        """
        # Get all OTP input fields
        inputs = self.driver.find_elements(*self.OTP_INPUTS)

        if len(inputs) >= 6 and len(code) == 6:
            for i, digit in enumerate(code):
                inputs[i].clear()
                inputs[i].send_keys(digit)
        else:
            # Fallback: try to find a single input field
            single_input = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='number']")
            if single_input:
                single_input[0].clear()
                single_input[0].send_keys(code)

        return self

    def click_verify(self):
        """Click the verify button."""
        # Try multiple selectors for the verify button
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            for button in buttons:
                if "verify" in button.text.lower():
                    button.click()
                    return self
            # Fallback to submit button
            self.click(self.VERIFY_BUTTON)
        except Exception:
            pass
        return self

    def click_resend(self):
        """Click the resend code button."""
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            for button in buttons:
                if "resend" in button.text.lower():
                    button.click()
                    return self
        except Exception:
            pass
        return self

    def verify_code(self, code):
        """Complete verification flow: enter code and click verify."""
        self.enter_code(code)
        self.click_verify()
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

    def get_success_message(self):
        """Get success message text if visible."""
        try:
            return self.get_text(self.SUCCESS_MESSAGE, timeout=3)
        except Exception:
            return None

    def is_on_2fa_page(self):
        """Check if currently on the 2FA verification page."""
        url = self.get_current_url()
        return "/2fa" in url or "/verify" in url

    def wait_for_redirect_after_verify(self, timeout=10):
        """Wait for redirect to profile after successful verification."""
        try:
            self.wait_for_url_contains("/profile", timeout)
            return True
        except Exception:
            return False

    def get_otp_input_count(self):
        """Get the number of OTP input fields."""
        inputs = self.driver.find_elements(*self.OTP_INPUTS)
        return len(inputs)

    def clear_otp_inputs(self):
        """Clear all OTP input fields."""
        inputs = self.driver.find_elements(*self.OTP_INPUTS)
        for inp in inputs:
            inp.clear()
        return self
