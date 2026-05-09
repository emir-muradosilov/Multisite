from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import City
from pages.models import ServicePage, FAQ


@receiver(post_save, sender=City)
def create_default_content(sender, instance, created, **kwargs):
    if not created:
        return

    # ✅ Создаем только FAQ (без спама страниц)
    FAQ_TEMPLATES = [
        {
            "slug": "almaznoe-burenie",
            "title": "Алмазное бурение",
        },
        {
            "slug": "almaznaya-rezka",
            "title": "Алмазная резка",
        }
    ]


    for template in FAQ_TEMPLATES:
        FAQ.objects.create(
            city=instance,
            question=f"Сколько стоит {template['title'].lower()} в {instance.name}?",
            slug=f"price-{template['slug']}",
            answer=f"Стоимость зависит от объема работ в {instance.name}."
        )