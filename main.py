from playwright.sync_api import sync_playwright
import time
import random
import string

# GUARANTEED SUBDOMAIN TARGET
BASE_URL = "https://ninja.greninja.xyz"

# FIXED: Using a standard, universally acceptable alphanumeric password string
PASSWORD = "NinjaBotPassword99"

def generate_clean_username():
    """Generates a clean username WITHOUT underscores to prevent database validation drops."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"ninjabot{random_suffix}" # Example output: ninjabota1b2c3

def create_account():
    USERNAME = generate_clean_username()
    print(f"Generated Clean Username for this run: {USERNAME}")

    with sync_playwright() as p:
        print("Launching automated browser...")
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )  
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Navigating directly to: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(3)

        print("Clicking the signup navigation link fallback...")
        try:
            page.get_by_text("Join Ninja", exact=True).first.click()
            print("Signup modal overlay box triggered.")
        except Exception as e:
            print(f"Click failed ({e}). Attempting structural banner button path extraction...")
            page.locator("div.banner button:has-text('Join')").first.click()

        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # ====================================================
        # INPUT SECTION: CHARACTER-BY-CHARACTER TYPING
        # ====================================================
        print("Locating form fields inside the active signup modal...")
        username_field = page.locator("input[placeholder*='Username'], input[id*='user']").first
        username_field.wait_for(state="visible", timeout=10000)
        
        # Click, focus, and type credentials safely
        username_field.click()
        for char in USERNAME:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.05, 0.12))

        password_slots = page.locator("input[type='password']")
        if password_slots.count() >= 2:
            # Fill slot 1
            password_slots.nth(0).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.04, 0.10))
                
            # Fill slot 2 (confirm password)
            password_slots.nth(1).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.04, 0.10))
        else:
            p1 = page.get_by_placeholder("Password", exact=True).first
            p1.click()
            p1.fill(PASSWORD)
            
            p2 = page.get_by_placeholder("Type password again").first
            p2.click()
            p2.fill(PASSWORD)

        time.sleep(2)

        # ====================================================
        # EXPLICIT ACCOUNT REGISTRATION SUBMISSION
        # ====================================================
        print("Locating submission button...")
        next_button = page.locator("button:has-text('Next'), input[type='submit'], .next-btn").first
        next_button.wait_for(state="visible", timeout=5000)
        
        print("Submitting the account credentials package...")
        next_button.click()
        
        # Give the server a clear 15 seconds to safely register and save the user rows
        print("Holding runtime process alive for backend write synchronization...")
        page.wait_for_load_state("networkidle")
        time.sleep(15) 

        # 3. Validation Link Check
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Navigating directly to check profile validation: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(5)
        
        page.screenshot(path="final_verified_status.png")
        print(f"Automation execution concluded. Terminal page url read state: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
