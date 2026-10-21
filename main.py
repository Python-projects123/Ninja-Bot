from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://greninja.xyz"
USERNAME = "randombot"
PASSWORD = "bot"

def create_account():
    with sync_playwright() as p:
        # Launch with custom user args to prevent cloud bot blocking
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )  
        
        # Set a standard desktop window size and realistic browser identity
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to target site...")
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"Initial navigation warning: {e}. Trying alternative wait step...")

        # Safe search locator loop for the introductory registration portal button
        print("Locating signup wizard trigger button...")
        join_selectors = [
            "text=Join Ninja", 
            "button:has-text('Join')", 
            "a:has-text('Join')",
            ".join-btn"
        ]
        
        join_btn = None
        for selector in join_selectors:
            try:
                el = page.locator(selector).first
                if el.count() > 0 and el.is_visible():
                    join_btn = el
                    break
            except:
                continue

        if join_btn:
            join_btn.click()
            print("Successfully entered signup wizard portal step.")
        else:
            print("Warning: Standard 'Join' elements hidden. Attempting to proceed assuming form is open.")

        time.sleep(3) # Safe buffer pause for DOM rendering animations

        # Step 1: Account Identification Details
        print("Processing Step 1 registration inputs...")
        try:
            user_input = page.get_by_placeholder("Username").first
            user_input.wait_for(state="attached", timeout=5000)
            user_input.fill(USERNAME)
            
            page.get_by_placeholder("Password", exact=True).first.fill(PASSWORD)
            page.get_by_placeholder("Type password again").first.fill(PASSWORD)
            
            next_step_btn = page.locator("button:has-text('Next'), input[type='submit'], .next-btn").first
            next_step_btn.click()
            print("Step 1 basic details submitted successfully.")
        except Exception as e:
            print(f"Step 1 input exception crashed: {e}")
            browser.close()
            return

        # Step 2: Handle Secondary Wizard Content Transitions Safely
        print("Awaiting Step 2 backend wizard elements...")
        time.sleep(4) 
        print("Active page location position:", page.url)

        # Catch-all input query selectors to handle variable Step 2 fields dynamically
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

        time.sleep(4)
        print("Automation execution concluded. Terminal page url status:", page.url)
        browser.close()

if __name__ == "__main__":
    create_account()
