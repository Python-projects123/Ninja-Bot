# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright

BASE_URL = "https://ninja.greninja.xyz"
USERNAME = "your_bot_username"
PASSWORD = "a-strong-password"

def create_account():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set True once working
        page = browser.new_page()
        page.goto(BASE_URL, wait_until="networkidle")

        # Open signup (nav "Join Ninja" button)
        page.get_by_text("Join Ninja", exact=True).first.click()
        page.wait_for_load_state("networkidle")

        # Step 1
        page.get_by_placeholder("Username").fill(USERNAME)
        page.get_by_placeholder("Password", exact=True).fill(PASSWORD)
        page.get_by_placeholder("Type password again").fill(PASSWORD)
        page.get_by_text("Next", exact=True).click()

        # Step 2 is unknown: inspect it and extend below
        page.wait_for_load_state("networkidle")
        page.screenshot(path="step2.png")
        print("URL after step 1:", page.url)

        # TODO: fill step-2 fields here, then submit

        browser.close()

if __name__ == "__main__":
    create_account()
