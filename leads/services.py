import requests
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

from .models import Lead


def is_duplicate_lead(phone):

    time_limit = timezone.now() - timedelta(
        minutes=30
    )

    return Lead.objects.filter(
        phone=phone,
        created_at__gte=time_limit
    ).exists()


def send_telegram_message(text, chat_id):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
    }

    requests.post(url, data=data)