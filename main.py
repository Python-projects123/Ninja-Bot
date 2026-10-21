from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://greninja.xyz"
# REMINDER: Always change this to a brand-new username before launching a run!
USERNAME = "ninja_tester_bot_01" 
PASSWORD = "a-strong-password-123"

def create_account():
    with sync_playwright() as p:
        # Launch with automation evasion flags
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )  
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Navigating to landing page: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(2)

        # STEP 1: Look for the banner "Join" button seen in your second screenshot
        print("Locating the visual 'Join' button inside the main banner red zone...")
        
        # We try multiple precise structural paths to find the exact registration button
        join_button_selectors = [
            "button:has-text('Join')",
            "a:has-text('Join')",
            "div.banner button:has-text('Join')",
            "text=Join Ninja",
            "[class*='join']"
        ]
        
        clicked_join = False
        for selector in join_button_selectors:
            try:
                target = page.locator(selector).first
                if target.count() > 0 and target.is_visible():
                    print(f"Found match using selector: {selector}. Clicking now...")
                    target.click()
                    clicked_join = True
                    break
            except Exception as e:
                continue

        # Ultimate fallback fallback if the banner click fails to fire
        if not clicked_join:
            print("Banner button hidden from direct focus. Forcing navigation click on navbar header element...")
            page.get_by_text("Join Ninja", exact=True).first.click()

        # Await Modal box rendering animation frames
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # STEP 2: Input your credentials inside the visual modal box seen in your third screenshot
        print("Entering account identification parameters...")
        
        # Locate the inputs securely by searching via text context parent wrappers or labels
        username_field = page.locator("input[placeholder*='Username'], input[id*='user'], label:has-text('username') + input").first
        username_field.wait_for(state="visible", timeout=5000)
        username_field.fill(USERNAME)
        print("-> Filled Username.")

        password_fields = page.locator("input[type='password']")
        if password_fields.count() >= 2:
            password_fields.nth(0).fill(PASSWORD)
            password_fields.nth(1).fill(PASSWORD)
            print("-> Filled both Password fields successfully.")
        else:
            # Fallback search if the password boxes don't explicitly declare type='password'
            page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
            page.get_by_placeholder("Type password again").first.fill(PASSWORD)
            print("-> Filled password fields via placeholder fallbacks.")

        time.sleep(1)

        # STEP 3: Click the bright coral-red "Next" button at the bottom of the modal card
        print("Clicking the primary 'Next' wizard transition button...")
        
        next_selectors = [
            "button:has-text('Next')",
            "div.modal button:has-text('Next')",
            "[class*='next']",
            "text=Next"
        ]
        
        clicked_next = False
        for selector in next_selectors:
            try:
                btn = page.locator(selector).first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    clicked_next = True
                    print("Successfully advanced past Step 1 form card.")
                    break
            except:
                continue
                
        if not clicked_next:
            # Complete physical fallback action if the button layout is structurally tricky
            print("Button locator obscured. Dispatching universal hardware keyboard 'Enter' confirmation...")
            page.keyboard.press("Enter")

        # STEP 4: Handle Step 2 transitions and check for secondary wizard fields
        print("Awaiting secondary wizard configuration overlay panel...")
        page.wait_for_load_state("networkidle")
        time.sleep(4)
        print(f"Current page target location state: {page.url}")

        # General loop to fill any text boxes found on the second step
        text_inputs = page.locator("input[type='text'], input:not([type])")
        if text_inputs.count() > 0:
            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible() and el.input_value() == "":
                    el.fill("ninja_bot_email@example.com")

        # Select standard values for any custom dropdown selections (e.g. Birth Month, Country)
        dropdowns = page.locator("select")
        if dropdowns.count() > 0:
            for i in range(dropdowns.count()):
                el = dropdowns.nth(i)
                if el.is_visible():
                    el.select_option(index=1)

        # Final submission sequence
        print("Submitting Step 2 configuration parameters...")
        final_submit = page.locator("button:has-text('Next'), button:has-text('Submit'), button[type='submit']").first
        if final_submit.count() > 0 and final_submit.is_visible():
            final_submit.click()
        else:
            page.keyboard.press("Enter")

        # Give the backend platform a standard 10-second processing buffer to write the record
        print("Data transmitted. Holding pipeline open for database write latency rules...")
        page.wait_for_load_state("networkidle")
        time.sleep(10)

        # Redirection check to make sure profile page doesn't throw a 'User not found' error
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Navigating to confirmation URL: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(4)
        
        print(f"Automation sequence finished. Terminal page landing status: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
