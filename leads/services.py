import requests
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

from .models import Lead

from django.core.mail import send_mail
from django.conf import settings


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


def send_lead_email(lead):

    tenant = getattr(
        lead.city,
        'tenant_profile',
        None
    )

    if not tenant:
        return

    if not tenant.is_active:
        return

    if not tenant.email:
        return

    subject = f'Новая заявка ({lead.city.name})'

    message = f"""
Получена новая заявка.

Город:
{lead.city.name}

Имя:
{lead.name}

Телефон:
{lead.phone}

"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[tenant.email],
        fail_silently=False,
    )



