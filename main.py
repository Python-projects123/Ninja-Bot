from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://greninja.xyz"
# Tip: Ensure you change this to a brand new username every run to prevent duplicate errors!
USERNAME = "randombot_v2" 
PASSWORD = "a-strong-password"

def create_account():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )  
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to target site...")
        page.goto(BASE_URL, wait_until="networkidle")

        print("Opening signup wizard...")
        try:
            page.get_by_text("Join Ninja", exact=True).first.click()
        except:
            page.locator("text=Join Ninja").first.click()
        page.wait_for_load_state("networkidle")

        # Step 1: Account Identification Details
        print("Processing Step 1 registration inputs...")
        page.get_by_placeholder("Username").first.wait_for(state="visible")
        page.get_by_placeholder("Username").first.fill(USERNAME)
        page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
        page.get_by_placeholder("Type password again").first.fill(PASSWORD)
        
        page.locator("button:has-text('Next'), input[type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(3) 

        # Step 2: Handle Wizard Content Transitions
        print("Processing Step 2 form components...")
        
        text_inputs = page.locator("input[type='text'], input:not([type])")
        if text_inputs.count() > 0:
            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible():
                    el.fill("bot_user_account@example.com")

        dropdowns = page.locator("select")
        if dropdowns.count() > 0:
            for i in range(dropdowns.count()):
                el = dropdowns.nth(i)
                if el.is_visible():
                    el.select_option(index=1)

        # Finalize and Submit Wizard Record
        print("Executing Step 2 record submission sequence...")
        submit_btn = page.locator("button:has-text('Next'), button:has-text('Submit'), button[type='submit']").first
        if submit_btn.count() > 0 and submit_btn.is_visible():
            submit_btn.click()
        else:
            page.keyboard.press("Enter") 

        # CRITICAL FIX: The backend requires processing time to save the profile.
        # We wait for the network to go silent, then sleep for 10 seconds before navigating away.
        print("Account submitted. Holding connection open for database indexing...")
        page.wait_for_load_state("networkidle")
        time.sleep(10) 
        
        # Safe redirection to confirm the user exists on the platform
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Navigating to verification profile: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(5)
        
        print("Automation execution concluded. Final profile URL page state:", page.url)
        browser.close()

if __name__ == "__main__":
    create_account()
