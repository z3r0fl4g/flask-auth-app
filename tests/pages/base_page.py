"""Base page object with common Selenium methods."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver, base_url="http://localhost:5173"):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 10

    def navigate(self, path=""):
        """Navigate to a specific path."""
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        return self

    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present and return it."""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible and return it."""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable and return it."""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        """Wait for element and click it."""
        element = self.wait_for_element_clickable(locator)
        element.click()
        return self

    def type_text(self, locator, text, clear=True):
        """Wait for element and type text into it."""
        element = self.wait_for_element_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator, timeout=None):
        """Wait for element and return its text."""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text

    def is_visible(self, locator, timeout=2):
        """Check if element is visible within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator, timeout=2):
        """Check if element is present within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text, timeout=None):
        """Wait for URL to contain specific text."""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def wait_for_url_to_be(self, url, timeout=None):
        """Wait for URL to match exactly."""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )

    def get_current_url(self):
        """Return current page URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Return current page title."""
        return self.driver.title

    def wait_for_page_load(self, timeout=None):
        """Wait for page to fully load."""
        timeout = timeout or self.timeout
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    def scroll_to_element(self, locator):
        """Scroll element into view."""
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self

    def get_attribute(self, locator, attribute):
        """Get attribute value from element."""
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def has_class(self, locator, class_name):
        """Check if element has specific class."""
        classes = self.get_attribute(locator, "class") or ""
        return class_name in classes.split()
