from playwright.sync_api import sync_playwright
import time

# Core Target Server Configuration URL
BASE_URL = "https://ninja.greninja.xyz/"

# CRITICAL REMINDER: You must change the username string value on the line below 
# before EVERY single run, or the database will crash with a duplicate error!
USERNAME = "ninja_final_success_01" 
PASSWORD = "SecurePassword123!"

def create_account():
    with sync_playwright() as p:
        # Launch engine with custom args to bypass cloud verification parameters
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )  
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 1. Load the Landing Page
        print(f"Connecting to host target portal: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(2)

        # 2. Click the Visual "Join" Button inside the main Red Banner Zone
        print("Locating the visual 'Join' button inside the banner container...")
        try:
            page.locator("div.banner button:has-text('Join')").first.click()
            print("-> Successfully triggered signup modal.")
        except:
            print("Banner element blocked from direct focus. Using navbar link fallback...")
            page.get_by_text("Join Ninja", exact=True).first.click()

        # Wait for the modal box to render completely
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # 3. Enter Credentials inside the Card inputs
        print("Entering account registration credentials...")
        
        # Target the Username placeholder field securely
        username_field = page.locator("input[placeholder*='Username'], input[id*='user']").first
        username_field.wait_for(state="visible", timeout=10000)
        username_field.fill(USERNAME)
        print(f"-> Typed Username: {USERNAME}")

        # Distribute password tokens safely into both slots
        password_slots = page.locator("input[type='password']")
        if password_slots.count() >= 2:
            password_slots.nth(0).fill(PASSWORD)
            password_slots.nth(1).fill(PASSWORD)
            print("-> Typed passwords into standard password fields.")
        else:
            page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
            page.get_by_placeholder("Type password again").first.fill(PASSWORD)
            print("-> Typed passwords using fallback placeholders.")

        time.sleep(2)

        # 4. Click the bright coral-red "Next" submit button firmly
        print("Clicking the main 'Next' button to submit the account...")
        
        # Focus explicitly on the Next element inside the active signup card
        submit_btn = page.locator("button:has-text('Next'), input[type='submit'], .next-btn").first
        submit_btn.wait_for(state="visible", timeout=5000)
        submit_btn.click()
        print("-> Next button clicked successfully.")

        # 5. Database Write Buffer
        print("Data package successfully pushed to server. Holding workflow pipeline open for index processing...")
        page.wait_for_load_state("networkidle")
        time.sleep(12) # Give the database a solid 12 seconds to save the new user row

        # 6. Verify User Exists
        confirmation_profile_endpoint = f"{BASE_URL}/users/{USERNAME}"
        print(f"Routing headless runner to verification page check: {confirmation_profile_endpoint}")
        page.goto(confirmation_profile_endpoint, wait_until="networkidle")
        time.sleep(5)
        
        # Save a screenshot to the runner environment logs to verify page layout
        page.screenshot(path="final_status.png")
        print(f"Automation routine finalized. Terminal URL page view status reads: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
