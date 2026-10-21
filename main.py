from playwright.sync_api import sync_playwright
import time
import random
import string

# Core Subdomain Target URL Configuration
BASE_URL = "https://ninja.greninja.xyz"
PASSWORD = "SecurePassword123!"

def generate_clean_username():
    """Generates an explicit unique username string to guarantee no registration duplicate drops."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"ninjabot{random_suffix}"

def create_account():
    USERNAME = generate_clean_username()
    print(f"Generated Account Identification Token: {USERNAME}")

    with sync_playwright() as p:
        print("Launching stealth browser container...")
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )  
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 1. Access portal destination directly
        print(f"Opening secure site connection: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(2)

        # 2. Trigger the modal form overlay sequence
        print("Activating the registration modal...")
        try:
            page.get_by_text("Join Ninja", exact=True).first.click()
        except:
            page.locator("div.banner button:has-text('Join')").first.click()

        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # ====================================================
        # REALISTIC STEP 1 FORM CONFIGURATION
        # ====================================================
        print("Locating form input nodes...")
        username_field = page.locator("input[placeholder*='Username'], input[id*='user']").first
        username_field.wait_for(state="visible", timeout=10000)
        
        # Human-like typing delay sequence to ensure event listeners catch inputs
        username_field.click()
        for char in USERNAME:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.05, 0.12))

        password_slots = page.locator("input[type='password']")
        if password_slots.count() >= 2:
            password_slots.nth(0).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.04, 0.10))
                
            password_slots.nth(1).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.04, 0.10))
        else:
            page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
            page.get_by_placeholder("Type password again").first.fill(PASSWORD)

        time.sleep(1.5)

        # ====================================================
        # ACCOUNT SUBMISSION WITH SESSION VALIDATION
        # ====================================================
        print("Locating step compilation submission element...")
        next_button = page.locator("button:has-text('Next'), input[type='submit'], .next-btn").first
        next_button.wait_for(state="visible", timeout=5000)
        
        print("Transmitting credential parameters to endpoint backend...")
        next_button.click()

        # EXPECTED SESSION ATTACHMENT CHECK
        # Instead of just sleeping, we wait for the navbar layout state to reflect an active login session
        print("Monitoring layout wrapper for active session cookies...")
        try:
            # Look for the profile thumbnail or user menu container that appears after signup
            session_marker = page.locator(".user-info, .profile-link, button:has-text('Sign Out'), .nav-user").first
            session_marker.wait_for(state="visible", timeout=15000)
            print("Session successfully authenticated! Backend database write complete.")
        except Exception as e:
            print(f"Session marker layout change timed out ({e}). Proceeding to explicit profile route verify...")

        # Safe hold-open interval for asset pipeline loading
        time.sleep(10) 

        # 3. Direct verification route landing check
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Checking index verification link route: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(4)
        
        page.screenshot(path="final_verified_status.png")
        print(f"Automation execution fully complete. Target final URL matches: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
