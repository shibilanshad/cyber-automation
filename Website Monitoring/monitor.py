#!/usr/bin/env python3
import requests
import time
import sys

TELEGRAM_BOT_TOKEN = <YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHAT_ID =  <TELEGRAM_CHAT_ID>
URLS = ["example.com", "example.com"]
CHECK_INTERVAL = 60  # seconds

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=payload, timeout=10)
        data = r.json()
        if r.ok == True:
            print(data['result']['text'])
        else:
            print(data['description'])
    except Exception as e:
        print("Telegram error:", e)

def check_url(u):
    try:
        r = requests.get(u, timeout=10)
        return r.status_code
    except Exception as e:
        return None

if __name__ == "__main__":
    while True:
        for u in URLS:
            status = check_url(u)
            if status is None or status >= 500:
                send_telegram(f"[ALERT] {u} status -> {status}")
                print(f"ALERT: {u} -> {status}")
            elif status == 200:
                print(f"{u} Is up and running.")
                send_telegram(f"[ALERT] {u} status -> {status}")
        time.sleep(CHECK_INTERVAL)
