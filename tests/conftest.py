"""Pytest fixtures for Selenium authentication tests."""
import os
import sys
import time
import subprocess
import platform
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================================
# Configuration
# ============================================================================

FLASK_URL = "http://localhost:5001"
VUE_URL = "http://localhost:5173"
HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"

# Detect WSL environment
IS_WSL = "microsoft" in platform.uname().release.lower() or "wsl" in platform.uname().release.lower()

# Windows Chrome path for WSL
WINDOWS_CHROME_PATH = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"


# ============================================================================
# Browser Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def chrome_options():
    """Configure Chrome options for testing."""
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Enable console log capture
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    return options


@pytest.fixture(scope="function")
def driver(chrome_options):
    """Create a Chrome WebDriver instance for each test."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def logged_out_driver(driver):
    """Ensure driver starts logged out by clearing cookies."""
    driver.get(VUE_URL)
    driver.delete_all_cookies()
    return driver


# ============================================================================
# Test User Data Fixtures
# ============================================================================

@pytest.fixture
def test_user_data():
    """Generate unique test user credentials using timestamp."""
    timestamp = int(time.time() * 1000)
    return {
        "email": f"testuser_{timestamp}@example.com",
        "password": "TestPass123!",
        "fullname": "Test User"
    }


@pytest.fixture
def existing_user_data():
    """Credentials for a pre-existing test user (for login tests).

    Note: This user should be created in the database before running login tests,
    or created during test setup.
    """
    return {
        "email": "existing_test_user@example.com",
        "password": "ExistingPass123!",
        "fullname": "Existing Test User"
    }


@pytest.fixture
def invalid_credentials():
    """Invalid credentials for negative testing."""
    return {
        "email": "nonexistent@example.com",
        "password": "WrongPassword123!"
    }


@pytest.fixture
def weak_passwords():
    """Collection of weak passwords for validation testing."""
    return [
        "short",           # Too short (< 8 chars)
        "nolowercase1",    # Missing lowercase (actually has it, testing)
        "NOLOWERCASE1",    # All uppercase
        "nonumber",        # No number
        "12345678",        # Only numbers
    ]


# ============================================================================
# Page Object Fixtures
# ============================================================================

@pytest.fixture
def login_page(driver):
    """Create LoginPage instance."""
    from tests.pages import LoginPage
    return LoginPage(driver, VUE_URL)


@pytest.fixture
def signup_page(driver):
    """Create SignupPage instance."""
    from tests.pages import SignupPage
    return SignupPage(driver, VUE_URL)


@pytest.fixture
def twofa_page(driver):
    """Create TwoFAPage instance."""
    from tests.pages import TwoFAPage
    return TwoFAPage(driver, VUE_URL)


# ============================================================================
# Flask Process Fixtures (for 2FA code capture)
# ============================================================================

@pytest.fixture(scope="session")
def flask_log_file(tmp_path_factory):
    """Create a temporary log file for Flask output."""
    log_dir = tmp_path_factory.mktemp("logs")
    return str(log_dir / "flask.log")


@pytest.fixture(scope="module")
def flask_process(flask_log_file):
    """Start Flask backend and capture output for 2FA codes.

    Note: This assumes Flask is NOT already running.
    If Flask is already running separately, use the manual_flask_output fixture instead.
    """
    # Check if Flask is already running
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5001))
    sock.close()

    if result == 0:
        # Flask is already running, skip starting it
        pytest.skip("Flask is already running on port 5001. Use manual 2FA code entry.")
        return None

    # Start Flask with output captured
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    flask_cmd = [
        sys.executable,  # Use same Python interpreter
        os.path.join(project_root, "app.py")
    ]

    with open(flask_log_file, "w") as log_file:
        process = subprocess.Popen(
            flask_cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            cwd=project_root,
            env={**os.environ, "FLASK_ENV": "development"}
        )

    # Wait for Flask to start
    time.sleep(3)

    yield process

    # Cleanup
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


# ============================================================================
# 2FA Code Capture Fixtures
# ============================================================================

@pytest.fixture
def get_2fa_code(flask_log_file):
    """Factory fixture to get 2FA codes from Flask logs.

    Usage in tests:
        code = get_2fa_code()  # Gets the latest code
        code = get_2fa_code(timeout=15)  # With custom timeout
    """
    from tests.utils import extract_2fa_code

    def _get_code(timeout=10):
        """Wait for and extract 2FA code from Flask logs."""
        start_time = time.time()
        last_position = 0

        while time.time() - start_time < timeout:
            try:
                with open(flask_log_file, 'r') as f:
                    f.seek(last_position)
                    content = f.read()
                    last_position = f.tell()

                    code = extract_2fa_code(content)
                    if code:
                        return code
            except FileNotFoundError:
                pass

            time.sleep(0.5)

        return None

    return _get_code


@pytest.fixture
def manual_2fa_code():
    """Fixture for manual 2FA code entry when Flask runs separately.

    Use this when Flask is running in a separate terminal and you need
    to manually copy the verification code.

    Usage in tests:
        @pytest.mark.manual_2fa
        def test_something(manual_2fa_code):
            code = manual_2fa_code()  # Prompts for code input
    """
    def _get_code():
        """Prompt user to enter 2FA code from Flask console."""
        print("\n" + "=" * 50)
        print("MANUAL 2FA CODE ENTRY REQUIRED")
        print("Check the Flask console for the verification code")
        print("=" * 50)
        code = input("Enter 6-digit verification code: ").strip()
        return code if len(code) == 6 and code.isdigit() else None

    return _get_code


# ============================================================================
# Database Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=False)
def cleanup_test_users():
    """Clean up test users after tests complete.

    Note: Only use this fixture when you want automatic cleanup.
    Import it explicitly in tests that need it.
    """
    yield

    # Cleanup: Delete test users matching pattern
    try:
        # Import here to avoid circular imports
        from auth.models import User, db
        from app import app

        with app.app_context():
            User.query.filter(User.email.like('testuser_%@example.com')).delete()
            db.session.commit()
    except Exception as e:
        print(f"Warning: Failed to cleanup test users: {e}")


@pytest.fixture
def create_test_user(test_user_data):
    """Create a test user in the database for login tests.

    Returns the user data dict with the created user's info.
    """
    from werkzeug.security import generate_password_hash

    try:
        from auth.models import User, db
        from app import app

        with app.app_context():
            # Check if user already exists
            existing = User.query.filter_by(email=test_user_data["email"]).first()
            if existing:
                return test_user_data

            user = User(
                email=test_user_data["email"],
                password=generate_password_hash(test_user_data["password"]),
                fullname=test_user_data["fullname"],
                provider='local',
                twofa_enabled=True,
                twofa_method='email',
                twofa_verified=False
            )
            db.session.add(user)
            db.session.commit()

        return test_user_data

    except Exception as e:
        pytest.skip(f"Could not create test user: {e}")


# ============================================================================
# URL Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the Vue.js frontend (required by pytest-selenium)."""
    return VUE_URL


@pytest.fixture(scope="session")
def api_url():
    """Base URL for the Flask API."""
    return FLASK_URL


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def wait_for_page_load(driver):
    """Factory fixture to wait for page load completion."""
    def _wait(timeout=10):
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    return _wait


@pytest.fixture
def screenshot_on_failure(driver, request):
    """Take screenshot on test failure."""
    yield

    if request.node.rep_call.failed:
        timestamp = int(time.time())
        screenshot_path = f"screenshots/failure_{request.node.name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")


# ============================================================================
# Pytest Hooks
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
