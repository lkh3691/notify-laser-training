from playwright.sync_api import sync_playwright
import os
import requests

URL = "https://makeinyongsan.kr/program/view/6881c4751c3899787169dc9a"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LAST_VALUE_FILE = "last_value.txt"

def get_current_participant_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_timeout(3000)  # wait for JS rendering
        content = page.content()
        browser.close()

        import re
        match = re.search(r"현재 참여 (\d+)명", content)
        return int(match.group(1)) if match else None

def read_last_value():
    if not os.path.exists(LAST_VALUE_FILE):
        return None
    with open(LAST_VALUE_FILE, "r") as f:
        content = f.read().strip()
        return int(content) if content.isdigit() else None


def write_last_value(value):
    with open(LAST_VALUE_FILE, "w") as f:
        f.write(str(value))

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)

if __name__ == "__main__":
    current = get_current_participant_count()
    previous = read_last_value()
    
    if current is not None and current != previous:
        send_telegram_message(f"[레이저커팅기 교육] 현재 참여 인원이 변경됨: {previous}명 → {current}명")
        write_last_value(current)
