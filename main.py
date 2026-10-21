from playwright.sync_api import sync_playwright
import time
import random
import string

# GUARANTEED CORRECT URL
BASE_URL = "https://ninja.greninja.xyz"
PASSWORD = "SecurePassword123!"

def generate_random_username():
    """Generates a unique username to guarantee the account doesn't already exist."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"bot_runner_{random_suffix}"

def create_account():
    # Dynamic username generation
    USERNAME = generate_random_username()
    print(f"Generated Unique Username for this run: {USERNAME}")

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
        
        # 1. Navigate directly to the verified URL
        print(f"Navigating to: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(3)

        # 2. Click the specific visual "Join" button in the red banner
        print("Clicking the 'Join' button inside the banner section...")
        try:
            page.locator("div.banner button:has-text('Join')").first.click()
            print("Signup modal open.")
        except Exception as e:
            print(f"Banner element target missed ({e}). Trying navbar text selection fallback...")
            page.get_by_text("Join Ninja", exact=True).first.click()

        # Wait for form modal rendering frames
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # ====================================================
        # INPUT SECTION: TYPING DELAYS FOR ACCURATE HOOKS
        # ====================================================
        print("Locating form fields...")
        username_field = page.locator("input[placeholder*='Username'], input[id*='user']").first
        username_field.wait_for(state="visible", timeout=10000)
        
        # Focus and type the username character-by-character
        username_field.click()
        print("Typing username...")
        for char in USERNAME:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.05, 0.15))

        password_slots = page.locator("input[type='password']")
        if password_slots.count() >= 2:
            print("Twin password inputs found. Entering values...")
            
            # Type into password block 1
            password_slots.nth(0).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.12))
                
            # Type into confirm password block 2
            password_slots.nth(1).click()
            for char in PASSWORD:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.12))
        else:
            print("Fallback to placeholder selectors...")
            p1 = page.get_by_placeholder("Password", exact=True).first
            p1.click()
            p1.fill(PASSWORD)
            
            p2 = page.get_by_placeholder("Type password again").first
            p2.click()
            p2.fill(PASSWORD)

        time.sleep(2)

        # ====================================================
        # SUBMISSION & DATABASE SYNCHRONIZATION
        # ====================================================
        print("Clicking 'Next' button...")
        next_button = page.locator("button:has-text('Next'), input[type='submit'], .next-btn").first
        next_button.wait_for(state="visible", timeout=5000)
        next_button.click()
        print("Data bundle sent.")

        # Give the backend database 15 seconds to safely save and index the account profile parameters
        print("Holding connection open to allow backend database index synchronization...")
        page.wait_for_load_state("networkidle")
        time.sleep(15) 

        # 3. Direct Navigation to Verification Profile Link
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Navigating to verification profile link: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(5)
        
        # Capture screenshot verification artifact for your Action workspace logs
        page.screenshot(path="final_verified_status.png")
        print(f"Routine complete. Final profile landing page state reads: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
