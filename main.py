# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright
import time

# FIXED: Locked down the accurate subdomain string destination endpoint 
BASE_URL = "https://ninja.greninja.xyz"
USERNAME = "ninja_bot_runner_99" 
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
        
        print(f"Navigating explicitly to: {BASE_URL}")
        # Explicit wait setup targeted directly onto the full BASE_URL parameter string
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        print("Opening signup wizard...")
        join_btn = page.get_by_text("Join Ninja", exact=True).first
        join_btn.wait_for(state="visible", timeout=10000)
        join_btn.click()
        page.wait_for_load_state("networkidle")

        # Step 1: Form Fill
        print("Processing Step 1 registration inputs...")
        page.get_by_placeholder("Username").first.wait_for(state="visible")
        page.get_by_placeholder("Username").first.fill(USERNAME)
        page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
        page.get_by_placeholder("Type password again").first.fill(PASSWORD)
        
        # Safe forward click
        next_step_btn = page.locator("button:has-text('Next'), input[type='submit']").first
        next_step_btn.click()
        
        print("Step 1 basic details submitted. Transitioning to Step 2...")
        time.sleep(4) 

        # Step 2: Handle Secondary Form Elements
        print("Processing Step 2 form configurations...")
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

        print("Account submitted. Holding connection open for backend indexing write...")
        time.sleep(10) 
        
        # Safe structural redirection path using the full subdomain string
        target_profile_url = f"{BASE_URL}/users/{USERNAME}"
        print(f"Navigating to confirmation URL profile string: {target_profile_url}")
        page.goto(target_profile_url, wait_until="networkidle")
        time.sleep(5)
        
        print("Automation execution concluded successfully. Final profile URL page state:", page.url)
        browser.close()

if __name__ == "__main__":
    create_account()
