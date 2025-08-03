import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch weather:", response.text)
        return False
    data = response.json()
    today = datetime.now().date()
    for forecast in data["list"]:
        dt = datetime.fromtimestamp(forecast["dt"])
        if dt.date() == today:
            description = forecast["weather"][0]["description"].lower()
            if "rain" in description:
                return True
    return False

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)
    print("Telegram message sent.")

def main():
    if get_weather():
        msg = f"☔ It's going to rain today in {CITY} — take your umbrella!"
        send_telegram(msg)
    else:
        print("No rain today. No message sent.")

if __name__ == "__main__":
    main()
