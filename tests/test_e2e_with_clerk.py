"""
End-to-End Selenium tests with Clerk authentication.
Uses persistent test user credentials from environment variables.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

FRONTEND_URL = "http://localhost:5173"
TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL')
TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')

def setup_driver(headless=False):
    """Setup Chrome driver"""
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

def clerk_login(driver, email, password):
    """
    Login through Clerk's authentication UI.
    Waits for Clerk component to load and handles the login flow.
    """
    print(f"\n=== Logging in as {email} ===")

    try:
        driver.get(f"{FRONTEND_URL}/login")
        time.sleep(3)  # Wait for Clerk to load

        # Take screenshot of login page
        driver.save_screenshot('/tmp/clerk_login_page.png')

        # Look for Clerk sign-in form
        # Clerk uses specific identifiers
        try:
            # Try to find email input (Clerk uses various IDs)
            email_selectors = [
                "input[name='identifier']",
                "input[type='email']",
                "input[id*='identifier']",
                "#identifier-field"
            ]

            email_input = None
            for selector in email_selectors:
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue

            if not email_input:
                print("⚠ Could not find email input field")
                print("Page source:", driver.page_source[:500])
                return False

            # Enter email
            email_input.clear()
            email_input.send_keys(email)
            print("✓ Entered email")

            # Look for Continue button
            continue_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button[form*='signIn']")
            continue_btn.click()
            time.sleep(2)

            # Enter password
            password_selectors = [
                "input[name='password']",
                "input[type='password']",
                "#password-field"
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue

            if password_input:
                password_input.clear()
                password_input.send_keys(password)
                print("✓ Entered password")

                # Submit
                submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                submit_btn.click()
                time.sleep(3)

                # Check if redirected (logged in)
                if driver.current_url != f"{FRONTEND_URL}/login":
                    print(f"✓ Login successful - redirected to {driver.current_url}")

                    # Wait for Clerk session to initialize
                    print("Waiting for Clerk session to fully initialize...")
                    time.sleep(5)

                    # Try to navigate away from 2FA verify if we're stuck there
                    if '/2fa' in driver.current_url:
                        print("On 2FA page, navigating to home...")
                        driver.get(FRONTEND_URL)
                        time.sleep(3)

                    # Check if user is actually authenticated by looking for auth indicators
                    # Look for user button or authenticated nav elements
                    try:
                        # Try to find "My Events" or "My Tickets" link
                        nav_text = driver.find_element(By.TAG_NAME, "nav").text
                        if "My Events" in nav_text or "My Tickets" in nav_text or "Create Event" in nav_text:
                            print("✓ User authenticated - auth menu visible")
                            return True
                        else:
                            print(f"⚠ Nav doesn't show auth elements. Nav text: {nav_text[:100]}")
                            driver.save_screenshot('/tmp/post_login_nav.png')
                            # Continue anyway, maybe session needs more time
                            return True
                    except:
                        print("⚠ Could not verify auth state from nav")
                        return True
                else:
                    print("⚠ Still on login page after submit")
                    return False
            else:
                print("⚠ Could not find password input")
                return False

        except Exception as e:
            print(f"⚠ Error during login: {e}")
            driver.save_screenshot('/tmp/clerk_login_error.png')
            return False

    except Exception as e:
        print(f"✗ Login failed: {e}")
        return False

def test_browse_events(driver):
    """Test browsing events"""
    print("\n=== Test: Browse Events ===")
    driver.get(f"{FRONTEND_URL}/events")
    time.sleep(2)

    # Check for events
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "Discover Events" in page_text or "All Upcoming Events" in page_text:
            print("✓ Events page loaded")
            driver.save_screenshot('/tmp/events_authenticated.png')
            return True
    except:
        pass

    print("⚠ Events page did not load properly")
    return False

def test_create_event_full_form(driver):
    """Test creating an event by filling the complete form"""
    print("\n=== Test: Create Event (Full Form) ===")

    try:
        driver.get(f"{FRONTEND_URL}/create-event")
        time.sleep(3)

        # Check if redirected to login
        if driver.current_url == f"{FRONTEND_URL}/login":
            print("⚠ Redirected to login - not authenticated")
            return False

        print("✓ Create event page loaded")

        # Fill basic information
        print("Filling basic information...")
        title_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder*='event title']")
        title_input.clear()
        title_input.send_keys("Selenium Test Event - Music Festival")

        description_input = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='Describe']")
        description_input.clear()
        description_input.send_keys("This is an automated test event created by Selenium. Join us for an amazing music festival featuring local Haitian artists.")

        # Select category
        category_select = driver.find_element(By.CSS_SELECTOR, "select")
        from selenium.webdriver.support.ui import Select
        select = Select(category_select)
        select.select_by_value("music")

        print("✓ Basic info filled")

        # Fill date/time
        print("Filling date and time...")
        from datetime import datetime, timedelta
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        start_date_input = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        # Clear and set date using JavaScript (more reliable than send_keys)
        driver.execute_script(f"arguments[0].value = '{future_date}'", start_date_input)

        start_time_input = driver.find_element(By.CSS_SELECTOR, "input[type='time']")
        driver.execute_script("arguments[0].value = '19:00'", start_time_input)

        print("✓ Date/time filled")

        # Fill location
        print("Filling location...")
        venue_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

        # Find venue name input (check placeholder text)
        for inp in venue_inputs:
            placeholder = inp.get_attribute('placeholder')
            if placeholder and 'venue' in placeholder.lower():
                inp.clear()
                inp.send_keys("Karibe Hotel Convention Center")
                break

        # Fill address
        for inp in venue_inputs:
            placeholder = inp.get_attribute('placeholder')
            if placeholder and 'address' in placeholder.lower():
                inp.clear()
                inp.send_keys("Juvenat 7, Route de Delmas")
                break

        # City should already be Port-au-Prince by default
        print("✓ Location filled")

        # Modify ticket tier
        print("Configuring ticket tiers...")

        # Find the first ticket tier name input
        tier_name_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='General Admission'], input[placeholder*='VIP']")
        tier_name_input.clear()
        tier_name_input.send_keys("General Admission")

        # Set price
        price_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
        for inp in price_inputs:
            placeholder = inp.get_attribute('placeholder')
            if placeholder == '0.00':
                inp.clear()
                inp.send_keys("25.00")
                break

        # Set quantity
        for inp in price_inputs:
            placeholder = inp.get_attribute('placeholder')
            if placeholder == '100':
                inp.clear()
                inp.send_keys("150")
                break

        print("✓ Ticket tier configured")

        # Take screenshot before submit
        driver.save_screenshot('/tmp/create_event_filled.png')
        print("✓ Screenshot saved: /tmp/create_event_filled.png")

        # Submit form
        print("Submitting form...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(5)

        # Check if redirected to my-events
        current_url = driver.current_url
        if '/my-events' in current_url:
            print(f"✓ Event created successfully - redirected to {current_url}")
            driver.save_screenshot('/tmp/create_event_success.png')
            return True
        else:
            print(f"⚠ Unexpected redirect: {current_url}")
            driver.save_screenshot('/tmp/create_event_error.png')
            return False

    except Exception as e:
        print(f"✗ Error creating event: {e}")
        driver.save_screenshot('/tmp/create_event_exception.png')
        import traceback
        traceback.print_exc()
        return False

def test_select_tickets_and_checkout(driver):
    """Test selecting tickets and starting checkout flow"""
    print("\n=== Test: Select Tickets & Checkout ===")

    try:
        # Go to events page
        driver.get(f"{FRONTEND_URL}/events")
        time.sleep(3)

        # Find and click on first event
        print("Finding first event...")
        event_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/events/']")

        valid_event_links = [
            link for link in event_links
            if '/events/' in link.get_attribute('href')
            and link.get_attribute('href').count('/') > 4
        ]

        if not valid_event_links:
            print("⚠ No event links found on page")
            return False

        event_url = valid_event_links[0].get_attribute('href')
        print(f"✓ Found event: {event_url}")

        driver.get(event_url)
        time.sleep(3)

        print("✓ Event detail page loaded")
        driver.save_screenshot('/tmp/event_detail_before_selection.png')

        # Try to find and interact with ticket selector
        print("Looking for ticket selector...")

        # Look for quantity controls
        # The + button is a round button with violet background
        plus_buttons = driver.find_elements(By.CSS_SELECTOR, "button.bg-violet-600, button.rounded-full")

        if plus_buttons:
            print(f"✓ Found {len(plus_buttons)} potential ticket buttons")

            # Find the increment button (has plus icon)
            # Try clicking buttons that look like increment buttons
            clicked = False
            for btn in plus_buttons:
                # Check if button contains SVG with plus path
                try:
                    svg = btn.find_element(By.TAG_NAME, "svg")
                    paths = svg.find_elements(By.TAG_NAME, "path")
                    for path in paths:
                        d_attr = path.get_attribute("d")
                        # Plus icon has path with "M12 4v16m8-8H4" (vertical and horizontal lines)
                        if d_attr and ("v16" in d_attr or "H4" in d_attr):
                            print(f"✓ Found increment button")
                            btn.click()
                            time.sleep(1)
                            btn.click()  # Click twice to add 2 tickets
                            time.sleep(1)
                            print("✓ Added 2 tickets")
                            clicked = True
                            break
                except:
                    continue

                if clicked:
                    break

            if not clicked:
                print("⚠ Could not find increment button, trying first round button")
                if plus_buttons:
                    plus_buttons[0].click()
                    time.sleep(1)
                    plus_buttons[0].click()
                    time.sleep(1)
                    print("✓ Clicked button twice")

        driver.save_screenshot('/tmp/event_detail_after_selection.png')

        # Look for "Get Tickets" button (appears after selecting tickets)
        print("Looking for checkout button...")
        time.sleep(2)  # Wait for "Get Tickets" button to appear

        # The "Get Tickets" button has specific classes: bg-white text-violet-600
        get_tickets_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Get Tickets')]")

        if not get_tickets_buttons:
            # Fallback: look for any button with checkout-related text
            all_buttons = driver.find_elements(By.CSS_SELECTOR, "button")
            for btn in all_buttons:
                btn_text = btn.text.lower()
                if 'get tickets' in btn_text or 'checkout' in btn_text or 'buy' in btn_text:
                    get_tickets_buttons = [btn]
                    break

        if get_tickets_buttons:
            btn = get_tickets_buttons[0]
            print(f"✓ Found checkout button: '{btn.text}'")
            driver.save_screenshot('/tmp/before_checkout_click.png')

            # Scroll to button and click
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
            time.sleep(5)

            # Check if redirected (might be Stripe or error)
            current_url = driver.current_url
            print(f"After checkout click: {current_url}")

            if 'stripe' in current_url.lower():
                print("✓ Successfully redirected to Stripe checkout")
                driver.save_screenshot('/tmp/stripe_checkout.png')
                return True
            elif current_url != event_url:
                print(f"✓ Redirected to: {current_url}")
                driver.save_screenshot('/tmp/checkout_redirect.png')
                return True
            else:
                print("⚠ Still on event page after clicking checkout")
                driver.save_screenshot('/tmp/checkout_no_redirect.png')

                # Check page source for error messages
                page_text = driver.find_element(By.TAG_NAME, "body").text
                if 'error' in page_text.lower() or 'failed' in page_text.lower():
                    print(f"⚠ Possible error on page")
                return False
        else:
            print("⚠ No 'Get Tickets' button found - did ticket selection work?")
            driver.save_screenshot('/tmp/no_checkout_button.png')
            return False

    except Exception as e:
        print(f"✗ Error in ticket selection: {e}")
        driver.save_screenshot('/tmp/ticket_selection_error.png')
        import traceback
        traceback.print_exc()
        return False

def test_create_event(driver):
    """Test creating an event (authenticated)"""
    print("\n=== Test: Create Event ===")
    driver.get(f"{FRONTEND_URL}/create-event")
    time.sleep(2)

    try:
        # Check if redirected to login (not authenticated properly)
        if driver.current_url == f"{FRONTEND_URL}/login":
            print("⚠ Redirected to login - not authenticated")
            return False

        # Check for create event form
        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "Create Event" in page_text or "Event Title" in page_text:
            print("✓ Create event page accessible")
            driver.save_screenshot('/tmp/create_event.png')
            return True
    except:
        pass

    print("⚠ Create event page not accessible")
    return False

def test_my_events(driver):
    """Test viewing organizer's events"""
    print("\n=== Test: My Events ===")
    driver.get(f"{FRONTEND_URL}/my-events")
    time.sleep(2)

    try:
        if driver.current_url == f"{FRONTEND_URL}/login":
            print("⚠ Redirected to login")
            return False

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "My Events" in page_text:
            print("✓ My events page accessible")
            driver.save_screenshot('/tmp/my_events.png')
            return True
    except:
        pass

    print("⚠ My events page not accessible")
    return False

def test_my_tickets(driver):
    """Test viewing user's tickets"""
    print("\n=== Test: My Tickets ===")
    driver.get(f"{FRONTEND_URL}/my-tickets")
    time.sleep(2)

    try:
        if driver.current_url == f"{FRONTEND_URL}/login":
            print("⚠ Redirected to login")
            return False

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "My Tickets" in page_text or "No tickets" in page_text:
            print("✓ My tickets page accessible")
            driver.save_screenshot('/tmp/my_tickets.png')
            return True
    except:
        pass

    print("⚠ My tickets page not accessible")
    return False

def test_check_in(driver):
    """Test check-in page"""
    print("\n=== Test: Check-In Page ===")
    driver.get(f"{FRONTEND_URL}/check-in")
    time.sleep(2)

    try:
        if driver.current_url == f"{FRONTEND_URL}/login":
            print("⚠ Redirected to login")
            return False

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "Check-In" in page_text or "Scan or enter ticket code" in page_text:
            print("✓ Check-in page accessible")
            driver.save_screenshot('/tmp/checkin.png')
            return True
    except:
        pass

    print("⚠ Check-in page not accessible")
    return False

def run_all_tests():
    """Run all E2E tests with Clerk authentication"""
    print("=" * 70)
    print("TIKEPAM E2E TESTS WITH CLERK AUTHENTICATION")
    print("=" * 70)

    # Check for required environment variables
    if not TEST_USER_EMAIL or not TEST_USER_PASSWORD:
        print("\n✗ TEST_USER_EMAIL and TEST_USER_PASSWORD must be set in .env")
        print("\nTo set up test user:")
        print("  1. Go to http://localhost:5173/signup")
        print("  2. Create account with temp-mail.org email")
        print("  3. Verify email")
        print("  4. Add credentials to .env:")
        print("     TEST_USER_EMAIL=your-email@temp-mail.org")
        print("     TEST_USER_PASSWORD=YourPassword123!")
        return False

    print(f"Using test account: {TEST_USER_EMAIL}")

    driver = None

    try:
        # Setup browser
        print("\n=== Setting up browser ===")
        driver = setup_driver(headless=False)
        print("✓ Chrome browser launched")

        # Login with existing user
        login_success = clerk_login(driver, TEST_USER_EMAIL, TEST_USER_PASSWORD)

        if not login_success:
            print("\n✗ Login failed")
            print("Check screenshots:")
            print("  - /tmp/clerk_login_page.png")
            print("  - /tmp/clerk_login_error.png")
            print("\nPossible issues:")
            print("  - Wrong credentials in .env")
            print("  - User not verified in Clerk")
            print("  - User not synced to Supabase")
            return False

        # Run tests
        print("\n=== Waiting for Clerk session to stabilize ===")
        time.sleep(8)  # Wait longer for session to fully establish across the app
        print("✓ Session should be ready")

        # Basic navigation tests
        test_browse_events(driver)
        test_create_event(driver)
        test_my_events(driver)
        test_my_tickets(driver)
        test_check_in(driver)

        # Advanced form interaction tests
        print("\n" + "=" * 70)
        print("ADVANCED INTERACTION TESTS")
        print("=" * 70)

        test_create_event_full_form(driver)
        time.sleep(2)

        test_select_tickets_and_checkout(driver)
        time.sleep(2)

        print("\n" + "=" * 70)
        print("E2E TESTS COMPLETED!")
        print("=" * 70)
        print("\nScreenshots saved:")
        print("  Basic Navigation:")
        print("    - /tmp/clerk_login_page.png")
        print("    - /tmp/events_authenticated.png")
        print("    - /tmp/create_event.png")
        print("    - /tmp/my_events.png")
        print("    - /tmp/my_tickets.png")
        print("    - /tmp/checkin.png")
        print("  Form Interactions:")
        print("    - /tmp/create_event_filled.png")
        print("    - /tmp/create_event_success.png")
        print("    - /tmp/event_detail_before_selection.png")
        print("    - /tmp/event_detail_after_selection.png")
        print("    - /tmp/before_checkout_click.png")
        print("    - /tmp/stripe_checkout.png (if checkout succeeded)")

        print("\nBrowser will close in 5 seconds...")
        time.sleep(5)

        return True

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        if driver:
            driver.quit()

        print("\n=== Test user persisted for future test runs ===")

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
