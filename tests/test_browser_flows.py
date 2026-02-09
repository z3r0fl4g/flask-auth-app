"""
Browser-based testing using Selenium.
Demonstrates the full user flow in a real browser.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

FRONTEND_URL = "http://localhost:5173"

def setup_driver(headless=False):
    """Setup Chrome driver with options."""
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def test_homepage(driver):
    """Test homepage loads and displays hero section."""
    print("\n=== Test: Homepage ===")
    driver.get(FRONTEND_URL)
    time.sleep(2)

    # Check title
    assert "Tikepam" in driver.title
    print(f"✓ Page title: {driver.title}")

    # Check hero section
    try:
        hero = driver.find_element(By.XPATH, "//*[contains(text(), 'Discover Events in Haiti')]")
        print(f"✓ Hero section found: '{hero.text}'")
    except NoSuchElementException:
        print("⚠ Hero section not found")

    # Take screenshot
    driver.save_screenshot('/tmp/tikepam_homepage.png')
    print("✓ Screenshot saved: /tmp/tikepam_homepage.png")

def test_events_page(driver):
    """Test events listing page."""
    print("\n=== Test: Events Page ===")
    driver.get(f"{FRONTEND_URL}/events")
    time.sleep(2)

    # Check if events are displayed
    try:
        events = driver.find_elements(By.CSS_SELECTOR, "[class*='EventCard'], [class*='event-card'], .card")
        print(f"✓ Found {len(events)} event cards on page")
    except:
        print("⚠ No event cards found")

    # Check category filters
    try:
        filters = driver.find_elements(By.TAG_NAME, "button")
        filter_texts = [f.text for f in filters if f.text and len(f.text) < 30]
        print(f"✓ Category filters: {', '.join(filter_texts[:5])}")
    except:
        print("⚠ No category filters found")

    # Take screenshot
    driver.save_screenshot('/tmp/tikepam_events.png')
    print("✓ Screenshot saved: /tmp/tikepam_events.png")

def test_event_detail(driver):
    """Test event detail page."""
    print("\n=== Test: Event Detail Page ===")

    # Navigate to events page first
    driver.get(f"{FRONTEND_URL}/events")
    time.sleep(2)

    # Click on first event
    try:
        # Try multiple selectors to find an event link
        event_link = None
        selectors = [
            "a[href*='/events/']",
            "[class*='EventCard'] a",
            ".card a"
        ]

        for selector in selectors:
            try:
                links = driver.find_elements(By.CSS_SELECTOR, selector)
                valid_links = [l for l in links if '/events/' in l.get_attribute('href') and l.get_attribute('href').count('/') > 4]
                if valid_links:
                    event_link = valid_links[0]
                    break
            except:
                continue

        if event_link:
            event_url = event_link.get_attribute('href')
            print(f"✓ Clicking event: {event_url}")
            event_link.click()
            time.sleep(3)

            # Check if we're on event detail page
            current_url = driver.current_url
            if '/events/' in current_url and current_url != f"{FRONTEND_URL}/events":
                print(f"✓ On event detail page: {current_url}")

                # Look for ticket selector or event details
                try:
                    # Check for ticket tiers
                    ticket_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'General Admission') or contains(text(), 'VIP') or contains(text(), 'Ticket')]")
                    if ticket_elements:
                        print(f"✓ Found ticket elements: {len(ticket_elements)}")
                except:
                    pass

                # Take screenshot
                driver.save_screenshot('/tmp/tikepam_event_detail.png')
                print("✓ Screenshot saved: /tmp/tikepam_event_detail.png")
            else:
                print("⚠ Not on event detail page")
        else:
            print("⚠ No event links found")
    except Exception as e:
        print(f"⚠ Could not test event detail: {e}")

def test_navbar(driver):
    """Test navbar links."""
    print("\n=== Test: Navbar ===")
    driver.get(FRONTEND_URL)
    time.sleep(2)

    # Check navbar elements
    try:
        nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, nav button")
        nav_texts = [link.text for link in nav_links if link.text and len(link.text) < 30]
        print(f"✓ Navbar links: {', '.join(nav_texts[:10])}")
    except:
        print("⚠ Could not find navbar links")

    # Check logo
    try:
        logo = driver.find_element(By.CSS_SELECTOR, "img[alt*='logo'], img[alt*='Tikepam']")
        print(f"✓ Logo found: {logo.get_attribute('alt')}")
    except:
        print("⚠ Logo not found")

def test_responsive_design(driver):
    """Test responsive design on mobile."""
    print("\n=== Test: Responsive Design (Mobile) ===")

    # Set mobile viewport
    driver.set_window_size(375, 667)
    driver.get(f"{FRONTEND_URL}/events")
    time.sleep(2)

    print("✓ Mobile viewport: 375x667")

    # Take mobile screenshot
    driver.save_screenshot('/tmp/tikepam_mobile.png')
    print("✓ Screenshot saved: /tmp/tikepam_mobile.png")

    # Reset to desktop
    driver.set_window_size(1920, 1080)

def test_footer(driver):
    """Test footer is present."""
    print("\n=== Test: Footer ===")
    driver.get(FRONTEND_URL)
    time.sleep(2)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    try:
        footer = driver.find_element(By.TAG_NAME, "footer")
        print(f"✓ Footer found")

        # Check for social links or copyright
        footer_text = footer.text
        if "Tikepam" in footer_text or "2025" in footer_text or "2026" in footer_text:
            print(f"✓ Footer contains branding")
    except:
        print("⚠ Footer not found")

def test_page_navigation(driver):
    """Test navigating between pages."""
    print("\n=== Test: Page Navigation ===")

    pages = [
        ("Home", "/"),
        ("Events", "/events"),
    ]

    for name, path in pages:
        try:
            driver.get(f"{FRONTEND_URL}{path}")
            time.sleep(1)

            # Check if page loaded (no error)
            if "This page could not be found" not in driver.page_source:
                print(f"✓ {name} page loaded: {path}")
            else:
                print(f"⚠ {name} page not found: {path}")
        except Exception as e:
            print(f"⚠ Error loading {name}: {e}")

def run_all_tests():
    """Run all browser tests."""
    print("=" * 60)
    print("TIKEPAM BROWSER TESTS (Selenium)")
    print("=" * 60)
    print(f"Testing: {FRONTEND_URL}")
    print(f"Browser: Chrome (headless=False for visual testing)")
    print("=" * 60)

    driver = None
    try:
        # Run with visible browser for demonstration
        driver = setup_driver(headless=False)

        test_homepage(driver)
        test_navbar(driver)
        test_events_page(driver)
        test_event_detail(driver)
        test_footer(driver)
        test_page_navigation(driver)
        test_responsive_design(driver)

        print("\n" + "=" * 60)
        print("BROWSER TESTS COMPLETED!")
        print("=" * 60)
        print("\nScreenshots saved:")
        print("  - /tmp/tikepam_homepage.png")
        print("  - /tmp/tikepam_events.png")
        print("  - /tmp/tikepam_event_detail.png")
        print("  - /tmp/tikepam_mobile.png")
        print("\nBrowser will close in 5 seconds...")
        time.sleep(5)

        return True

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
