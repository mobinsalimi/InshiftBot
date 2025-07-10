import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Telegram bot settings
BOT_TOKEN = "Your_telegram_bot_token"
CHAT_ID = "Your_chat_id"

# The link to check for available shifts
URL_TO_CHECK = "https://example.ex/jobs?job_type=4&time_range=morning"

CHECK_INTERVAL = 5  

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

# Set up Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Manual login
    driver.get("https://example.ex/user/login")
    print("Please log in and press Enter once you are inside your account.")
    input()

    driver.get(URL_TO_CHECK)

    while True:
        driver.refresh()
        time.sleep(CHECK_INTERVAL)  

        links = driver.find_elements(By.TAG_NAME, "a")
        found_link = None

        for link_element in links:
            href = link_element.get_attribute("href")
            if href and "jobs/details" in href:
                print("Shift link found:", href)
                send_telegram_message(BOT_TOKEN, CHAT_ID, f" Shift link found:\n{href}")
                found_link = href
                break  
            
        if found_link:
            driver.get(found_link)
            time.sleep(3)

            try:
                submit_button = driver.find_element(By.XPATH, "//div[contains(text(), 'ثبت درخواست')]")
                submit_button.click()
                print("Request submitted successfully.")
                send_telegram_message(BOT_TOKEN, CHAT_ID, "Request submitted successfully.")
            except Exception as e:
                print("Could not find the submit button.")
                send_telegram_message(BOT_TOKEN, CHAT_ID, "Could not find the submit button.")
            break
        else:
            print("No available shift found. Checking again...")

finally:
    driver.quit()
