"""Headless Selenium test: Signup → 2FA → Dashboard."""
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

FLASK_LOG = "/tmp/flask_output.log"
VUE_URL = "http://localhost:5173"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,900")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

timestamp = int(time.time() * 1000)
email = f"test_{timestamp}@example.com"
password = "TestPass123!"
fullname = "Test User"

try:
    # Snapshot existing codes
    try:
        with open(FLASK_LOG, "r") as f:
            pre_codes = set(re.findall(r"VERIFICATION CODE:\s*(\d{6})", f.read()))
    except FileNotFoundError:
        pre_codes = set()

    # --- SIGNUP ---
    print(f"[1] Navigating to signup...")
    driver.get(f"{VUE_URL}/signup")
    time.sleep(2)
    print(f"    URL: {driver.current_url}")
    print(f"    Title: {driver.title}")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fullname")))
    print(f"    Form found. Filling in...")
    driver.find_element(By.CSS_SELECTOR, "#fullname").send_keys(fullname)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)

    print(f"    Submitting signup form...")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    print(f"    URL after submit: {driver.current_url}")

    # Check for errors on page
    errors = driver.find_elements(By.CSS_SELECTOR, ".bg-rose-50, .bg-red-50")
    for e in errors:
        if e.is_displayed():
            print(f"    ERROR ON PAGE: {e.text}")

    # Check browser console for network errors
    logs = driver.get_log("browser")
    for log in logs:
        if "error" in log.get("level", "").lower() or "ERR" in log.get("message", ""):
            print(f"    CONSOLE: {log['message'][:200]}")

    if "/2fa/verify" not in driver.current_url:
        print(f"    FAIL: Not redirected to 2FA page")
        # Try to capture what's on the page
        body = driver.find_element(By.TAG_NAME, "body").text[:500]
        print(f"    Page content: {body}")

        # Also check network by trying the API directly via JS
        result = driver.execute_script("""
            try {
                const r = await fetch('http://localhost:5001/api/auth/session', {credentials: 'include'});
                const d = await r.json();
                return JSON.stringify(d);
            } catch(e) {
                return 'FETCH ERROR: ' + e.message;
            }
        """)
        print(f"    Session check: {result}")
        raise SystemExit(1)

    # --- 2FA ---
    print(f"\n[2] On 2FA page. Getting code...")
    time.sleep(2)

    code = None
    for _ in range(30):
        with open(FLASK_LOG, "r") as f:
            all_codes = re.findall(r"VERIFICATION CODE:\s*(\d{6})", f.read())
            new = [c for c in all_codes if c not in pre_codes]
            if new:
                code = new[-1]
                break
        time.sleep(0.5)

    if not code:
        print(f"    FAIL: No 2FA code found in Flask log")
        raise SystemExit(1)

    print(f"    Code: {code}")

    otp_inputs = driver.find_elements(By.CSS_SELECTOR, "input[maxlength='1']")
    print(f"    OTP inputs found: {len(otp_inputs)}")
    for i, digit in enumerate(code):
        otp_inputs[i].send_keys(digit)

    time.sleep(3)

    # Handle alert
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

    print(f"    URL after code entry: {driver.current_url}")

    if "/profile" not in driver.current_url:
        # Try clicking Continue
        buttons = driver.find_elements(By.CSS_SELECTOR, "button")
        for btn in buttons:
            if "continue" in btn.text.lower() and btn.is_enabled():
                btn.click()
                break
        time.sleep(2)
        try:
            driver.switch_to.alert.accept()
        except Exception:
            pass
        time.sleep(2)

    print(f"    Final URL: {driver.current_url}")

    # --- DASHBOARD ---
    if "/profile" in driver.current_url:
        print(f"\n[3] Dashboard loaded!")
        h1 = driver.find_element(By.CSS_SELECTOR, "h1")
        print(f"    Heading: {h1.text}")

        # --- NAVBAR VERIFICATION ---
        print(f"\n[4] Verifying authenticated navbar...")
        nav = driver.find_element(By.CSS_SELECTOR, "nav")
        nav_text = nav.text
        print(f"    Nav text: {nav_text}")

        # Check for Eventbrite-style icon links
        checks = {
            "Create Event": "Create Event" in nav_text,
            "Favorites": "Favorites" in nav_text,
            "Tickets": "Tickets" in nav_text,
            "User email": email in nav_text,
        }
        all_pass = True
        for label, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"    [{status}] {label}")
            if not passed:
                all_pass = False

        # Check guest links are NOT present
        guest_links = ["Live Events", "How We Work", "Buy Tickets", "Join Tikepam"]
        for link in guest_links:
            if link in nav_text:
                print(f"    [FAIL] Guest link '{link}' should not appear for authenticated user")
                all_pass = False

        if all_pass:
            print(f"\n=== SUCCESS ===")
        else:
            print(f"\n=== NAVBAR CHECKS FAILED ===")
    else:
        print(f"\n[3] FAIL: Not on profile page")
        body = driver.find_element(By.TAG_NAME, "body").text[:500]
        print(f"    Page content: {body}")

finally:
    driver.quit()
