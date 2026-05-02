import requests
from django.conf import settings


def send_telegram_message(text, chat_id):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
    }

    requests.post(url, data=data)