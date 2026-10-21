from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://greninja.xyz"
USERNAME = "your_bot_username"
PASSWORD = "a-strong-password"

def create_account():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        
        print("Navigating to site...")
        page.goto(BASE_URL, wait_until="networkidle")

        # Open signup wizard safely
        print("Opening signup wizard...")
        join_btn = page.get_by_text("Join Ninja", exact=True).first
        join_btn.wait_for(state="visible", timeout=10000)
        join_btn.click()
        page.wait_for_load_state("networkidle")

        # Step 1: Account Details
        print("Filling out Step 1...")
        page.get_by_placeholder("Username").wait_for(state="visible")
        page.get_by_placeholder("Username").fill(USERNAME)
        page.get_by_placeholder("Password", exact=True).fill(PASSWORD)
        page.get_by_placeholder("Type password again").fill(PASSWORD)
        
        # Click next using a broad selector search
        next_btn = page.locator("button:has-text('Next'), input[type='submit']").first
        next_btn.click()

        # Step 2: Handle transition safely
        print("Waiting for Step 2 wizard fields...")
        page.wait_for_load_state("networkidle")
        time.sleep(3) # Safe buffer for animations
        
        # Log active page state
        print("Current page URL position:", page.url)

        # Dynamic fallback form selection engine for Step 2
        text_inputs = page.locator("input[type='text'], input:not([type])")
        if text_inputs.count() > 0:
            for i in range(text_inputs.count()):
                el = text_inputs.nth(i)
                if el.is_visible():
                    el.fill("bot_user@example.com")

        dropdowns = page.locator("select")
        if dropdowns.count() > 0:
            for i in range(dropdowns.count()):
                el = dropdowns.nth(i)
                if el.is_visible():
                    el.select_option(index=1)

        # Submit Step 2
        print("Submitting Step 2...")
        submit_btn = page.locator("button:has-text('Next'), button:has-text('Submit'), button[type='submit']").first
        if submit_btn.count() > 0 and submit_btn.is_visible():
            submit_btn.click()
        else:
            page.keyboard.press("Enter") # Absolute fallback action trigger

        page.wait_for_load_state("networkidle")
        time.sleep(3)
        print("Final target landing page:", page.url)
        browser.close()

if __name__ == "__main__":
    create_account()
