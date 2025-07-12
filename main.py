import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Telegram bot settings
BOT_TOKEN = "Your_telegram_bot_token"
CHAT_ID = "Your_chat_id"

# The link to check for available shifts
URL_TO_CHECK = "https://example.ex/jobs?job_type=4&time_range=morning&from_date=2025-07-15"

CHECK_INTERVAL = 10  # seconds
HEARTBEAT_INTERVAL = 3600  # 60 minutes

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

# Set up Chrome in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # headless login in terminal
    driver.get("https://example.ex/user/login")

    phone_number = input("Enter your phone number: ").strip()
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='شماره موبایل']"))
    )
    phone_input.send_keys(phone_number)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='ورود']"))
    )
    login_button.click()

    otp_inputs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@type='tel' and @maxlength='1']"))
    )

    otp_code = input("Enter the 5-digit OTP code you received: ").strip()

    if len(otp_inputs) < len(otp_code):
        print(f"Warning: only found {len(otp_inputs)} OTP input fields but code length is {len(otp_code)}")

    for i in range(min(len(otp_inputs), len(otp_code))):
        otp_inputs[i].send_keys(otp_code[i])

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='ادامه']"))
    )
    continue_button.click()

    time.sleep(5)  # Wait for login to complete

    # Logged in and ready to check shifts
    driver.get(URL_TO_CHECK)
    last_heartbeat = time.time()

    while True:
        driver.refresh()
        time.sleep(CHECK_INTERVAL)

        links = driver.find_elements(By.TAG_NAME, "a")
        found_link = None

        for link_element in links:
            href = link_element.get_attribute("href")
            if href and "jobs/details" in href:
                print("Shift link found:", href)
                send_telegram_message(BOT_TOKEN, CHAT_ID, f"Shift link found:\n{href}")
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
            except Exception:
                print("Could not find the submit button.")
                send_telegram_message(BOT_TOKEN, CHAT_ID, "Could not find the submit button.")
            break
        else:
            print("No available shift found. Checking again...")

        if time.time() - last_heartbeat >= HEARTBEAT_INTERVAL:
            send_telegram_message(BOT_TOKEN, CHAT_ID, "Still running... no shifts found yet.")
            last_heartbeat = time.time()

finally:
    driver.quit()
