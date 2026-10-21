# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://greninja.xyz"
USERNAME = "randombot"
PASSWORD = "bot"

def create_account():
    with sync_playwright() as p:
        # CRITICAL FIX: Changed headless to True so it runs on cloud servers without a monitor
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="networkidle")

        # Open signup (nav "Join Ninja" button)
        page.get_by_text("Join Ninja", exact=True).first.click()
        page.wait_for_load_state("networkidle")

        # Step 1: Account Details
        page.get_by_placeholder("Username").fill(USERNAME)
        page.get_by_placeholder("Password", exact=True).fill(PASSWORD)
        page.get_by_placeholder("Type password again").fill(PASSWORD)
        page.get_by_text("Next", exact=True).click()

        # Wait for Step 2 to load completely
        page.wait_for_load_state("networkidle")
        time.sleep(2)  # Short pause to ensure the UI fully renders
        print("URL after step 1:", page.url)

        # Step 2: Handle Unknown Form Fields Automatically
        # This looks for any input fields or dropdown selects on the second page
        text_inputs = page.locator("input[type='text'], input:not([type])")
        dropdown_selects = page.locator("select")

        # 1. Fill in any text input fields found on step 2 (e.g., Email, Location)
        if text_inputs.count() > 0:
            for i in range(text_inputs.count()):
                if text_inputs.nth(i).is_visible():
                    # Fills out placeholders safely depending on field presence
                    text_inputs.nth(i).fill("bot_info@example.com") 

        # 2. Select the first option for any dropdowns found (e.g., Birth Month, Country)
        if dropdown_selects.count() > 0:
            for i in range(dropdown_selects.count()):
                if dropdown_selects.nth(i).is_visible():
                    dropdown_selects.nth(i).select_option(index=1)

        # 3. Handle typical radio button selections if present (e.g., Gender/Agreement)
        radio_buttons = page.locator("input[type='radio'], input[type='checkbox']")
        if radio_buttons.count() > 0:
            for i in range(radio_buttons.count()):
                if radio_buttons.nth(i).is_visible():
                    radio_buttons.nth(i).check()

        # Step 2 Submission: Try clicking Next, Submit, or the main submit button
        submit_button = page.locator("button[type='submit'], input[type='submit']").first
        if submit_button.count() > 0 and submit_button.is_visible():
            submit_button.click()
        else:
            # Fallback text-based click if no submit type element is explicit
            try:
                page.get_by_text("Next", exact=True).click()
            except:
                page.get_by_text("Submit", exact=True).click()

        # Finalize and log out
        page.wait_for_load_state("networkidle")
        time.sleep(3)  # Give the database a moment to register the new account
        print("Final Registration URL page reached:", page.url)

        browser.close()

if __name__ == "__main__":
    create_account()
