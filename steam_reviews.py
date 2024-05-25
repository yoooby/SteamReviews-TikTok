import json
import os
from pathlib import Path
import time
from playwright.sync_api import sync_playwright
import cv2
from datetime import datetime

# Utility Functions
def add_transparency(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img[:, :, 3] = 240
    cv2.imwrite(img_path, img)



def save_text(review_texts):
    with open("review_texts.txt", "w", encoding="utf-8") as file:
        for idx, text in enumerate(review_texts):
            file.write(f"Review {idx}:\n{text}\n\n")



# Main Function
def download_funny_steam_reviews(app_id):
    review_texts = []

    folder_path = f"./assets/{app_id}"
    
    with sync_playwright() as p:
        print("Launching Headless Browser")
        browser = p.chromium.launch(headless=False)  # Set to False to see the browser
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        page.goto(f"https://store.steampowered.com/app/{app_id}/")
        #page.wait_for_load_state('networkidle')

        # Handle age verification if necessary
        if page.locator('#ageYear').is_visible():
            page.select_option('#ageYear', '1990')
            page.click('text="View Page"')



        display_as_dropdown = page.locator('#review_context')  # Select the dropdown by its ID
        display_as_dropdown.scroll_into_view_if_needed()
        page.evaluate('''document.querySelector('#review_context').value = 'funny';''')
        page.evaluate('''document.querySelector('#review_context').dispatchEvent(new Event('change'));''')
        time.sleep(5)
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        # display_as_dropdown.click()
        # print("waiti g for funyny to load")
        # time.sleep(2)
        # display_as_dropdown.locator('option[value="funny"]').click(force=True)
        # # Wait for the reviews to load
        # #page.wait_for_selector('.apphub_CardContentMain')

        # # Scroll to load more reviews
        # print("Scrolling to load all reviews")
        # while True:
        #     page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        #     page.wait_for_timeout(2000)  # Wait for new content to load
        #     new_height = page.evaluate("document.body.scrollHeight")
        #     if new_height == previous_height:
        #         break
        #     previous_height = new_height
        review_elements = page.locator("#Reviews_funny .review_box").all()
        #review_elements = page.query_selector_all('.review_box')
        for idx, element in enumerate(review_elements):
            if "partial" in element.get_attribute("class"):
                continue
            screenshot_path = f'{folder_path}/{idx}.png'
            element.screenshot(path=screenshot_path)
            print(f"Saved screenshot: {screenshot_path}")

            print("saving text")
            review_text = element.locator('.content').inner_text()
            review_texts.append({"text": review_text, "screenshot_path": screenshot_path})

    # Save review data to a JSON file
        with open(f"{folder_path}/review_data.json", "w", encoding="utf-8") as json_file:
            json.dump(review_texts, json_file, ensure_ascii=False, indent=4)
            browser.close()

    # print("Applying Transparency")
    # for img_file in os.listdir(folder_path):
    #     add_transparency(f"{folder_path}/{img_file}")

    print("Done!")

    
