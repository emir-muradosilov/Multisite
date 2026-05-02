from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import City
from pages.models import ServicePage, FAQ


@receiver(post_save, sender=City)
def create_default_pages(sender, instance, created, **kwargs):
    if created:
        ServicePage.objects.create(
            city=instance,
            title=f'Алмазное бурение в {instance.name}',
            slug='almaznoe-burenie',
            content=f'Услуги алмазного бурения в городе {instance.name}',
            seo_title=f'Алмазное бурение в {instance.name}',
            seo_description=f'Заказать алмазное бурение в {instance.name}'
        )

        FAQ.objects.create(
            city=instance,
            question=f'Сколько стоит алмазное бурение в {instance.name}?',
            slug='skolko-stoit-almaznoe-burenie',
            answer=f'Цена алмазного бурения в {instance.name} зависит от диаметра.'
        )