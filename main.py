from playwright.sync_api import sync_playwright
import os
import requests

URL = "https://makeinyongsan.kr/program/view/6881c5901c3899787169dfe0"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)

if __name__ == "__main__":
    current = get_current_participant_count()

    if current is None:
        print("참여 인원 정보를 찾지 못했습니다.")
    else:
        # 8명이 아니면 알림 보내기
        if current != 10:
            send_telegram_message(f"[레이저커팅기 교육] 현재 참여 인원이 8명이 아닙니다: {current}명")
