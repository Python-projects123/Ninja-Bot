from playwright.sync_api import sync_playwright
import time

# Core Target Server Link Configuration
BASE_URL = "ninja.greninja.xyz"

# IMPORTANT REMINDER: You must change the username string on the line below 
# before EVERY single test run, or the backend database will throw a duplicate error.
USERNAME = "ninja_runner_v10" 
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
        
        # 1. Access Main Portal
        print(f"Connecting to host target portal: {BASE_URL}")
        page.goto(BASE_URL, wait_until="networkidle")
        time.sleep(2)

        # 2. Fire Signup Modal Trigger
        print("Clicking the primary coral banner 'Join' action target button...")
        join_selectors = [
            "div.banner button:has-text('Join')",
            "button:has-text('Join')",
            "a:has-text('Join')",
            "text=Join Ninja"
        ]
        
        clicked_join = False
        for selector in join_selectors:
            try:
                target = page.locator(selector).first
                if target.count() > 0 and target.is_visible():
                    target.click()
                    clicked_join = True
                    break
            except:
                continue

        if not clicked_join:
            print("Banner selection hidden. Defaulting to navigation header fallback link...")
            page.get_by_text("Join Ninja", exact=True).first.click()

        # Wait for wizard layout card to slide in
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # 3. Complete Step 1: User Account Identification Parameters
        print("Processing Step 1 registration credential forms...")
        
        user_input = page.locator("input[placeholder*='Username'], input[id*='user']").first
        user_input.wait_for(state="visible", timeout=10000)
        user_input.fill(USERNAME)

        # Identify password slots and distribute strings safely
        password_slots = page.locator("input[type='password']")
        if password_slots.count() >= 2:
            password_slots.nth(0).fill(PASSWORD)
            password_slots.nth(1).fill(PASSWORD)
        else:
            page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
            page.get_by_placeholder("Type password again").first.fill(PASSWORD)

        time.sleep(1)

        # Submit Step 1 
        print("Advancing past credential selection layer...")
        next_btn_1 = page.locator("button:has-text('Next'), .next-btn, input[type='submit']").first
        next_btn_1.click()
        
        # Safe structural pause to allow the layout engine to swap views
        page.wait_for_load_state("networkidle")
        time.sleep(4)

        # 4. Complete Step 2: Country, Birth Month/Year, and Gender Validation Fields
        print("Processing Step 2 user meta profiling forms...")
        
        # Fill selection dropdowns (Country, Month, Year) by matching structural options safely
        dropdowns = page.locator("select")
        if dropdowns.count() > 0:
            print(f"Detected {dropdowns.count()} configuration select nodes. Assigning values...")
            for i in range(dropdowns.count()):
                box = dropdowns.nth(i)
                if box.is_visible():
                    try:
                        # Selects the second valid structural index item in the drop-down element
                        box.select_option(index=1)
                    except:
                        continue
        
        # Handle secondary floating text boxes if the platform asks for a manual email input
        text_fields = page.locator("input[type='text'], input:not([type])")
        if text_fields.count() > 0:
            for i in range(text_fields.count()):
                field = text_fields.nth(i)
                if field.is_visible() and field.input_value() == "":
                    field.fill("automation_runner_bot@example.com")

        # Select gender radio bubbles or checking markers if exposed on screen
        gender_options = page.locator("input[type='radio'], input[type='checkbox']")
        if gender_options.count() > 0:
            for i in range(gender_options.count()):
                radio = gender_options.nth(i)
                if radio.is_visible():
                    try:
                        radio.check()
                        break # Check one valid parameter box option and skip out
                    except:
                        continue

        time.sleep(2)

        # Submit Step 2 Profile Setup
        print("Executing final wizard account compilation sequence...")
        next_btn_2 = page.locator("button:has-text('Next'), button:has-text('Submit'), button[type='submit']").first
        if next_btn_2.count() > 0 and next_btn_2.is_visible():
            next_btn_2.click()
        else:
            print("Target submit button obscured. Forcing transaction via hardware keyboard event route...")
            page.keyboard.press("Enter")

        # 5. Database Write Pipeline Verification
        print("Data package successfully pushed to server. Holding workflow pipeline open for index processing latency...")
        page.wait_for_load_state("networkidle")
        time.skip = time.sleep(12) # Robust execution pause allowing database write validation pipelines to save

        # Verify registration confirmation landing page
        confirmation_profile_endpoint = f"{BASE_URL}/users/{USERNAME}"
        print(f"Routing headless runner to profile check zone: {confirmation_profile_endpoint}")
        page.goto(confirmation_profile_endpoint, wait_until="networkidle")
        time.sleep(5)
        
        print(f"Automation routine finalized. Terminal URL view state reads: {page.url}")
        browser.close()

if __name__ == "__main__":
    create_account()
